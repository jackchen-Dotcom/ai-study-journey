# ════════════════════════════════════════════════
# 876. 链表的中间结点 — 最终版 ✅（第二版 · 2026-09-05 二刷）
# 经典三行差速写法：防御搬进循环条件（先检查后迈步）
# 要点：
#   1. while fast and fast.next = 两个守门员（and 短路：第一道没过第二道不执行）
#      → 循环体内 fast.next.next 永不踩空
#   2. 奇偶双出口自动对位：偶数链 fast 跨出链表（=None）退出 → slow 停第二个中间；
#      奇数链 fast 踩尾（fast.next=None）退出 → slow 停正中间
#   3. slow 从 head 出发（起跑线比第一版前移一格）→ 直接 return slow，无需补一步
#   4. while 执行模型：检查只在每轮开头，条件为假挡住的是下一轮，正在跑的这轮一定合法
#
# 第一版教训（见下方存档）：逻辑正确但结构绕——双重检查放循环内，
# 需要 dummy、开头特判、循环内提前 return 三件套；经典版全部省掉
# 详见 notebook.md 2026-09-04 条目（二刷已勾）
# ════════════════════════════════════════════════

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def middleNode(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow


# ════════════════════════════════════════════════
# 第一版（2026-09-04 自创防御式写法）✅ 力扣全用例通过
# 逻辑正确但结构绕：双重检查放循环内 + dummy + 开头特判 + 提前 return 三件套
# 关键行：while 1: ← 教训：无限循环 + 内部提前 return，可被 while 条件守门替代
#         elif p2.next.next is None: return p1.next ← 教训：奇偶双出口正确但难维护
# ════════════════════════════════════════════════
# class Solution(object):
#     def middleNode(self, head):
#         dummy = ListNode(0)
#         dummy.next = head
#         p1 = dummy
#         p2 = dummy
#         if p1.next.next is None:
#             return p1.next
#
#         while 1:
#             if p2.next is not None:
#                 p2 = p2.next.next
#             p1 = p1.next
#             if p2.next is None:
#                 return p1.next
#             elif p2.next.next is None:
#                 return p1.next
