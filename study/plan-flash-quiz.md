# 「闪刷」项目设计书（背诵卡 → AI 学习助手）※ 2026-09-11 立

> 信息截至 2026-09-11（依据当日联网搜索校准：FSRS 算法现状、牛客题库获取方式、个人部署方案；规则见 AGENTS.md 规则 1）。
> 定位一句话：**把你踩过的坑变成可调度、可判分的题库，手机随时刷，最终长成你的私人 AI 学习助手。**
> 项目名暂定「闪刷」（flashquiz），后续可改。

---

## 0. 战略定位（先读这段，防止项目走歪）

### 0.1 和现有路线图的关系——不是第三个项目，是十月主项目的具体形态

10 月主线本来就是「judge.py CLI → FastAPI Web 版 → LangGraph → MCP」。本项目的 v1/v2 阶段**恰好就是这条线的载体**：FastAPI、SQL、AI 判题、RAG、MCP 全部在这个项目里学、在这个项目里用。因此：

- **同一个仓库**（错题本 repo），新建 `flashquiz/` 目录，不另开 repo
- 10 月的「刷题工具 Web 化」与本项目合并为一个 FastAPI 应用：`judge` 路由（算法判题）+ `flash` 路由（知识闪刷）
- 简历叙事升级：「AI 学习助手——算法判题 × 间隔重复闪刷 × AI 判题 × RAG 出题 × MCP 接入」，一条完整产品线
- 正式合并进 roadmap 在 **9/30 月度复盘**时执行

### 0.2 防烂尾三条铁律

1. **每个阶段结束都有一个"当天就能用"的东西**（CLI 能刷、网页能刷、AI 能判），不许攒大招
2. **不做什么清单**（见 §7）优先级高于做什么
3. 9 月主线（chatbot → mini_search → rag.py）神圣不动——本项目 v0 排在**国庆弹性周**

---

## 1. 产品形态：三个板块

### 板块 A「闪刷」（背诵卡的数字化 + 间隔重复）

- 内容来源：`背诵卡.md`（35 张，持续增长）——**你的坑就是题库**
- 题型自适应：概念类出选择题，原理类出简答题
- **间隔重复调度**：今天答对的卡 3 天后再见，连对拉长间隔（1→3→7→16→35 天），答错回炉第 2 天重来——这就是你刷题的三天法，算法化了
- 每次打开 = 「今日到期」队列 + 到期数量徽标，刷完即清零

### 板块 B「模式雷达」（思路训练，本项目的差异化核心）

面试的真正考点不是"会不会写"，是"**看到题能不能识别该用哪个模式**"。三个训练模式：

| 模式 | 玩法 | 数据来源 |
|---|---|---|
| B1 模式识别 | 给题干（不给代码），四选一：该用哪个模式（哑结点/快慢指针/二分/双指针相向/栈/DP…）？答对后展示同族题清单 | [patterns.md](patterns.md) 的模式清单 + [problems/](problems/) 的题干 |
| B2 找茬 | 展示一段**你自己写错过的代码**（错误存档版），问：这段哪里有坑？为什么错？怎么修？ | [records/](../records/) 的错误存档——一座金矿 |
| B3 适用边界 | 给一个模式，列出 N 道题，判"适用/不适用"——练 patterns.md 里写的"适用信号" | patterns.md 的适用信号字段 |

> B2 是灵魂：别人的找茬题你背答案，自己的坑你真的会再踩。**训练目标 = 你的三连问本能化**：题目要什么输出？输入有什么特征？哪个模式沾边？

### 板块 C「外部题库」（八股扩充）

- v1 内容源（**不爬虫**）：① 半人工搬运牛客面经题（看到好题手动录入统一 JSON 格式，10~20 道起步）；② **LLM 批量生成** AI 八股题（Transformer/RAG/Agent/MCP——题纲直接用 roadmap 的面试八股清单），生成后人工审校入库
- 为什么 v1 不爬牛客（2026-09 搜索结论）：官方 API 仅企业版开放（试卷管理类接口，非题库）；页面动态渲染+登录墙+反爬，爬虫处于合规灰区（robots.txt/ToS/频率限制）。**个人学习用途、低频、不二次分发**是底线——v2/v3 若做自动化，只做"面经解析"（贴一篇文章 URL → LLM 抽题入库），不做批量爬取

---

## 2. 总体架构（分层 + 演进）

