---
name: legal-kb-maintenance
description: 单主库法律知识库整理技能。负责巡检结构、修 index/log/overview/schema、识别 raw 与 wiki 脱节、生成治理报告，并在低风险范围内做收口清理。
---

# Legal KB Maintenance

本文件用于维护 `~/Documents/知识库` 的结构健康。目标不是重做一套系统，而是让 raw、source、topic、index、log 之间保持可追踪、可搜索、可复用。

## 固定前提

- 唯一主库：`~/Documents/知识库`
- 不创建平行库、镜像库、展示库。
- 不负责重新 OCR；发现 OCR 需求时转交入库流程或提示需要 OCR 扩展链路。
- 默认先修结构、索引和 source 质量；高风险删除、批量重命名、目录迁移先列方案，等用户确认。

## 核心目标

1. 让主库目录职责清楚。
2. 让 `index.md`、`log.md`、`overview.md`、`.wiki-schema.md` 彼此一致。
3. 识别 `raw/` 与 `wiki/` 是否脱节。
4. 把有长期复用价值的材料从“堆原文”推进到“可导航、可复用、可维护”。
5. 保留来源链路，避免生成无来源的漂亮空壳。

## 目录职责基线

### 根目录

- `purpose.md`：主库目标、范围、排除项。
- `gap-log.md`：本地未命中但值得补库的高价值缺口。
- `.wiki-schema.md`：维护规则与目录职责。
- `log.md`：主库级重要操作记录。

### raw/

- `raw/notes/`：原文或近原文材料，包括法规、案例、实务文章、OCR 整理稿、用户手动下载文件转 Markdown。
- `raw/images/`：少量需要留档的图片。
- `raw/yuandian-cache/`：元典检索缓存。
- `raw/companies/`：企业档案或查档结果（如用户使用）。

### wiki/

- `wiki/sources/`：单篇来源页/整理页。
- `wiki/topics/`：专题入口。
- `wiki/reports/`：治理报告、批次报告、专题报告。
- `wiki/index.md`：导航入口，不是全量垃圾清单。
- `wiki/log.md`：wiki 层批处理、索引修复、巡检记录。
- `wiki/overview.md`：当前覆盖面、结构状态、治理判断。

## 标准流程

### A. 先体检

1. 统计 `raw/notes/`、`wiki/sources/`、`wiki/topics/`、`wiki/reports/` 数量。
2. 检查锚点文件是否存在且内容可信：
   - `purpose.md`
   - `gap-log.md`
   - `.wiki-schema.md`
   - `log.md`
   - `wiki/index.md`
   - `wiki/log.md`
   - `wiki/overview.md`
3. 判断当前状态：
   - 只有 raw 堆积；
   - 已有 sources，但缺 topic；
   - 有 topic，但 index/overview 过期；
   - source 有坏链、缺段、占位摘要；
   - 报告目录堆积过多过程文件。

### B. 分级处理

#### 低风险，可直接修

- 标题、说明、索引摘要过期。
- `overview.md` 是空模板。
- `.wiki-schema.md` 与真实目录不一致。
- source 页缺 `## 核心内容`、`## 关键概念`、`## 原文位置`。
- `## 原文位置` 写法不统一但能确定真实 raw。
- 明显过程垃圾，如 `.DS_Store`。

#### 中风险，先小批修

- 重复索引项。
- source 页面命名不统一。
- `raw/` 与 `wiki/sources/` 映射关系不清。
- 高价值材料应提升为 topic，但材料簇边界还要人工判断。

#### 高风险，默认只记录

- 大规模删除 raw 正文。
- 批量覆盖重写 sources。
- 批量重命名 100+ 文件。
- 迁移整个目录结构。
- 合并大量疑似重复但未确认来源的材料。

## raw/source 映射检查

不要只用“raw 文件名是否和 source 文件名相同”判断覆盖率。更稳的方法：

1. 扫描全部 `wiki/sources/*.md`。
2. 解析每页 `## 原文位置`。
3. 展开 `~` 后检查 raw 文件是否真实存在。
4. 统计：
   - raw 总数；
   - source 总数；
   - 已被 source 映射的 raw 数；
   - 未被 source 映射的 raw 数；
   - source 坏链数。

输出分三类：

- 已闭环：raw 存在，source 结构完整，路径可追踪。
- 应补 source：raw 有价值但没有对应 source。
- 应提升 topic：同主题已有 2-3 篇以上强相关 source。

## source 页统一标准

每个 `wiki/sources/` 页面至少应有五段：

```md
# 标题

> 来源：xxx | 处理日期：YYYY-MM-DD

## 核心内容

## 关键概念

## 原文位置
```

硬规则：

