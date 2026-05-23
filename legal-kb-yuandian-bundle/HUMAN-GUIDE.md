# 给人看的简明说明

这是一个给法律同行和同事分享用的知识库增强包。

你不用研究里面的脚本。正常用法很简单：
**把压缩包给 agent，让它自己安装；你只用自然语言告诉它做什么。**

---

## 这个包能干什么

### 1. 建立和维护本地法律知识库
默认知识库位置：
`~/Documents/知识库`

### 2. 把微信公众号文章入库
输入公众号文章链接，agent 会尝试抓正文、清洗噪音、写入 raw 和 source。

默认用浏览器直接提取正文（不需要任何 API Key）；如果被微信拦截或提取失败，再用 Firecrawl 作为备用路径。

### 3. 搜索本地知识库
你可以先让 agent 查本地有没有相关内容，避免重复入库、重复下载。

### 4. 体检 source 质量
agent 可以扫描 source 页有没有缺段、原文路径坏链、占位摘要，以及还有多少 raw 没被 source 接住。

### 5. 把本地文件入库
当前支持：
- Markdown (`.md`)
- 纯文本 (`.txt`)
- Word (`.docx`)
- **可直接抽取文字的 PDF**
- **扫描版 PDF**（通过 MinerU 在线 OCR 解析）
- **图片/截图**（png/jpg/webp 等，通过 MinerU 在线 OCR 识别）
- **图片型 PDF**（通过 MinerU 在线 OCR 逐页解析）

前提：已安装 `npm install -g mineru-open-api` 并配置 MinerU Token。

### 6. 把 raw 整理成 source
`raw` 是原始材料，`source` 是可复用知识页。agent 可以把已有 raw 生成 source，并继续整理到 L3。

### 7. 从元典获取法规 / 案例 / 企业信息并入库
前提：你已经配置好了元典 API。

### 8. 导出知识库片段给同事
agent 可以把指定的 raw / source 打包成共享 zip。

### 9. 导入同事发来的共享 zip
导入前会先查重，避免把重复内容灌进知识库。

---

## 你平时可以直接说的话

### 安装
```text
安装这个知识库增强包
```

### 入库公众号文章
```text
加载 legal-kb 技能，把这个微信公众号文章链接完整抓取并入库：<文章链接>
```
agent 会优先用浏览器直接提取正文（不需要任何 API Key）；如果失败，再尝试 Firecrawl 备用路径。

### 入库 Word 文档
```text
加载 legal-kb 技能，把这个 Word 文档整理进本地知识库，并生成 raw 和 source。
```

### 搜索本地知识库
```text
加载 legal-kb 技能，先搜索本地知识库里有没有“执行异议 首查封”的材料。
```

### 体检 source 质量
```text
加载 legal-kb 技能，体检一下本地知识库 source 层，告诉我缺段、坏链、占位摘要和未映射 raw 的情况。
```

### 把 raw 整理成 source
```text
加载 legal-kb 技能，把这个 raw 文件整理成 source，并维护到 L3 标准；如果暂时达不到 L3，就告诉我缺什么。
```

### 入库 PDF（包括扫描版）
```text
加载 legal-kb 技能，把这个 PDF 导入知识库；如果是可直抽文字 PDF 就直接入库，如果是扫描版就通过 MinerU 在线 OCR 解析后入库。
```

### 入库图片/截图
```text
加载 legal-kb 技能，把这张图片通过 MinerU 在线 OCR 识别后整理入库。
```

### 导出给同事
```text
加载 legal-kb 技能，把这几个 raw 和 source 导出成共享压缩包给同事。
```

### 导入同事的共享包
```text
加载 legal-kb 技能，把这个共享 zip 导入知识库，先查重，再告诉我导入了多少、跳过了多少。
```

### 从元典拉法规全文
```text
加载 legal-kb 技能和 yuandian-legal-search 技能，帮我从元典获取《公司法》全文并入库到本地知识库。
```

---

## 什么是 L3

简单说，L3 就是“以后能直接复用”的知识页，不是只把原文搬进去。

- L0：只有 raw 原文
- L1：有 source 页面，但只是标题、来源、原文路径
- L2：有摘要、要点、限制和基础标签
- L3：有结论摘要、适用场景、规则/案例要点、事实或证据线索、使用限制、关联主题和维护记录

如果页面里还大量写着“待整理”“待补”，那就还不是 L3。

---

## PDF 现在能做什么

### 可直抽文字的 PDF
直接提取文字、清洗后入库。

### 扫描版 PDF / 图片型 PDF
通过 MinerU 在线 OCR 解析后入库。
- 安装：`npm install -g mineru-open-api`
- Token 申请：https://mineru.net/apiManage/token
- 调用：`mineru-open-api extract file.pdf -o ./out/ --model vlm`
- 如果 Token 无效或额度用完，agent 会根据 `ocr-mineru` 技能中的错误码表告诉你具体原因和解决办法

### 这意味着什么
你不需要手动做 OCR 或提前转换 PDF。扫描版 PDF、图片型 PDF、甚至单独的图片/截图，都可以直接交给 agent 处理。它会调用 MinerU 在线服务完成解析，清洗后入库。

如果没有配置 MinerU Token，agent 应该明确告诉你需要申请 Token（https://mineru.net/apiManage/token），或临时使用 `flash-extract` 免 Token 模式（≤10MB/20 页，IP 限频）。
---

## 哪些 API 需要额外配置

这一节只讲"要不要配 / 点哪个链接"。**详细配置步骤、CLI 安装、免 Token 模式、故障排查**见 [`../docs/API-SETUP.md`](../docs/API-SETUP.md)（仓库根目录下的 `docs/API-SETUP.md`）。

### 元典（法规/案例/企业信息检索）
要。没有 API，就用不了元典入库能力。
注册入口：https://open.chineselaw.com/

### MinerU（扫描 PDF/图片/Word/PPT/Excel 在线 OCR 解析）
要。如果要解析扫描版 PDF 或图片，需要申请 MinerU Token。
申请入口：https://mineru.net/apiManage/token
安装 CLI：`npm install -g mineru-open-api`

### Firecrawl（公众号/网页备用抓取）
可选。它只是公众号抓取失败后的备用方案，不是默认主链路。
公众号入库默认用浏览器直接提取正文（不需要任何 API Key）。
除 API Key 外，当前环境还需要能调用 `firecrawl` CLI。
没配 API 的话，agent 应该明确告诉你：
> 备用抓取链路未就绪。

API Key 页面：https://www.firecrawl.dev/app/api-keys

---

## 你真正要记住的就一句话
**人只负责说自然语言；agent 负责安装、判断、执行、验证。**
