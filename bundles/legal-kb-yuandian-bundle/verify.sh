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
fi
if [ -n "${FIRECRAWL_API_KEY:-}${FIRECRAWL_KEY:-}" ]; then
  echo "OK: Firecrawl API detected (backup crawl path available)"
else
  echo "WARN: no Firecrawl API detected (backup crawl path not ready)"
fi

echo "READY COMMAND 1: 加载 legal-kb 技能，把这个微信公众号文章链接完整抓取并入库：<文章链接>"
echo "READY COMMAND 2: 加载 legal-kb 技能，把这个 Word 文档整理进本地知识库，并生成 raw 和 source。"
echo "READY COMMAND 3: 加载 legal-kb 技能，把这个共享 zip 导入知识库，先查重，再告诉我导入了多少、跳过了多少。"
echo "READY COMMAND 4: 加载 legal-kb 技能和 yuandian-legal-search 技能，帮我从元典获取《公司法》全文并入库到本地知识库。"
