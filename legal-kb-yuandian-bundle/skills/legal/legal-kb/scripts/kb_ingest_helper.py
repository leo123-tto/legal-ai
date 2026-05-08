#!/usr/bin/env python3
import argparse
import html
import hashlib
import json
import os
import re
import shutil
import subprocess
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional

KB_ROOT = Path.home() / 'Documents' / '知识库'
RAW_DIR = KB_ROOT / 'raw' / 'notes'
SOURCE_DIR = KB_ROOT / 'wiki' / 'sources'
YUANDIAN_CACHE_DIR = KB_ROOT / 'raw' / 'yuandian-cache'
SEARCH_ROOTS = [
    RAW_DIR,
    SOURCE_DIR,
    KB_ROOT / 'wiki' / 'topics',
    KB_ROOT / 'wiki' / 'reports',
    YUANDIAN_CACHE_DIR,
]


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


def html_to_text(markup: str) -> str:
    markup = re.sub(r'(?is)<(script|style).*?>.*?</\1>', '\n', markup)
    markup = re.sub(r'(?is)<br\s*/?>', '\n', markup)
    markup = re.sub(r'(?is)</p\s*>', '\n\n', markup)
    markup = re.sub(r'(?is)</h[1-6]\s*>', '\n\n', markup)
    text = re.sub(r'(?is)<[^>]+>', ' ', markup)
    text = html.unescape(text)
    lines = [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines()]
    return '\n'.join(line for line in lines if line).strip()


def title_from_html(markup: str, fallback: str) -> str:
    for pattern in [
        r'(?is)<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']',
        r'(?is)<meta\s+content=["\']([^"\']+)["\']\s+property=["\']og:title["\']',
        r'(?is)<title[^>]*>(.*?)</title>',
    ]:
        match = re.search(pattern, markup)
        if match:
            title = html.unescape(re.sub(r'\s+', ' ', match.group(1))).strip()
            if title:
                return title
    return fallback


