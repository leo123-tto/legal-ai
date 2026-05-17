---
name: ocr-mineru
description: MinerU 在线文档解析技能。支持 PDF、图片（png/jpg/webp 等）、Word、PPT、Excel 转 Markdown。通过官方 CLI 调用，需申请 Token。
---

# MinerU 在线 OCR

## 概述

MinerU 是在线文档解析服务，能把 PDF、图片、Word、PPT、Excel 转为高质量 Markdown。

- 官网：https://mineru.net
- API 文档：https://mineru.net/apiManage/docs
- Token 申请：https://mineru.net/apiManage/token

## 首次使用

### 1. 申请 Token

前往 https://mineru.net/apiManage/token，注册登录后申请 API Token。

### 2. 安装 CLI

```bash
npm install -g mineru-open-api
```

### 3. 配置 Token

```bash
# 方式 1：环境变量
export MINERU_TOKEN="your-token-here"

# 方式 2：CLI 交互
mineru-open-api auth

# 方式 3：配置文件 ~/.mineru/config.yaml
```

## 两种模式

| 维度 | `flash-extract`（轻量） | `extract`（精准） |
|------|------|------|
| Token | ❌ 免登录（IP 限频） | ✅ 需要 |
| 模型 | 固定 pipeline 轻量 | `pipeline`（默认）/ `vlm`（推荐）/ `MinerU-HTML` |
| 文件大小 | ≤ 10 MB | ≤ 200 MB |
| 页数 | ≤ 20 页 | ≤ 200 页 |
| 批量 | ❌ 单文件 | ✅ ≤ 200 个文件 |
| 输出 | Markdown（CDN 链接） | Zip（Markdown/JSON，可选 docx/html/latex） |
| 额度 | 免费 IP 限频 | 每天 1000 页高优先级 |

## 支持的文件格式

PDF、图片（png/jpg/jpeg/jp2/webp/gif/bmp）、Doc、Docx、Ppt、PPTx、Xls、Xlsx、HTML

## 调用方式

```bash
# 轻量模式（免 Token，快速试看，≤10MB/20页）
mineru-open-api flash-extract file.pdf -o ./out/

# 精准模式（Token 认证，推荐）
mineru-open-api extract file.pdf -o ./out/ --model vlm

# 批量处理（PDF + 图片混合）
mineru-open-api extract *.pdf *.png -o ./out/ --concurrency 5

# 指定页码范围
mineru-open-api extract file.pdf -o ./out/ --pages "2,4-6"

# 导出额外格式
mineru-open-api extract file.pdf -o ./out/ -f docx,html

# 网页解析
mineru-open-api extract "https://example.com/article" -o ./out/
```

## 常见错误码

| 错误码 | 说明 | 解决建议 |
|--------|------|----------|
| A0202 | Token 错误 | 检查 Token 是否正确，是否有 Bearer 前缀，或更换新 Token |
| A0211 | Token 过期 | 更换新 Token |
| -500 | 传参错误 | 确保参数类型及 Content-Type 正确 |
| -10001 | 服务异常 | 请稍后再试 |
| -10002 | 请求参数错误 | 检查请求参数格式 |
| -60001 | 生成上传 URL 失败 | 请稍后再试 |
| -60002 | 文件格式失败 | 文件名及链接需带正确后缀，且为支持的格式之一 |
| -60003 | 文件读取失败 | 检查文件是否损坏并重新上传 |
| -60004 | 空文件 | 请上传有效文件 |
| -60005 | 文件超出限制 | 检查文件大小，最大支持 200MB |
| -60006 | 文件页数超限 | 请拆分文件后重试 |
| -60007 | 模型服务不可用 | 请稍后重试或联系技术支持 |
| -60008 | 文件读取超时 | 检查 URL 可访问性 |
| -60009 | 任务队列已满 | 请稍后再试 |
| -60010 | 解析失败 | 请稍后再试 |
| -60011 | 获取有效文件失败 | 请确保文件已上传 |
| -60012 | 找不到任务 | 请确保 task_id 有效且未删除 |
| -60013 | 没有权限访问该任务 | 只能访问自己提交的任务 |
| -60014 | 删除运行中的任务 | 运行中的任务暂不支持删除 |
| -60015 | 文件转换失败 | 可以手动转为 PDF 再上传 |
| -60016 | 文件转换失败 | 文件转换为指定格式失败，可尝试其他格式或重试 |
| -60017 | 重试次数达到上限 | 等后续模型升级后重试 |
| -60018 | 每日解析任务数量已达上限 | 明日再来 |
| -60019 | HTML 解析额度不足 | 明日再来 |
| -60020 | 文件拆分失败 | 请稍后重试 |
| -60021 | 读取文件页数失败 | 请稍后重试 |
| -60022 | 网页读取失败 | 可能因网络问题或限频导致，请稍后重试 |

## 遇到错误怎么办

CLI 会返回明确的错误信息。根据错误码查上表：

- **Token 问题**（A0202/A0211）→ 去 https://mineru.net/apiManage/token 重新申请
- **额度用完**（-60018/-60019）→ 等第二天，或切换到 `flash-extract` 免 Token 模式
- **文件格式问题**（-60002/-60003/-60004/-60005/-60006）→ 检查文件是否损坏、格式是否支持、大小是否超限
- **服务问题**（-10001/-60007/-60009/-60010）→ 稍后重试
- **权限问题**（-60013）→ 确认 Token 属于你
- **网络问题**（-60008/-60022）→ 检查 URL 是否可访问，是否被限频

## 输出说明

成功时，CLI 会把 Markdown 输出到 `-o` 指定的目录。目录内包含：
- `<文件名>.md` — 解析后的 Markdown 文本
- `images/` — 提取的图片（如果有）

解析结果保留原文的排版结构、表格、公式等信息。
