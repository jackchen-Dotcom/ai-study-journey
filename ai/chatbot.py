import os
from pathlib import Path

from dotenv import load_dotenv
import requests
import json

from Prompt import chatbot_prompt   # 人设提示词统一在 Prompt.py 维护（是字典不是字符串）

REPO_ROOT = Path(__file__).resolve().parents[1]   # 仓库根（.env 统一放那里）
load_dotenv(REPO_ROOT / ".env")

api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_URL")
model = os.getenv("MODEL")

class ChatBot:
    def __init__ (self,key,url,model,max_history=10):
        self.key = key
        self.url = url
        self.model = model
        self.history = []
        self.max_history = max_history
    
    def add_message(self,text):
        self.history.append(text)

    def save(self, path= "history.json"):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False)

    def load(self, path= "history.json"):
        with open("history.json", encoding="utf-8") as f:
            self.history = json.load(f)

    def ensure_system(self, prompt):
        if not self.history or self.history[0]["role"] != "system":
            self.history.insert(0, prompt)

    def chat(self,user_input):

        self.add_message({"role": "user", "content": user_input})
        if len(self.history) > self.max_history:
            self.history = [self.history[0]]+self.history[-self.max_history:]

        try:
            resp = requests.post(
                self.url,   # DeepSeek 的对话接口（OpenAI 兼容格式）
                headers={"Authorization": f"Bearer {self.key}"},  # HTTP 认证惯例：Bearer + 空格 + key
                json={  # requests 会把这个字典转成 JSON 请求体
                    "model": self.model,
                    "temperature": 0,
                    "messages": self.history,
                },
            )
            resp.raise_for_status()# 状态码不是 2xx 就在这里抛异常（比如 401=key 错）  
        except requests.exceptions.ConnectionError:
            return "网络异常，请检查连接" 
        except requests.exceptions.HTTPError:
            return "api_key Error"
        
        data = resp.json()       # 把响应的 JSON 字符串解析成 Python 字典
        self.add_message({"role": "assistant", "content": data["choices"][0]["message"]["content"]})
        self.save()
        return data["choices"][0]["message"]["content"]

prompt = chatbot_prompt
if __name__ == "__main__":
    myllm = ChatBot(api_key,base_url,model)

    try:
        myllm.load()                # 可能出事的代码：打开可能不存在的文件
        
        if myllm.history[0]["role"] != "system":
            myllm.history.insert(0, prompt)
    except FileNotFoundError:       # 只接"文件不存在"这一种异常
        myllm.add_message(prompt)      # 兜底：第一次运行，从新对话开始（先记人设）


    while True:
        user_input = input()
        if user_input == "q":
            break
        print(myllm.chat(user_input))
        
