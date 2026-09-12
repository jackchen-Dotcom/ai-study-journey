"""v0.5 Web 版：FastAPI 后端 + 单页 HTML 前端（手机浏览器友好）。

运行（仓库根目录）：
    python -m uvicorn flashquiz.web:app --host 0.0.0.0 --port 8000
然后浏览器打开 http://127.0.0.1:8000（手机同 WiFi 用电脑局域网 IP 访问）。

设计要点：
- 领域层（models/scheduler/grader/store）原封不动复用——当初分层的好处兑现
- 判分全部在服务端：选择题不给前端发答案，防"开卷作弊"
- 简答题 AI 判分不可用时降级为"前端自评"，和 CLI 一个思路
- v1（10 月）会补 Pydantic 深入、SQLite、Jinja2 模板化——这版只是壳
"""
import random
from datetime import date
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import grader, scheduler, store
from .cli import pick_ids          # 抽题策略和 CLI 共用一份
from .models import ReviewState

app = FastAPI(title="闪刷 FlashQuiz")
STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/due_counts")
def due_counts():
    """三个板块的到期数（菜单徽标）。"""
    bank, state = store.load_bank(), store.load_state()
    today = date.today().isoformat()
    return {
        m: sum(1 for q in bank.values()
               if q.module == m and state.get(q.id, ReviewState()).due <= today)
        for m in ("flash", "radar", "external")
    }


@app.get("/api/next/{module}")
def next_question(module: str):
    """抽一道题。选择题只回传题干+打乱的选项，不回传答案。"""
    bank, state = store.load_bank(), store.load_state()
    ids = pick_ids(bank, state, module, 1)
    if not ids:
        return {"question": None, "due_count": 0}
    q = bank[ids[0]]
    today = date.today().isoformat()
    due_count = sum(1 for x in bank.values()
                    if x.module == module and state.get(x.id, ReviewState()).due <= today)
    if q.qtype == "choice":
        options = list(q.options or [])
        random.shuffle(options)
        body = {"id": q.id, "qtype": q.qtype, "stem": q.stem,
                "options": options, "source": q.source}
    else:
        body = {"id": q.id, "qtype": q.qtype, "stem": q.stem, "source": q.source}
    return {"question": body, "due_count": due_count}


# ---------- 请求体模型（Pydantic：自动校验 JSON 字段，10 月会深学） ----------
class ChoiceAnswer(BaseModel):
    qid: str
    picked: str


class ShortSubmit(BaseModel):
    qid: str
    text: str = ""


class SelfGrade(BaseModel):
    qid: str
    correct: bool


def _finish(bank: dict, qid: str, correct: bool, extra: dict | None = None) -> dict:
    """统一收尾：更新调度状态 → 落盘 → 组装反馈（答案/解析/下次日期）。"""
    state = store.load_state()
    s = state.setdefault(qid, ReviewState())
    scheduler.review(s, correct)
    store.save_state(state)
    q = bank[qid]
    out = {"correct": correct, "answer": q.answer,
           "explanation": q.explanation, "next_due": s.due}
    if extra:
        out.update(extra)
    return out


@app.post("/api/answer_choice")
def answer_choice(body: ChoiceAnswer):
    bank = store.load_bank()
    q = bank[body.qid]
    correct = grader.grade_choice(q, body.picked)
    return _finish(bank, body.qid, correct)


@app.post("/api/submit_short")
def submit_short(body: ShortSubmit):
    bank = store.load_bank()
    q = bank[body.qid]
    if not body.text.strip():
        return _finish(bank, body.qid, False, {"graded": "skipped"})
    result = grader.ai_grade_short(q.stem, q.answer, body.text)
    if result is None:
        # AI 不可用 → 不更新状态，把答案发给前端让用户自评
        return {"graded": "self", "answer": q.answer}
    correct = result.get("verdict") == "pass"
    return _finish(bank, body.qid, correct, {
        "graded": "ai",
        "score": result.get("score"),
        "verdict": result.get("verdict"),
        "feedback": result.get("feedback"),
    })


@app.post("/api/self_grade")
def self_grade(body: SelfGrade):
    bank = store.load_bank()
    return _finish(bank, body.qid, body.correct)
