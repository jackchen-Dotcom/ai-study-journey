"""判分器：选择题精确匹配；简答题 AI 判分（不可用时降级为自评）。

降级策略直接复用 chatbot 的异常处理课：
AI 判分失败绝不能弄崩刷题体验 → 返回 None，调用方转自评。
"""
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# .env 在仓库根目录（和 chatbot.py 共用同一份 key/URL/模型配置）
REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")

# 评分标准写死在 system prompt 里——这是"提示词即接口契约"的最小实现：
# 程序要解析模型的 JSON 输出，所以格式必须用法律条文式的口吻锁死
JUDGE_SYSTEM = (
    "你是严格的判分器。根据题目和标准答案，给用户答案打分。"
    '只输出 JSON，不要输出任何其他内容，格式：'
    '{"score": 0到100的整数, "verdict": "pass|partial|fail", '
    '"feedback": "一句话中文点评，答对时说明好在哪，没答全时指出漏了什么"}。'
    "评分标准：方向正确且覆盖关键点=pass；沾边但有明显遗漏=partial；方向错误或答非所问=fail。"
)


def grade_choice(question, picked_text: str) -> bool:
    """选择题：答案存的是选项原文，直接比较文本（不怕选项被打乱）。"""
    return picked_text == question.answer


def parse_ai_json(content: str) -> dict:
    """从模型回复里抠出 JSON，容忍 ```json 围栏和前后废话。"""
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("模型回复里没有 JSON")
    return json.loads(content[start:end + 1])


def ai_grade_short(stem: str, standard_answer: str, user_answer: str) -> dict | None:
    """AI 判简答题。

    返回 {"score", "verdict", "feedback"}；
    任何失败（没配 key / 断网 / 回复解析不出）返回 None，由调用方降级自评。
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    url = os.getenv("DEEPSEEK_URL")
    model = os.getenv("MODEL")
    if not (api_key and url and model):
        return None

    user_msg = (
        f"题目：{stem}\n\n标准答案：{standard_answer}\n\n用户答案：{user_answer or '（未作答）'}"
    )
    try:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "temperature": 0,       # 判分要稳定，不要创造性
                "messages": [
                    {"role": "system", "content": JUDGE_SYSTEM},
                    {"role": "user", "content": user_msg},
                ],
            },
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return parse_ai_json(content)
    except (requests.exceptions.RequestException, KeyError, IndexError, ValueError):
        # 这里故意接"全家桶"（requests 异常家族 + JSON 结构错 + 解析错）：
        # 判分是锦上添花的功能，失败路径的唯一正确行为 = 优雅降级
        return None
