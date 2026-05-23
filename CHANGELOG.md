# Changelog

所有重要的版本变更都会记录在这里。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Planned
- 见 [ROADMAP.md](./ROADMAP.md)

---

## [1.0.0] - 2026-05-17

第一个对外发布版本。已上架 [法律元力平台](https://yuanli.ailaw.cn) 工具包模块，被公众号「律川 Planet」专文推介。

### Added
- **`legal-kb`** 本地法律知识库主技能
  - 默认知识库根目录 `~/Documents/知识库`
  - 支持搜索本地 raw/source/topic/reports 内容
  - 支持公众号文章入库（浏览器直抽 `#js_content`，Firecrawl 备用）
  - 支持本地文件入库：md、txt、docx、可直抽 PDF、扫描 PDF（经 OCR）、图片（经 OCR）、图片型 PDF
  - 支持 raw → source 整理，L0–L3 维护成熟度分级
  - 支持 source 质量体检（缺段 / 坏链 / 占位摘要 / 未映射 raw）
- **`yuandian-legal-search`** 元典法规/案例/企业信息检索与入库
- **`ocr-mineru`** MinerU 在线 OCR（PDF、图片、Word、PPT、Excel → Markdown）
- 共享 ZIP 导入导出脚本（带 manifest + 导入前查重）
- 安装/验证脚本（`install.sh` / `verify.sh`）适配 Hermes
- 三层文档：
  - `README.md` 项目入口
  - `HUMAN-GUIDE.md` 给同事看的简明说明
  - `AGENT-ONBOARDING.md` 给 agent 看的安装与执行规则
  - `TEAM-SHARING.md` 团队共享规则

### Configuration
- 元典 API：`YUANDIAN_API_KEY` / `YUANDIAN_API` / `CHINESELAW_API_KEY`
- MinerU：`MINERU_TOKEN` + `npm install -g mineru-open-api`
- Firecrawl：`FIRECRAWL_API_KEY` / `FIRECRAWL_KEY` + `firecrawl` CLI

### Notes
- 仓库本身不含任何密钥
- License：MIT
- 不再单独依赖任何 WeChat 抓取 skill，公众号入库能力已并入 `legal-kb`

---

## 早期里程碑（提交历史摘录）

- `2026-05-17` · 适配 MinerU OCR 能力（公众号 browser 直抽 + PDF/图片入库）
- `2026-05-09` · 增强本地知识库搜索能力的对外说明
- `2026-05-08` · 仓库公开
