#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

KB_ROOT = Path.home() / 'Documents' / '知识库'
RAW_DIR = KB_ROOT / 'raw' / 'notes'
SOURCE_DIR = KB_ROOT / 'wiki' / 'sources'
YUANDIAN_CACHE_DIR = KB_ROOT / 'raw' / 'yuandian-cache'


def ensure_kb_root():
    for p in [
        RAW_DIR,
        KB_ROOT / 'raw' / 'images',
        YUANDIAN_CACHE_DIR,
        SOURCE_DIR,
        KB_ROOT / 'wiki' / 'topics',
        KB_ROOT / 'wiki' / 'reports',
        KB_ROOT / '_inbox',
    ]:
        p.mkdir(parents=True, exist_ok=True)
    defaults = {
        KB_ROOT / 'purpose.md': '# 本地法律知识库\n\n目标：沉淀可复用的法律材料，并与团队共享格式保持一致。\n',
        KB_ROOT / 'gap-log.md': '# gap-log\n\n记录本地未命中但值得后续补库的高价值缺口。\n',
        KB_ROOT / 'log.md': '# log\n\n记录主库级重要操作。\n',
        KB_ROOT / '.wiki-schema.md': '# 最小知识库结构\n\n- raw/notes/\n- raw/images/\n- raw/yuandian-cache/\n- wiki/sources/\n- wiki/topics/\n- wiki/reports/\n- _inbox/\n',
        KB_ROOT / 'wiki' / 'index.md': '# 本地知识库索引\n\n> 最小初始化索引。\n',
        KB_ROOT / 'wiki' / 'log.md': '# wiki log\n\n记录 wiki 层结构调整与批处理。\n',
    }
    for path, text in defaults.items():
        if not path.exists():
            path.write_text(text, encoding='utf-8')


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]+', '-', name).strip()
    name = re.sub(r'\s+', ' ', name)
    return name[:80].strip(' .-_') or 'untitled'


