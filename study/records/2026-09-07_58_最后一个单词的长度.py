# ══ #58 最后一个单词的长度 · 最终版：反向遍历 ✅（2026-09-07，思考题加练版）══
# 双状态变量在反向遍历下的退化：t 与 tmp 永远相等 → 可合并为单变量（职责重合就合，
# 与"变量三权分立"是一体两面：职责独立才拆，重合即合）
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        re_s = reversed(s)              # 迭代器，省内存（s[::-1] 会复制整串，大字符串内存翻倍）

        t = 0
        tmp = 0
        for x in re_s:
            if x != " ":
                t += 1
                tmp = t
            if x == " " and tmp != 0:   # ← 点睛之门：尾部空格时 tmp==0 不返回，
                t = 0                   #    数完最后一个单词再遇空格才 return——尾部空格陷阱化解
                return tmp

        return tmp


# ══ 第1版（正向扫描，力扣通过 ✅，O(n) 全串扫描）══
# class Solution:
#     def lengthOfLastWord(self, s: str) -> int:
#         t = 0
#         tmp = 0
#         for x in s:
#             if x != " ":
#                 t += 1
#                 tmp = t            # ← tmp 职责：最近一个完整单词的长度（持久），遇空格不清零
#             if x == " ":
#                 t = 0              # ← t 职责：当前单词长度（易失）
#         return tmp
# ← 教训：if/if 互斥条件可改 elif（顺手小优化）
# ← 反向版收益：提前退出，复杂度从 O(n) 降到 O(尾部空格数 + 最后单词长度)——1GB 字符串只扫几个字符
