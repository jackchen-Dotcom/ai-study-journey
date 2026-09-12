# 每日执行清单 · 第 1 个月（2026-09-03 → 10-07）

> 三层文件关系：[roadmap.md](roadmap.md) 管战略 → [plan.md](plan.md) 管算法节奏 → **本文件管每天干什么**。
> 用法：做完一项把 `[ ]` 改 `[x]`；没做标 `⏭`（自动顺延）；**每周日晚上对我说一声进度，我重排下周**。
> 崩溃日保底方案：中午 1 题 + 睡前翻 10 分钟 patterns.md。保底不算中断。

## 🎯 弹药库（试用期空档专用 · 9/11 建，每周日晚重排补新）

> 用法：空档打开 → 按剩余时间取一条 → 做完打勾 → **每次只取一条，做完就收**。
> 公司忙起来整体作废、零负担——赚到的每分钟都是纯利润，不许反向焦虑。

### 15 分钟档（随时可断）
- ☐ 背诵卡 3 张（遮 A 默答，答不上的标 ⬜）
- ☐ 力扣 APP 重刷 1 道错题
- ☐ requirements.txt 补 `pytest` 一行

### 30 分钟档（小整块）
- ☐ Prompt.py 字典坑修复（chatbot_prompt 是**字符串**不是字典：`json.loads()` 或改字典字面量）
- ☐ README 写一节：项目介绍 / 快速开始 / 已知限制（三节凑齐 = 明日里程碑①提前完工）
- ☐ 读 judge.py 20 行（Python 地基；卡住的行记下来晚上问）
- ☐ 遮答案复写一道旧题（#206 / #19 白板重写 + 判题）

### 60 分钟档（上午整块）
- ☐ 3Blue1Brown 深度学习第 1 章（19min）+ 三行笔记
- ☐ pytest 加餐：给 chat() 错误路径写第 4 个测试（先想：不联网怎么测？想不出晚上问）
- ☐ patterns.md 补两条（用户执笔）：类名无括号=图纸、变量三权分立

---

## 时间槽（沿用 roadmap.md）

| 时段 | 时长 | 干什么 |
|---|---|---|
| 中午 | ~1h | LeetCode 队列 1 题（MEDIUM 允许占 2 个中午） |
| 晚 8 点后 | 1.5~2h | 主线任务（下面标 🌙 的） |
| 周六 | 3~4h | 上午错题复盘（plan.md 规定）+ 下午项目攻坚 |
| 周日 | 3h | 测验（plan.md）+ 弹性/休息 |

## 本月终点验收（9/30 对照）

- [ ] 三个能演示的东西：`chatbot.py`（多轮对话）→ `mini_search.py`（语义搜索）→ `rag.py`（引用版问答）
- [ ] GitHub 上有 1 个仓库，README 能看
- [ ] 刷题推进到 #102（第 2 周队列过半）
- [ ] 读懂 judge.py 每一行（roadmap 9 月验收标准）

---

## 第 1 周（9/3 四 ~ 9/6 日）：地基收尾 + 点火

### 9/3（四）
- 🌙 主线：judge.py 从第 72 行 `try:` 读到文件尾（异常处理 + `if __name__ == "__main__"`）
  - 完成标准：能口头说出 judge.py 从启动到出结果的完整流程
- ☀️ 刷题：今天中午已过，无

### 9/4（五）
- ☀️ #19 删除链表的倒数第 N 个结点 ✅ **全流程完成**（5版 5/5，判题+存档+notebook+收尾思考题；哑结点+同速错位）
- 🌙 主线：类与对象① ✅ **完成**（ChatBot 类：`__init__` 装属性 + `greet` 方法 + self 三连问全答；`bot.greet()` 自动塞 self 的机制已点透）
  - 完成标准：能讲清 self、__init__、实例属性 vs 局部变量 → 已达成（test.py）
- ➕ 加课：类与对象② ✅（用户主动要求加练）——盒中盒（history 列表）+ `__str__` + remember 方法 + 作用域问答（"model 不住 greet 里，住盒子里"）+ 实例隔离两连问 → 全部达成；伏笔：类属性 vs 实例属性（写在外面 = 全实例共享，以后回收）

### 9/5（六）
- ☀️ 上午：错题复盘（本周若有错题，遮答案重做）
- 🌙 下午（点火日，3h）：✅ **完成**（已有 DeepSeek key 直接跳过注册）
  1. ~~注册 DeepSeek 或硅基流动 API key~~（用户已有 DeepSeek key）
  2. 建 venv（`.venv`，Python 3.14）+ `pip install requests python-dotenv` + `.env` 存 key ✅
  3. 跑通 20 行 hello 调用（`first_call.py`：load_dotenv → requests.post → 解析 choices/usage）✅ 终端已打印模型回复 + 39 tokens
  - 完成标准：终端打印出模型回复 → 已达成