1. `## 原文位置` 必须指向真实 raw 文件。
2. 路径必须包在反引号中，推荐写法：``~/Documents/知识库/raw/notes/文件名.md``。
3. `## 核心内容` 不得只是“本文讨论了……”这类占位句。
4. `## 关键概念` 应服务检索，不要全是泛词。
5. source 只能基于原文整理，不得补造案号、法院、金额、日期、法条或裁判结果。

## L0-L3 成熟度

- `L0 Raw`：只有 raw 原文。
- `L1 Indexed`：有 source 页，但主要是标题、来源、原文路径。
- `L2 Structured`：有摘要、要点、限制和基础标签。
- `L3 Reusable`：可直接用于法律研究、检索或起草。

L3 至少具备：

- 清晰结论摘要；
- 适用场景或问题标签；
- 规则、案例要点或实务要点；
- 重要事实、证据线索或数据字段；
- 限制条件，如地域、时效、法院层级、数据新鲜度；
- 关联 topic；
- 最近维护记录。

不要因为页面有模板就标为 L3。仍有 `待整理`、`待补`、占位摘要、坏链的页面，通常只能算 L1 或 L2。

## source 巡检最小指标

每次巡检至少输出四个数：

- 标题异常数；
- 原文位置异常数；
- 模板缺段数；
- 占位式摘要数。

任一不为 0，不应把该轮维护标记为完成；最多标记为“已发现并部分修复”。

## 单页修复

用户只点名修一篇 source 时，也要联查三处：

1. 对应 raw 文件是否存在。
2. source 页内 `原文位置` 是否准确。
3. `wiki/index.md` 或相关 topic 是否引用旧标题/旧路径。

低风险做法：

- raw 文件真实存在：修 source 的路径和结构。
- source 有价值但 raw 缺失：先补一个同主题 raw，再修 source。
- 发现重复 source：优先保留来源链路更清楚、内容更完整的一页，另一页先列为待确认，不直接删除。

## 批量补 source

适用条件：

- raw 未映射数量较多；
- source 结构巡检基本健康；
- 用户明确要补 source 或提升可复用性。

推荐顺序：

1. 先查重，确认目标 raw 没有对应 source。
2. 小批试跑，每批 3-5 篇。
3. 每篇按五段模板生成 source。
4. 抽检原文路径、摘要质量、关键概念和 L0-L3 判断。
5. 同步更新 `wiki/index.md`、`wiki/log.md`、必要的 topic 或报告。

禁止事项：

- 不读 raw 就批量造空壳 source。
- 用处理日期新造一批重复文件名。
- 把低价值、重复、脏 OCR 材料硬升 source。
- 擅自改 schema、目录职责或大规模删除 raw。

## topic 提升

满足任一条件，可考虑做 topic：

- 同主题已有 2-3 篇以上强相关材料。
- 用户后续更可能按“问题/专题”检索。
- 材料之间需要交叉整理、去重、形成入口。
- 能形成稳定工作场景，如执行异议、公司责任、劳动争议、建设工程、婚姻家事等。

topic 应回答：

- 这个专题解决什么问题；
- 已有哪些 source 支撑；
- 每个 source 的用途和边界；
- 还有哪些缺口；
- 最近维护时间。

## 报告目录清理

当 `wiki/reports/` 堆积过多时，先盘点：

- 文件名；
- 大小；
- 修改时间；
- 一级标题；
- 是否被 `index.md`、`overview.md`、topic 或日志引用。

处理分类：

- 保留顶层：当前仪表盘、仍指导下一步的方案、最新健康报告。
- 归档：已被后续总览覆盖的旧治理报告、小批次收口报告。
- 删除：空文件、过程 JSON、可随时重算且无阅读价值的中间文件。

归档默认放入 `wiki/reports/archive/YYYY-MM/`。删除 Markdown 报告前需确认它没有独立阅读价值和引用关系。

## 文档同步纪律

只要发生结构修复、规则调整、批量任务或报告清理，至少考虑同步：

- 根目录 `log.md`；
- `wiki/log.md`；
- `wiki/index.md`；
- `wiki/overview.md`；
- `.wiki-schema.md`；
- 必要时写 `wiki/reports/YYYY-MM-DD-kb-maintenance.md`。

不要让文档状态和真实文件状态再次脱节。

## 治理报告模板

```md
# 知识库治理报告

## 当前状态
- raw/notes：
- wiki/sources：
- wiki/topics：
- wiki/reports：

## 本轮发现
- 结构问题：
- source 问题：
- 映射问题：
- 待提升专题：

## 本轮已修复
-

## 暂不自动处理
-

## 下一步建议
-
```

## 注意事项

- 维护动作要克制，优先修可验证的小问题。
- 不要把国外 wiki 工作流、个人知识管理方法硬套到法律主库。
- 不要留下大量过程文件；真正有价值的是 raw/source/topic/index/log 的一致性。
- 如果发现入库规则导致 source 长期脏化，应反向修 `legal-kb` 的 ingest 规则。
