#!/usr/bin/env python3
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def normalize_text(text: str) -> str:
    return ''.join(text.split())

def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return ''

def duplicate_reason(src: Path, dst: Path):
    src_hash = sha256_file(src)
    dst_hash = sha256_file(dst)
    if src_hash == dst_hash:
        return 'same_sha256'
    src_text = read_text_safe(src)
    dst_text = read_text_safe(dst)
    if src_text and dst_text and normalize_text(src_text) == normalize_text(dst_text):
        return 'same_normalized_text'
    src_origin = ''
    dst_origin = ''
    for line in src_text.splitlines()[:20]:
        if '原链接：' in line:
            src_origin = line.split('原链接：', 1)[1].strip()
            break
    for line in dst_text.splitlines()[:20]:
        if '原链接：' in line:
            dst_origin = line.split('原链接：', 1)[1].strip()
            break
    if src_origin and dst_origin and src_origin == dst_origin:
        return 'same_origin_url'
    if src.stem == dst.stem:
        return 'same_filename_possible_duplicate'
    return None

parser = argparse.ArgumentParser(description='Import a portable KB zip pack into local KB with dedupe.')
parser.add_argument('--pack-zip', required=True)
parser.add_argument('--kb-root', default='~/Documents/知识库')
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()

pack_zip = Path(args.pack_zip).expanduser().resolve()
kb_root = Path(args.kb_root).expanduser().resolve()
staging = pack_zip.parent / (pack_zip.stem + '_unzipped')
if staging.exists():
    shutil.rmtree(staging)
staging.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(pack_zip, 'r') as zf:
    zf.extractall(staging)

manifest = json.loads((staging / 'manifest.json').read_text(encoding='utf-8'))
payload_dir = staging / 'payload'
imported = 0
skipped = 0
skipped_reasons = []
for item in manifest['items']:
    rel = item['relative_path']
    src = payload_dir / rel
    if not src.exists():
        raise SystemExit(f'missing payload file: {src}')
    digest = sha256_file(src)
    if digest != item['sha256']:
        raise SystemExit(f'sha256 mismatch: {rel}')
    dst = kb_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    # dedupe scan: exact target path + same filename anywhere under same subtree
    candidates = []
    if dst.exists():
        candidates.append(dst)
    subtree = kb_root / Path(rel).parts[0] / Path(rel).parts[1] if len(Path(rel).parts) >= 2 else kb_root
    if subtree.exists():
        candidates.extend([p for p in subtree.rglob(src.name) if p.is_file()])
    # remove duplicates in candidate list
    uniq = []
    seen = set()
    for c in candidates:
        rc = str(c.resolve())
        if rc not in seen:
            seen.add(rc)
            uniq.append(c)
    reason = None
    for cand in uniq:
        reason = duplicate_reason(src, cand)
        if reason:
            break
    if reason and not args.overwrite:
        skipped += 1
        skipped_reasons.append({'relative_path': rel, 'reason': reason, 'existing': str(cand)})
        continue
    dst.write_bytes(src.read_bytes())
    imported += 1

report = {
    'zip': str(pack_zip),
    'imported': imported,
    'skipped': skipped,
    'skipped_reasons': skipped_reasons,
}
print(json.dumps(report, ensure_ascii=False, indent=2))
shutil.rmtree(staging)