- 🌙 傍晚：#19 已提前完成 → 补位 **#35 搜索插入位置**（读题+写码+judge 一气呵成，二分入门）
  - 完成标准：判题通过 + 队列勾掉

### 9/6（日）
- ☀️ 测验日：plan.md 组卷（本周错题变式）✅ 部分完成（卷：T1 #977 ❌→重做✅ / T2 #69 ✅→二分重做✅ / T3 #61 ❌→挂起，画图作业待做；详见 plan.md 9/6 进度行）
- 🌙 主线：多轮对话脚本 v1：`while True` + `messages` 列表 ✅ **提前完成**（9/5 深夜，`ai/chatbot.py`）
  - 亮点：自主升级为 `LLM_client` 类（__init__ 装配置 + remember 收消息）——超出任务书；调试中踩实 4 个类与对象实战坑：类≠实例（别名≠造盒子）、__init__ 参数装全局变量、append 返回 None 覆盖列表、role 三标签分工
  - 完成标准：连续对话记得上文 → 已达成（第 3 轮"你现在的版本"接住第 2 轮"你是什么模型"的指代）；tokens 53→87→116 递增 = history 每轮全量重发的直接证据
  - 思考题（自答）：所谓"记忆"到底存在哪里？→ **不在模型里，在用户程序的 history 列表里**，每轮全量重发——"模型无记忆，记忆是你的程序喂给它的完整历史"

---

## 第 2 周（9/7 一 ~ 9/13 日）：API 熟练 + 异常/文件/Git

### 9/7（一）
- ☀️ #35 搜索插入位置 EASY（二分）✅ 已提前（9/5 完成）
- ➕ 加餐：#58 最后一个单词的长度 ✅ 一题两版（正向状态机+反向遍历）、#66 加一 ✅ 双解（数学取巧+进位模拟）——今日 2 题达标
- 🌙 主线：参数实验：temperature=0 vs 1.5 各跑 3 次；加 system prompt 设定人设 ⏭ **顺延 9/8**

### 9/8（二）
- ☀️ #58 最后一个单词的长度 EASY ✅ 已提前（9/7 完成）→ 中午补位 **#67 二进制求和 EASY** ✅ 完成（磨 6 轮，坑史见 notebook）
- 🌙 主线：参数实验（9/7 顺延）✅ **完成**（temperature 0 vs 1.5：0=收敛不冻结、1.5=突发胡言即参数生效铁证；system 人设实验：毒舌程序员完全入戏，system prompt 是最强行为旋钮；结论已指导写入注释）+ 思考题自答（temperature=0 仍不确定 → LLM 非确定性 = 测试难/评测难根源）；异常处理 try/except ⏭ 顺延 9/9
  - 完成标准：差异结论写进代码注释 → 已达成；拔网线程序不崩 ⏭ 顺延
- 📎 挂账：~~#61 合上重写~~ ✅ 9/8 已清、~~patterns.md 两条~~ ✅ 9/8 已清（用户授权代录，AI 整理 8 条新模式入册）
- 📱 零碎时间计划（试用期闲散专用）：**背诵卡**（[背诵卡.md](背诵卡.md)，已复制手机）——5 分钟级翻 3~5 张（遮 A 默答）；10 分钟级可在力扣 APP 重刷错题本 ⬜ 题；上午有整块时间先清 #61 重写（20 分钟）；睡前 10 分钟背诵卡二刷

### 9/9（三）
- ☀️ ~~#66 加一 EASY~~ 已提前（9/7）→ 补位 **#70 爬楼梯 EASY** ✅ 双解（枚举数学法自己的逻辑 + DP 五步法第一课）——**第 1 周队列全清 🎉**
- 🌙 主线：文件与 JSON：对话历史存 `history.json`，重启后读回来接着聊 ✅ **完成**（save + load + try/except FileNotFoundError；验收实锤：跨 2 次重启历史连续，模型答出上次运行的问题）
  - 完成标准：关掉程序再打开，它还记得你说过什么 → 已达成
  - 踩坑史：① `remember(myllm.history)` = 列表把自己塞进自己 → `Circular reference detected`（循环引用初见）② except 里光写异常类名 = 无效语句 ③ 裸 except 会吞 NameError/Ctrl+C → 接什么写什么 ④ **错误回答被持久化**：早期"我没有记忆"的回复存进文件，重启后模型复读前科、污染后续对话（Context Engineering 预演）⑤ 相对路径基于运行命令的 CWD（文件落在项目根而非 ai/）
  - 思考题（自答）：模型否认记忆 = 裸模型免责话术；实际记忆在 messages 里，"我承诺有记忆"写在 system prompt——人设实验已自行完成

