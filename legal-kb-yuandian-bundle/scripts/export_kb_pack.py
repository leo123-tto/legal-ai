#!/usr/bin/env python3
import argparse, hashlib, json
from datetime import datetime
from pathlib import Path

ALLOWED_PREFIXES = [
    'raw/notes/',
    'raw/yuandian-cache/',
    'wiki/sources/',
    'wiki/topics/',
    'wiki/reports/',
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def kind_for(rel: str) -> str:
    if rel.startswith('raw/notes/') or rel.startswith('raw/yuandian-cache/'):
        return 'raw'
    if rel.startswith('wiki/sources/'):
        return 'source'
    if rel.startswith('wiki/topics/'):
        return 'topic'
    if rel.startswith('wiki/reports/'):
        return 'report'
    return 'other'

parser = argparse.ArgumentParser(description='Export selected KB files into a team-share pack manifest.')
parser.add_argument('--kb-root', default='~/Documents/知识库')
parser.add_argument('--out-dir', required=True)
parser.add_argument('--files', nargs='+', required=True, help='Relative paths under kb root')
parser.add_argument('--source-agent', default='unknown-agent')
parser.add_argument('--notes', default='')
args = parser.parse_args()

kb_root = Path(args.kb_root).expanduser().resolve()
out_dir = Path(args.out_dir).expanduser().resolve()
payload_dir = out_dir / 'payload'
payload_dir.mkdir(parents=True, exist_ok=True)
items = []

for rel in args.files:
    rel = rel.strip().replace('\\', '/')
    src = kb_root / rel
    if not src.exists() or not src.is_file():
        raise SystemExit(f'missing file: {src}')
    dst = payload_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())
    items.append({
        'kind': kind_for(rel),
        'relative_path': rel,
        'sha256': sha256_file(src),
        'title': src.stem,
    })

manifest = {
    'format_version': 'team-kb-pack/v1',
    'exported_at': datetime.now().isoformat(timespec='seconds'),
    'kb_root': '~/Documents/知识库',
    'source_agent': args.source_agent,
    'notes': args.notes,
    'items': items,
}
(out_dir / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Exported {len(items)} files -> {out_dir}')
