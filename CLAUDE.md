# CLAUDE.md · 项目维护手册

> 这份文档是给**任何接手维护这个仓库的 AI agent**（Claude Code / Codex / Hermes / 等等）看的。
> 它告诉你：这个项目是什么、当前到哪儿了、铁律是什么、下一步该干什么。
> 维护者：刘成律师 ([@leo123-tto](https://github.com/leo123-tto))。

如果你是人类贡献者：欢迎，请直接看 [README.md](./README.md) 和 [CONTRIBUTING.md](./CONTRIBUTING.md)。

---

## 1. 项目身份

- **名字**：legal-ai
- **定位**：面向中国法律人的 AI 工具与开源工作流仓库
- **维护者**：刘成律师（公众号「零代码法律人」，笔名"不折腾的刘律"）
- **License**：MIT
- **当前主项目**：`legal-kb-yuandian-bundle` v1.0.0
  - 已上架 [法律元力平台](https://yuanli.ailaw.cn) 工具包模块
  - 被公众号「律川 Planet」专文推介（[文章](https://mp.weixin.qq.com/s/C6qONWt52soPtfqJdtWmBw)，2026-05-22）
- **GitHub**：https://github.com/leo123-tto/legal-ai

## 2. 几条铁律（违反等于做坏事）

1. **不主动 `git push`**：除非维护者明确说"推一下 / 推上去 / push 吧"。git commit 是可恢复的，push 出去就会被全世界看到。
2. **改任何对外行为前先确认**：SKILL.md 内容、安装脚本、API 调用逻辑、模型选择——这些会影响用户行为的改动，要先把方案告诉维护者，等"OK"或"改成 X 再做"，再动手。
3. **文档错字 / CI 配置 / .gitignore / Issue 模板**这类低风险改动可以直接 commit（但不 push）。
4. **不上传任何 API Key / Token / 密码**：仓库严格保持"零密钥"。提到 API 时只写注册地址 + 环境变量名，永远不写值。
5. **不写入真实当事人姓名 / 案号 / 客户隐私**：测试数据用化名（张三/李四）、虚构案号（如 `(2099)苏99民初0001号`）、占位号（`13800000000`）。
6. **SKILL 改动要保持四份文档一致**：改 `skills/.../SKILL.md` 时，对应的 `README.md` / `legal-kb-yuandian-bundle/README.md` / `HUMAN-GUIDE.md` / `AGENT-ONBOARDING.md` 也要同步更新。
7. **维护时机敏感**：这个仓库被律川 Planet 公开推介过，社区会盯着 v1.1 路线图。每一次 commit 都是公开的对外信号——慢一点、稳一点，比快一点重要。

## 3. 当前状态（截至 2026-05-23）

### 3.1 已发布

- v1.0.0 是当前发布版本，对应 origin/main 上的 commit `9953ebd`（2026-05-17）。
- 包含 3 个 SKILL（`legal-kb` / `yuandian-legal-search` / `ocr-mineru`）+ 共享 ZIP 脚本 + 4 份文档。

### 3.2 本地未 commit 的改动（2026-05-23 这次会话产物）

仓库根目录新增了 5 项（全部 untracked）：

- `CHANGELOG.md` — 整理 v1.0.0 节点 + 早期里程碑
- `CONTRIBUTING.md` — 贡献指南，4 种参与方式
- `ROADMAP.md` — v1.0.x / v1.1 / v2.0 路线图
- `.github/ISSUE_TEMPLATE/` — bug_report / feature_request / new_skill_proposal / config.yml
- `.github/PULL_REQUEST_TEMPLATE.md`

**README.md 改写草稿**还没落到位，放在仓库**外**：
`~/projects/new-idea/2026-05-23-legal-ai-README草稿.md`
（写 README.md 时把那份草稿的内容写进去；草稿文件本身是临时审阅用，不进仓库）

### 3.3 还没做的事

- README.md 替换（用上面那份草稿）
- 第一次 commit（把 5 项新文件 + README 替换 一起 commit）
- 文档去重：主 README / 子 README / HUMAN-GUIDE / AGENT-ONBOARDING 现在 API 配置说明重复 4 次，下一轮抽出 `docs/API-SETUP.md`
- 让维护者在 GitHub 网页给 repo 加 topics（`legal-ai` / `chinese-law` / `legal-skills` / `claude-skills` / `legal-tech`）+ 改 About 段（这个 agent 做不了，维护者点几下）

## 4. 下一步任务清单（按优先级）

> 干每一项前都先 `git status` 看一下当前状态再动手。

### P0 · 立即做（这次会话剩下的事）

- [ ] **任务 1**：用 `~/projects/new-idea/2026-05-23-legal-ai-README草稿.md` 的内容替换 `README.md`。注意只替换"# Legal AI"到文件结尾的部分（草稿文件里前面有元数据说明）。
- [ ] **任务 2**：把 6 项新文件 + README 改写做成**一次 commit**（不要分多次，因为它们是同一波"对外身份呈现升级"）：
  ```bash
  git add CHANGELOG.md CONTRIBUTING.md ROADMAP.md CLAUDE.md .github/ README.md
  git diff --cached  # 给维护者看 diff
  ```
  Commit message 草稿（**等维护者 review 后再执行**）：
  ```
  docs: 加 CLAUDE/CONTRIBUTING/CHANGELOG/ROADMAP + 重写 README

  - 新增 CLAUDE.md 长期维护手册（供 agent 接手）
  - 新增 CONTRIBUTING/CHANGELOG/ROADMAP 三份社区维护文档
  - 新增 .github/ Issue + PR 模板
  - README 加作者段 / 被推介段（律川 Planet 引用）/ Star 引导 / badges
  - 同步仓库结构图
  ```
- [ ] **任务 3**：等维护者确认后 commit。**不要 push**——push 由维护者自己决定时机（铁律 #1）。

### P1 · 这周内（v1.0.x 维护范围）

- [ ] **任务 4**：文档去重。抽出 `docs/API-SETUP.md` 作为唯一的 API 配置说明源，让主 README / 子 README / HUMAN-GUIDE / AGENT-ONBOARDING 都改成"详见 docs/API-SETUP.md"。改完之前先把方案告诉维护者（铁律 #2，这是会影响安装流程的改动）。
- [ ] **任务 5**：HUMAN-GUIDE 增加截图/录屏占位。维护者会自己补图，agent 准备好 `assets/screenshots/` 目录和文件命名规范就行。
- [ ] **任务 6**：整理首批用户反馈到 FAQ。从 GitHub Issues 拉数据，落到 `docs/FAQ.md`。

### P2 · 接下来一个月（v1.1 准备期）

- [ ] **任务 7**：v1.1 候选 SKILL 调研。维护者列在 ROADMAP 里的 6 个候选（执行查询 / 合同审查 / 法院文书生成 / 庭审准备 / 法规校验 / 跨案件知识沉淀），按"实现难度 × 用户呼声 × 跟现有 SKILL 协同度"排个优先级，落到 `docs/v1.1-planning.md`。
- [ ] **任务 8**：观察 Issues 区。出现 Feature Request 时，先回个"我看到了"，然后整理到 `docs/feedback-log.md`，每周拿给维护者看一次。

### P3 · 长期（v2.0 开放贡献者生态）

按 ROADMAP.md 走。具体路径维护者会陆续给指引。

## 5. 工作流约定

### 5.1 Commit Message

用 [Conventional Commits](https://www.conventionalcommits.org/) 风格：

- `feat:` 新功能 / 新 SKILL
- `fix:` 修 bug
- `docs:` 改文档
- `refactor:` 重构（不改行为）
- `chore:` 杂项（依赖、配置、CI）

每条 commit message 都用中文写正文 + 英文写动词前缀。例如：

```
feat: 新增执行查询 SKILL

- 支持被执行人状态/限消/失信查询
- 接入元典 API 缓存
- 输出结构化 markdown 报告
```

### 5.2 改动决策矩阵

| 改动类型 | 改前要问吗 | 改后能 commit 吗 | 能 push 吗 |
|---------|----------|----------------|-----------|
| 文档错字 / 格式 | 不用 | 可以 | 维护者授权 |
| 加 issue / PR 模板 | 不用 | 可以 | 维护者授权 |
| 改 SKILL.md 行为 | **要问** | 维护者确认后可以 | 维护者授权 |
| 改 install.sh / verify.sh | **要问** | 维护者确认后可以 | 维护者授权 |
| 加新 SKILL | **要问 + 列方案** | 维护者确认后可以 | 维护者授权 |
| 改 API 接入方式 | **要问** | 维护者确认后可以 | 维护者授权 |
| 改 CHANGELOG / ROADMAP | 不用（按事实更新） | 可以 | 维护者授权 |
| 改 LICENSE / README 顶部署名 | **要问** | 维护者确认后可以 | 维护者授权 |

### 5.3 跟维护者的协作

- 维护者是律师，不一定看每个技术细节——优先给"做了什么 + 为什么"+ "影响范围"，再给"具体怎么改"。
- 维护者偏好**克制、不焦虑、大白话**的表达。文档/commit message 不要堆术语。
- 维护者称呼自己"刘律"或"刘成律师"，对外身份是公众号「零代码法律人」。
- 维护者已经有 CaseBoard 案件看板项目（在 `~/projects/law-case/`），那里的 CLAUDE.md 写的是同款铁律——遵守那里的"老板"称呼习惯（在 law-case 里），**这个项目（legal-ai）里用"维护者"或"刘成律师"**，因为是开源项目。

## 6. 文件地图

```
legal-ai/
├── CLAUDE.md                            ← 你正在看的，给 agent 看
├── README.md                            ← 项目入口，给所有人看
├── CONTRIBUTING.md                      ← 贡献指南
├── CHANGELOG.md                         ← 版本变更
├── ROADMAP.md                           ← 路线图
├── LICENSE                              ← MIT
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   ├── new_skill_proposal.md
│   │   └── config.yml
│   └── PULL_REQUEST_TEMPLATE.md
└── legal-kb-yuandian-bundle/            ← v1.0.0 主项目
    ├── README.md                        ← 包入口
    ├── HUMAN-GUIDE.md                   ← 给同事看
    ├── AGENT-ONBOARDING.md              ← 给 agent 看
    ├── TEAM-SHARING.md                  ← 团队共享规则
    ├── install.sh / verify.sh           ← Hermes 安装脚本
    ├── manifest-schema.json
    ├── scripts/                         ← 共享 ZIP 导入导出
    └── skills/
        ├── legal/
        │   ├── legal-kb/                ← 本地知识库主技能
        │   └── yuandian-legal-search/   ← 元典检索技能
        └── ocr-mineru/                  ← MinerU OCR 技能
```

## 7. 常用命令

```bash
# 状态检查
git status
git log --oneline -10

# 看本次会话的本地改动
git diff
git diff --cached

# 准备一次 commit
git add <files>
git diff --cached       # 让维护者审
git commit -m "..."     # 维护者确认后做

# 同步 origin（如果别处有更新）
git pull --ff-only

# 看 origin 还有什么没拉
git fetch
git log HEAD..origin/main --oneline
```

## 8. 重要的"不在路线图里"

为了让项目保持专注，**这些方向短期不做**：

- 跟某家律所/平台深度耦合的私有 SKILL
- 闭源 / 付费版本
- 自营云端 SaaS
- 网页版编辑器 / UI 客户端
- 在仓库内做 AI 模型训练 / 微调

如果维护者或别人提出这类需求，记下来放到 `docs/out-of-scope.md`（如果没这文件，新建一个），不要直接开始做。

## 9. 维护者的其它项目（上下文参考）

- **`~/projects/law-case/`** —— CaseBoard 案件看板，Tauri + Rust + React 桌面 App。是 `legal-kb-yuandian-bundle` 同款产品逻辑在"诉讼场景"的产品化形态。这个项目跟 legal-ai 是**姐妹项目**——legal-ai 是给所有律师的通用 SKILL 底座，CaseBoard 是带 UI 的产品。两个项目的设计哲学（本地优先 / 原文件只读 / 隐私铁律）是一致的。
- **`~/projects/legal-article/`** —— 公众号「零代码法律人」文章源文件。维护者每两天一篇，已发 7 篇 + 准备访谈系列。
- **`~/projects/new-idea/`** —— 维护者的 AI 思考归档项目，收录郭宇、黄灵宝、Anthropic、十字路口播客、李想等人的 AI 观点。本仓库的设计思路有不少来自这里的归档。

这些项目互相引用的时候用绝对路径写明，让以后看这份 CLAUDE.md 的 agent 能找到。

---

## 10. 维护日志（每次大改动追加一段）

### 2026-05-23 · 初始建立维护手册

- 添加本 CLAUDE.md 作为长期维护手册
- 添加 CONTRIBUTING.md / CHANGELOG.md / ROADMAP.md
- 添加 .github/ Issue + PR 模板
- 重写 README.md（加作者段 / 被推介段 / Star 引导 / badges）
- 第一次 commit 时机：等维护者 review 完所有 diff

(下一次维护者交接给 agent 时，在这里追加新段。)