### 9/10（四）
- ☀️ #67 二进制求和 EASY（已提前 9/8 完成）→ 中午加餐 **#206 反转链表 EASY** ✅ 两版通过（首版 cur/nex 同步断链+返回空 → 诊断后标准解一次修正；面试 No.1 高频拿下，2 版坑史见 notebook）
- 🌙 主线：重构日 ⏭ **顺延 9/11**（晚间实际投入链表：#206 两版 + 默写挑战 #19 + 硬核 #92 磨 3 版卡"前驱接缝"；接缝两刀语义已讲透——三刀各管一段、反转不删节点只改箭头、prev 提前占位、循环故意漏 p2 退出后补刀）

### 9/11（五）
- ☀️（缓冲日）**#92 反转链表 II MEDIUM ✅ 4 版通过**（9/10 晚磨 3 版卡接缝 → 9/11 定稿：三定位+两刀接缝；坑史见 notebook——==零循环/前驱缺失连坑两次/起点漏位）——硬核题单开张 ✓
- 🌙 顺延账：**ChatBot 重构 ✅ 完成**（四方法 ChatBot 类：add_message/chat/save/load；self 全员上岗、return 替代 print、拼写修正、.env 补 MODEL=deepseek-chat；主程序 11 行 < 15 达标；跨会话记忆验收过）
  - 重构坑史：① chat 内写死全局 myllm = 实例串门风险（self 三连问重现，已修）② "model": "model" 字符串占位 bug ③ .env 缺 MODEL 键 → getenv 返 None（链式排查：代码→传参→配置源）
- 🌙 **Git 第一课 ✅ 完成**（超出任务卡：init → .gitignore 安检 → root-commit c84ca54 45 文件 → 浏览器 OAuth 授权 → push 成功；完成标准"浏览器能看到仓库"达成）
  - 排障坑史（6 连，全是实战级）：① .gitignore 只挡未跟踪文件——history.json 已 add 后改规则追不回，须 `git rm --cached` ② 嵌套仓库 refs/hello-agents（clone 的教程）→ gitignore 除名 ③ **全局幽灵配置**：.gitconfig 里 insteadOf 规则把所有 github.com 自动改写成 gh-proxy（加速教程残留）——排查钥匙：我写入的地址和 -v 显示不符 = 有重写 ④ PowerShell 反引号 = 续行符/URL 混入字符，幽灵字符三连 ⑤ unrelated histories → pull --allow-unrelated-histories --no-edit ⑥ 凭据管理器浏览器授权一次免密
  - 教训沉淀：git 命令粘贴先瞄首尾；地址写入和显示不符时查 --get-regexp insteadof；官方排障 hint 的每个命令都要读懂再执行
- 💭 **深度焦虑五连 → 收束**（9/11 晚，重要认知资产）：① 焦虑对象漂移（RAG 烂大街→chatbot 太浅→ReAct 才深→全部都浅→没人要）= 根源不是技术是心急 ② 资深评审法：他主动求狠评 → 9 条工程债清单（P0:3轮自杀/网络裸奔/无requirements/人设漂移；P1:token预算/硬编码/零测试/无日志/input裸奔）——**清单全在 roadmap 找得到还款日 = 路线被反向验证** ③ 生产级 = 学习态 + 工程化增量堆叠（规范×真实场景×可维护性三件齐）；hello-agents 是教程产品非生产系统，但其工程规范可当抄写模板 ④ 检验标准三问：自己在用吗→真实数据会被查吗→陌生人 5 分钟能跑吗 ⑤ 深度=穿透度不是行数；摇摆才是皮毛最大制造机，单线走到里程碑
- 📌 **9/12 开工单 → 任务包制首发**（9/11 用户要求加大每日密度：核心任务 + 评审债抢跑，每晚 ~2h 满负荷；P1 债务在 9 月分摊消化，10 月 FastAPI/SQL 量级不动）：
  1. P0 四连（~30min）：q 退出替代 3 轮自杀 / chat 网络异常 try/except（还 9/8 顺延账）/ requirements.txt / load 后检查 history[0] 人设
  2. P1 抢跑①（~40min）：token 预算雏形——history 超 N 条触发滑动窗口截断（Context Engineering 第一课，从 10 月提前）
  3. P1 抢跑②（~40min）：pytest 第一课——test_chatbot.py 三连测（save→load 往返原样 / add_message 计数 / 人设检查）
  4. README（~30min）：照 hello-agents 骨架写
  5. commit + push（~20min）：**脱拐跑，只给任务不给命令**
  - ☀️ 上午照旧：错题复盘（#19/#35 三天法）+ 检查昨晚 JD 对照作业

