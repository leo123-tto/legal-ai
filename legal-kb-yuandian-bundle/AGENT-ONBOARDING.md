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
   - Firecrawl API（若打算启用公众号备用抓取）
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

## 你必须明确反馈的结论
- 默认知识库路径：`~/Documents/知识库`
- 主技能：`legal-kb`
- 公众号链接入库：先用 `kb_ingest_helper.py ingest-url`，直抓失败再用 Firecrawl 备用路径
- 本地搜索：用 `kb_ingest_helper.py search-kb`
- raw 转 source：用 `kb_ingest_helper.py raw-to-source`
- source 体检：用 `kb_ingest_helper.py audit-sources`
- L3 标准：source 页必须具备摘要、适用场景、规则/案例要点、事实线索、限制、关联主题和维护记录
- 若未检测到元典 key，必须明确说“元典功能暂未就绪，需要申请并配置 API”
- 若未检测到 Firecrawl API，必须明确说“公众号备用抓取链路未就绪”
- 元典 API 注册入口：`https://open.chineselaw.com/`
- Firecrawl API Key 页面：`https://www.firecrawl.dev/app/api-keys`
- 团队共享能力已预埋：manifest + zip + export/import + helper

## 不要做的事
- 不要再提 wechat 独立技能
- 不要把 Firecrawl 当默认全文方案
- 不要把这个包说成只能 Hermes 用
