# -*- coding: utf-8 -*-
# 2026-09-03 | #27 移除元素
# ─────────────────────────────────────────────
# ✅ 力扣直接一次通过（116/116 用例）——#26 快慢指针框架的成功迁移
# 注意：本文件无历史版本（一次通过）
# 小瑕疵：fast = 0 是死代码（立刻被循环变量覆盖），下次注意删干净

class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
        return slow
