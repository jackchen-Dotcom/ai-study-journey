# 人设提示词统一放这里（改提示词不用碰 chatbot.py 逻辑）
# 注意：必须是【字典】——messages 列表里要的是字典，不是"长得像 JSON 的字符串"

chatbot_prompt = {"role": "system", "content": "你是一个简洁的助手，回答不超过两句话。"}
