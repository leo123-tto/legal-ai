# API 配置指南

这一份是本仓库**唯一的 API 配置权威文档**。所有 SKILL、bundle 文档、HUMAN-GUIDE、AGENT-ONBOARDING 在涉及 API 时都会指回这里。

> 安全铁律：本仓库不包含任何密钥或凭据，也不要把你申请到的密钥写进任何 commit 里。所有密钥都通过环境变量传入。

---

## 一图看懂

| 服务 | 是否必需 | 用途 | 没配会怎样 |
|------|---------|------|----------|
| **元典**（ChineseLaw） | 用元典功能才需要 | 法规 / 案例 / 企业信息检索与入库 | `yuandian-legal-search` 技能装上但调用时报"未就绪" |
| **MinerU** | 处理扫描件/图片才需要 | 扫描 PDF、图片型 PDF、图片/截图、Word/PPT/Excel 在线 OCR 解析 | 可直抽文字的 PDF 仍可入库；扫描件入库会被拒绝 |
| **Firecrawl** | 可选 | 公众号 / 网页抓取的**备用**路径（默认主路径是浏览器直抽，不用任何 API Key） | 公众号入库主路径仍可用；主路径失败时无备用 |

整个 bundle 的**主流程在零 API Key 的状态下就能跑通**：本地知识库搭建、可直抽文字 PDF 入库、Markdown/Word 入库、本地搜索、raw 转 source、ZIP 导入导出。
API 只在解锁特定能力时才需要。

---

## 1. 元典（ChineseLaw）

### 1.1 注册与申请

1. 打开 https://open.chineselaw.com/
2. 注册账号 → 实名认证
3. 进入控制台获取 API Key
4. 部分高级能力（执行查询、跨库检索）可能需要单独开通，按平台提示走

### 1.2 配置环境变量

元典 API Key 可以通过以下任一环境变量传入，agent 会按优先级读取：

```bash
export YUANDIAN_API_KEY="你的-key"     # 推荐
# 或
export YUANDIAN_API="你的-key"          # 兼容历史命名
# 或
export CHINESELAW_API_KEY="你的-key"    # 兼容元典官方命名
```

把上面任意一行写进 `~/.zshrc` 或 `~/.bashrc`，重开终端生效。
**不要写进任何 commit 文件里**。

### 1.3 没配置时的标准反馈

agent 在检测不到元典 Key 时，必须主动告诉用户：

> 元典技能已安装，但元典功能暂未就绪，因为未检测到 API 配置。
> 请先到 https://open.chineselaw.com/ 注册并配置 API Key。

不要装作能查，也不要瞎编结果。

### 1.4 验证

```bash
echo "${YUANDIAN_API_KEY:-${YUANDIAN_API:-${CHINESELAW_API_KEY:-未配置}}}"
```

输出不是"未配置"即视为已就绪。

---

## 2. MinerU（在线文档 OCR 解析）

### 2.1 注册与申请

1. 打开 https://mineru.net/apiManage/token
2. 注册账号
3. 在 Token 管理页申请 Token

### 2.2 安装 CLI

MinerU 调用统一走官方 CLI（**不要手搓 REST 调用**）：

```bash
npm install -g mineru-open-api
mineru-open-api --version    # 验证安装成功
```

CLI 依赖 Node.js（建议 18 LTS 以上）。

### 2.3 配置 Token

二选一：

**方式 A：环境变量**
```bash
export MINERU_TOKEN="你的-token"
```

**方式 B：交互式配置**
```bash
mineru-open-api auth
# 按提示粘贴 Token，CLI 会写入本地配置
```

环境变量优先级高于本地配置；agent 默认读 `MINERU_TOKEN`。

### 2.4 没 Token 时的兜底：`flash-extract` 免 Token 模式

MinerU 提供一个免 Token 的轻量模式，限制如下：

- 单个文件 ≤ 10 MB
- 单次最多 20 页
- 按调用方 IP 限频
- 不适合长扫描卷宗 / 大量图片批量识别

agent 在用户没配置 Token、但只是临时想 OCR 一张图或一份短文件时，可以走 flash-extract；用户后续要批量处理就必须申请 Token。

### 2.5 没配置时的标准反馈

agent 在用户上传扫描 PDF / 图片、但检测不到 MinerU Token 时：

> 这份是扫描版/图片，需要走 MinerU 在线 OCR 才能入库。
> 当前未检测到 MinerU Token。
> 若只是临时识别一份短文件（≤10MB / 20 页），可以走 `flash-extract` 免 Token 模式。
> 长期使用请申请 Token：https://mineru.net/apiManage/token
> 申请后执行 `npm install -g mineru-open-api` 并配置 `MINERU_TOKEN`。

### 2.6 常见错误处理

