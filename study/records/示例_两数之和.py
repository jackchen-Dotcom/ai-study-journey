# -*- coding: utf-8 -*-
# 示例解法：演示 judge.py 的判题流程（故意写一个会挂的暴力解法）
# 验证命令:
#   python judge.py problems/1_两数之和.md records/示例_两数之和.py


def solve(nums, target):
    # 暴力枚举：O(n^2)，能过前两个用例，但第4个用例会挂（供演示）
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return [-1, -1]
