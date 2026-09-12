"""判分器测试——全部离线，绝不真调 API（网络调用不做单测，那是降级策略要兜的）。"""
import pytest

from flashquiz.grader import grade_choice, parse_ai_json


class FakeQuestion:
    answer = "栈：最近匹配"


def test_grade_choice_exact_match():
    assert grade_choice(FakeQuestion(), "栈：最近匹配") is True
    assert grade_choice(FakeQuestion(), "队列：先进先出") is False


def test_parse_ai_json_tolerates_fences():
    content = (
        "好的，判分如下：\n```json\n"
        '{"score": 80, "verdict": "partial", "feedback": "漏了先判空"}\n'
        "```\n以上。"
    )
    data = parse_ai_json(content)
    assert data["score"] == 80
    assert data["verdict"] == "partial"


def test_parse_ai_json_garbage_raises():
    with pytest.raises(ValueError):
        parse_ai_json("我觉得你答得不错。")


def test_parse_ai_json_plain_json():
    data = parse_ai_json('{"score": 95, "verdict": "pass", "feedback": "完整"}')
    assert data["verdict"] == "pass"
