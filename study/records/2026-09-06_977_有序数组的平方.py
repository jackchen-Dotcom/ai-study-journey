# ══ #977 有序数组的平方 · 最终版（测验 T1 重做版）✅（2026-09-06）══
# 双指针第二流派：相向（两端向中心）——对比快慢同向（#26/#27/#283）
# 核心性质：有序数组平方后呈 U 形，最大值只能在两端 → 谁大谁填 result 末尾
# ⭐ 本题教训（用户自己的洞察，已进 patterns）：变量三权分立——首版 i 一人分饰三角
#   （左指针+右端偏移+填充计数）致乱；拆成 left/right/fill 后逻辑自明
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        result = [0] * len(nums)      # ← 必须新建！result = nums 是"同一列表贴两个标签"，
                                      #    写 result 就是写 nums，原数组被污染（Python 引用语义）
        left = 0
        right = len(nums) - 1
        p1 = nums[left]
        p2 = nums[right]
        i = 0
        while left <= right:          # 门上只挂范围条件；== 时还剩中间一个元素（奇数长度），< 会漏
            if p1 * p1 > p2 * p2:
                result[len(nums) - 1 - i] = p1 * p1
                i += 1
                left += 1             # 左边赢 → 只有左指针动
                p1 = nums[left]
            elif p1 * p1 <= p2 * p2:
                result[len(nums) - 1 - i] = p2 * p2
                i += 1
                right -= 1            # 右边赢 → 只有右指针动
                p2 = nums[right]

        return result


# ══ 第1版（测验首 attempt，IndexError 必炸）❌ 存档 ══
# result = []                # ← 空列表不能按下标赋值 → result[i]=... 直接 IndexError
# （核心逻辑伤：把 #35 的二分模板套在 U 形非单调数组上——二分前提是单调分界，平方数组先降后升不存在）
# ← 教训：套模板前先验证前提（单调性/有序性）是否成立
# ══ 第2版（重做首 attempt，逻辑错）❌ 存档 ══
# result = nums              # ← 教训：赋值=贴标签不是拷贝，原数组被污染
# i 一人分饰三角（左指针/右端偏移/填充计数），两个分支都 i+=1 → 左指针被强行拖动、元素被跳过
# while i != (len-1-i)       # ← 教训：!= 当门，两指针交叉错过相等点后死循环+越界；门挂 left <= right