def fetch_url_direct(url: str):
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X) legal-kb-ingest/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,text/plain;q=0.8,*/*;q=0.7',
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        raw = resp.read()
    markup = raw.decode(charset, errors='ignore')
    title = title_from_html(markup, url)
    text = html_to_text(markup)
    if len(text) < 300 or any(token in text for token in ['环境异常', '请在微信客户端打开', '访问过于频繁']):
        raise RuntimeError('direct_fetch_too_short_or_blocked')
    return {'title': title, 'body': text, 'method': 'direct'}


def fetch_url_firecrawl(url: str):
    if not (os.getenv('FIRECRAWL_API_KEY') or os.getenv('FIRECRAWL_KEY')):
        raise RuntimeError('firecrawl_api_not_configured')
    if not shutil.which('firecrawl'):
        raise RuntimeError('firecrawl_cli_not_installed')
    proc = subprocess.run(
        ['firecrawl', 'scrape', url, '--only-main-content'],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=90,
        check=False,
    )
    output = proc.stdout.strip()
    if proc.returncode != 0 or len(output) < 300:
        detail = proc.stderr.strip() or 'empty_or_short_firecrawl_output'
        raise RuntimeError(f'firecrawl_failed: {detail}')
    title = output.splitlines()[0].lstrip('# ').strip() if output.splitlines() else url
    return {'title': title or url, 'body': output, 'method': 'firecrawl'}


def fetch_url(url: str, prefer_firecrawl: bool = False):
    if prefer_firecrawl:
        return fetch_url_firecrawl(url)
    try:
        return fetch_url_direct(url)
    except Exception as direct_error:
        try:
            result = fetch_url_firecrawl(url)
            result['direct_error'] = str(direct_error)
            return result
        except Exception as firecrawl_error:
            raise RuntimeError(
                'url_ingest_failed: direct path failed and Firecrawl backup is unavailable or failed; '
                f'direct={direct_error}; firecrawl={firecrawl_error}'
            )


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


def kb_relative(path: Path) -> str:
    try:
        return str(path.relative_to(KB_ROOT))
    except ValueError:
        return str(path)


def text_snippet(text: str, terms: list[str], width: int = 120) -> str:
    collapsed = re.sub(r'\s+', ' ', text).strip()
    lower = collapsed.lower()
    positions = [lower.find(term.lower()) for term in terms if term]
    positions = [p for p in positions if p >= 0]
    start = max(min(positions) - width // 2, 0) if positions else 0
    end = min(start + width, len(collapsed))
    return collapsed[start:end]


def search_kb(query: str, roots: Optional[list[str]] = None, limit: int = 20):
    ensure_kb_root()
    terms = [t for t in re.split(r'\s+', query.strip()) if t]
    if not terms:
        raise RuntimeError('empty_query')
    search_dirs = []
    if roots:
        for root in roots:
            p = (KB_ROOT / root).expanduser()
            if p.exists():
                search_dirs.append(p)
    else:
        search_dirs = [p for p in SEARCH_ROOTS if p.exists()]
    results = []
    seen = set()
    for root in search_dirs:
        for path in root.rglob('*.md'):
            resolved = str(path.resolve())
            if resolved in seen:
                continue
            seen.add(resolved)
            text = path.read_text(encoding='utf-8', errors='ignore')
            lower = text.lower()
            score = sum(lower.count(term.lower()) for term in terms)
            if score <= 0:
                continue
            results.append({
                'path': kb_relative(path),
                'score': score,
                'snippet': text_snippet(text, terms),
            })
    results.sort(key=lambda item: (-item['score'], item['path']))
    return {'query': query, 'count': len(results), 'results': results[:limit]}


def source_path_for_raw(raw_path: Path) -> Path:
    name = raw_path.name
    return SOURCE_DIR / name


def extract_title_from_markdown(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip() or fallback
    return fallback


def raw_to_source(raw_path: Path, level: str = 'L3', overwrite: bool = False):
    ensure_kb_root()
    raw_path = raw_path.expanduser().resolve()
    if not raw_path.exists() or not raw_path.is_file():
        raise RuntimeError(f'missing_raw_file: {raw_path}')
    text = raw_path.read_text(encoding='utf-8', errors='ignore')
    title = extract_title_from_markdown(text, raw_path.stem)
    source_path = source_path_for_raw(raw_path)
    existed = source_path.exists()
    if existed and not overwrite:
        return {
            'status': 'skipped',
            'reason': 'source_exists',
            'raw_path': str(raw_path),
            'source_path': str(source_path),
        }
    today = datetime.now().strftime('%Y-%m-%d')
    source_content = '\n'.join([
        f'# {title}',
        '',
        f'> 来源：raw整理 | 处理日期：{today} | 目标等级：{level} | 当前状态：结构化草稿',
        '',
        '## 核心内容',
        '',
        '### 结论摘要',
        '',
        '- 待整理：用 3-5 句话写清楚这份材料能解决什么问题。',
        '',
        '### 适用场景',
        '',
        '- 待整理：列出可以复用到哪些案件、咨询或检索任务。',
        '',
        '### 规则 / 裁判要点',
        '',
        '- 待整理：保留出处，不要改写成无法追溯的结论。',
        '',
        '### 事实与证据线索',
        '',
        '- 待整理：提炼对办案、检索、尽调有用的事实线索。',
        '',
        '### 使用限制',
        '',
        '- 待整理：说明地域、时间、效力、案由或数据来源限制。',
        '',
        '## 关键概念',
        '',
        '- [[待补主题]]',
        '- [[待补规则]]',
        '- [[待补案由]]',
        '- [[待补程序]]',
        '- [[待补风险点]]',
        '',
        '## 原文位置',
        '',
        f'`~/Documents/知识库/{kb_relative(raw_path)}`',
        '',
        '## 维护记录',
        '',
        f'- {today}：由 raw 生成 source 框架；当前仅为结构化草稿，需逐条读取 raw 后才能确认是否达到 L3。',
        '',
    ])
    source_path.write_text(source_content, encoding='utf-8')
    return {
        'status': 'updated' if existed else 'created',
        'raw_path': str(raw_path),
        'source_path': str(source_path),
        'level': level,
    }


def extract_raw_reference(text: str) -> Optional[str]:
    if '## 原文位置' not in text:
        return None
    after = text.split('## 原文位置', 1)[1]
    match = re.search(r'`([^`]+)`', after)
    if match:
        return match.group(1).strip()
    for line in after.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            return line.strip('` ')
    return None


def expand_kb_path(path_text: str) -> Path:
    if path_text.startswith('~/'):
        return Path.home() / path_text[2:]
    path = Path(path_text)
    if path.is_absolute():
        return path
    return KB_ROOT / path


def source_quality_level(text: str, raw_exists: bool) -> str:
    has_core = '## 核心内容' in text
    has_concepts = '## 关键概念' in text
    has_raw = '## 原文位置' in text and raw_exists
    placeholder = any(token in text for token in ['待整理', '待补', '本文讨论了', '相关法律问题'])
    core_text = ''
    if has_core:
        core_text = text.split('## 核心内容', 1)[1].split('## ', 1)[0].strip()
    concept_count = len(re.findall(r'\[\[[^\]]+\]\]', text))
    if not has_core or not has_concepts or not has_raw:
        return 'L1'
    if placeholder or len(core_text) < 120 or concept_count < 5:
        return 'L2'
    return 'L3-candidate'


def audit_sources(limit: int = 20):
    ensure_kb_root()
    issues = {
        'missing_core': [],
        'missing_concepts': [],
        'missing_raw_section': [],
        'bad_raw_path': [],
        'placeholder_summary': [],
    }
    levels = {'L1': 0, 'L2': 0, 'L3-candidate': 0}
    mapped_raw = set()
    source_files = sorted(SOURCE_DIR.glob('*.md'))
    for path in source_files:
        text = path.read_text(encoding='utf-8', errors='ignore')
        rel = kb_relative(path)
        if '## 核心内容' not in text:
            issues['missing_core'].append(rel)
        if '## 关键概念' not in text:
            issues['missing_concepts'].append(rel)
        raw_ref = extract_raw_reference(text)
        raw_exists = False
        if not raw_ref:
            issues['missing_raw_section'].append(rel)
        else:
            raw_path = expand_kb_path(raw_ref)
            raw_exists = raw_path.exists()
            if raw_exists:
                mapped_raw.add(str(raw_path.resolve()))
            else:
                issues['bad_raw_path'].append({'source': rel, 'raw_ref': raw_ref})
        if any(token in text for token in ['待整理', '待补', '本文讨论了', '相关法律问题']):
            issues['placeholder_summary'].append(rel)
        levels[source_quality_level(text, raw_exists)] += 1
    raw_files = [p for p in RAW_DIR.glob('*.md') if p.is_file()]
    summarized = {name: values[:limit] for name, values in issues.items()}
    return {
        'raw_notes': len(raw_files),
        'sources': len(source_files),
        'mapped_raw': len(mapped_raw),
        'unmapped_raw_estimate': max(len(raw_files) - len(mapped_raw), 0),
        'levels': levels,
        'issue_counts': {name: len(values) for name, values in issues.items()},
        'issue_samples': summarized,
    }


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

    p_ingest_url = sub.add_parser('ingest-url')
    p_ingest_url.add_argument('--url', required=True)
    p_ingest_url.add_argument('--title', default='')
    p_ingest_url.add_argument('--source-label', default='网页/公众号')
    p_ingest_url.add_argument('--prefer-firecrawl', action='store_true')

    p_export = sub.add_parser('export-zip')
    p_export.add_argument('--out-zip', required=True)
    p_export.add_argument('--files', nargs='+', required=True)
    p_export.add_argument('--source-agent', default='unknown-agent')
    p_export.add_argument('--notes', default='')

    p_import = sub.add_parser('import-zip')
    p_import.add_argument('--pack-zip', required=True)
    p_import.add_argument('--overwrite', action='store_true')

    p_search = sub.add_parser('search-kb')
    p_search.add_argument('--query', required=True)
    p_search.add_argument('--roots', nargs='*', default=None)
    p_search.add_argument('--limit', type=int, default=20)

    p_raw_to_source = sub.add_parser('raw-to-source')
    p_raw_to_source.add_argument('--raw-path', required=True)
    p_raw_to_source.add_argument('--level', default='L3')
    p_raw_to_source.add_argument('--overwrite', action='store_true')

    p_audit = sub.add_parser('audit-sources')
    p_audit.add_argument('--limit', type=int, default=20)

    args = parser.parse_args()

    if args.cmd == 'ingest-file':
        path = Path(args.path).expanduser().resolve()
        text = file_text(path)
        title = args.title or path.stem
        result = write_raw_source(title=title, source_label=args.source_label, origin=str(path), body=text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'ingest-url':
        fetched = fetch_url(args.url, prefer_firecrawl=args.prefer_firecrawl)
        title = args.title or fetched['title']
        result = write_raw_source(
            title=title,
            source_label=args.source_label,
            origin=args.url,
            body=fetched['body'],
            note=f"抓取方式：{fetched['method']}",
        )
        result['method'] = fetched['method']
        if 'direct_error' in fetched:
            result['direct_error'] = fetched['direct_error']
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'export-zip':
        result = export_zip(Path(args.out_zip).expanduser().resolve(), args.files, args.source_agent, args.notes)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'import-zip':
        result = import_zip(Path(args.pack_zip).expanduser().resolve(), overwrite=args.overwrite)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'search-kb':
        result = search_kb(args.query, roots=args.roots, limit=args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'raw-to-source':
        result = raw_to_source(Path(args.raw_path), level=args.level, overwrite=args.overwrite)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.cmd == 'audit-sources':
        result = audit_sources(limit=args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
