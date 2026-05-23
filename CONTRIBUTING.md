# 贡献指南 · Contributing

> 欢迎所有法律人 / AI 工程师 / 设计师参与这个项目。

这个仓库的初衷是让更多法律人能用上 AI——所以**贡献门槛尽量降低**。你不一定要懂 Python，写一份 SKILL.md 也是贡献，提一条用户体验问题也是贡献。

---

## 你可以怎么参与

### 1. 提 Issue 反馈问题或想法

打开 [Issues](https://github.com/leo123-tto/legal-ai/issues/new/choose) 页面，从模板选一个：

- **Bug Report** — 跑 `install.sh` 报错、入库失败、OCR 没识别出来等
- **Feature Request** — 希望增加某个能力（比如"我希望支持 WPS 文档"）
- **New SKILL Proposal** — 你想到一个新 SKILL，希望加进来或者自己来写

写得越具体越好——什么场景、报了什么错、你期望的行为是什么。

### 2. 提 PR 修复或新增内容

任何 PR 都欢迎，但请：

- 一个 PR 只做一件事（小步快走）
- 在 PR 描述里说清楚动机和影响范围
- 不要在 PR 里塞密钥、token、真实当事人姓名、真实案号
- 改动 SKILL.md 时记得跟 README / HUMAN-GUIDE 保持一致

### 3. 贡献你自己的 SKILL

如果你写了一个对法律人有用的 SKILL（合同审查、文书生成、法规校验、判例检索……），欢迎贡献过来。两种方式：

- **方式 A**：把 SKILL 整个 commit 到 `skills/<分类>/<skill-name>/`，开 PR 让我 review 合并
- **方式 B**：先开一个 New SKILL Proposal Issue，讨论清楚结构后再写

参考现有的 `skills/legal/legal-kb/SKILL.md` 写法。

### 4. 改进文档

文档错字、表述不清、链接坏掉、流程对不上现状—— **改文档跟改代码一样重要**。直接开 PR。

---

## 行为准则

- 友善、尊重彼此
- 用大白话讨论，不抢概念高地
- 不在 issue / PR / 文档里写客户姓名 / 案号 / 隐私信息
- 不上传任何 API Key、Token、密码

---

## 提交流程（开发者视角）

```bash
# 1. Fork 这个 repo

# 2. 在你 fork 的副本上 clone
git clone https://github.com/<你的用户名>/legal-ai.git
cd legal-ai

# 3. 起一个分支
git checkout -b feat/your-feature-name

# 4. 改完之后跑 verify
cd legal-kb-yuandian-bundle
bash verify.sh

# 5. commit + push
git add .
git commit -m "feat: 简短描述你做了什么"
git push origin feat/your-feature-name

# 6. 在 GitHub 上开 PR
```

Commit message 建议用 [Conventional Commits](https://www.conventionalcommits.org/) 风格：

- `feat:` 新功能
- `fix:` 修 bug
- `docs:` 改文档
- `refactor:` 重构（不改行为）
- `chore:` 杂项（依赖、配置）

---

## License

提交 PR 即表示你同意你的贡献以 [MIT License](./LICENSE) 发布。
