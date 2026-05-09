# 增强包：legal-kb + 元典开放接口 + 团队共享

这是一个给通用 agent 用的增强包。Hermes 可直接安装，但不是唯一宿主。

目标很明确：
1. 用 `legal-kb` 作为唯一主技能处理本地法律知识库；
2. 支持公众号链接、md、docx、可直抽文字 PDF 入库；
3. 支持元典法规 / 案例 / 企业信息进入知识库；
4. 支持搜索本地知识库，避免重复入库和重复下载；
5. 支持把已有 `raw` 整理成 `source`，并按 L0-L3 维护成熟度分级；
6. 支持共享 zip 导入导出与导入前查重；
7. 文档设计成 agent 自己读、自己安装、自己验证、自己执行。

---

## 包含的技能
- `legal-kb`
- `yuandian-legal-search`

不再单独依赖任何 wechat 技能。公众号入库能力已经并入 `legal-kb`。

---

## 额外前置：API
### 元典
如果要用元典功能，必须自行申请并配置 API。
注册入口：https://open.chineselaw.com/

可识别环境变量：
- `YUANDIAN_API_KEY`
- `YUANDIAN_API`
- `CHINESELAW_API_KEY`

如果没有这个 key，agent 必须主动反馈：
> 元典技能已安装，但元典功能暂未就绪，因为未检测到 API 配置。
> 请先到 https://open.chineselaw.com/ 注册并配置 API Key。

### Firecrawl（公众号备用抓取）
如果想启用 Firecrawl 备用抓取，也必须自行申请和配置 API。
API Key 页面：https://www.firecrawl.dev/app/api-keys

没有就直说，不要装懂。

已知 URL、公众号文章和网页正文抓取统一走 `legal-kb`，需要备用抓取时再走 Firecrawl。

---

## 团队共享能力
- `TEAM-SHARING.md`
- `manifest-schema.json`
- `scripts/export_kb_pack_zip.py`
- `scripts/import_kb_pack_zip.py`
- `skills/legal/legal-kb/scripts/kb_ingest_helper.py`

大家如果都按同一个 `raw/source` 结构跑，以后接共享盘、NAS 或事务所服务器会很顺。

---

## 安装
### Hermes 方式
```bash
bash install.sh
bash verify.sh
```

### 非 Hermes 方式
至少做到：
1. 建立与本包一致的知识库目录结构；
2. 让 agent 按 `skills/legal/legal-kb/` 和 `skills/legal/yuandian-legal-search/` 中的规则执行；
3. 保持 raw/source/manifest 结构一致；
4. 自行配置元典 API 后再启用相关能力。

安装完成后，agent 应主动提醒：
- 元典 API 注册入口：https://open.chineselaw.com/
- Firecrawl API Key 页面：https://www.firecrawl.dev/app/api-keys

---

## 使用方式
### 公众号链接入库
```text
加载 legal-kb 技能，把这个微信公众号文章链接完整抓取并入库：<文章链接>
```

执行口径：先走 `ingest-url` 直抓；直抓失败、正文过短或遇到微信验证页时，再用 Firecrawl 备用路径。

### 本地 md / Word / PDF 入库
```text
加载 legal-kb 技能，把这个 Word 文档整理进本地知识库，并生成 raw 和 source。
```

```text
加载 legal-kb 技能，把这个 PDF 导入知识库；如果是可直抽文字 PDF 就直接入库，如果不是就明确告诉我需要 OCR 扩展链路。
```

### 搜索本地知识库
```text
加载 legal-kb 技能，先搜索本地知识库里有没有“执行异议 首查封”的材料，并告诉我 raw 和 source 分别命中了哪些。
```

### raw 整理成 source
```text
加载 legal-kb 技能，把这个 raw 文件整理成 source，并说明目前是 L1/L2/L3 哪个等级，还缺什么才能到 L3。
```

### 导出共享 zip
```text
加载 legal-kb 技能，把这几个 raw 和 source 导出成共享压缩包给同事。
```

### 导入共享 zip
```text
加载 legal-kb 技能，把这个共享 zip 导入知识库，先查重，再告诉我导入了多少、跳过了多少。
```

### 元典法规入库
```text
加载 legal-kb 技能和 yuandian-legal-search 技能，帮我从元典获取《公司法》全文并入库到本地知识库。
```

### 元典案例入库
```text
加载 legal-kb 技能和 yuandian-legal-search 技能，帮我检索与股东损害公司债权人利益责任相关的典型案例，挑高价值内容入库。
```

---

## helper 执行器
包内已提供：
`skills/legal/legal-kb/scripts/kb_ingest_helper.py`

agent 在处理本地文件入库、共享 zip 导入导出时，应优先调用这个 helper，而不是现场临时拼命令。

常用命令包括：
- `ingest-url`：公众号文章或已知网页 URL 入库；主路径直抓，备用路径 Firecrawl
- `search-kb`：搜索本地知识库
- `raw-to-source`：把已有 raw 文件生成 source 框架
- `audit-sources`：巡检 source 缺段、原文位置坏链、占位摘要和 raw 映射数
- `ingest-file`：本地文件入库并生成 raw/source
- `export-zip` / `import-zip`：共享包导入导出

## legal-kb 详细规则
`legal-kb` 主技能下面还带了三份参考文件，agent 会按任务需要读取：

- `skills/legal/legal-kb/references/local-first.md`：本地优先检索、外部补检、gap-log
- `skills/legal/legal-kb/references/ingest.md`：材料入库、清洗、source 模板、写库校验
- `skills/legal/legal-kb/references/maintenance.md`：结构巡检、raw/source 映射、L2/L3 判断、批量治理

## 给人看的简明说明

如果是给同事或同行看，直接看：`HUMAN-GUIDE.md`。
它只讲人需要知道的事，不逼人研究技能结构。