#### 9/11 下午 + 晚间抢跑单（开工单前置，P0 是债不是加餐）

**下午·零碎时间（实习闲散专用）**：
- ⬜ 背诵卡 3~5 张（重点翻：#92 三定位+两刀接缝、Git 六连坑）
- ~~力扣 APP 重刷 #92~~ → **取消**（当天重刷太早，记忆未衰减验不出水平；三天法复写已排 9/14）

**下午·整块时间（若有 ≥30min）**：
- ✅ P0-1（3 版迭代）：q 退出替代 3 轮自杀——终版 `while 1` + `if user_input == "q": break`（判断在 chat 之前，q 不进 history）；坑史：① 首版 `while max_conver_len < 3 or q != "q"` 两坑叠加——q 未赋值先在条件里用 = NameError 崩（变量先赋值再进条件）+ or 方向反（or 一边真就继续，应 and）② 中间变量 q 冗余，直接判 user_input
  - 待清：L49 `max_conver_len = 0` 成死代码
- ✅ P0-2（5 版迭代）：chat() 网络异常 try/except——终版单 try 双 except：ConnectionError→网络提示 / HTTPError→key 错误提示，return 交还决策权（**还清 9/8 顺延账**）；坑链（异常处理最重一课）：① except 后接方法调用/数字 → NameError、TypeError（**except 接异常类名，类名 = traceback 冒号前**）② 把自己写错代码的 TypeError 诊断书误当 401 病名抄进去 ③ 裸 except 三犯（吞 Ctrl+C）④ break 进方法 = SyntaxError → return 交还决策权 ⑤ raise_for_status 必须罩进 try
  - 待清：L52/L71 注释死代码、L55 max_conver_len 死代码、"api_key Error" 措辞（HTTPError 还含 429/500，不止 key 错）

**晚 8 点后（~2h 满负荷）**：
- ✅ P0-3（5min）：requirements.txt——`pip freeze > requirements.txt`（6 行：2 直接 + 4 传递依赖）；验收 `pip install -r` 全 already satisfied；坑：PowerShell 裸 `>` = UTF-16 编码（pip 能读但其他工具可能不认），`Out-File -Encoding utf8` 转 UTF-8
- ✅ P0-4（15min）：load 后检查 history[0] 人设——`if myllm.history[0]["role"] != "system": myllm.history.insert(0, prompt)`（insert 塞队首 vs append 塞队尾）；伪代码→Python 一步到位
  - 已知坑（P1 健壮性）：空 history `[]` → `history[0]` 触发 IndexError（FileNotFoundError 接不住），取索引前先判空
- ✅ P1-①（~50min）：token 预算雏形（Context Engineering 第一课）——滑动窗口截断：`self.history = [self.history[0]] + self.history[-self.max_history:]`（保 system 头 + 最近 N-1 条）；max_history 提成 __init__ 参数（还"硬编码"债半条）；验收：len 封顶不再涨（N=5 实测稳 6 / N=10 机制同路）
  - 坑史：① 切片不改原列表，`myllm.history[-5:]` 无接收者=蒸发（表达式必须有接收者）② 发送切片 [-5:] 把 system 切丢——人设丢失（截断要一刀保头，别"切丢再补"）③ [0]字典+[-5:]列表相加 TypeError（+ 拼接两边同类，单字典要包 [ ]）④ max_history 参数化后 chat 里漏 self. 前缀两处——L33 每轮炸/L34 条件分支才炸（**分支内代码也要过变量名**）⑤ "截断没生效"实为算术：1(system)+N=总条数
- ✅ P1-②（~60min）：pytest 第一课全绿（3 passed）——test_add_message_counts / test_save_load_roundtrip（tmp_path 临时目录）/ test_ensure_system
  - 前置重构三件：① `if __name__ == "__main__":` 护栏（防 import 执行主程序——9/3 读 judge.py 的知识落地）② ensure_system 收编进类（`not self.history or` 短路先判空——**顺手还清 P0-4 IndexError 债**）③ save/load 加 path 默认参数（测试不覆盖真实 history.json）
  - 坑史：① 根目录裸跑 pytest → 递归收集 refs/ 教程仓库 24 个测试全炸（collection≠执行；.gitignore 管不了 pytest）→ pytest.ini `testpaths=ai` 钉边界 ② IDE 缓冲区 ≠ 磁盘：改完没 Ctrl+S 重跑，红的一字不差 ③ `len(bot.history == 1)` 括号位置=运算顺序（bool 无 len()）④ chatbot_prompt 字符串 vs 字典（Prompt.py 待修：json.loads 或字典字面量）
  - pytest.ini：testpaths = ai（test 边界）；pytest 加入依赖待办

