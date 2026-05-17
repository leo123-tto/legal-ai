---
name: legal-kb
description: Build, search, maintain, import, export, and deduplicate a local Chinese legal knowledge base under ~/Documents/知识库; ingest WeChat public-account article URLs, webpages, markdown, text, Word, PDF (text-extractable and scanned via OCR), and images; create raw/source pairs; turn existing raw notes into source pages; maintain source pages to L3 reusable quality; and exchange knowledge-base fragments through manifest-based ZIP packs.
---

# Legal KB

Use this skill when the user wants to search or maintain a local legal knowledge base, ingest legal materials or WeChat public-account article URLs, create raw/source records, turn raw notes into source pages, improve a source page to L3 reusable quality, export materials for colleagues, or import a shared knowledge-base ZIP.

Default knowledge-base root:

```text
~/Documents/知识库
```

Expected structure:

```text
raw/notes/
raw/images/
raw/yuandian-cache/
wiki/sources/
wiki/topics/
wiki/reports/
_inbox/
```

## Operating Rules

- Treat `legal-kb` as the main knowledge-base skill.
- Preserve source traceability: every imported item should keep its origin, processing date, and raw/source relationship.
- Search the local KB before adding or downloading new material.
- Prefer the helper script for deterministic local file or URL ingest, raw-to-source conversion, search, ZIP export, and ZIP import.
- Deduplicate before importing shared packs.
- Do not invent legal facts, missing citations, or source metadata.
- For scanned or image-only PDFs, and for images/screenshots: load `ocr-mineru` to parse them via MinerU online OCR, then clean and ingest the result.
- If Yuandian content is needed, load `yuandian-legal-search` as a companion skill and verify API configuration first.
- For known URLs and WeChat public-account articles, use browser extraction first, then direct URL ingest, and Firecrawl only as the backup path.

## Helper

Use this script first for supported mechanical operations:

```text
scripts/kb_ingest_helper.py
```

Common commands:

```bash
python3 scripts/kb_ingest_helper.py ingest-file --path "/path/to/file.docx" --title "材料标题" --source-label "本地文件"
```

```bash
python3 scripts/kb_ingest_helper.py ingest-url --url "https://mp.weixin.qq.com/s/..." --source-label "微信公众号"
```

```bash
python3 scripts/kb_ingest_helper.py export-zip --out-zip "/path/to/share.zip" --files raw/notes/example.md wiki/sources/example.md --source-agent "agent-name" --notes "共享说明"
```

```bash
python3 scripts/kb_ingest_helper.py import-zip --pack-zip "/path/to/share.zip"
```

```bash
python3 scripts/kb_ingest_helper.py search-kb --query "执行异议 首查封" --limit 20
```

```bash
python3 scripts/kb_ingest_helper.py raw-to-source --raw-path "~/Documents/知识库/raw/notes/example.md" --level L3
```

```bash
python3 scripts/kb_ingest_helper.py audit-sources --limit 20
```

Supported local ingest file types:

