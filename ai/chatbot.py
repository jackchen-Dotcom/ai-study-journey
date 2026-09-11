import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_URL")
model = os.getenv("MODEL")

class ChatBot:
    def __init__ (self,key,url,model):
        self.key = key
        self.url = url
        self.model = model
        self.history = []
    
    def add_message(self,text):
        self.history.append(text)

    def save(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False)

    def load(self):
        with open("history.json", encoding="utf-8") as f:
            self.history = json.load(f)

    def chat(self,user_input):

        self.add_message({"role": "user", "content": user_input})
        resp = requests.post(
            self.url,   # DeepSeek 的对话接口（OpenAI 兼容格式）
            headers={"Authorization": f"Bearer {self.key}"},  # HTTP 认证惯例：Bearer + 空格 + key
            json={  # requests 会把这个字典转成 JSON 请求体
                "model": self.model,
                "temperature": 0,
                "messages": self.history,
            },
        )
        
        resp.raise_for_status()  # 状态码不是 2xx 就在这里抛异常（比如 401=key 错）
        data = resp.json()       # 把响应的 JSON 字符串解析成 Python 字典
        self.add_message({"role": "assistant", "content": data["choices"][0]["message"]["content"]})
        #history = json.dumps({"role": "assistant", "content": data["choices"][0]["message"]["content"]})
        self.save()
        return data["choices"][0]["message"]["content"]

max_conver_len = 0
prompt = {"role": "system", "content": "你是一个简洁的助手，回答不超过两句话。"}
myllm = ChatBot(api_key,base_url,model)

try:
    myllm.load()                # 可能出事的代码：打开可能不存在的文件
except FileNotFoundError:       # 只接"文件不存在"这一种异常
    myllm.add_message(prompt)      # 兜底：第一次运行，从新对话开始（先记人设）


while max_conver_len < 3:
    max_conver_len += 1
    user_input = input()
    print(myllm.chat(user_input))

    #print("本次消耗 tokens：", data["usage"]["total_tokens"])
    #print(myllm.history)
    #print(history)
    