def read_text_file(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def read_docx_file(path: Path) -> str:
    try:
        import docx
        doc = docx.Document(str(path))
        return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        raise RuntimeError(f'docx_extract_failed: {e}')


def read_pdf_file(path: Path) -> str:
    try:
        import pypdf
        reader = pypdf.PdfReader(str(path))
        text = '\n'.join((page.extract_text() or '') for page in reader.pages)
        if text and len(text.strip()) > 50:
            return text
    except Exception:
        pass
    try:
        import PyPDF2
        with path.open('rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = '\n'.join((page.extract_text() or '') for page in reader.pages)
            if text and len(text.strip()) > 50:
                return text
    except Exception:
        pass
    raise RuntimeError('pdf_text_extract_failed: needs OCR or a PDF text extractor backend')


def file_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {'.md', '.txt'}:
        return read_text_file(path)
    if suffix == '.docx':
        return read_docx_file(path)
    if suffix == '.pdf':
        return read_pdf_file(path)
    raise RuntimeError(f'unsupported_file_type: {suffix}')


def write_raw_source(title: str, source_label: str, origin: str, body: str, note: str = ''):
    ensure_kb_root()
    today = datetime.now().strftime('%Y-%m-%d')
    safe = sanitize_filename(title)
    raw_name = f'{today}-{safe}.md'
    raw_path = RAW_DIR / raw_name
    meta_lines = [
        f'# {title}',
        '',
        f'> 来源：{source_label}',
        f'> 原始输入：{origin}',
        f'> 处理时间：{today}',
        '',
        '---',
        '',
        body.strip(),
    ]
    if note:
        meta_lines += ['', '---', '', f'备注：{note}']
    raw_path.write_text('\n'.join(meta_lines) + '\n', encoding='utf-8')

    source_path = SOURCE_DIR / raw_name
    source_content = '\n'.join([
        f'# {title}',
        '',
        f'> 来源：{source_label} | 处理日期：{today}',
        '',
        '## 核心内容',
        '',
        '待 agent 基于原文补充一段信息性摘要。',
        '',
        '## 关键概念',
        '',
        '- [[待补概念1]]',
        '- [[待补概念2]]',
        '- [[待补概念3]]',
        '- [[待补概念4]]',
        '- [[待补概念5]]',
        '',
        '## 原文位置',
        '',
        f'`~/Documents/知识库/raw/notes/{raw_name}`',
        ''
    ])
    source_path.write_text(source_content, encoding='utf-8')
    return {'raw_path': str(raw_path), 'source_path': str(source_path), 'title': title}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def normalize_text(text: str) -> str:
    return ''.join(text.split())


def duplicate_reason(src: Path, dst: Path):
    src_hash = sha256_file(src)
    dst_hash = sha256_file(dst)
    if src_hash == dst_hash:
        return 'same_sha256'
    try:
        src_text = src.read_text(encoding='utf-8', errors='ignore')
        dst_text = dst.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        src_text = dst_text = ''
    if src_text and dst_text and normalize_text(src_text) == normalize_text(dst_text):
        return 'same_normalized_text'
    src_origin = ''
    dst_origin = ''
    for line in src_text.splitlines()[:30]:
        if '原链接：' in line or '原始输入：' in line:
            src_origin = line.split('：', 1)[1].strip()
            break
    for line in dst_text.splitlines()[:30]:
        if '原链接：' in line or '原始输入：' in line:
            dst_origin = line.split('：', 1)[1].strip()
            break
    if src_origin and dst_origin and src_origin == dst_origin:
        return 'same_origin_url'
    if src.stem == dst.stem:
        return 'same_filename_possible_duplicate'
    return None


def export_zip(out_zip: Path, files: list[str], source_agent: str, notes: str):
    ensure_kb_root()
    staging = out_zip.parent / (out_zip.stem + '_staging')
    if staging.exists():
        shutil.rmtree(staging)
    payload_dir = staging / 'payload'
    payload_dir.mkdir(parents=True, exist_ok=True)
    items = []
    for rel in files:
        rel = rel.replace('\\', '/').strip()
        src = KB_ROOT / rel
        if not src.exists() or not src.is_file():
            raise RuntimeError(f'missing_file: {src}')
        dst = payload_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(src.read_bytes())
        items.append({'relative_path': rel, 'sha256': sha256_file(src), 'title': src.stem})
    manifest = {
        'format_version': 'team-kb-pack/v2-zip',
        'exported_at': datetime.now().isoformat(timespec='seconds'),
        'kb_root': '~/Documents/知识库',
        'source_agent': source_agent,
        'notes': notes,
        'items': items,
    }
    (staging / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in staging.rglob('*'):
            zf.write(p, p.relative_to(staging))
    shutil.rmtree(staging)
    return {'zip_path': str(out_zip), 'count': len(items)}


def import_zip(pack_zip: Path, overwrite: bool = False):
    ensure_kb_root()
    staging = pack_zip.parent / (pack_zip.stem + '_unzipped')
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(pack_zip, 'r') as zf:
        zf.extractall(staging)
    manifest = json.loads((staging / 'manifest.json').read_text(encoding='utf-8'))
    payload_dir = staging / 'payload'
    imported = 0
    skipped = []
    for item in manifest['items']:
        rel = item['relative_path']
        src = payload_dir / rel
        dst = KB_ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        candidates = []
        if dst.exists():
            candidates.append(dst)
        subtree = KB_ROOT / Path(rel).parts[0] / Path(rel).parts[1] if len(Path(rel).parts) >= 2 else KB_ROOT
        if subtree.exists():
            candidates.extend([p for p in subtree.rglob(src.name) if p.is_file()])
        reason = None
        existing = None
        seen = set()
        for cand in candidates:
            rc = str(cand.resolve())
            if rc in seen:
                continue
            seen.add(rc)
            reason = duplicate_reason(src, cand)
            if reason:
                existing = str(cand)
                break
        if reason and not overwrite:
            skipped.append({'relative_path': rel, 'reason': reason, 'existing': existing})
            continue
        dst.write_bytes(src.read_bytes())
        imported += 1
    shutil.rmtree(staging)
    return {'zip': str(pack_zip), 'imported': imported, 'skipped': len(skipped), 'skipped_reasons': skipped}


def main():
    parser = argparse.ArgumentParser(description='legal-kb helper for ingest/export/import tasks')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_ingest = sub.add_parser('ingest-file')
    p_ingest.add_argument('--path', required=True)
    p_ingest.add_argument('--title', default='')
    p_ingest.add_argument('--source-label', default='本地文件')

    p_export = sub.add_parser('export-zip')
    p_export.add_argument('--out-zip', required=True)
    p_export.add_argument('--files', nargs='+', required=True)
    p_export.add_argument('--source-agent', default='unknown-agent')
    p_export.add_argument('--notes', default='')

    p_import = sub.add_parser('import-zip')
    p_import.add_argument('--pack-zip', required=True)
    p_import.add_argument('--overwrite', action='store_true')

    args = parser.parse_args()

    if args.cmd == 'ingest-file':
        path = Path(args.path).expanduser().resolve()
        text = file_text(path)
        title = args.title or path.stem
        result = write_raw_source(title=title, source_label=args.source_label, origin=str(path), body=text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'export-zip':
        result = export_zip(Path(args.out_zip).expanduser().resolve(), args.files, args.source_agent, args.notes)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'import-zip':
        result = import_zip(Path(args.pack_zip).expanduser().resolve(), overwrite=args.overwrite)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