- `.md`
- `.txt`
- `.docx`
- text-extractable `.pdf`
- scanned/image-based `.pdf` (requires `ocr-mineru` skill — MinerU online OCR)
- images (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`, `.bmp`) — requires `ocr-mineru`
- `.doc`, `.ppt`, `.pptx`, `.xls`, `.xlsx` — requires `ocr-mineru`

## WeChat Article Ingest

When the user asks to ingest a WeChat public-account article or another known webpage URL:

1. Search the local KB first with the article title, URL, or key phrase to avoid duplicate ingest.
2. **Primary path (no API key needed):** open the page in a browser and extract the article body directly:
   - Navigate to the URL.
   - Extract the article body via `document.querySelector('#js_content')?.innerText || ''`.
   - Extract metadata: title (`document.title` or `#activity-name`), publish time (`#publish_time`), account name (`#js_name`).
   - Clean noise: remove follow prompts, ads, author bios, read-more prompts, comments, platform footer.
   - Write paired `raw/notes/` and `wiki/sources/` files.
3. **Backup path:** if the browser approach fails (page blocked, redirected, or `#js_content` is empty/missing), run `ingest-url` through the helper to fetch directly.
4. **Firecrawl fallback:** if direct fetch is blocked, too short, or returns a verification page, use Firecrawl. Requires `FIRECRAWL_API_KEY` or `FIRECRAWL_KEY` and the `firecrawl` CLI. If not configured, tell the user the backup path is not ready and ask for the article text or a saved file.
5. After ingest, clean obvious public-account noise such as follow prompts, ads, author bios, read-more prompts, comments, and platform footer text.

Use Firecrawl explicitly when needed:

```bash
python3 scripts/kb_ingest_helper.py ingest-url --url "https://mp.weixin.qq.com/s/..." --source-label "微信公众号" --prefer-firecrawl
```

**Browser extraction reference:**
- Body: `document.querySelector('#js_content')?.innerText || ''`
- Title: `document.querySelector('#activity-name')?.innerText || document.title || ''`
- Publish time: `document.querySelector('#publish_time')?.innerText || ''`
- Account name: `document.querySelector('#js_name')?.innerText || ''`

## Local Search

When the user asks whether the KB already has something, or before adding a new source, run `search-kb`.

Default search roots:

- `raw/notes/`
- `wiki/sources/`
- `wiki/topics/`
- `wiki/reports/`
- `raw/yuandian-cache/`

Report high-signal matches with path, score, and snippet. If no useful match is found, say it is not found in the local KB and suggest the next source to retrieve.

## Raw To Source

`raw/notes/` is the preserved source layer. `wiki/sources/` is the reusable working layer.

When the user asks to "把 raw 变成 source", "整理入 source", or "做成可复用知识页":

1. Use `raw-to-source` to create the source page framework if it does not exist.
2. Read the raw material and fill the generated source page.
3. Keep the raw path and source traceability in the source page.
4. Do not delete or rewrite the raw file.
5. If the raw is low quality, incomplete, OCR-broken, or source-unclear, mark the source page as below L3 and explain the gap.

Every `wiki/sources/` page must keep this stable five-part template:

1. Title
2. Source and processing date line
3. `## 核心内容`
4. `## 关键概念`
5. `## 原文位置`

The `## 原文位置` path must be wrapped in backticks and must point to a real raw file. If the raw file is missing but the source page itself is valuable, create a matching raw file first, then fix the source page.

## L3 Maintenance Standard

Use this practical maturity scale:

- `L0 Raw`: source material is only saved under `raw/`.
- `L1 Indexed`: a matching `wiki/sources/` page exists with title, origin, raw path, and processing date.
- `L2 Structured`: the source page has a usable summary, key points, limitations, and basic topic links.
- `L3 Reusable`: the source page can be directly reused in legal research or drafting.

A source page is `L3` only when it has:

- a clear conclusion summary
- applicable scenarios or issue tags
- rules, case points, or practical takeaways with traceable source basis
- important facts, evidence clues, or data fields preserved where relevant
- limits such as jurisdiction, effective date, court level, data freshness, or uncertainty
- links to related topics using `[[topic]]`
- a maintenance record showing when it was last reviewed

Do not mark a page as `L3` just because it has a template. If it still contains placeholders like `待整理` or `待补`, report it as `L1` or `L2` and list what is missing.

Common fake-source signals:

- `## 核心内容` is too short or says only "本文讨论了..." without usable information.
- `## 关键概念` contains generic tags such as `[[案例]]`, `[[实务参考]]`, `[[裁判规则]]` only.
- `## 原文位置` is missing, not wrapped in backticks, or points to a missing raw file.
- The page repeats the title but does not extract rules, facts, issue boundaries, or practical use.
- Case pages invent case numbers, court names, amounts, or results not found in raw.

For case source pages, L3 requires at least: case type, case number or "案号：未知", court if available, cause of action, basic facts, core issue, holding/rule, result, and practical use. Do not fabricate missing metadata.

For statute/rule source pages, L3 requires at least: current validity if known, issuing body, effective date or revision date if available, key articles or rule points, application scenario, and limits.

## OCR for Scanned PDFs and Images

When the input is a scanned PDF, image-based PDF, or a screenshot/photo that cannot be directly text-extracted:

1. Load the `ocr-mineru` skill.
2. Use MinerU online OCR to parse the file:
   ```bash
   mineru-open-api extract file.pdf -o ./ocr-out/ --model vlm
   ```
   For images: `mineru-open-api extract image.png -o ./ocr-out/ --model vlm`
3. Read the generated Markdown output from the output directory.
4. Clean the OCR result: fix obvious recognition errors, merge broken lines, remove table artifacts.
5. Ingest the cleaned text into the KB as usual (write `raw/notes/` and optionally `wiki/sources/`).
6. If MinerU returns an error (quota exceeded, token invalid, service unavailable), report the specific error and suggest: re-apply for a Token at https://mineru.net/apiManage/token, or wait for the daily quota to reset.

**Note:** `ocr-mineru` requires `npm install -g mineru-open-api` and a valid MinerU API Token (apply at https://mineru.net/apiManage/token). Without a Token, only the `flash-extract` mode works (limited to ≤10MB/20 pages, IP rate-limited).

## Maintenance Checks

When the user asks to maintain or audit the KB, inspect real files first. At minimum check:

- counts for `raw/notes/`, `wiki/sources/`, `wiki/topics/`, and `wiki/reports/`
- source pages missing `## 核心内容`, `## 关键概念`, or `## 原文位置`
- source pages whose raw path does not exist
- source pages with placeholder summaries
- mapped raw count by parsing `## 原文位置`, not by assuming raw/source file names match

Use `audit-sources` for the first pass whenever possible.

Useful maintenance output:

- `L0`: raw exists but has no source page
- `L1`: source exists but is only an index shell
- `L2`: source is structured but not yet reusable
- `L3`: source is verified against raw and reusable

For batch work, start small. Fix or create a few source pages, verify them, then expand. Do not generate many source shells without reading raw.

## Detailed References

Load only the relevant reference when the task needs more detail:

- `references/local-first.md`: when answering from the KB, checking whether material already exists, deciding whether to use external sources, or writing `gap-log.md`.
- `references/ingest.md`: when importing PDF, Word, Markdown, text, webpage, screenshot, or API output into the KB.
- `references/maintenance.md`: when auditing structure, fixing source quality, checking raw/source mapping, cleaning reports, or planning L3 source batches.

## Workflow

1. Confirm or initialize the knowledge-base structure.
2. Search the KB before ingesting new material.
3. For local files, use `ingest-file` and then improve the generated `wiki/sources/` page toward L3 if the user asks for a reusable knowledge page.
4. For existing raw files, use `raw-to-source`, then fill and grade the source page.
5. For exports, include paired `raw/notes/` and `wiki/sources/` files whenever possible.
6. For imports, run `import-zip` first and report imported count, skipped count, and duplicate reasons.
7. For Yuandian laws, cases, or enterprise data, use `yuandian-legal-search` to retrieve content, then write it into the same raw/source structure.

## Reporting

After each operation, report:

- what was created or changed
- exact local paths
- current maturity level (`L0`/`L1`/`L2`/`L3`) when maintaining source pages
- duplicate skips, if any
- whether follow-up manual legal review is needed
