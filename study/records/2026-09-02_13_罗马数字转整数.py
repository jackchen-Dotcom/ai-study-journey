# -*- coding: utf-8 -*-
# 2026-09-02 | #13 罗马数字转整数
# ─────────────────────────────────────────────
# 版本规则：最终版在最上方（唯一可执行代码），历史版本以注释存档于下方，便于对照错误思路
# ─────────────────────────────────────────────

# ══ 最终版（第2版）✅ 6/6 通过 ══
class Solution(object):
    def romanToInt(self, s):
        roma_map = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }
        ans = 0
        pre_val = 0
        for x in reversed(s):
            cur = roma_map[x]
            if cur < pre_val:
                ans -= cur
            else:
                ans += cur
            pre_val = cur
        return ans


# ══ 第1版（错误存档）❌ SyntaxError + 3处逻辑错误 ══
# 教训：缩进跑出方法体 / 字典取值写成调用 roma_map(x) / 赋值方向写反 cur = pre_val
# class Solution(object):
#     def romanToInt(self, s):
#         roma_map = {
#             "I": 1,
#             "V": 5,
#             "X": 10,
#             "L": 50,
#             "C": 100,
#             "D": 500,
#             "M": 1000
#         }
#     ans = 0                  # ← 缩进只有4格，跑到了方法外
#     pre_val = 0
#     rotate_s = reversed(s)
#     for x in rotate_s:
#         cur = roma_map(x)    # ← 字典取值应为 roma_map[x]
#         if cur < pre_val:
#             ans -= cur
#         else:
#             ans += cur
#         cur = pre_val        # ← 方向反了，应为 pre_val = cur
#
#     return ans
