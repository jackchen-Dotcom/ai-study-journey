"""调度器测试：莱特纳盒的升盒/回炉/封顶三件事。

纯逻辑零网络——这就是当初把调度器单独抽成模块的好处。
"""
from datetime import date

from flashquiz.models import ReviewState
from flashquiz.scheduler import review


def test_correct_climbs_ladder():
    s = ReviewState()
    review(s, True, date(2026, 9, 11))
    assert s.box == 2
    assert s.due == "2026-09-14"          # 第 2 盒 = 3 天后
    review(s, True, date(2026, 9, 14))
    assert s.box == 3
    assert s.due == "2026-09-21"          # 第 3 盒 = 7 天后


def test_wrong_resets_to_box1():
    s = ReviewState(box=4)
    review(s, False, date(2026, 9, 11))
    assert s.box == 1
    assert s.due == "2026-09-12"          # 回炉：明天见
    assert s.wrong == 1


def test_box_caps_at_five():
    s = ReviewState(box=5)
    review(s, True, date(2026, 9, 11))
    assert s.box == 5                      # 不再上升
    assert s.due == "2026-10-16"           # 35 天后
