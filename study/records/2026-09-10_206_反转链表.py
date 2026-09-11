# ══ #206 反转链表 · 最终版：三指针接力 ✅（2026-09-10）══
# 指针接线试金石 · 面试 No.1 高频
# 三指针分工：pre=已完成区的头 / cur=当前加工位 / nex=探路先锋（每轮第一个动作先存后继，防断链）
class Solution(object):
    def reverseList(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        cur = head
        pre = None                    # 已完成区 initially 空
        while cur:
            nex = cur.next            # ① 先存后继（此刻链还没断）
            cur.next = pre            # ② 反转当前指针
            pre = cur                 # ③ 已完成区头前移
            cur = nex                 # ④ 加工位前进（用刚存的）
        return pre                    # 退出时 cur=None，pre=新头（原尾）


# ══ 第1版（错误存档）❌：cur/nex 同步双指针 → 断链 + 返回空 ══
# class Solution(object):
#     def reverseList(self, head):
#         cur = head
#         nex = head          # ← 教训1：cur 和 nex 出生即同一节点
#         pre = None
#
#         while nex:
#             cur.next = pre  # ← 教训2：先把 next 掐断，nex 再取 next 已取到刚改的指针
#             pre = cur
#             nex = nex.next  # ← [1,2,3] 实测：nex=1.next=None，循环只跑 1 轮，2、3 没被摸过
#             cur = nex       # ← 教训1续：循环末 cur=nex 永远同步，两个名字一个节点
#
#         return cur          # ← 教训3：退出时 cur=nex=None，返回空；新头在 pre
