# Legal AI

> 一个面向中国法律人的 AI 工具与开源工作流仓库。
> 当前主项目：`legal-kb-yuandian-bundle` —— 一个给 AI agent 用的本地法律知识库增强包。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/leo123-tto/legal-ai?style=social)](https://github.com/leo123-tto/legal-ai/stargazers)
[![公众号](https://img.shields.io/badge/公众号-零代码法律人-brightgreen)](https://github.com/leo123-tto/legal-ai#关于作者)

---

## 关于这个仓库

这是刘成律师维护的、面向**中国法律人**的 AI 工具与开源工作流合集。

定位很简单——**不折腾配置、不追概念，把一个又一个开源的、可落地的系统，搬到法律人身边。**

当前仓库聚焦在"**让 AI 真的能用在法律人本地工作流**"这件事上，下一个版本会扩到更多场景（见 [ROADMAP.md](./ROADMAP.md)）。

## 当前项目

### `legal-kb-yuandian-bundle` · 法律知识库组合技能包

路径：`legal-kb-yuandian-bundle/`

> v1.0.0 · MIT License · 已上架 [法律元力平台](https://yuanli.ailaw.cn) 工具包模块

这是一个给 AI agent 使用的本地法律知识库增强包，用于**建立、搜索、维护、导入、导出和共享**法律知识库材料。

它是一个**组合技能包**——把三个 SKILL + 一套共享脚本组合成一个能自洽运转的小系统：

- `legal-kb`：本地法律知识库主技能，支持搜索已有 raw/source/topic/reports 内容，支持公众号文章入库、文件入库（含扫描 PDF 和图片的 OCR 解析）
- `yuandian-legal-search`：元典法规、案例、企业信息检索与入库支持
- `ocr-mineru`：MinerU 在线文档解析，支持 PDF、图片、Word、PPT、Excel 转 Markdown
- 共享 ZIP 导入导出脚本，带 manifest 和导入前查重
- 给同事看的简明说明，以及给 agent 看的安装/执行说明

它覆盖了从"把材料抓进来"到"整理维护"到"本地检索调用"到"团队共享"的**完整闭环**。每个人都可以在这个底座上继续改造，做成更适合自己的版本。

#### 快速开始

```bash
cd legal-kb-yuandian-bundle
bash install.sh
bash verify.sh
```

给同事看的简明说明：[`legal-kb-yuandian-bundle/HUMAN-GUIDE.md`](./legal-kb-yuandian-bundle/HUMAN-GUIDE.md)

#### 本地搜索示例

```text
加载 legal-kb 技能，先搜索本地知识库里有没有"执行异议 首查封"的材料，
并告诉我 raw 和 source 分别命中了哪些。
```

## 被推介

2026-05-22，公众号「律川 Planet」专文推介了这个项目，作为法律元力平台「工具包」模式的范本案例，与 Anthropic 官方 Claude for Legal 插件包并排上架：

> 「刘成律师把它做成了开源的、可组合的包——这正是工具包模块想鼓励的方向。用他自己的话说，他想成为'让大家都能方便用上 AI 的法律人'。」
>
> —— 律川 Planet《[法律元力上线「工具包」模块](https://mp.weixin.qq.com/s/C6qONWt52soPtfqJdtWmBw)》

## API 配置

本仓库不包含任何密钥或凭据。以下 API 需要使用者自行申请并配置：

| 服务 | 用途 | 注册地址 |
|------|------|----------|
| 元典 | 法规/案例/企业信息检索 | https://open.chineselaw.com/ |
| MinerU | 在线文档 OCR 解析（PDF/图片/Word/PPT/Excel） | https://mineru.net/apiManage/token |
| Firecrawl | 公众号/网页抓取备用路径 | https://www.firecrawl.dev/app/api-keys |

可识别的环境变量：

- `YUANDIAN_API_KEY` / `YUANDIAN_API` / `CHINESELAW_API_KEY` — 元典
- `MINERU_TOKEN` — MinerU（CLI：`npm install -g mineru-open-api`）
- `FIRECRAWL_API_KEY` / `FIRECRAWL_KEY` — Firecrawl

详细配置、CLI 安装和故障排查见 [`docs/API-SETUP.md`](./docs/API-SETUP.md)。

## 仓库结构

```text
legal-ai/
├── legal-kb-yuandian-bundle/        # 当前主项目
│   ├── skills/
│   │   ├── legal/
│   │   │   ├── legal-kb/            # 本地知识库主技能
│   │   │   └── yuandian-legal-search/  # 元典检索技能
│   │   └── ocr-mineru/              # MinerU OCR 技能
│   ├── scripts/                     # 共享脚本（ZIP 导入导出 + 查重）
│   ├── README.md                    # 包入口
│   ├── HUMAN-GUIDE.md               # 给同事看
│   ├── AGENT-ONBOARDING.md          # 给 agent 看
│   └── TEAM-SHARING.md              # 团队共享规则
├── .github/                         # Issue / PR 模板
├── CHANGELOG.md                     # 版本变更记录
├── ROADMAP.md                       # 后续版本计划
├── CONTRIBUTING.md                  # 贡献指南
├── LICENSE                          # MIT
└── README.md                        # 你正在看的这份
```

## 关于作者

**刘成律师**，执业律师，公众号「零代码法律人」作者。

定位："不聊底层原理，不敲一行代码——用大白话和自然语言把 AI 变成得力助手的法律人。"

- 公众号：搜索 **零代码法律人**（笔名：不折腾的刘律）
- GitHub：[@leo123-tto](https://github.com/leo123-tto)

如果这个仓库帮到了你的法律工作，欢迎：
- ⭐ Star 这个仓库
- 🐛 [提 Issue](https://github.com/leo123-tto/legal-ai/issues/new/choose) 反馈使用问题
- 🤝 [提交 PR](https://github.com/leo123-tto/legal-ai/pulls) 贡献你的 SKILL 或改进
- 📖 阅读 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解怎么参与

## 使用提示

这个仓库里的内容是工作流、自动化和知识库辅助材料，**不是法律意见**。使用元典、知识库材料或 agent 生成内容时，请自行核对来源、事实和法律依据。

AI 时代，建议多使用自己的 AI，亲自感受它在知识整理、检索、入库和工作流自动化中的力量。祝使用愉快。

## License

MIT © 2026 刘成律师。详见 [LICENSE](./LICENSE)。