**留给明天（9/12 周六下午·里程碑①）**：README + 脱拐 commit/push → 「别人 clone 下来 5 分钟能跑起来」

#### 🚀 闪刷 v0 建成（9/11 深夜插队，用户主动要求；占用国庆 v0 名额）
- [x] 三板块本地可刷：A 闪刷 35 题（背诵卡自动转换）/ B 模式雷达 23 题（模式识别 17 + 找茬 6）/ C 外部题库 13 题（八股）= 71 题
- [x] 设计书 → [plan-flash-quiz.md](plan-flash-quiz.md)（WebSearch 校准：FSRS / 牛客合规 / Tailscale 部署）
- [x] 结构：models / scheduler（莱特纳盒，可换 FSRS）/ grader（AI 判简答，降级自评）/ store（JSON→v1 SQLite）/ importers（背诵卡解析器 + 种子）/ cli；14 测试全绿；pytest.ini testpaths=ai flashquiz
- [x] **v0.5 Web 版追加**（用户要求前端）：flashquiz/web.py（FastAPI，判分全在服务端防作弊）+ static/index.html（单页 vanilla JS，手机友好）；AI 判分真回路实测 pass；requirements.txt 重写 UTF-8
- [x] 顺带排障：.env 从 ai/ 收编仓库根（单真相源，chatbot.py/grader.py 显式指向）；Prompt.py 字符串→字典坑修复（用户自己正在做，AI 补完）；fastapi/uvicorn 入 venv
- [ ] 用户任务：跑一遍三板块真实体验 → 扒源码学习（建议顺序：models → scheduler → cli → recite_md → grader）；README 一节照实写

### 9/12（六）
- ☀️ 上午：错题复盘（3 天法：#19/#35 重做验证）✅ **双题白板一遍对**（#19 同速错位+p2.next 踩尾语义主动选对；#35 门挂范围条件±1 收缩，return right+1 ≡ left——口径提醒：面试统一 return left）
- 🌙 下午：里程碑①：chatbot 定稿（类 + 异常 + JSON 持久化 + README 三件套）
  - 完成标准：别人 clone 下来 5 分钟能跑起来

### 9/13（日）
- ☀️ 测验日 + 晚上休息（连轴 10 天了，强制半休）
- 🌙 弹性：落后补这里；没落后 → 休息就是任务

---

## 第 3 周（9/14 一 ~ 9/20 日）：embedding 与检索（RAG 前半，全部手写不用框架）

### 9/14（一）
- ☀️ #69 x 的平方根 EASY（二分）（已提前完成）→ 补位：**#92 遮答案复写（三天法到期）**——不看 notebook，白板写出三定位+两刀接缝
- 🌙 主线：概念日：调 embedding API，把"猫在睡觉/狗在吃饭/飞机起飞"变向量并 print
  - 完成标准：能说出"向量 = 意思的坐标，越近 = 越像"

### 9/15（二）
- ☀️ #70 爬楼梯 EASY（DP 入门，重点题）
- 🌙 主线：手写 cos_sim（纯 Python，不用任何库），验证"猫vs狗 > 猫vs飞机"
  - 完成标准：相似度排序符合直觉

### 9/16（三）
- ☀️ #83 删除排序链表中的重复元素 EASY（对比 #26 找差异）
- 🌙 主线：切块实验：把 notebook.md + patterns.md 按 ~200 字/重叠 50 字切块
  - 完成标准：打印块数 + 随机 3 块看切得对不对

### 9/17（四）
- ☀️ #61 旋转链表 MEDIUM（上）：读题 + 思路（又是链表 + 计数）
- 🌙 主线：全部块向量化 + 存 `kb.json`
  - 完成标准：重启程序能加载，不重新调 API

### 9/18（五）
- ☀️ #61（下）：写码 + 判题 + 收尾
- 🌙 主线：写 `search(query)` 返回 Top3 块
  - 完成标准：问"栈的套路"能召回 patterns.md 对的块

### 9/19（六）
- ☀️ 上午：错题复盘
- 🌙 下午：`mini_search.py` 定稿 + 推 GitHub
  - 完成标准：命令行输入问题 → 输出最相关的 3 个知识块

### 9/20（日）
- ☀️ 测验日
- 🌙 弹性：落后补这里；没落后 → **加餐：给 chatbot 装 search 工具（ReAct 雏形）**——mini_search.py 的 search() 包成 tool：模型输出 JSON 决策 → 程序执行 → 结果回注 → 循环。约 50 行，串起 9 月全部产出（用户对 Agent 兴趣强烈，提前开 Agent 之门；10 月 LangGraph 即此循环的工业化）

