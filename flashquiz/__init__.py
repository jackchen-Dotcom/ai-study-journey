"""闪刷 FlashQuiz——把错题本变成可调度的题库。

三个板块（对应设计书 study/plan-flash-quiz.md）：
  flash     闪刷      背诵卡.md 自动转换，间隔重复调度
  radar     模式雷达  模式识别（选择题）+ 找茬（你真实踩过的坑）
  external  外部题库  AI 八股选择题（来自 roadmap 面试清单）

v0 = 命令行版。运行方式（仓库根目录）：python -m flashquiz
"""
__version__ = "0.1.0"
