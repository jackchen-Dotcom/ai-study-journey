# ══ #35 搜索插入位置 · 最终版：二分查找 ✅ 力扣通过 66/66（2026-09-05，0ms 击败 100%）══
# ⚠️ 双语义存档说明（今日最大教训）：
#   力扣通过时语言选的 "Python"(=2.7)——Py2 的 / 对两个 int 是整除，mid 为 int，合法。
#   但 Py2 已死（2020 停止维护），本地 3.14 / 全行业都是 Python3：/ 是真除法返回 float，
#   nums[1.5] 当场 TypeError。→ 下面的 mid 按 Py3 语义写 //（对通过版的唯一必要改动）。
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:            # 范围里还有没检查过的元素（== 时还剩 1 个，也要查）
            mid = (right + left) // 2   # ← Py2 的 / 能过是"整除"；Py3 必须 //，float 下标必崩
            if nums[mid] == target:
                return mid
            if nums[mid] > target:
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1

        return right + 1                # ← 退出瞬间 left = right + 1，与 return left 等价（等价性证明待补）


# ══ 第1版（线性扫描版，朴素解，力扣通过）❌→✅ 存档 ══
# class Solution:
#     def searchInsert(self, nums: List[int], target: int) -> int:
#         if target < nums[0]:            # ← 教训：左边界坑——循环覆盖不了"插在头部"，前置哨兵特判
#             return 0
#         for i, x in enumerate(nums):
#             if target == x:
#                 return i
#             elif target > x:
#                 if i + 1 == len(nums):  # ← 教训：右边界坑——访问 nums[i+1] 前先判界，顺序即生命
#                     return i + 1
#                 elif target < nums[i + 1]:
#                     return i + 1
# ← 教训：target < x 无分支处理却依然正确——它在前一轮就被 target < nums[i+1] 拦截了
# ← 对比：朴素版 O(n) 每轮淘汰 1 个；二分版 O(log n) 每轮淘汰一半——"朴素解→优化解"第一份对照档案
