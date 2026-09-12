from chatbot import ChatBot
from Prompt import chatbot_prompt

def test_add_message_counts():
    bot = ChatBot("fake_key","fake_url","fake_model")
    bot.add_message({"role": "user", "content": "hi"})
    assert len(bot.history) == 1
    bot.add_message({"role": "assistant", "content": "hello"})
    assert len(bot.history) == 2

def test_save_load_roundtrip(tmp_path):
    bot1 = ChatBot("u","k","m")
    bot1.add_message({"role": "user","content": "wenti"})
    bot1.add_message({"role" : "assistant" , "content" : "回答"})

    save_path = tmp_path / "history.json"

    bot1.save(save_path)

    bot2 = ChatBot("u","k","m")
    bot2.load(save_path)
    assert bot2.history == bot1.history

def test_ensure_system():
    bot = ChatBot("u","k","m")
    bot.ensure_system(chatbot_prompt)
    assert bot.history[0]["role"] == "system"