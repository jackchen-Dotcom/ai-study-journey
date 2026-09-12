"""题源适配器：把「背诵卡.md」解析成题目列表。

解析约定（每张卡的格式）：
    **Q7 问题文本？**
    A：答案文本（可能多行，直到下一张卡 / 下一节标题 / 分隔线）

章节标题（## 一、算法模式）里的序号被剥掉，剩下的作为这道题的 tag。
"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RECITE_PATH = REPO_ROOT / "study" / "背诵卡.md"

CARD_RE = re.compile(r"^\*\*Q(\d+)\s+(.+?)\*\*\s*$")
SECTION_RE = re.compile(r"^##\s+(.+)$")


def _clean_section(title: str) -> str:
    """'一、算法模式（10 张）' → '算法模式'：剥掉中文序号和括号注释。"""
    title = re.sub(r"（.*?）", "", title)
    title = re.sub(r"^[一二三四五六七八九十]+、", "", title)
    return title.strip()


def parse(path=RECITE_PATH) -> list[dict]:
    """解析背诵卡，返回 [{"qnum", "stem", "answer", "tags"}, ...]（按 Q 号升序）。"""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    cards, tag, cur = [], None, None

    for line in lines:
        if line.startswith("## 滚动计划"):
            break  # 滚动计划不是卡片内容，到此为止
        m = SECTION_RE.match(line)
        if m:
            if cur:
                cards.append(cur)  # 边界处先落袋，再换节——否则本节最后一张卡会丢
            tag = _clean_section(m.group(1))
            cur = None
            continue
        if line.startswith("---"):
            if cur:
                cards.append(cur)
            cur = None
            continue
        m = CARD_RE.match(line)
        if m:
            if cur:
                cards.append(cur)
            cur = {
                "qnum": int(m.group(1)),
                "stem": m.group(2).strip(),
                "answer_lines": [],
                "tag": tag,
            }
            continue
        # 答题行：收集到当前卡（空行跳过，防误收格式噪音）
        if cur is not None and line.strip():
            cur["answer_lines"].append(line.strip())

    if cur:
        cards.append(cur)

    result = []
    for c in cards:
        answer = "\n".join(c["answer_lines"])
        answer = re.sub(r"^A[：:]\s*", "", answer)  # 去掉开头的 "A："
        result.append({
            "qnum": c["qnum"],
            "stem": c["stem"],
            "answer": answer,
            "tags": [c["tag"]] if c["tag"] else [],
        })
    return result
