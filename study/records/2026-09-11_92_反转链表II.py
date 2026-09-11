# ══ #92 反转链表 II · 最终版：三定位 + 段内反转 + 两刀接缝 ✅（2026-09-11，4 版）══
# 硬核题单第一题 · 区间反转 = #206 引擎 + 接缝工程
# 铁律：想改谁的 next 就站谁的位（单向链表不能回头）——prev 提前占位专管接缝
class Solution(object):
    def reverseBetween(self, head, left, right):
        """
        :type head: Optional[ListNode]
        :type left: int
        :rtype: Optional[ListNode]
        """
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy                # 前驱工位：走 left-1 步后停在 left 位的前驱
        p2 = dummy

        if left == right:
            return dummy.next

        for _ in range(left-1):
            prev = prev.next        # ← prev 必须走！v3 忘走 → "1 没了"
        p1 = prev.next              # left 位（反转起点）

        for _ in range(right):
            p2 = p2.next            # right 位

        cur = p1                    # 从 left 位开始（v1 漏了 left 位）
        pre = p2.next               # pre 会演变：5→2→3，退出时=已反转段头

        while cur != p2:            # 故意不处理 p2 自己（v1 把 == 写反 → 零次循环）
            nex = cur.next          # ①存
            cur.next = pre          # ②改
            pre = cur               # ③平移
            cur = nex               # ④前进

        p2.next = pre               # 接缝刀1：right 位归队（接已反转段头 3）
        prev.next = p2              # 接缝刀2：前驱接新头 4（left=1 时 prev=dummy 自动兼容）
        return dummy.next           # 永远返回新入口——head 变量 ≠ 链表头（反转后 head 是区间尾巴）


# ══ 第1版（错误存档）❌：== 写反 + 起点漏位 + 前驱缺失（三伤合一）══
# class Solution(object):
#     def reverseBetween(self, head, left, right):
#         p1 = head
#         p2 = head
#         if left == right:
#             return head
#         for _ in range(left-1):
#             p1 = p1.next
#         for _ in range(right-1):
#             p2 = p2.next
#         cur = p1.next        # ← 教训2：起点 = p1.next，left 位被跳过没反转
#         pre = p2.next
#         while cur == p2.next: # ← 教训1：== 是"相等才继续"，首次 3==5 即 False，循环体零次执行
#             nex = cur.next    #    （想表达的语义是 != p2：没走到 right 位就继续）
#             cur.next = pre
#             pre = cur
#             cur = nex
#         p1.next = cur         # ← 教训3：没有前驱角色——接缝无从下手；left=1 时 return head 也是错的
#         return head
# ← v2：循环/起点/补刀改对，但 prev 角色缺失——dummy.next = p2 接不上（dummy 不在链上，整段挂空）+ return head
# ← v3：声明了 prev = dummy 但忘了让它走（定位循环里只有 p1）→ 1.next 没人改 →
#    输出 4→3→2→5，"1 没了"（1 整段挂在外面）；诊断钥匙：症状 = 谁没接上，就查谁该站没站
# ← 接缝两刀语义（追问过的）：p2.next=pre 不是"4 指向 5"——pre 退出时=3（已演变 5→2→3），
#    是"4 归队"；prev.next=p2 是"1 接 4"。三刀各管一段：轮1 的 2.next=5（区间尾接后续）、
#    p2.next=pre（right 位补刀）、prev.next=p2（前驱接新头）
# ← 核心认知：反转不删节点只改箭头；节点永远都在，变的只是队形和入口
