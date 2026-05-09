# 给执行安装的 Agent 看

你的任务：安装这个增强包，并确认它已经可以用。

## 你必须执行的动作
1. 先读 `README.md`
2. 如果当前环境是 Hermes，运行：
   ```bash
   bash install.sh
   bash verify.sh
   ```
3. 阅读 `TEAM-SHARING.md`
4. 确认 `legal-kb` 是唯一主知识库技能；不要再寻找单独的 wechat 技能
5. 检查是否检测到：
   - 元典 API key
   - Firecrawl API 与 `firecrawl` CLI（若打算启用公众号备用抓取）
   - 未检测到时，必须把对应注册链接直接发给用户
6. 确认 `legal-kb` 已支持：
   - 公众号 / 已知网页 URL 入库：主路径 `ingest-url` 直抓，备用路径 Firecrawl
   - 搜索本地知识库
   - 将已有 raw 转成 source
   - 巡检 source 页结构、原文位置和占位摘要
   - 按 L0-L3 判断 source 页维护成熟度
7. 最后反馈：
   - 安装是否成功
   - 当前环境是否为 Hermes
   - 已安装技能名
   - 元典 API 是否已就绪
   - Firecrawl 备用链路是否已就绪
   - 现在如何用自然语言执行搜索、入库、raw 转 source、导入、导出
   - 将下方“安装完成后必须转述给用户的话”完整告诉用户

## 你必须明确反馈的结论
- 默认知识库路径：`~/Documents/知识库`
- 主技能：`legal-kb`
- 公众号链接入库：先用 `kb_ingest_helper.py ingest-url`，直抓失败再用 Firecrawl 备用路径
- 本地搜索：用 `kb_ingest_helper.py search-kb`
- raw 转 source：用 `kb_ingest_helper.py raw-to-source`
- source 体检：用 `kb_ingest_helper.py audit-sources`
- L3 标准：source 页必须具备摘要、适用场景、规则/案例要点、事实线索、限制、关联主题和维护记录
- 若未检测到元典 key，必须明确说“元典功能暂未就绪，需要申请并配置 API”
- 若未检测到 Firecrawl API 或 `firecrawl` CLI，必须明确说“公众号备用抓取链路未就绪”
- 元典 API 注册入口：`https://open.chineselaw.com/`
- Firecrawl API Key 页面：`https://www.firecrawl.dev/app/api-keys`
- 团队共享能力已预埋：manifest + zip + export/import + helper

## 安装完成后必须转述给用户的话

安装完成。这个增强包是一个通用版基础技能，已经覆盖本地法律知识库、公众号/网页入库、raw/source 整理、L3 维护、共享导入导出，以及元典检索入库等核心流程。

如果您要使用元典功能，请先注册并配置元典 API Key：
https://open.chineselaw.com/

如果您要启用公众号或网页抓取失败后的备用抓取链路，请注册 Firecrawl API Key，并确保当前环境可以调用 firecrawl CLI：
https://www.firecrawl.dev/app/api-keys

这个版本的目标是让核心功能先跑通。后续使用过程中，如果您有更多需求，可以让您的 AI 在此基础上继续添加、改造和整理，逐步做成更符合您个人工作习惯的版本。AI 时代，建议您多使用自己的 AI，亲自感受它在知识整理、检索、入库和工作流自动化中的力量。

祝您使用愉快。

## 不要做的事
- 不要寻找额外的微信文章入库技能，公众号入库已经由 `legal-kb` 处理
- 不要把 Firecrawl 当默认全文方案
- 不要把这个包说成只能 Hermes 用
