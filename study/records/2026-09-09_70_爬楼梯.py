# ══ #70 爬楼梯 · 最终版：DP 滚动变量版 ✅ + 枚举数学版 ✅ 双解（2026-09-09）══
# DP 第一课——五步法框架见 patterns「动态规划入门：五步法 + 适用雷达」
# dp[i] = 到达第 i 阶的方法数 = dp[i-1] + dp[i-2]（最后一步迈 1 或 2，无第三种来源）
class Solution(object):
    def climbStairs(self, n):
        if n <= 2:
            return n
        prev, curr = 1, 2            # dp[1]=1, dp[2]=2——只滚前两阶，O(1) 空间
        for _ in range(3, n + 1):
            prev, curr = curr, prev + curr
        return curr


# ══ 第2版：DP 数组版（状态可见，DP 入门推荐先写这版）✅ ══
# class Solution(object):
#     def climbStairs(self, n):
#         if n <= 2:
#             return n
#         dp = [0] * (n + 1)           # 五步法：①状态 dp[i]=到第 i 阶的方法数
#         dp[1] = 1                    # ③初始化（手数最小子问题）
#         dp[2] = 2
#         for i in range(3, n + 1):    # ④从小到大（大依赖小）
#             dp[i] = dp[i-1] + dp[i-2]  # ②转移方程：最后一步迈 1 或 2
#         return dp[n]                 # ⑤返回值

# ══ 第1版：枚举数学法（用户自己的逻辑修正版）✅ O(n²) ══
# 思路：枚举"2步"数量 y（0 到 n//2），1步数量 x=n-2y；x+y 个位置选 y 个放"2"→ 组合数 C(x+y,y)
# from math import comb
# class Solution(object):
#     def climbStairs(self, n):
#         methods = 0
#         for y in range(n // 2 + 1):
#             x = n - 2 * y
#             methods += comb(x + y, y)
#         return methods
# ← 首版三坑：计数公式 x*(2y)（排列数应为组合数，n=4,y=1 手验 3 种 vs 公式 4）；range(1,n//2) 漏 y=0
#   且不含上界；奇偶分支+特判全是给错误公式打的补丁（#19 教训：修根因别叠补丁）
# ← 双解对比：枚举数"每条路径"（组合级）；DP 数"每阶方法数"（线性）——路径共享前缀，
#   dp[4] 存一次后面全复用。子问题答案复用 = DP 的全部秘密