```
┌─ 手机浏览器 / PWA（添加到主屏幕）
│        │ HTTPS
├─ 接入层：Tailscale（v1，私有组网，10 分钟通）→ Cloudflare Tunnel（v2+，公网域名）
│        │
├─ 应用层：FastAPI（v1 起）
│   ├─ flash 路由：今日到期 / 答题 / 结果反馈 / 统计
│   ├─ radar 路由：模式识别 / 找茬 / 边界判题
│   ├─ judge 路由：算法判题（10 月原计划收编）
│   └─ auth：单用户 token（Header 校验，不做注册体系）
│        │
├─ 领域层（纯 Python 包，v0 就存在，与 Web 解耦）
│   ├─ models.py      Question / ReviewState / Attempt（dataclass）
│   ├─ scheduler.py   间隔重复算法（v0 莱特纳盒 → v2 可换 FSRS）
│   ├─ grader.py      判分器：选择题精确匹配 / 简答题 AI 判分（v2）
│   └─ importers/     题源适配器：recite_md.py（背诵卡）/ records.py（错误存档）/ llm_gen.py（LLM 生成）/ manual_json.py
│        │
└─ 存储层：v0 JSON 文件 → v1 SQLite（SQLAlchemy）→ 可换 PostgreSQL
```

**扩展点设计**（这是"可拓展性"的落点，全部是你能理解的抽象）：
- **题源 = 适配器**：新内容源（牛客搬运、LLM 生成、RAG 从 notebook 挖题）= 新增一个 importer，不动主逻辑
- **题型 = 注册表**：choice/short/bug 用一个 dict 注册（题型 → 出题渲染 + 判分函数），加新题型不改旧代码
- **算法可换**：scheduler 暴露统一接口 `next_interval(state, result)`，v0 莱特纳 → v2 FSRS 平滑替换
- **LLM 可换**：OpenAI 兼容接口（DeepSeek/通义/Kimi 都是这个协议），换模型=换 .env 里一个 URL

## 3. 数据模型

```
questions        题库主表
  id, module(flash|radar|external), qtype(choice|short|bug)
  stem(题干), options(JSON, 选择题), answer(标准答案), explanation(解析)
  tags(JSON, 如 ["异常处理","chatbot"]), source(背诵卡Q7/records#92v2/llm/牛客搬运)
  difficulty(1-3), created_at

review_state     间隔重复状态（每题一条）
  question_id(FK), box(1-5 莱特纳盒), due_date, last_reviewed
  streak(连对次数), lapses(答错次数)

attempts         答题流水（统计的原料）
  id, question_id(FK), user_answer, is_correct
  ai_score(v2, 简答题 0-100), ai_feedback(v2)
  duration_s, reviewed_at
```

统计能力（SQL 练习场）：各 tag 正确率、7 日刷题量、到期堆积曲线、薄弱 tag 排行——**10 月的 SQL/聚合全在这练**。

## 4. AI 判题设计（v2，简答题）

- 调 DeepSeek（你已有 key），**temperature=0**，要求 JSON 输出：

```json
{"score": 0-100, "verdict": "pass|partial|fail", "feedback": "一句话点评+漏了什么"}
```

- 判分 prompt 三要素：题目 + 标准答案 + 评分标准（关键词覆盖/方向正确/无事实错误）
- **降级策略**（直接复用你 chatbot 的异常处理课）：API 失败 → 提示"AI 判分不可用，请自评 对/错"，绝不崩
- 你已有的技能全覆盖：requests + JSON 解析 + try/except + 滑动窗口（判题上下文不用长对话）

## 5. 部署方案（云电脑当服务器）

### v1 首选：Tailscale（2026-09 搜索结论：个人自用最省心）

1. 云电脑装 Tailscale + 手机装 Tailscale，登同一账号
2. 云电脑跑 `uvicorn main:app --host 0.0.0.0 --port 8000`
3. 手机浏览器访问 `http://100.x.x.x:8000`（Tailscale 分配的固定 IP，永不变）
4. 零端口映射、零域名、端到端加密、个人免费——**10 分钟通**

### v2+ 升级：Cloudflare Tunnel（要分享/要 HTTPS/要 PWA 时）

`cloudflared` 隧道 → 固定公网 HTTPS 域名，手机"添加到主屏幕"后体验接近原生 App。

### 云电脑专属风险与对策

