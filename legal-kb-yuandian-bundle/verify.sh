#!/usr/bin/env bash
set -euo pipefail

KB_ROOT="$HOME/Documents/知识库"
for skill in legal-kb yuandian-legal-search; do
  [ -d "$HOME/.hermes/skills/legal/$skill" ]
done
[ -d "$KB_ROOT/raw/notes" ]
[ -d "$KB_ROOT/raw/yuandian-cache" ]
[ -d "$KB_ROOT/wiki/sources" ]
[ -f "$KB_ROOT/wiki/index.md" ]
[ -f "$KB_ROOT/.wiki-schema.md" ]

echo "OK: legal-kb and yuandian-legal-search copied into Hermes skill directory"
echo "OK: KB root ready -> $KB_ROOT"
if [ -n "${YUANDIAN_API_KEY:-}${YUANDIAN_API:-}${CHINESELAW_API_KEY:-}" ]; then
  echo "OK: Yuandian API key detected"
else
  echo "WARN: no Yuandian API key detected; Yuandian features are not ready"
  echo "INFO: Register Yuandian API here: https://open.chineselaw.com/"
fi
if [ -n "${FIRECRAWL_API_KEY:-}${FIRECRAWL_KEY:-}" ] && command -v firecrawl >/dev/null 2>&1; then
  echo "OK: Firecrawl API and CLI detected (backup crawl path available)"
elif [ -n "${FIRECRAWL_API_KEY:-}${FIRECRAWL_KEY:-}" ]; then
  echo "WARN: Firecrawl API key detected, but firecrawl CLI is not installed (backup crawl path not ready)"
  echo "INFO: Create Firecrawl API key here: https://www.firecrawl.dev/app/api-keys"
else
  echo "WARN: no Firecrawl API detected (backup crawl path not ready)"
  echo "INFO: Create Firecrawl API key here: https://www.firecrawl.dev/app/api-keys"
fi

echo "READY COMMAND 1: 加载 legal-kb 技能，把这个微信公众号文章链接完整抓取并入库：<文章链接>"
echo "READY COMMAND 2: 加载 legal-kb 技能，把这个 Word 文档整理进本地知识库，并生成 raw 和 source。"
echo "READY COMMAND 3: 加载 legal-kb 技能，先搜索本地知识库里有没有“执行异议 首查封”的材料。"
echo "READY COMMAND 4: 加载 legal-kb 技能，体检一下 source 层，告诉我缺段、坏链、占位摘要和未映射 raw 的情况。"
echo "READY COMMAND 5: 加载 legal-kb 技能，把这个 raw 文件整理成 source，并说明是否达到 L3。"
echo "READY COMMAND 6: 加载 legal-kb 技能，把这个共享 zip 导入知识库，先查重，再告诉我导入了多少、跳过了多少。"
echo "READY COMMAND 7: 加载 legal-kb 技能和 yuandian-legal-search 技能，帮我从元典获取《公司法》全文并入库到本地知识库。"
echo "NOTE: 公众号备用抓取只使用 Firecrawl。"

cat <<'EOF'

INSTALL COMPLETE MESSAGE:
安装完成。这个增强包是一个通用版基础技能，已经覆盖本地法律知识库搭建、本地检索、公众号/网页入库、raw/source 整理、L3 维护、共享导入导出，以及元典检索入库等核心流程。

如果您要使用元典功能，请先注册并配置元典 API Key：
https://open.chineselaw.com/

如果您要启用公众号或网页抓取失败后的备用抓取链路，请注册 Firecrawl API Key，并确保当前环境可以调用 firecrawl CLI：
https://www.firecrawl.dev/app/api-keys

这个版本的目标是让核心功能先跑通。后续使用过程中，如果您有更多需求，可以让您的 AI 在此基础上继续添加、改造和整理，逐步做成更符合您个人工作习惯的版本。AI 时代，建议您多使用自己的 AI，亲自感受它在知识整理、检索、入库和工作流自动化中的力量。

祝您使用愉快。
EOF
