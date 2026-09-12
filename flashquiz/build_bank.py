"""题库构建器：把三路题源合并成 questions.json。

ID 是确定性的（flash:Q7 永远是 Q7，radar:20 永远是 20 号题）——
所以背诵卡更新后重建题库，复习进度不会错乱。
"""
from . import store
from .importers import recite_md, seeds
from .models import Question


def build_questions() -> list[Question]:
    questions: list[Question] = []

    # 板块 A：闪刷——背诵卡.md 自动转换（简答题：遮 A 默答，和纸质用法一致）
    for c in recite_md.parse():
        questions.append(Question(
            id=f"flash:Q{c['qnum']}",
            module="flash",
            qtype="short",
            stem=c["stem"],
            answer=c["answer"],
            source=f"背诵卡 Q{c['qnum']}",
            tags=c["tags"],
        ))

    # 板块 B1：模式识别（选择题；B 板块的核心——练"看到题识别模式"）
    for r in seeds.RADAR:
        questions.append(Question(
            id=f"radar:{r['slug']}",
            module="radar",
            qtype="choice",
            stem=r["stem"],
            answer=r["answer"],
            options=[r["answer"]] + r["distractors"],   # 存原文，展示时才打乱
            explanation=r.get("knowledge", ""),          # 答对也有解析：patterns.md 你的原话
            tags=["模式识别"],
            source="patterns.md 模式库",
        ))

    # 板块 B2：找茬（简答题，全部来自你真实踩过的坑）
    for i, b in enumerate(seeds.BUGS, 1):
        questions.append(Question(
            id=f"radar:bug{i:02d}",
            module="radar",
            qtype="short",
            stem=b["stem"],
            answer=b["answer"],
            explanation=b.get("knowledge", ""),          # 同族提醒：防再踩
            tags=["找茬"],
            source=b["source"],
        ))

    # 板块 C：外部题库（八股选择题）
    for i, e in enumerate(seeds.EXTERNAL, 1):
        questions.append(Question(
            id=f"ext:{i:03d}",
            module="external",
            qtype="choice",
            stem=e["stem"],
            answer=e["answer"],
            options=list(e["options"]),
            explanation=e["explanation"],
            tags=["八股"],
            source="AI 八股题库 v0",
        ))

    return questions


def build_and_save() -> list[Question]:
    qs = build_questions()
    store.save_bank(qs)
    return qs
