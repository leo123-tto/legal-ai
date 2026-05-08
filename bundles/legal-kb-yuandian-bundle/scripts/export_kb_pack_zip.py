#!/usr/bin/env python3
import argparse, hashlib, json, shutil, zipfile
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

parser = argparse.ArgumentParser(description='Export selected KB files into a portable zip pack.')
parser.add_argument('--kb-root', default='~/Documents/知识库')
parser.add_argument('--out-zip', required=True)
parser.add_argument('--files', nargs='+', required=True, help='Relative paths under kb root')
parser.add_argument('--source-agent', default='unknown-agent')
parser.add_argument('--notes', default='')
args = parser.parse_args()

kb_root = Path(args.kb_root).expanduser().resolve()
out_zip = Path(args.out_zip).expanduser().resolve()
staging = out_zip.parent / (out_zip.stem + '_staging')
if staging.exists():
    shutil.rmtree(staging)
payload_dir = staging / 'payload'
payload_dir.mkdir(parents=True, exist_ok=True)
items = []

for rel in args.files:
    rel = rel.strip().replace('\\', '/')
    if not any(rel.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise SystemExit(f'path not allowed for export: {rel}')
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
    'format_version': 'team-kb-pack/v2-zip',
    'exported_at': datetime.now().isoformat(timespec='seconds'),
    'kb_root': '~/Documents/知识库',
    'source_agent': args.source_agent,
    'notes': args.notes,
    'items': items,
}
(staging / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

if out_zip.exists():
    out_zip.unlink()
with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in staging.rglob('*'):
        zf.write(p, p.relative_to(staging))

shutil.rmtree(staging)
print(f'Exported {len(items)} files -> {out_zip}')
