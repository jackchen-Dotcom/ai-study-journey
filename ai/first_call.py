# 第一个 LLM 调用：三步走
#   1. load_dotenv()  把 .env 文件里的键值对灌进环境变量
#   2. os.getenv()    从环境变量里取 key（key 永远不写死在代码里）
#   3. requests.post  给 DeepSeek 的 /chat/completions 接口发一个 HTTP 请求
import os
from dotenv import load_dotenv
import requests

load_dotenv()  # 默认读当前目录下的 .env
api_key = os.getenv("DEEPSEEK_API_KEY")

# 防呆：key 没填或没生效，立刻给出人话提示，而不是跑到一半报 401
if not api_key or "粘贴" in api_key:
    raise SystemExit("❌ .env 里的 DEEPSEEK_API_KEY 还没填真实 key")

resp = requests.post(
    "https://api.deepseek.com/chat/completions",   # DeepSeek 的对话接口（OpenAI 兼容格式）
    headers={"Authorization": f"Bearer {api_key}"},  # HTTP 认证惯例：Bearer + 空格 + key
    json={  # requests 会把这个字典转成 JSON 请求体
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个简洁的助手，回答不超过两句话。"},
            {"role": "user", "content": "用一句话说明什么是 API"},
        ],
    },
    timeout=30,  # 30 秒没响应就放弃，防止程序卡死
)

resp.raise_for_status()  # 状态码不是 2xx 就在这里抛异常（比如 401=key 错）
data = resp.json()       # 把响应的 JSON 字符串解析成 Python 字典

# 响应结构：data["choices"][0]["message"]["content"] —— OpenAI 兼容格式的固定套路
print("模型回复：", data["choices"][0]["message"]["content"])
print("本次消耗 tokens：", data["usage"]["total_tokens"])