| 风险 | 对策 |
|---|---|
| 云电脑重置/回收 → 数据没了 | SQLite 文件每日定时复制 + 每周 push 一次数据备份到 git（私有） |
| 会话断开服务就停 | `nssm` 或任务计划程序把 uvicorn 注册为开机自启服务 |
| 公网暴露被扫 | Tailscale 天然私有（只有你的设备能访问）；上 Tunnel 后加 token 校验 |

## 6. 分阶段路线（对齐现有 roadmap，不新增时间总量）

### 阶段 v0（国庆 10/1~10/7 弹性周，纯 Python，~2 个晚上）
- [ ] `flashquiz/` 目录 + `importers/recite_md.py`：解析背诵卡.md → questions.json（正则/字符串切分练习）
- [ ] `models.py`（dataclass）+ `scheduler.py`（莱特纳盒：答对 box+1 间隔 [1,3,7,16,35] 天，答错回 box1）
- [ ] `cli.py`：命令行刷题（抽到期卡 → 出题 → 选择题判分 → 更新状态存 JSON）
- [ ] pytest 三连（沿用你今天学的：转换器输出原样 / 答题后状态正确 / 到期计算）
- **验收**：云电脑 SSH 进去能刷；面试叙事第一句成立"从自己的错题本长出来的系统"

### 阶段 v1（10 月中下旬，与 FastAPI/SQL 主线合并）
- [ ] FastAPI + SQLAlchemy + SQLite：三个路由（flash/radar/judge）
- [ ] 手机端 Web（Jinja2 模板 + 少量原生 JS，移动优先 CSS）
- [ ] Tailscale 部署上线 + token 校验
- [ ] 统计页（SQL 聚合：tag 正确率、到期堆积）
- **验收**：手机随时刷，README 可复现，里程碑「可访问链接」达成

### 阶段 v2（11~12 月，与 RAG/Agent 主线合并）
- [ ] AI 判题上线（简答题，grader.py）
- [ ] 模式雷达三模式全量（B1/B2/B3），records 错误存档批量入库
- [ ] LLM 题目生成器（roadmap 八股清单 → 选择题 → 人工审校入库）
- [ ] scheduler 换 FSRS（官方 py 包 `fsrs`，2026 年 SRS 事实标准，预测误差 4% vs SM-2 的 14%）
- [ ] （可选）面经解析器：贴牛客面经 URL → LLM 抽题入库（个人低频使用）
- **验收**：简答题 AI 判分 + 模式雷达可用 = 简历项目深度层

### 阶段 v3（2027-01+，AI 学习助手形态）
- [ ] RAG 出题：检索 notebook.md/records 的坑史 → 生成变式题（直接复用你的 rag.py！）
- [ ] MCP server：Claude Desktop 里"查题库/出 5 道题/看薄弱点"
- [ ] PWA（离线刷选择）+ Cloudflare Tunnel 公网域名
- [ ] 学习报告 Agent：每周自动汇总薄弱点 + 推荐加练清单（LangGraph 编排）
- **验收**：roadmap 全部技能点在同一个项目里闭环，跳槽作品集主展项

## 7. 不做什么清单（防烂尾，与 §0.2 配套）

- ❌ 原生 App（iOS/Android）——Web + PWA 够用，且你精力该花在后端/AI
- ❌ 注册登录/多用户体系——单用户 token，永远
- ❌ v1 就上前端框架（React/Vue）——Jinja2 + 原生 JS；前端不是 AI 应用岗的简历卖点
- ❌ v1 就爬牛客——半人工搬运 + LLM 生成先行；爬虫只在 v2+ 做"单篇面经解析"这种低频、合规动作
- ❌ 自研间隔重复算法——v0 莱特纳盒（20 行）起步，v2 直接用 `fsrs` 官方包
- ❌ 9 月动手——v0 排国庆，主线神圣

## 8. 为什么这个项目对跳槽值钱（简历叙事预埋）

1. **个人真实性**：数据全部来自你的错题本/坑史——"我把自己踩的坑做成了训练系统"，比抄的 demo 高两个段位
2. **技能全覆盖**：Python OOP → FastAPI/SQL → 异常容错 → AI 判题（结构化输出）→ RAG → LangGraph → MCP → 部署，roadmap 每月主线都有落点
3. **有算法味**：间隔重复（莱特纳→FSRS）是可讲解的算法选型，面试能聊 trade-off
4. **有数据闭环**：attempts 表 + 统计 + 薄弱分析——评测思维（和 roadmap 的 RAG 评测闭环同构）
