# Legal AI

这是一个用于分享法律 AI 相关项目的仓库。

它和 `legal-tools` 分开维护：`legal-tools` 是静态网页工具集合；这个仓库专门放 AI 工作流、本地知识库项目、agent 技能、提示词包、共享脚本，以及以后可以给同事下载使用的法律 AI 资料。

## 当前项目

### `legal-kb-yuandian-bundle`

路径：`legal-kb-yuandian-bundle/`

这是一个给 agent 使用的本地法律知识库增强包，用于建立、维护、导入、导出和共享法律知识库材料。

它包含：

- `legal-kb`：本地法律知识库主技能
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

## API 配置

元典和 Firecrawl 功能需要使用者自行申请并配置 API。仓库里不包含任何密钥或凭据。

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