| 现象 | 含义 | 处理 |
|------|------|------|
| `401 / Unauthorized` | Token 无效或过期 | 重新生成 Token，更新 `MINERU_TOKEN` |
| `403 / quota exceeded` | 当月额度用完 | 等下个计费周期，或购买升级 |
| `413 / file too large` | 文件超过单次上限 | 拆分文件；或免 Token 模式时压到 10MB 以下 |
| `429 / rate limit` | 触发限频 | 降低并发；免 Token 模式注意 IP 限频 |
| `mineru-open-api: command not found` | CLI 未安装或 PATH 未生效 | `npm install -g mineru-open-api`；检查 `npm root -g` 是否在 PATH |

更详细的错误码表见 `skills/ocr-mineru/SKILL.md`。

### 2.7 验证

```bash
mineru-open-api --version          # CLI 是否就绪
echo "${MINERU_TOKEN:-未配置}"     # Token 是否就绪
```

两者都通过即视为可用。

---

## 3. Firecrawl（公众号 / 网页抓取备用路径）

### 3.1 它的角色：备用，不是默认

请先记住一句话：**公众号入库默认走浏览器直接提取 `#js_content`，不需要任何 API Key**。
Firecrawl 只在以下情况启用：

- 浏览器直抽失败
- 正文异常短或被微信验证页拦截
- 用户明确指定要用 Firecrawl

不要把 Firecrawl 当默认全文方案，也不要给用户造成"必须配 Firecrawl 才能抓公众号"的错觉。

### 3.2 注册与申请

1. 打开 https://www.firecrawl.dev/app/api-keys
2. 注册账号 → 在 API Keys 页面新建一个 Key

### 3.3 安装 CLI

```bash
npm install -g @mendable/firecrawl-cli
firecrawl --version
```

（具体 CLI 包名以 Firecrawl 官方文档为准；agent 检测时只要 `firecrawl` 命令可执行即可。）

### 3.4 配置环境变量

```bash
export FIRECRAWL_API_KEY="你的-key"     # 推荐
# 或
export FIRECRAWL_KEY="你的-key"         # 兼容备用命名
```

### 3.5 没配置时的标准反馈

agent 在浏览器直抽失败、需要走 Firecrawl 备用时，如果检测不到 Key 或 CLI：

> 备用抓取链路未就绪。
> 公众号主路径抓取失败，备用 Firecrawl 路径需要 API Key 和 `firecrawl` CLI。
> Key 申请页面：https://www.firecrawl.dev/app/api-keys
> CLI 安装：`npm install -g @mendable/firecrawl-cli`

不要装作能继续抓。

### 3.6 验证

```bash
which firecrawl                              # CLI 是否就绪
echo "${FIRECRAWL_API_KEY:-${FIRECRAWL_KEY:-未配置}}"
```

---

## 4. 一键自检：我配齐了吗？

复制以下脚本到终端，可以快速看清三个 API 的就绪状态：

```bash
echo "—— 元典 ——"
echo "  Key: ${YUANDIAN_API_KEY:-${YUANDIAN_API:-${CHINESELAW_API_KEY:-未配置}}}"

echo "—— MinerU ——"
echo "  Token: ${MINERU_TOKEN:-未配置}"
command -v mineru-open-api >/dev/null && echo "  CLI: 已安装 ($(mineru-open-api --version 2>/dev/null))" || echo "  CLI: 未安装"

echo "—— Firecrawl ——"
echo "  Key: ${FIRECRAWL_API_KEY:-${FIRECRAWL_KEY:-未配置}}"
command -v firecrawl >/dev/null && echo "  CLI: 已安装" || echo "  CLI: 未安装"
```

agent 在 `install.sh` / `verify.sh` 之外、用户问"我都配好了吗"时，可以直接用这段。

---

## 5. 安全注意

- 任何密钥 / Token / Key **永远不要写进**：仓库内代码、注释、commit message、文档示例、issue / PR 描述
- `.env` 文件不应被 commit；项目根目录的 `.gitignore` 已经覆盖（如未覆盖请补）
- 团队共享 ZIP 通过 `scripts/export_kb_pack_zip.py` 导出时，agent 应该扫描内容是否泄露 Key，发现可疑字段要拒绝导出
- 如果误把 Key commit 出去，立刻在对应平台**吊销并重发 Key**，再清理仓库历史（`git filter-repo` 或平台支持工单）

---

## 6. 相关文档

- 主仓库 README：[`../README.md`](../README.md)
- bundle README：[`../legal-kb-yuandian-bundle/README.md`](../legal-kb-yuandian-bundle/README.md)
- 给同事看：[`../legal-kb-yuandian-bundle/HUMAN-GUIDE.md`](../legal-kb-yuandian-bundle/HUMAN-GUIDE.md)
- 给 agent 看：[`../legal-kb-yuandian-bundle/AGENT-ONBOARDING.md`](../legal-kb-yuandian-bundle/AGENT-ONBOARDING.md)
- MinerU 技能：[`../legal-kb-yuandian-bundle/skills/ocr-mineru/SKILL.md`](../legal-kb-yuandian-bundle/skills/ocr-mineru/SKILL.md)
- 元典技能：[`../legal-kb-yuandian-bundle/skills/legal/yuandian-legal-search/SKILL.md`](../legal-kb-yuandian-bundle/skills/legal/yuandian-legal-search/SKILL.md)
