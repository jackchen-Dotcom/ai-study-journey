"""数据模型：题目（Question）+ 复习状态（ReviewState）。

为什么拆成两个类：题目本身是静态的（建库后不变），
你和某道题的关系（几号该复习、连对几次）是动态的。
分开存，重建题库才不会弄丢复习进度——前提是题目 ID 稳定。
"""
from dataclasses import dataclass, field, asdict


@dataclass
class Question:
    id: str                # 全局唯一且稳定，如 flash:Q7 / radar:20 / ext:001
    module: str            # 板块：flash | radar | external
    qtype: str             # 题型：choice 选择 | short 简答
    stem: str              # 题干
    answer: str            # 标准答案（选择题存【选项原文】而不是字母——展示时打乱顺序也不怕）
    source: str            # 来源，如 "背诵卡 Q7" / "找茬 #61" / "AI 八股 v0"
    tags: list = field(default_factory=list)
    options: list | None = None    # 选择题的选项原文列表；简答题为 None
    explanation: str = ""          # 解析，答完展示

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Question":
        return cls(**d)


@dataclass
class ReviewState:
    """你与一道题的复习关系（间隔重复的状态）。

    from_dict 故意写宽容：未来加新字段时，旧 state.json 里缺的键用默认值补齐。
    """
    box: int = 1           # 莱特纳盒 1~5，盒子越高间隔越长
    due: str = ""          # 下次该见的日期（ISO 格式）；空串 = 新题，立即可刷
    last: str = ""         # 上次复习日期
    correct: int = 0       # 累计答对
    wrong: int = 0         # 累计答错

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ReviewState":
        known = cls.__dataclass_fields__.keys()
        return cls(**{k: v for k, v in d.items() if k in known})