---

## 第 4 周（9/21 一 ~ 9/30 三）：RAG 闭环 + 项目 A 启动

### 9/21（一）
- ☀️ #88 合并两个有序数组 EASY（对比 #21 找差异）
- 🌙 主线：RAG v1：检索块拼进 prompt → 生成回答
  - 完成标准：答案明显基于你的文档，不是模型瞎编

### 9/22（二）
- ☀️ #94 二叉树的中序遍历 EASY
- 🌙 主线：加引用：答案末尾标注（来源：patterns.md · 第X块）
  - 完成标准：每句回答可溯源

### 9/23（三）
- ☀️ #144 前序遍历 EASY
- 🌙 主线：调优实验：块大小 200 vs 500、top_k 2 vs 5，各跑 5 问对比
  - 完成标准：结论一句话写进 README

### 9/24（四）
- ☀️ #145 后序遍历 EASY
- 🌙 主线：`rag.py` 定稿：加载 → 循环问答 → 引用。里程碑②
  - 完成标准：推 GitHub

### 9/25（五·中秋）
- 放假：休或弹性

### 9/26（六）
- ☀️ 上午：错题复盘
- 🌙 下午：项目 A 启动：收集 20~30 条**脱敏**工单（抹掉姓名/号码，只留业务结构）→ 存 JSON
  - 完成标准：knowledge base 能被 rag.py 加载
- 🌙 晚上：工单知识库接入 rag.py，试问 10 条

### 9/27（日）
- ☀️ 测验日
- 🌙 主线：项目 A 加分项：工单自动分类（LLM 输出 JSON：类别/紧急度/建议回复）
  - 完成标准：对 5 条工单给出正确分类

### 9/28（一）
- ☀️ #100 相同的树 EASY
- 🌙 主线：项目 A：自动回复草稿生成 + 简单 CLI 菜单

### 9/29（二）
- ☀️ #101 对称二叉树 EASY
- 🌙 主线：项目 A 收尾 + README（背景-动作-结果写法，为简历预演）

### 9/30（三）
- ☀️ #102 层序遍历 MEDIUM（上）：BFS 第一课
- 🌙 主线：**月度复盘**：对照"本月终点验收"逐项打分 → 告诉我结果，我按 AGENTS.md 规则 1 先联网搜 2026 年 10 月最新技术动态，再出 10 月计划

---

## 国庆 10/1（四）~ 10/7（三）：弹性黄金周

- [ ] 强制休息 ≥2 天（防止 10 月中旬崩盘）
- [ ] #102（下）+ #104 最大深度（把第 2 周队列收尾）
- [ ] 追赶所有 ⏭ 项
- [ ] 没落后的话加餐：LangGraph 开胃第一课（装包 + 跑通第一个两节点图）※ 2026-09 校准：生产编排标准是 LangGraph，不是裸 LangChain
- [ ] 10/8 回来对表
- [ ] 10 月计划见下 ↓（信息截至 2026-09-04，依据 AGENTS.md 规则 1 搜索校准）

---

# 第 2 个月（2026-10-08 → 10-31）：FastAPI/SQL 打底 + LangGraph/MCP 入门

> 主项目贯穿全月：**智能刷题助手演进**——judge.py CLI → FastAPI Web 版 → LangGraph 编排 → MCP Server 化。
> 刷题：中午 1 题照旧，第 2 周队列收尾后我拉新题单。

## 10 月终点验收（10/31 对照）

- [ ] FastAPI 三个接口：`POST /ask`（RAG 问答）、`POST /judge`（判题）、`GET /stats`（错题统计）
- [ ] SQLite 判题记录入库；SQL 增删改查 + JOIN 能手写
- [ ] LangGraph v1.0：三节点 + 条件边 + checkpointer 的判题流水线图
- [ ] MCP：自定义 Server 含 2 个工具，Claude Desktop 能调你的错题本
- [ ] Git 会 branch/merge；项目全推 GitHub

## 第 1 周（10/8 四 ~ 10/11 日）：FastAPI 起步

### 10/8（四）
- ☀️ #102 层序遍历（下）：写码 + 判题 + 收尾
- 🌙 主线：`pip install fastapi uvicorn` → 第一个 GET 接口 → `uvicorn` 起服务 → 浏览器访问
  - 完成标准：能说清"装饰器路由 + uvicorn 是什么"

### 10/9（五）
- ☀️ #104 二叉树的最大深度 EASY
- 🌙 主线：POST 接口 + Pydantic 模型 → 把 rag.py 包成 `POST /ask`
  - 完成标准：curl/接口工具调 /ask 能得到 RAG 回答

