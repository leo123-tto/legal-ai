# Legal AI

这是一个用于分享法律 AI 相关项目的仓库。

## 当前项目

### `legal-kb-yuandian-bundle`

路径：`legal-kb-yuandian-bundle/`

这是一个给 agent 使用的本地法律知识库增强包，用于建立、搜索、维护、导入、导出和共享法律知识库材料。

这个增强包是一个通用版基础技能，目标是先让核心流程跑通。它覆盖本地法律知识库搭建、本地检索、公众号/网页入库、raw/source 整理、L3 维护、共享导入导出，以及元典检索入库。后续如果有更多工作习惯或专业场景需求，可以让自己的 AI 在此基础上继续添加、改造和整理，逐步做成更适合自己的版本。

它包含：

- `legal-kb`：本地法律知识库主技能，支持搜索已有 raw/source/topic/reports 内容
- `yuandian-legal-search`：元典法规、案例、企业信息检索与入库支持
- 共享 ZIP 导入导出脚本，带 manifest 和导入前查重
- 给同事看的简明说明，以及给 agent 看的安装/执行说明

快速开始：

```bash
cd legal-kb-yuandian-bundle
bash install.sh
bash verify.sh
```

给同事看的简明说明：

```text
legal-kb-yuandian-bundle/HUMAN-GUIDE.md
```

本地搜索示例：

```text
加载 legal-kb 技能，先搜索本地知识库里有没有“执行异议 首查封”的材料，并告诉我 raw 和 source 分别命中了哪些。
```

## API 配置

元典功能需要使用者自行申请并配置 API。Firecrawl 备用抓取需要 API Key，并需要当前环境可以调用 `firecrawl` CLI。仓库里不包含任何密钥或凭据。

注册链接：

- 元典 API：https://open.chineselaw.com/
- Firecrawl API Key：https://www.firecrawl.dev/app/api-keys

可识别的环境变量包括：

- `YUANDIAN_API_KEY`
- `YUANDIAN_API`
- `CHINESELAW_API_KEY`
- `FIRECRAWL_API_KEY`
- `FIRECRAWL_KEY`

## 仓库结构

```text
legal-ai/
├── legal-kb-yuandian-bundle/
│   ├── skills/
│   ├── scripts/
│   ├── README.md
│   ├── HUMAN-GUIDE.md
│   ├── AGENT-ONBOARDING.md
│   └── TEAM-SHARING.md
├── LICENSE
└── README.md
```

## 使用提示

这个仓库里的内容是工作流、自动化和知识库辅助材料，不是法律意见。使用元典、知识库材料或 agent 生成内容时，请自行核对来源、事实和法律依据。

AI 时代，建议多使用自己的 AI，亲自感受它在知识整理、检索、入库和工作流自动化中的力量。祝使用愉快。
