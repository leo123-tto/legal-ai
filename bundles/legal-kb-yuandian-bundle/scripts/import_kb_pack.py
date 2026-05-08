#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

parser = argparse.ArgumentParser(description='Import a team-share KB pack into local KB.')
parser.add_argument('--pack-dir', required=True)
parser.add_argument('--kb-root', default='~/Documents/知识库')
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()

pack_dir = Path(args.pack_dir).expanduser().resolve()
kb_root = Path(args.kb_root).expanduser().resolve()
manifest = json.loads((pack_dir / 'manifest.json').read_text(encoding='utf-8'))
payload_dir = pack_dir / 'payload'
count = 0
for item in manifest['items']:
    rel = item['relative_path']
    src = payload_dir / rel
    if not src.exists():
        raise SystemExit(f'missing payload file: {src}')
    dst = kb_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not args.overwrite:
        continue
    digest = sha256_file(src)
    if digest != item['sha256']:
        raise SystemExit(f'sha256 mismatch: {rel}')
    dst.write_bytes(src.read_bytes())
    count += 1
print(f'Imported {count} files into {kb_root}')
