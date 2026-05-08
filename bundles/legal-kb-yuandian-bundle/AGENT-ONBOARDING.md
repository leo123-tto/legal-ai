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
6. 最后反馈：
   - 安装是否成功
   - 当前环境是否为 Hermes
   - 已安装技能名
   - 元典 API 是否已就绪
   - Firecrawl 备用链路是否已就绪
   - 现在如何用自然语言执行入库、导入、导出

## 你必须明确反馈的结论
- 默认知识库路径：`~/Documents/知识库`
- 主技能：`legal-kb`
- 若未检测到元典 key，必须明确说“元典功能暂未就绪，需要申请并配置 API”
- 若未检测到 Firecrawl API，必须明确说“公众号备用抓取链路未就绪”
- 团队共享能力已预埋：manifest + zip + export/import + helper

## 不要做的事
- 不要再提 wechat 独立技能
- 不要把 Firecrawl 当默认全文方案
- 不要把这个包说成只能 Hermes 用
