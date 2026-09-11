# ══ #67 二进制求和 · 最终版：右对齐进位法（修复版）✅（2026-09-08）══
# 本题磨 6+ 轮，坑史豪华（见底部）——核心 carry 机制（%2//2）首版就写对，败的全是收尾与对齐
# 骨架：右对齐（短串补零）→ 从末位往左逐位三数相加（a+b+carry）→ %2 写本位 //2 传进位
#       → 循环外 carry 剩 1 则前置 '1'
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        n = max(len(a), len(b))
        aarr = [0] * n
        barr = [0] * n
        for i, x in enumerate(a):
            aarr[n - len(a) + i] = int(x)    # ← 右对齐正确公式：最高位字符落在下标 n-len(a)
        for i, x in enumerate(b):
            barr[n - len(b) + i] = int(x)    #    （错误公式 n-1-i 会整串镜像反转，见坑史）
        carry = 0
        dig = [0] * n
        for j in range(n - 1, -1, -1):       # 从末位往左——进位向高处传，必须低位起算
            tmp = aarr[j] + barr[j] + carry  # 三数相加：本位 a + 本位 b + 低位进位
            carry = tmp // 2
            dig[j] = tmp % 2
        if carry:
            dig = [1] + dig                  # 前置一位，天然无前导零
        return ''.join(str(x) for x in dig)


# ══ 对照解法：力扣官方题解（反转世界流）══
# 来源：https://leetcode.cn/problems/add-binary/solutions/299667/（学习用途，已注明出处）
# class Solution:
#     def addBinary(self, a: str, b: str) -> str:
#         ans = []
#         a = a[::-1]                                  # 反转 = 低位在先，下标 i 即"从低位数第 i 位"
#         b = b[::-1]
#         n = max(len(a), len(b))
#         carry = 0
#         for i in range(n):
#             carry += int(a[i]) if i < len(a) else 0  # 短的越界补 0
#             carry += int(b[i]) if i < len(b) else 0
#             ans.append(str(carry % 2))
#             carry //= 2
#         if carry:
#             ans.append('1')
#         return ''.join(ans)[::-1]                    # 反转回正序
# ← 两版同一数学：低位对齐 + 进位低位起算。官方走"反转世界"，本版走"坐标换算世界"

# ══ 坑史（磨 6 轮教训全集）══
# 坑1: ⭐ aarr[n-1-i] = int(x) 镜像反转——enumerate 从最高位字符起，n-1-i 送最低位，整串倒放
#      （事故核心：AI 推演也翻车！"看起来对"+脑内走查均判对，实测输出 10010 才现形。
#        推演一百遍不如跑一遍——测试用例是唯一真相）
# 坑2: ''.join(str(x))——join 参数必须是序列，单字符等于没拼；外面 for 每轮覆盖 → 只剩最后一字符
#      正确：''.join(str(x) for x in dig)——胶水空串 + 序列元素全 str
# 坑3: for j in range(len) 从高位开始加——进位向高处传，必须 range(n-1, -1, -1)（方向两连错）
# 坑4: final.append(x) 累加器误解 + final 未定义 + reversed(final) 返回迭代器不是 str
#      ——拼字符串用 ''.join 直接 return；dig 正序时无 reversed 事
# 坑5: carry 检查缩在循环内 if j==len1-1——循环结束后才检查剩余进位
# 坑6: dig 多开一格仅在进位时才有资格出现在结果——无进位 join 全量 = 前导零（"11"+"1" 出 "110"）
