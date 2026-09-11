# -*- coding: utf-8 -*-
# 2026-09-02 | #21 合并两个有序链表
# ─────────────────────────────────────────────
# 版本规则：最终版在最上方（唯一可执行代码），历史版本以注释存档于下方，便于对照错误思路
# ─────────────────────────────────────────────

# ══ 最终版（第2版）✅ 5/5 通过 ══
class Solution(object):
    def mergeTwoLists(self, list1, list2):
        """
        :type list1: Optional[ListNode]
        :type list2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        p1 = list1
        p2 = list2

        if p1 is None:
            return list2
        elif p2 is None:
            return list1

        dum = ListNode(0)
        tail = dum

        while p1 is not None and p2 is not None:
            if p1.val <= p2.val:
                tail.next = p1
                p1 = p1.next
            else:
                tail.next = p2
                p2 = p2.next
            tail = tail.next

        if p1 is not None:          # ← 一方打空，另一方整队并入
            tail.next = p1
        elif p2 is not None:
            tail.next = p2

        return dum.next


# ══ 第1版（错误存档）❌ ListNode[0] TypeError + 循环结束后剩余链尾丢失 ══
# 教训：()是"调用/创建"，[]是"取值/下标"（与#13的 roma_map(x) 同族错误）；
#       while双方都不空停止时，必有一方没走完，tail.next 要接上剩余整队
# class Solution(object):
#     def mergeTwoLists(self, list1, list2):
#         p1 = list1
#         p2 = list2
#         if p1 is None:
#             return list2
#         elif p2 is None:
#             return list1
#         dum = ListNode[0]          # ← 应为 ListNode(0)
#         tail = dum
#         while p1 is not None and p2 is not None:
#             if p1.val <= p2.val:
#                 tail.next = p1
#                 p1 = p1.next
#             else:
#                 tail.next = p2
#                 p2 = p2.next
#             tail = tail.next
#         return dum.next            # ← 缺收尾：p1/p2 剩余部分没接上（用例4丢5、6）
