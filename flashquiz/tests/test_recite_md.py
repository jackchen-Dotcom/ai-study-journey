"""解析器测试：直接对着真实的 背诵卡.md 跑——内容更新后这组测试就是同步哨兵。"""
from flashquiz.importers import recite_md


def test_parse_all_cards():
    cards = recite_md.parse()
    assert len(cards) >= 35                     # 9/11 起背诵卡有 35 张
    qnums = [c["qnum"] for c in cards]
    assert qnums == sorted(qnums)               # 顺序不乱
    assert qnums[0] == 1 and qnums[-1] >= 35


def test_every_card_has_stem_and_answer():
    for c in recite_md.parse():
        assert c["stem"], f"Q{c['qnum']} 缺题干"
        assert c["answer"], f"Q{c['qnum']} 缺答案"


def test_sections_become_tags():
    tags = {c["tags"][0] for c in recite_md.parse() if c["tags"]}
    assert "算法模式" in tags
    assert "Python 语言坑" in tags
    assert "AI 基础" in tags
    assert "工程实战" in tags


def test_answer_prefix_stripped():
    cards = {c["qnum"]: c for c in recite_md.parse()}
    assert not cards[1]["answer"].startswith("A：")   # 开头的 A： 已剥掉