### 10/10（六）
- ☀️ 上午：错题复盘（本周错题 + 国庆遗留）
- 🌙 下午：路径参数/查询参数 + 自动文档 `/docs` 玩一遍
- 🌙 晚上：弹性

### 10/11（日）
- ☀️ 测验日
- 🌙 弹性（新框架首周，留缓冲）

## 第 2 周（10/12 一 ~ 10/18 日）：SQL + Web 化项目

### 10/12（一）
- 🌙 主线：SQLite + SQLAlchemy 建库建表（problems、records 两张表）；SQL：SELECT/WHERE
  - 完成标准：命令行查表能看到 9 月判题数据

### 10/13（二）
- 🌙 主线：SQL INSERT/UPDATE/DELETE + SQLAlchemy CRUD → 判题结果自动入库
  - 完成标准：跑一次 judge 后数据库多一行

### 10/14（三）
- 🌙 主线：SQL JOIN + 聚合函数（面试八股级）→ 写 `GET /stats`（各题通过率统计）
  - 完成标准：/stats 返回真实统计 JSON

### 10/15（四）
- 🌙 主线：Web 化①：judge.py 判题逻辑抽成函数 → `POST /judge`（收代码+题号，回判题结果）
  - 完成标准：接口判一道 #19 能返回通过/失败

### 10/16（五）
- 🌙 主线：Git 进阶：branch / checkout / merge——开 `feature/judge-api` 分支开发，完成后合回
  - 完成标准：git log 里能看到分支合并记录

### 10/17（六）
- ☀️ 上午：错题复盘
- 🌙 下午：Web 化②：串起 /ask、/judge、/stats，写 README（含接口示例）
  - 完成标准：里程碑④——Web 版判题助手最小可用，推 GitHub

### 10/18（日）
- ☀️ 测验日
- 🌙 弹性

## 第 3 周（10/19 一 ~ 10/25 日）：LangGraph v1.0 周

> ⚠️ 教程防坑：网上多数教程是废弃的 v0.1 API。认准 v1：`add_edge(START, 'node')`（不是 `set_entry_point`）、`Annotated[list, add_messages]`（不是手动拼 messages）、`create_react_agent` 已废弃。

### 10/19（一）
- 🌙 主线：心智模型日：State/Node/Edge = "工人/工位/传送带"；`pip install langgraph langgraph-prebuilt` → 两节点线性图跑通
  - 完成标准：能画出自己第一个图的节点流向

### 10/20（二）
- 🌙 主线：State 深入：TypedDict + `Annotated[list, add_messages]` 自动合并；节点函数"收 state、回 dict"
  - 完成标准：能解释为什么 messages 要用 reducer 而不是直接覆盖

### 10/21（三）
- 🌙 主线：条件边：`add_conditional_edges` + router 函数 → 写"奇偶路由"小图
  - 完成标准：不同输入走不同路径，`print` 验证

### 10/22（四）
- 🌙 主线：实战①：把"读题 → 判题 → 点评"三步做成图（先硬编码顺序）
  - 完成标准：喂一道题，图跑完输出三步结果

### 10/23（五）
- 🌙 主线：实战②：加条件路由（通过→记笔记节点；失败→存错题本节点）+ checkpointer 持久化初体验
  - 完成标准：失败用例真的被写进错题本

### 10/24（六）
- ☀️ 上午：错题复盘
- 🌙 下午：里程碑⑤：graph 版判题流水线定稿 + 推 GitHub
  - 完成标准：README 里有图结构示意（手画拍照也行）

### 10/25（日）
- ☀️ 测验日
- 🌙 弹性（LangGraph 新概念多，留缓冲）

## 第 4 周（10/26 一 ~ 10/31 六）：MCP 周

### 10/26（一）
- 🌙 主线：概念日：Host/Client/Server 三层、Tools/Resources、STDIO vs SSE；口诀"MCP 调工具，A2A 调 Agent"
  - 完成标准：能对着自己的 chatbot 说清"如果它接 MCP 会多什么能力"

### 10/27（二）
- 🌙 主线：FastMCP hello world：`uv init` + `uv add "mcp[cli]"` → `@mcp.tool()` 写加法工具 → `mcp.run(transport="stdio")`
  - 完成标准：本地 server 跑通

### 10/28（三）
- 🌙 主线：接 Claude Desktop：配置 json 注册你的 server，实测加法工具
  - 完成标准：Claude 真的调用了你写的工具

### 10/29（四）
- 🌙 主线：实战：把 mini_search.py 封装成 MCP 工具 `search_notes(query)`
  - 完成标准：Claude 里问"栈的套路"能查到你的 patterns.md

