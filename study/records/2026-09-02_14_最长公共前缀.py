# -*- coding: utf-8 -*-
# 2026-09-02 | #14 最长公共前缀
# ─────────────────────────────────────────────
# 版本规则：最终版在最上方（唯一可执行代码），历史版本以注释存档于下方，便于对照错误思路
# ─────────────────────────────────────────────

# ══ 最终版（第3版）✅ 力扣全用例通过 ══
class Solution(object):
    def longestCommonPrefix(self, strs):
        minstr = strs[0]
        for x in range(len(strs)-1):
            if len(strs[x]) > len(strs[x+1]):
                minstr = strs[x+1]
            else:
                minstr = strs[x]

        ans = ""
        for i in range(len(minstr)):
            gstr = minstr[:i+1]        # ← [:i+1] 才能验证到完整 minstr
            for j in strs:
                if not j.startswith(gstr):
                    return ans         # ← 返回"最后一次成功"，不是当前失败者
            ans = gstr
        return ans


# ══ 第2版（错误存档）❌ 0/6：返回失败者 / 验不到完整minstr / 空串时gstr未定义 ══
# 教训：验证失败时应返回上一次成功的前缀(ans变量)；[:i]漏掉最后一位；循环可能一次不跑
# class Solution(object):
#     def longestCommonPrefix(self, strs):
#         if strs is None:
#             return ""
#         minstr = strs[0]
#         for x in range(len(strs)-1):
#             if len(strs[x]) > len(strs[x+1]):
#                 minstr = strs[x+1]
#             else:
#                 minstr = strs[x]
#         for i in range(len(minstr)):
#             gstr = minstr[:i]          # ← 永远验不到完整 minstr
#             for j in strs:
#                 if j.startswith(gstr):
#                     gstr = minstr[:i]  # ← 把 gstr 赋成它自己，多余
#                 else:
#                     return gstr        # ← 返回的是"验证失败的候选"
#         return gstr                    # ← minstr为空时 gstr 未定义 → UnboundLocalError
#
#
# ══ 第1版（错误存档）❌ TypeError：元素与下标混用 ══
# 教训：for i in strs 里 i 是元素(字符串)；前缀匹配用 startswith 而不是 in
# class Solution(object):
#     def longestCommonPrefix(self, strs):
#         if strs is None:
#             return ""
#         for x in range(len(strs)-1):
#             if len(strs[x]) > len(strs[x+1]):
#                 minstr = strs[x+1]
#             else:
#                 minstr = strs[x]
#         for i in strs:                 # ← i 是字符串，不是下标
#             gstr = minstr[i]           # ← 用字符串当下标 → TypeError
#             if gstr in strs[i]:        # ← in 是"任意位置包含"，不是前缀
#                 gstr = gstr + minstr[i+1]
#             else:
#                 return gstr
#         return gstr
