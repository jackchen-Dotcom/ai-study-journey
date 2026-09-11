class ChatBot:
    def __init__(self, api_key, model):
        # 任务：把两个参数装进盒子（变成实例属性）
        self.api_key = api_key
        self.model = model
        self.history = []

    def __str__(self):
        return f"chatbot:{self.model}"
    
    def greet(self):
        # 任务：返回一句话，里面要带上盒子里的 model
        # 提示1：方法的第一个参数也是 self（为什么？想想 __init__）
        # 提示2：方法内部用 self.model 取盒子里的东西
        return f"我是{self.model}"

    def remember(self, text):
        self.history.append(text)

    
    
# 测试代码：

bot = ChatBot("sk-test-123", "deepseek-chat")
bot.remember("nihao")
bot.remember("jintianbuchifan")
print(bot.history)
print(bot.model)    # 期望输出：deepseek-chat
print(bot)
print(bot.greet())    # 期望输出：我是deepseek-chat
