# ══ #69 x 的平方根 · 最终版：二分（测验重做版）✅（2026-09-06 测验线性版通过 → 二分重做通过）══
# 断层线第三形态：找"最后一个 i*i ≤ x"的 i —— 与 #35/#278（找第一个满足 → return left）方向相反：
# 退出时 left = right + 1，答案落在 right（= left - 1）
class Solution:
    def mySqrt(self, x: int) -> int:
        left = 0
        right = 65535                  # 上界需 ≥ √(2^31-1) ≈ 46341，够用；写 2**16 更自明
        mid = (left + right) // 2      # ← 冗余残留：循环体第一行会重算覆盖，可删（不影响正确性）
        while left <= right:           # 门上只挂范围条件——值条件曾致死循环/荒谬返回
            mid = (left + right) // 2
            if mid * mid == x:
                return mid
            if mid * mid > x:
                right = mid - 1        # 收缩永远边界 ±1；mid//2 曾致范围错乱（已纠正）
            elif mid * mid < x:
                left = mid + 1
        return right


# ══ 第2版（二分首 attempt，TLE 超时）❌ 存档 ══
# left = 0
# right = 2^16                 # ← 教训1：^ 是异或(2^16=18)，幂是 **——其他语言肌肉记忆坑
# mid = (left + right)//2
# while mid*mid < x:           # ← 教训2：值条件且 sqrt/mid 更新脱钩 → 死循环 TLE（#35 首版 while target!=nums[mid] 同病根）
#     mid = (left + right)//2
#     if mid*mid == x:
#         return mid
#     if mid*mid > x:
#         right = mid//2-1     # ← 教训3：收缩写成 mid//2±1——mid 已是中点，收缩=边界 ±1
#     elif mid*mid < x:
#         left = mid//2+1
# return left                  # ← 教训4：断层线方向反了——"最后一个满足"答案在 right（=left-1）
# ← 教训：门上只挂范围条件 left <= right；值的大小写在循环体三分支里

# ══ 第1版（线性扫描，力扣通过 ✅，O(√x)；测验报告：能过 ≠ 达标）══
# class Solution(object):
#     def mySqrt(self, x):
#         i = 0
#         sqrt = i * i
#         if sqrt == x:
#             return i
#         while sqrt < x:
#             i += 1
#             sqrt = i * i
#             if sqrt == x:
#                 return i
#         return i - 1
# ← 对比：O(√x) ≈ 4.6 万次循环 vs O(log x) = 31 次
