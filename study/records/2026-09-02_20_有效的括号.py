# -*- coding: utf-8 -*-
# 2026-09-02 | #20 有效的括号（复盘验证题·默写）
# ─────────────────────────────────────────────
# 版本规则：最终版在最上方（唯一可执行代码），历史版本以注释存档于下方，便于对照错误思路
# ─────────────────────────────────────────────

# ══ 最终版（第3版）✅ 8/8 通过 ══
class Solution(object):
    def isValid(self, s):
        stack = []
        stack_map = {
            ")":"(",
            "]":"[",
            "}":"{"
        }
        for x in s:
            if x in "{([":
                stack.append(x)              # 左括号：只管入栈
            else:                            # 右括号：才做配对检查
                if not stack:                # 空栈 pop 会 IndexError，先挡住
                    return False
                if stack.pop() != stack_map.get(x):
                    return False
        if not stack:                        # 栈空 = 全部配对成功
            return True
        else:
            return False


# ══ 第2版（错误存档）❌ 平行if导致"压完就弹" + 结尾判断写反 ══
# 教训：左/右括号是互斥的两条路，必须 if/else；栈空恰恰代表有效（return not stack）
# class Solution(object):
#     def isValid(self, s):
#         stack = []
#         stack_map = {")":"(", "]":"[", "}":"{"}
#         for x in s:
#             if x in "{([":
#                 stack.append(x)
#             if stack.pop() == stack_map.get(x):   # ← 不是else：左括号刚压入就被弹出
#                 continue                          #    且空栈pop会 IndexError（"]"用例）
#             else:
#                 return False
#         if not stack:
#             return False      # ← 反了！栈空 = 全部配对 = 有效
#         else:
#             return True
#
#
# ══ 第1版（默写存档）❌ SyntaxError：流程骨架缺失 ══
# 教训：漏了入栈动作；stack is None 永远False（判空用 if not stack）；
#       赋值= vs 比较==；return 后直接跟表达式；变量名手误
# class Solution(object):
#     def isValid(self, s):
#         stack = []
#         stack_map = {")":"(", "]":"[", "}":"{"}
#         if s[0] in stack_map:      # ← 特判，后来被"右括号且栈空"分支自然覆盖
#             return False
#         for x in s:
#             if stack is None:      # ← 永远False，空列表不是None
#                 stack.append(x)    # ← 且条件和动作都错了：该判"x是左括号"
#             if stack.pop() = stack_map.get(x):   # ← 赋值给函数调用 → SyntaxError
#                 continue
#             else:
#                 return False
#         return if satak is None    # ← 语法非法 + 手误
