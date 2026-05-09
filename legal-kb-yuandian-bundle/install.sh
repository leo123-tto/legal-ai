#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST_ROOT="$HOME/.hermes/skills/legal"
KB_ROOT="$HOME/Documents/知识库"

mkdir -p "$DEST_ROOT"
for skill in legal-kb yuandian-legal-search; do
  rm -rf "$DEST_ROOT/$skill"
  cp -R "$SRC_DIR/skills/legal/$skill" "$DEST_ROOT/"
done

mkdir -p   "$KB_ROOT/raw/notes"   "$KB_ROOT/raw/images"   "$KB_ROOT/raw/yuandian-cache"   "$KB_ROOT/wiki/sources"   "$KB_ROOT/wiki/topics"   "$KB_ROOT/wiki/reports"   "$KB_ROOT/_inbox"

write_if_missing() {
  local path="$1"
  local content="$2"
  if [ ! -f "$path" ]; then
    printf "%s" "$content" > "$path"
  fi
}

write_if_missing "$KB_ROOT/purpose.md" $'# 本地法律知识库

目标：沉淀可复用的法律材料，并与团队共享格式保持一致。
'
write_if_missing "$KB_ROOT/gap-log.md" $'# gap-log

记录本地未命中但值得后续补库的高价值缺口。
'
write_if_missing "$KB_ROOT/log.md" $'# log

记录主库级重要操作。
'
write_if_missing "$KB_ROOT/.wiki-schema.md" $'# 最小知识库结构

- raw/notes/：原文或近原文材料
- raw/images/：少量需要留档的图片
- raw/yuandian-cache/：元典检索缓存
- wiki/sources/：来源页/整理页
- wiki/topics/：专题入口
- wiki/reports/：治理或专题报告
- _inbox/：待处理材料
- 团队共享使用 manifest + payload 结构
'
write_if_missing "$KB_ROOT/wiki/index.md" $'# 本地知识库索引

> 这是最小初始化索引。

## 使用入口
- raw：`raw/notes/`
- yuandian-cache：`raw/yuandian-cache/`
- source：`wiki/sources/`
- topics：`wiki/topics/`
- reports：`wiki/reports/`
'
write_if_missing "$KB_ROOT/wiki/log.md" $'# wiki log

记录 wiki 层结构调整与批处理。
'

printf "Installed Hermes skills into: %s
" "$DEST_ROOT"
printf "Knowledge base root ready at: %s
" "$KB_ROOT"
if [ -n "${YUANDIAN_API_KEY:-}${YUANDIAN_API:-}${CHINESELAW_API_KEY:-}" ]; then
  echo "OK: Yuandian API key detected."
else
  echo "WARN: no Yuandian API key detected. Yuandian features are not ready."
  echo "INFO: Register Yuandian API here: https://open.chineselaw.com/"
fi
if [ -n "${FIRECRAWL_API_KEY:-}${FIRECRAWL_KEY:-}" ] && command -v firecrawl >/dev/null 2>&1; then
  echo "OK: Firecrawl API and CLI detected. Backup crawl path is available."
elif [ -n "${FIRECRAWL_API_KEY:-}${FIRECRAWL_KEY:-}" ]; then
  echo "WARN: Firecrawl API key detected, but firecrawl CLI is not installed. Backup crawl path is not ready."
  echo "INFO: Create Firecrawl API key here: https://www.firecrawl.dev/app/api-keys"
else
  echo "WARN: no Firecrawl API detected. Backup crawl path is not ready."
  echo "INFO: Create Firecrawl API key here: https://www.firecrawl.dev/app/api-keys"
fi
printf "Next: bash verify.sh
"
