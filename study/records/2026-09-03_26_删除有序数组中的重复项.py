# -*- coding: utf-8 -*-
# 2026-09-03 | #26 删除有序数组中的重复项
# ─────────────────────────────────────────────
# 版本规则：最终版在最上方（唯一可执行代码），历史版本以注释存档于下方，便于对照错误思路
# ─────────────────────────────────────────────

# ══ 最终版（第3版）══
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        lows = 0
        for highs in range(1, len(nums)):
            if nums[lows] != nums[highs]:
                lows += 1
                nums[lows] = nums[highs]
        return lows + 1


# ══ 第2版（错误存档）❌ 快指针卡死 + 数据被写0 + 返回值差1 ══
# 教训：for 循环变量本身就是快指针（highs），else 分支里不再需要手动前进；
#       "相等=重复=什么都不做"，写0是毁数据；返回个数=lows下标+1
# class Solution(object):
#     def removeDuplicates(self, nums):
#         lows = 0
#         highs = 0
#         pren = nums[lows]
#         for _ in range(len(nums)):
#             if nums[lows] == nums[highs]:
#                 nums[highs] = 0          # ← 数据被毁
#                 highs += 1
#             else:
#                 lows += 1
#                 nums[lows] = nums[highs]
#         return lows                      # ← 应为 lows + 1
#
#
# ══ 第1版（错误存档）❌ 无搬运动作 + 返回整个数组 ══
# 教训：去重=把不重复的搬到前面；for n in nums 的 n 是元素不是下标（第3次栽）
# class Solution(object):
#     def removeDuplicates(self, nums):
#         lows = 0
#         highs = 0
#         pren = nums[lows]
#         for n in nums:
#             if nums[lows] == nums[highs]:
#                 nums[highs] = 0
#                 highs += 1
#             else:
#                 lows += 1
#         return nums                      # ← 题目要返回 k
