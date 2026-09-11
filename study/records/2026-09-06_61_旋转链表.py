# ══ #61 旋转链表 · 最终版：下刀法（测验 T3 重写版）✅（2026-09-08，力扣通过）══
# 骨架：右旋 k = 后 k 个结点搬到前面。不真转——闭环 + 定位下刀，O(n) 一遍
# 坐标系换算（本题灵魂）：倒数第 m 个 = 正数下标 length−m；
#   新尾 = 倒数第 k+1 = 下标 length−k−1 → 从 head 走 length−k−1 步
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # 卫语句（guard clause）：拦截"不需要干活"的情况，让主逻辑放心假设健康输入
        if not head or k == 0 or not head.next:
            return head
        #   not head        → 空链，拦住 None.next 的 AttributeError
        #   k == 0          → 不转，拦住"下刀算出 None 新头"的逻辑错
        #   not head.next   → 单结点，转啥都自己（本版冗余：k%=1→0 会被下面兜住，但防御无害）
        #   ⭐ or 短路求值：条件顺序 = 依赖顺序，被依赖的放前面（not head.next 依赖 head 非 None）

        p1 = head
        length = 1
        while p1.next:              # 停在尾结点（不是 None！#61 测验版的踩尾坑已修）
            p1 = p1.next
            length += 1

        k %= length                 # 一行吞掉三分支：k>length 取余，余 0 = 原样返回
        if k == 0:
            return head

        p1.next = head              # 步骤 1：闭环（尾接回头，链永不丢）

        new_tail = head             # 步骤 2：走 length−k−1 步找新尾（倒数第 k+1 个）
        for _ in range(length - k - 1):
            new_tail = new_tail.next

        new_head = new_tail.next    # 步骤 3：下刀——新头 = 新尾.next，新尾断开
        new_tail.next = None
        return new_head


# ══ 第1版（测验首 attempt，多处错误）❌ 存档（2026-09-06）══
# 四伤清单：
#   伤1: dummy = ListNode       # 无括号——类≠实例（第 2 次踩，已立速查卡）
#   伤2: while p1: p1=p1.next   # 踩尾退出 p1=None，p1.next=p2 → AttributeError
#   伤3: p2 从 head 走 k 步     # 定位在正数端，右旋新头在倒数端——坐标系没换算，断口/接线全错位
#   伤4: 三分支 if/elif 且无 k%len==0 短路  # k=0、k=2len 时链被拦腰截断
#   另：接线对象错——原尾应接 head（闭环），不是接 p2
# ← 教训链：旋转题先画 5 结点方框图标新旧头尾；k 数的是新链坐标，下刀用原链坐标（length−k−1）；
#   防御卫语句置顶；调试 print 交卷前清场
