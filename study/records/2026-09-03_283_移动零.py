# -*- coding: utf-8 -*-
# 2026-09-03 | #283 移动零
# ─────────────────────────────────────────────
# 版本规则：最终版在最上方（唯一可执行代码），历史版本以注释存档于下方，便于对照错误思路
# ─────────────────────────────────────────────

# ══ 最终版（第4版·两阶段）✅ 通过 ══
# 核心教训：当"搬运+清理"一步走不通时，拆成两个独立步骤，分别保证正确
# （第一阶段就是 #27 的框架原样复用；slow==fast 时自己赋值给自己，无害）
class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: None 原地修改，无返回值
        """
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != 0:
                nums[slow] = nums[fast]
                slow += 1
        for i in range(slow, len(nums)):
            nums[i] = 0


# ══ 版本3（错误存档）❌ slow+=1 之后又多写一次，产生重复 ══
# class Solution(object):
#     def moveZeroes(self, nums):
#         slow = 0
#         for fast in range(len(nums)):
#             if nums[fast] != 0 and nums[slow] == 0:
#                 nums[slow] = nums[fast]
#                 nums[fast] = 0
#                 slow += 1
#                 nums[slow] = nums[fast]
#         return nums
#
#
# ══ 版本2（错误存档）❌ 条件加 nums[slow]==0 后，slow 卡在非零位，后面元素搬不动 ══
# class Solution(object):
#     def moveZeroes(self, nums):
#         slow = 0
#         for fast in range(len(nums)):
#             if nums[fast] != 0 and nums[slow] == 0:
#                 nums[slow] = nums[fast]
#                 nums[fast] = 0
#                 slow += 1
#         return nums
#
#
# ══ 版本1（错误存档）❌ slow==fast 时"自己写自己再清零"，毁掉尚未搬运的原件 ══
# 失败用例全是"开头没有0"的数组：[1,0,2]→[0,2,0]、[2,1]→[0,0]、[1]→[0]
# class Solution(object):
#     def moveZeroes(self, nums):
#         slow = 0
#         for fast in range(len(nums)):
#             if nums[fast] != 0:
#                 nums[slow] = nums[fast]
#                 nums[fast] = 0
#                 slow += 1
#         return nums
