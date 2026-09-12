"""间隔重复调度器（v0：莱特纳盒 Leitner box）。

规则一句话：答对升一盒（间隔变长），答错打回第 1 盒（明天见）。
这就是你刷题"三天法"的算法化。

可插拔设计：对外只暴露 review(state, is_correct) 一个动作。
将来换 FSRS（2026 年 SRS 事实标准，官方 Python 包现成），
只需重写本文件，models/cli/store 全都不用动。
"""
from datetime import date, timedelta

# 每个盒子对应的复习间隔（天）。第 1 盒答对 → 进第 2 盒 → 3 天后再见……
INTERVALS = [1, 3, 7, 16, 35]


def review(state, is_correct: bool, today: date | None = None):
    """根据答题结果更新复习状态（原地修改并返回）。"""
    today = today or date.today()
    if is_correct:
        # 升盒，最高第 5 盒封顶；间隔取"当前盒"对应的值
        state.box = min(state.box + 1, len(INTERVALS))
        interval = INTERVALS[state.box - 1]
        state.correct += 1
    else:
        state.box = 1
        interval = INTERVALS[0]
        state.wrong += 1
    state.last = today.isoformat()
    state.due = (today + timedelta(days=interval)).isoformat()
    return state
