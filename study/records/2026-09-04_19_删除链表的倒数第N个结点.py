# ════════════════════════════════════════════════
# 19. 删除链表的倒数第 N 个结点 — 最终版 ✅（2026-09-05 优化版 · 真·一趟扫描）
# 思路（我自己的话）：有虚拟头节点后所有循环前移一位，同步走完刚好停在
#     被删节点的前一位——fast 先走 n 步拉开差距，然后两指针同步，fast 踩尾即停
# 好在哪（对照下方 count 版）：
#   1. 消灭 count 计数与 count=-1 的绕路初始化（昨天被"多算 1"折腾两版的根源）
#   2. 真·一趟扫描（达成题目进阶要求）
#   3. while p2.next 条件守门 = 零特判；与 #876 经典版同构——
#      错位 + 同步 + 踩尾退出，快慢指针两流派在此统一
# ════════════════════════════════════════════════

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: Optional[ListNode]
        :type n: int
        :rtype: Optional[ListNode]
        """
        dummy = ListNode(0)
        dummy.next = head
        p1 = dummy
        p2 = dummy
        for x in range(n):
            p2 = p2.next

        while p2.next:
            p1 = p1.next
            p2 = p2.next
        p1.next = p1.next.next
        return dummy.next


# ════════════════════════════════════════════════
# 第二版（2026-09-04 count=-1 计数版）✅ 5/5 通过
# 两趟扫描：先数长度（count=-1 起步修正多算问题）再走 count-n 步
# 关键行：count = -1 ← 教训：先加后移的计数循环会多算 1，用 -1 起步等效修正
#         （更好的选择是"先移动后计数"，或像上方优化版直接消掉计数）
# ════════════════════════════════════════════════
# class Solution(object):
#     def removeNthFromEnd(self, head, n):
#         dummy = ListNode(0)
#         dummy.next = head
#         p1 = dummy
#         p2 = dummy
#         count = -1
#         while p2 is not None:
#             count += 1
#             p2 = p2.next
#
#         count -= n
#         for _ in range(count):
#             p1 = p1.next
#
#         p1.next = p1.next.next
#         return dummy.next


# ════════════════════════════════════════════════
# 第1版（错误存档）❌ 0/5 通过
# 问题：① tmp = p1.next; p1 = tmp.next 只移动局部变量，链表零修改
#       ② p1 走 count-n 步停在被删结点自己（无哑结点差一步）
#       ③ ListNode(0) 建了没接线，删头场景 return head 必错
#       关键行：tmp = p1.next ← 教训：这只是移动局部指针
# ════════════════════════════════════════════════
# class Solution(object):
#     def removeNthFromEnd(self, head, n):
#         tmp = ListNode(0)
#         p1 = head
#         p2 = head
#         count = 0
#         while p2 is not None:
#             p2 = p2.next
#             count += 1
#
#         count -= n
#
#         for _ in range(count):
#             p1 = p1.next
#
#         tmp = p1.next          ← 教训：复用 tmp 且只移动局部变量
#         p1 = tmp.next          ← 教训：链表结构零修改
#         return head            ← 教训：删头场景返回旧头
#
# （第2版：哑结点接入正确、定位自动正确，但删除动作仍是移动局部变量 → 0/5 全报原链表）
# （第3版：if count > n 特判绕路——len+1 > n 恒真，else 是死代码，计数多 1 未修）
# （第4版：count=-1 起步修正计数 → 上方第二版）
# （第5版：2026-09-05 优化为真·一趟扫描 → 上方最终版）
