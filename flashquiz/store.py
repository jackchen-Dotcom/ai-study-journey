"""JSON 持久化：题库（questions.json）+ 复习状态（state.json）。

v0 用 JSON 文件足够；v1 换 SQLite 时只改这个文件——其他代码不感知存储。
"""
import json
from pathlib import Path

from .models import Question, ReviewState

DATA_DIR = Path(__file__).resolve().parent / "data"
BANK_PATH = DATA_DIR / "questions.json"
STATE_PATH = DATA_DIR / "state.json"


def save_bank(questions: list[Question]):
    DATA_DIR.mkdir(exist_ok=True)
    payload = [q.to_dict() for q in questions]
    BANK_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )


def load_bank() -> dict[str, Question]:
    raw = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    return {d["id"]: Question.from_dict(d) for d in raw}


def bank_exists() -> bool:
    return BANK_PATH.exists()


def load_state() -> dict[str, ReviewState]:
    if not STATE_PATH.exists():
        return {}
    raw = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {qid: ReviewState.from_dict(d) for qid, d in raw.items()}


def save_state(state: dict[str, ReviewState]):
    DATA_DIR.mkdir(exist_ok=True)
    payload = {qid: s.to_dict() for qid, s in state.items()}
    STATE_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )
