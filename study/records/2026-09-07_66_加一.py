# ══ #66 加一 · 最终版：原地进位模拟（标准解法）✅（2026-09-07）══
# 与数学版对照：取巧版依赖 Python 大整数；本版跨语言通用，O(n) 原地修改
# 骨架：末位起检查——是 9 就归 0 进位往前；非 9 直接 +1 收工；一路 9 到头 → 新数组 [1,0,...,0]
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        len1 = len(digits)
        dig = [0] * (len1 + 1)               # 全 9 备用新数组：长度按初始 len 算，恰好多一位
        while digits[len1 - 1] == 9:         # 末位是 9 → 要进位，往前走
            len1 -= 1
            if len1 == 0 and digits[0] == 9: # ← 一路 9 到头：越界前拦截（#35 "先判界再访问"迁移）
                dig[0] = 1
                return dig                   # [1, 0, ..., 0]
            digits[len1] = 0                 # 9 归 0，进位继续
        if digits[len1 - 1] < 9:
            digits[len1 - 1] += 1            # 首个非 9 位：+1 收工
            return digits
        return digits                        # ← 死代码：while 退出后上支必然命中，可删


# ══ 第1版（数学取巧版，力扣通过 ✅）══
# 思路：数组 → 按位权展开成整数 → +1 → str 逐位拆回数组
# [1,2,3]→123→124→[1,2,4]；[9,9,9]→999→1000→[1,0,0,0]（进位被大整数天然消化）
# class Solution:
#     def plusOne(self, digits: List[int]) -> List[int]:
#         length = len(digits) - 1
#         final = 0
#         for x in digits:
#             tmp = x * (10 ** length)
#             length -= 1
#             final += tmp
#         final += 1
#         len1 = len(str(final))
#         dig = [0] * len1
#         for i, x in enumerate(str(final)):
#             dig[i] = int(x)
#         return dig
# ← 教训：取巧成立的唯一前提是 Python int 无位数上限；digits 长 100 位时
#   Java/C++ 的 long long（≈19 位上限）中途溢出全盘皆错——面试两把刷子：会取巧 + 知道标准解
# ← 小优化：拆位循环可写列表推导 [int(c) for c in str(final)]
