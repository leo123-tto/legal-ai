---
name: legal-kb
description: Build, maintain, import, export, and deduplicate a local Chinese legal knowledge base under ~/Documents/知识库; ingest markdown, text, Word, and text-extractable PDF files; create raw/source pairs; and exchange knowledge-base fragments through manifest-based ZIP packs.
---

# Legal KB

Use this skill when the user wants to maintain a local legal knowledge base, ingest legal materials, create raw/source records, export materials for colleagues, or import a shared knowledge-base ZIP.

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
- Prefer the helper script for deterministic local file ingest, ZIP export, and ZIP import.
- Deduplicate before importing shared packs.
- Do not invent legal facts, missing citations, or source metadata.
- For scanned or image-only PDFs, clearly report that OCR is required.
- If Yuandian content is needed, load `yuandian-legal-search` as a companion skill and verify API configuration first.

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
python3 scripts/kb_ingest_helper.py export-zip --out-zip "/path/to/share.zip" --files raw/notes/example.md wiki/sources/example.md --source-agent "agent-name" --notes "共享说明"
```

```bash
python3 scripts/kb_ingest_helper.py import-zip --pack-zip "/path/to/share.zip"
```

Supported local ingest file types:

- `.md`
- `.txt`
- `.docx`
- text-extractable `.pdf`

## Workflow

1. Confirm or initialize the knowledge-base structure.
2. For local files, use `ingest-file` and then improve the generated `wiki/sources/` page if the user asks for summarization or topic links.
3. For exports, include paired `raw/notes/` and `wiki/sources/` files whenever possible.
4. For imports, run `import-zip` first and report imported count, skipped count, and duplicate reasons.
5. For Yuandian laws, cases, or enterprise data, use `yuandian-legal-search` to retrieve content, then write it into the same raw/source structure.

## Reporting

After each operation, report:

- what was created or changed
- exact local paths
- duplicate skips, if any
- whether follow-up manual legal review is needed
