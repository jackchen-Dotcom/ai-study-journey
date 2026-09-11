# ════════════════════════════════════════════════
# 203. 移除链表元素 — 最终版 ✅
# 2026-09-04 一次通过（力扣 + 四个刁钻边界静态验证：连删到空/删头/空表/隔位删）
# 模式：哑结点 + prev/cur 接线删除（#19 知识直接复用，#27 的链表版）
# 复盘要点：
#   1. 删除发生的那轮 p1/p2 都不动，下一轮 p2 = p2.next 恰好滑到正确位置——
#      「删除」没有消灭结点：主链绕过它，它自己的 .next 还指着原来的下一个（幽灵结点借道）
#   2. 做对之后还要能解释对——从"恰好写对"到有意为之
# 详见 notebook.md 2026-09-04 条目
# ════════════════════════════════════════════════

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def removeElements(self, head, val):
        """
        :type head: Optional[ListNode]
        :type val: int
        :rtype: Optional[ListNode]
        """
        dummy = ListNode(0)
        dummy.next = head
        p1 = dummy
        p2 = dummy
        while p1.next:
            p2 = p2.next
            if p2.val == val:
                p1.next = p1.next.next
            else:
                p1 = p1.next

        return dummy.next
