"""
元典律师检索 - 本地缓存模块

缓存目录：~/Documents/知识库/raw/yuandian-cache/
缓存文件：markdown 格式，YAML front matter + 内容正文
索引文件：index.json，映射查询→缓存文件
"""

import os
import json
import hashlib
import datetime

CACHE_ROOT = os.path.expanduser("~/Documents/知识库/raw/yuandian-cache")
INDEX_PATH = os.path.join(CACHE_ROOT, "index.json")

# 确保缓存目录存在
os.makedirs(CACHE_ROOT, exist_ok=True)


def _load_index():
    if os.path.exists(INDEX_PATH):
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def _save_index(index):
    # 限制索引大小，保留最近 2000 条
    if len(index) > 2000:
        # 按时间排序，保留最新的 1500 条
        sorted_keys = sorted(index.keys(),
                             key=lambda k: index[k].get("cached_at", ""),
                             reverse=True)
        index = {k: index[k] for k in sorted_keys[:1500]}
    try:
        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    except IOError:
        pass


def _query_hash(query_type, params):
    """生成查询的哈希键"""
    raw = f"{query_type}:{json.dumps(params, sort_keys=True, ensure_ascii=False)}"
    h = hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]
    return f"{query_type}-{h}"


def cache_search_result(query_type, params, results, summary=""):
    """缓存搜索结果"""
    key = _query_hash(query_type, params)
    file_name = f"SEARCH-{key}.md"
    file_path = os.path.join(CACHE_ROOT, file_name)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 写入 markdown 文件
    content = f"""---
cached_at: {now}
query_type: {query_type}
query_params: {json.dumps(params, ensure_ascii=False)}
summary: {summary}
result_count: {len(results) if results else 0}
---

# 元典检索缓存: {query_type}

**查询时间:** {now}
**查询参数:** `{json.dumps(params, ensure_ascii=False)}`
**结果数量:** {len(results) if results else 0}

---

"""
    if results:
        for i, r in enumerate(results):
            if isinstance(r, dict):
                content += f"### 结果 {i+1}\n"
                for k, v in r.items():
                    if v and k != "content":
                        content += f"- **{k}**: {v}\n"
                content += "\n"
            else:
                content += f"### 结果 {i+1}\n{str(r)}\n\n"

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError:
        return None

    # 更新索引
    index = _load_index()
    index[key] = {
        "path": file_name,
        "query_type": query_type,
        "summary": summary,
        "cached_at": now,
    }
    _save_index(index)
    return file_path


def cache_detail_result(type_name, obj_id, name, content):
    """缓存详情结果（法规/案例/企业）"""
    safe_name = name.replace("/", "／").replace(" ", "_")[:40]
    file_name = f"{type_name}-{obj_id}_{safe_name}.md"
    file_path = os.path.join(CACHE_ROOT, file_name)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 如果 content 是 dict，转成 yaml-like 格式
    body = ""
    if isinstance(content, dict):
        for k, v in content.items():
            if v:
                body += f"- **{k}**: {v}\n"
    else:
        body = str(content) if content else "（无内容）"

    md_content = f"""---
cached_at: {now}
type: {type_name}
id: {obj_id}
name: {name}
---

# {name}

**缓存时间:** {now}
**类型:** {type_name}
**ID:** {obj_id}

---

{body}
"""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
    except IOError:
        return None

    # 写入索引
    index = _load_index()
    key = f"{type_name}-{obj_id}"
    index[key] = {
        "path": file_name,
        "query_type": type_name,
        "summary": name,
        "cached_at": now,
    }
    _save_index(index)
    return file_path


def check_cache(query_type, params, max_age_days=30):
    """检查缓存是否命中。返回 (file_path, data) 或 (None, None)"""
    key = _query_hash(query_type, params)
    index = _load_index()

    if key not in index:
        return None, None

    entry = index[key]
    file_path = os.path.join(CACHE_ROOT, entry["path"])
    if not os.path.exists(file_path):
        return None, None

    # 检查时效性
    cached_at = entry.get("cached_at", "")
    if cached_at:
        try:
            cached_date = datetime.datetime.strptime(cached_at[:10], "%Y-%m-%d")
            if (datetime.datetime.now() - cached_date).days > max_age_days:
                return None, None
        except ValueError:
            pass

    # 读取缓存内容
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
        return file_path, data
    except IOError:
        return None, None


def search_cache(keyword, type_filter=None):
    """按关键词在缓存索引里搜索已有结果"""
    index = _load_index()
    hits = []
    for key, entry in index.items():
        summary = entry.get("summary", "")
        if keyword.lower() in summary.lower():
            if type_filter and entry.get("query_type") != type_filter:
                continue
            hits.append(entry)
    return hits


def get_cache_stats():
    """查看缓存统计"""
    index = _load_index()
    types = {}
    for entry in index.values():
        t = entry.get("query_type", "unknown")
        types[t] = types.get(t, 0) + 1
    return {
        "total_entries": len(index),
        "by_type": types,
        "cache_dir": CACHE_ROOT,
    }
