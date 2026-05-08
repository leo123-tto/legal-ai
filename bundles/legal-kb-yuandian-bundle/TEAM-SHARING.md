# Team Sharing

用于多人/多 agent 之间交换本地知识库片段。重点不是脚本本身，而是**统一格式 + 导入前查重 + 自然语言可触发**。

## 适用场景
- 导出某批 raw/source 给同事
- 导入同事发来的共享 zip
- 事务所未来要把多人知识库汇总到共享盘、NAS 或服务器

## 固定立场
1. 默认交换物是 **zip + manifest**，不是散落的文件。
2. 导出时优先打包成对的 `raw` + `wiki/sources/` 文件，减少半残结构。
3. 导入时必须先查重，不要无脑复制。
4. 用户用自然语言说“导出给同事”“导入共享包”时，agent 应直接执行，不要把命令丢给用户自己敲。
5. 优先调用 `skills/legal/legal-kb/scripts/kb_ingest_helper.py`，不要现场临时拼一堆命令。

## 最低查重规则
至少按这个顺序检查：
1. 同路径文件 sha256 是否相同
2. 文本归一化后是否相同（忽略空白/换行差异）
3. 公众号类 raw 的 `原链接` 是否相同
4. 同目录树下同名文件是否高度可疑重复

## 汇报要求
### 导出后
- zip 路径
- 内含文件数量
- 是否包含 raw/source 成对文件

### 导入后
- 成功导入多少
- 因重复跳过多少
- 各跳过原因（same_sha256 / same_normalized_text / same_origin_url / same_filename_possible_duplicate）

## 文件类型共享边界
- 可直接共享：`raw/notes/`、`raw/yuandian-cache/`、`wiki/sources/`、`wiki/topics/`、`wiki/reports/`
- 不默认共享：OCR 缓存、中间 JSON、临时摘要、杂项过程文件

## 给未来中心库的预埋
如果事务所未来上共享服务器，不必推翻现有格式：
- 继续沿用 `zip + manifest` 做手工交换
- 或把 `payload/ + manifest.json` 换成共享目录 / 对象存储 / API 上传目标
核心是格式一致，不是先把系统做大。
