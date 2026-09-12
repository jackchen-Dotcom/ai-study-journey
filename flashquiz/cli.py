"""「闪刷」v0 命令行入口。

运行方式（仓库根目录）：
    python -m flashquiz

菜单：A 闪刷（背诵卡，间隔重复） / B 模式雷达（模式识别+找茬）
     C 外部题库（八股） / S 统计 / R 重建题库 / Q 退出
任何答题环节敲 q 都能立即退出，进度自动保存。
"""
import random
import sys
from datetime import date

from . import grader, scheduler, store
from .build_bank import build_and_save
from .models import ReviewState

MODULE_NAMES = {"flash": "闪刷", "radar": "模式雷达", "external": "外部题库"}


def ensure_bank() -> dict:
    """题库不存在就自动构建（背诵卡更新后也可在菜单里手动 R 重建）。"""
    if not store.bank_exists():
        print("首次运行：正在从 背诵卡.md + 种子数据 构建题库……")
        qs = build_and_save()
        print(f"题库建成：共 {len(qs)} 题。\n")
    return store.load_bank()


def pick_ids(bank: dict, state: dict, module: str, limit: int) -> list[str]:
    """抽题策略：到期卡优先 → 没见过的新卡次之 → 未到期的垫底。各自打乱防顺序依赖。"""
    today = date.today().isoformat()
    due, unseen, rest = [], [], []
    for qid, q in bank.items():
        if q.module != module:
            continue
        s = state.get(qid)
        if s is None:
            unseen.append(qid)
        elif s.due <= today:      # 空串（新卡）也满足 <=，天然归入到期
            due.append(qid)
        else:
            rest.append(qid)
    random.shuffle(due)
    random.shuffle(unseen)
    random.shuffle(rest)
    return (due + unseen + rest)[:limit]


def run_choice(q, state: ReviewState):
    """选择题交互。返回 False = 用户要求退出本环节。"""
    options = list(q.options or [])
    random.shuffle(options)                # 展示时打乱；判分按选项原文比对
    letters = "ABCDEFG"[: len(options)]
    print(q.stem)
    for letter, text in zip(letters, options):
        print(f"  {letter}. {text}")
    picked = input("你的选择（字母）：").strip().upper()
    if picked == "Q":
        return None
    correct = False
    if picked in letters:
        correct = grader.grade_choice(q, options[letters.index(picked)])
    if correct:
        print("✅ 答对了")
    else:
        print(f"❌ 答错了。正确答案：{q.answer}")
    if q.explanation:
        print(f"💡 {q.explanation}")
    scheduler.review(state, correct)
    print(f"📅 下次见面：{state.due}")
    return True


def run_short(q, state: ReviewState):
    """简答题交互：先默答 → 揭示标准答案 → AI 判分（不可用则自评）。"""
    print(q.stem)
    user = input("\n（默答后把答案敲进来；直接回车=只看答案）：").strip()
    if user == "q":
        return None
    print(f"\n📌 标准答案：{q.answer}\n")

    correct = False
    if user:
        result = grader.ai_grade_short(q.stem, q.answer, user)
        if result is not None:
            verdict = result.get("verdict", "fail")
            correct = verdict == "pass"
            print(f"🤖 AI 判分：{result.get('score', '?')} 分 · {verdict} —— {result.get('feedback', '')}")
        else:
            y = input("🤖 AI 判分不可用（网络/配置），自评 [y=答对 / 其他=答错]：").strip().lower()
            correct = (y == "y")
    else:
        print("（未作答，按未掌握处理）")

    scheduler.review(state, correct)
    print(f"📅 下次见面：{state.due}")
    return True


def session(bank: dict, state: dict, module: str, limit: int):
    ids = pick_ids(bank, state, module, limit)
    if not ids:
        print("（该板块暂无题目）")
        return
    print(f"\n=== {MODULE_NAMES[module]} · 本次 {len(ids)} 题（敲 q 随时退出） ===")
    done = 0
    for i, qid in enumerate(ids, 1):
        q = bank[qid]
        s = state.setdefault(qid, ReviewState())
        print(f"\n【{i}/{len(ids)}】{q.source}")
        r = run_choice(q, s) if q.qtype == "choice" else run_short(q, s)
        if r is None:
            break
        done += 1
    store.save_state(state)
    print(f"\n本环节完成 {done} 题，进度已保存。")


def show_stats(bank: dict, state: dict):
    today = date.today().isoformat()
    print("\n=== 统计 ===")
    for module in ("flash", "radar", "external"):
        qs = [q for q in bank.values() if q.module == module]
        if not qs:
            continue
        due = sum(1 for q in qs if state.get(q.id, ReviewState()).due <= today)
        mastered = sum(1 for q in qs if state.get(q.id, ReviewState()).box >= 5)
        print(f"{MODULE_NAMES[module]}：共 {len(qs)} 题 · 今日到期 {due} · 已进第 5 盒 {mastered}")

    # 薄弱题排行：至少做过 2 次、正确率低于 100%，按正确率升序
    weak = []
    for q in bank.values():
        s = state.get(q.id)
        if s and (s.correct + s.wrong) >= 2:
            acc = s.correct / (s.correct + s.wrong)
            if acc < 1.0:
                weak.append((acc, q.source, s.correct + s.wrong))
    if weak:
        weak.sort()
        print("\n薄弱 Top5（正确率最低，优先重刷）：")
        for acc, source, attempts in weak[:5]:
            print(f"  {source} · 正确率 {acc:.0%}（{attempts} 次）")
    print()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # Windows GBK 终端保命（同 judge.py）
    except Exception:
        pass

    bank = ensure_bank()
    state = store.load_state()
    print("=== 闪刷 FlashQuiz v0 —— 你的坑，就是你的题库 ===")

    while True:
        today = date.today().isoformat()
        badge = {
            m: sum(1 for q in bank.values()
                   if q.module == m and state.get(q.id, ReviewState()).due <= today)
            for m in MODULE_NAMES
        }
        print(f"\n[A]闪刷·到期{badge['flash']}  [B]模式雷达·到期{badge['radar']}  "
              f"[C]外部题库·到期{badge['external']}  [S]统计  [R]重建题库  [Q]退出")
        cmd = input("> ").strip().lower()
        if cmd == "a":
            session(bank, state, "flash", limit=10)
        elif cmd == "b":
            session(bank, state, "radar", limit=6)
        elif cmd == "c":
            session(bank, state, "external", limit=6)
        elif cmd == "s":
            show_stats(bank, state)
        elif cmd == "r":
            qs = build_and_save()
            bank = store.load_bank()
            print(f"题库已重建：{len(qs)} 题（ID 稳定，复习进度不受影响）")
        elif cmd == "q":
            store.save_state(state)
            print("进度已保存，回见。")
            break
        else:
            print("看不懂的指令（a / b / c / s / r / q）")


if __name__ == "__main__":
    main()