### 10/30（五）
- 🌙 主线：加第二个工具 `get_problem(id)`（读 problems/ 目录）→ 在 Claude 里让 AI 查题 + 点评
  - 完成标准：里程碑⑥——AI 助手通过 MCP 直接用你的错题本

### 10/31（六）
- ☀️ 上午：错题复盘 + 国庆无测验顺延处理
- 🌙 下午：**月度复盘**：对照"10 月终点验收"逐项打分 → 告诉我结果，我按 AGENTS.md 规则 1 联网搜 11 月最新动态后出下月计划
- 🌙 晚上：休

---

## 加练菜单（9/4 用户主动要求，自愿加餐，不占主线队列）

> 规则：**主线优先，加餐用富余精力**；做完打勾、记 notebook；这些题不在 plan.md 队列，不影响原进度。

| ☐ | 题 | 什么时候做 | 练什么 | 和今天的关系 |
|---|---|---|---|---|
| ✅ | #203 移除链表元素 EASY（一次通过 9/4） | 今晚主线后富余 20~30min | 哑结点 + 接线删除 | #27 的链表版，今天全部知识直接复用 |
| ✅ | #876 链表的中间结点 EASY（9/4 自创防御式写法通过，力扣全过；双重检查=经典 while 条件守门，已讲透奇偶两分支） | 明天中午碎片 15min | 差速流派（快2慢1） | 你总结的"另一张牌"，与 #19 同速错位对照 |
| ✅ | 默写挑战：#19 count 版（9/10 骨架全对 + 5 边界走查过；结尾三 if 发胖 → 归约一行 `p2.next=p2.next.next`） | 9/10 提前清账 | 指针操作肌肉记忆 | 结尾发胖 = "None 即接线终点"还差半格，复盘已记 |
| ✅ | #206 反转链表 EASY（9/10 两版通过：首版断链+返回空 → 三指针接力标准解） | ~~周末弹性槽~~ 提前拿下 | 指针接线试金石，**面试 No.1 高频** | 专治"移动局部变量 vs 改 .next"——两个坑都踩了又都修好 |

⚠️ 防过载条款：以上全部可砍。哪天只够做一件事 → 做 daily.md 主线，加餐永远让位。

---

## 硬核题单（9/4 加餐二档：比队列难一档，用户主动要求）

> 预期管理：#19 你写了 5 版——在下面的题里，**3~5 版是常态，一次通过是意外**。卡 30 分钟可看题解 → 合上重写 → 记 notebook。

| ☐ | 题 | 难度 | 练什么 | 预期 |
|---|---|---|---|---|
| ✅ | #92 反转链表 II（9/11 通过，4 版：==零循环/起点漏位/前驱缺失/prev 忘走 → 三定位+两刀接缝） | 9/10 晚~9/11 | 区间反转（#206 进阶版） | 预期 2~4 版，实际 4 版符合；接缝"三刀各管一段"已吃透 |
| ☐ | #142 环形链表 II | MEDIUM | 差速找相遇 → 数学推入环点 | 2~4 版 |
| ☐ | #33 搜索旋转排序数组 | MEDIUM | 二分思维天花板 | 3~5 版 |
| ☐ | #146 LRU 缓存 | MEDIUM | 哈希+双链表设计题，面试超高频 | 3~5 版 |
| ☐ | #25 K 个一组翻转链表 | HARD | 链表全部技能总考 | 一天内不丢人 |

优先级：**主线 > 加练菜单 > 硬核题单**。硬核题单全部是弹性任务，周末/富余精力消化。

---

## 动态调整规则（我执行，你不用记）

| 情况 | 动作 |
|---|---|
| 落后 ≤2 天 | 顺延到下个弹性槽（周日/国庆），主线顺序不变 |
| 连续 3 天没学 | 触发减载：砍当周"实验类"任务（调优/Git），只保 刷题 + 核心里程碑 |
| 超前完成 | 周末加餐下一周任务，或提前进 LangChain |
| 某任务卡住 >2 天 | 直接告诉我卡在哪，我拆成更小的步 |
| 每周日 21:00 前 | 对我说一句本周情况，我重排下周清单 |
| ⭐ **高强度模式**（9/11 用户要求） | **主线神圣**：当日 🌙 主线未完成前禁碰一切加餐（含硬核题单/默写挑战）；周日弹性槽默认实弹（追赶 + 深度加餐），不再默认休息；主线的深度任务（评测/接缝类）不顺延只拆步 |
| 原则 | **宁少勿浅：刷题和两个里程碑（chatbot、rag.py）优先级最高，其他都可砍** |
