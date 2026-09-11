# ══ #278 第一个错误的版本 · 最终版（加练）✅ 力扣通过（2026-09-05）══
# ⭐ 本题价值：#35 二分模板的同族变体——断层线含义从"插入位置"变为"第一个坏版本"
# 区域不变量（二分的灵魂）：
#   走 left  = mid+1 前提：mid 是好版本 → "好全在坏前" → left 左边永远全好
#   走 right = mid-1 前提：mid 是坏版本 → "一旦坏全坏" → right 右边永远全坏
#   退出时 left = right+1，混合区消失：1..right 全好，left..n 全坏 → 断层线 = 第一个坏版本
#   （第一轮 mid 就是坏版本被扔出去也不丢——它被"盖章"进 right 右侧坏区，断层线最终精确回到它）
class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 0
        right = n - 1

        while left <= right:
            mid = (left + right) // 2
            if isBadVersion(mid) == False:    # ← Pythonic 建议：写 if not isBadVersion(mid): 布尔别再和 False/True 比
                left = mid + 1
            elif isBadVersion(mid) == True:   # ← 同上：此分支可直接 else:（两个分支已互斥穷尽）
                right = mid - 1

        return right + 1                      # = left = "最后的好"与"最先的坏"的分界线
