# Legal AI

Legal AI workflows, knowledge-base tools, agent skills, and reusable sharing packs maintained by `leo123-tto`.

This repository is intentionally separate from `legal-tools`, which is a static website project. Use this repository for AI-related legal workflows, local knowledge-base projects, agent skills, prompt packs, and materials that colleagues can download and install.

## Current Projects

### `legal-kb-yuandian-bundle`

Path: `legal-kb-yuandian-bundle/`

An agent-ready bundle for building and sharing a local legal knowledge base.

It includes:

- `legal-kb`: the main local legal knowledge-base skill
- `yuandian-legal-search`: Yuandian legal search and ingestion support
- shared ZIP import/export scripts with manifest-based duplicate checks
- human-facing and agent-facing onboarding docs

Start here:

```bash
cd legal-kb-yuandian-bundle
bash install.sh
bash verify.sh
```

For a non-technical overview, read:

```text
legal-kb-yuandian-bundle/HUMAN-GUIDE.md
```

## API Keys

Yuandian and Firecrawl integrations require your own API keys. This repository does not include keys or credentials.

Recognized environment variables include:

- `YUANDIAN_API_KEY`
- `YUANDIAN_API`
- `CHINESELAW_API_KEY`
- `FIRECRAWL_API_KEY`
- `FIRECRAWL_KEY`

## Repository Layout

```text
legal-ai/
├── legal-kb-yuandian-bundle/
│   ├── skills/
│   ├── scripts/
│   ├── README.md
│   ├── HUMAN-GUIDE.md
│   ├── AGENT-ONBOARDING.md
│   └── TEAM-SHARING.md
├── LICENSE
└── README.md
```

## Notes

These materials are workflow and automation aids. They are not legal advice, and users should verify all legal content, sources, and API outputs before relying on them.
