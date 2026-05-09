---
name: yuandian-legal-search
description: 元典平台律师检索技能。查公司、查法规、查案例；先本地缓存，未命中再联网查，结果存本地并默认输出 Markdown。
tags: [yuandian, legal-search, lawyer, company-check, regulation, case]
---

# 元典律师检索技能

> 适用场景：查对方公司背景、查法规全文、查裁判案例、查执行财产线索、批量法规下载、公司法律尽调
> 原则：先本地后联网，检索够用不调详情，汇报抓重点不堆原始数据

本技能是元典相关任务的统一入口。需要更细规则时，按任务读取对应支撑资料：

- `references/api-reference.md`：接口路径、参数、返回结构、常见异常。
- `references/batch-download.md`：清单式法规下载、精确名称匹配、效力级别过滤、质量筛选。
- `references/due-diligence.md`：公司法律尽调初始化、底稿、完整性检查和报告生成。

遇到具体 API 参数、批量下载或尽调项目结构时，先读对应 reference，再按本文通用缓存/查询/汇报流程执行。

## 前置

```python
import sys; sys.path.insert(0, "scripts")
import yd_ref           # 所有 API 函数
from cache import *     # 缓存管理
```

### 响应标准化与分页
案例检索返回 `{"total": N, "lst": [...]}`，企业列表常返回 `{"total", "pageNo", "pageSize", "hasMore", "list"}`：
```python
items = yd_ref._extract_items(data)   # → 列表
total = yd_ref._extract_total(data)   # → 总数

# 企业分页接口需要完整清单时，显式自动翻页；默认 max_pages=20，避免积分爆炸
all_patents = yd_ref._fetch_all_pages(
    lambda page_no: yd_ref.enterprise_patent(tyshxydm=USCC, page_no=page_no),
    max_pages=20,
)
```
**注意：分页接口每页约 10 积分。** 快速体检只取第 1 页；尽调/财产线索需要完整清单时再自动翻页。

## 通用流程

### Step 1：检查本地缓存
`check_cache(query_type, params)` → 命中且未过期直接汇报，未命中继续。

### Step 2：联网查询（元典 API）
按场景走对应的工作流（见下方）。

### Step 3：缓存 + 汇报
- 写入本地缓存
- 默认输出 MD 格式
- PDF / DOCX / 其他正式文件导出不属于本通用包内置能力；如用户需要，由使用者在自己的环境中另行配置导出工具。

---

## 场景一：查公司 / 合同相对方风险核验

### 触发词
"查某某公司" / "某某公司背景" / "查一下这家公司"

### 工作流

#### 1. 锁定主体
```python
candidates = yd_ref.enterprise_search(name, top_k=5)  # 1 积分，支持模糊查询
```
**关键规则：** 用户给名字时，必须先到这里模糊匹配 → 确认唯一主体 → 记录 `id` 和 `统一社会信用代码`。
**所有聚合接口（聚合总览、涉诉、知识产权等）只接受 `id` 或 `tyshxydm`，不接受企业名称。** 跳过这步直接调聚合会失败。

#### 2. 快速风险体检（按优先级）

**首选：聚合总览一条搞定（省积分）**
```python
agg = yd_ref.enterprise_aggregation_summary(id=主体id)
# 一次性拿到18个维度的统计汇总（对外投资/商标/专利/软著/失信/被执行/开庭公告/法院公告/股权冻结/行政处罚/股权出质/对外担保/经营异常/欠税公告/严重违法/变更记录等）
```

**需要明细时再按需补调：**
```python
detail = yd_ref.get_company_detail(id=主体id)
exec_p = yd_ref.enterprise_executed_person(id=...)
exec_d = yd_ref.enterprise_executions(id=...)
punish = yd_ref.enterprise_punishment(id=...)
abnormal = yd_ref.enterprise_abnormal_operation(id=...)
```

#### 3. 视情况补细节
```python
yd_ref.enterprise_writ_list(id=..., page_no=1)      # 涉诉文书
yd_ref.enterprise_change_info(id=...)                # 变更记录（大幅减资必查）
yd_ref.enterprise_out_invest(id=...)                 # 对外投资（子公司/参股公司/关联资产）
yd_ref.enterprise_frozen_equity(id=...)              # 股权冻结
yd_ref.enterprise_pledge(id=...)                     # 股权出质
yd_ref.enterprise_court_session_notice(id=...)       # 开庭公告
yd_ref.enterprise_court_notice(id=...)               # 法院公告
```

### 风险判断规则

#### R1 主体状态异常 → 直接高危
#### R2 新设+少股东+高资本+未足额实缴 → 中高危
#### R3 社保=0 + 实体行业 → 警惕
#### R4 大幅减资（>50%）→ 红色信号
#### R5 失信/被执行人/限高/严重违法 → 直接高危

---

## 场景二：查法律法规

### 触发词
"查一下XX法" / "XX规定有吗" / "XX司法解释全文"

### 工作流

#### 已知精确标题
```python
data = yd_ref.search_fagui(fgmc="精确名称", sxx="现行有效", xljb_1="对应级别", top_k=5)
detail = yd_ref.get_fagui_detail(id=items[0]["id"])
```

#### 只知道主题
```python
data = yd_ref.search_fagui(keyword="关键词", search_mode="AND", xljb_1="地方司法文件")
# 或语义检索
data = yd_ref.law_vector_search(query="问题描述", effect1="地方司法文件")
```

### 通知外壳处理
标题含"关于印发……通知" → 看 content 有无完整附件正文。有则保留，无则跳过。

---

## 场景三：查案例

### 触发词
"找XX案例" / "有没有关于XX的判决"

### 工作流

#### 1. 权威案例优先
```python
data = yd_ref.search_qwal(qw="关键词", xzqh_p=["江苏"], top_k=10)
items = yd_ref._extract_items(data)
```

#### 2. 普通案例补充
```python
data = yd_ref.search_ptal(
    qw="关键词", xzqh_p=["江苏"],
    wszl="判决书", ja_start="2023-01-01", top_k=10
)
```

### 关键判断
- content 含 `本院认为`/`裁判分析`/`应当认定` 且 >500 字 → 直接入库
- content < 200 字 → 调 `get_case_detail(type="ptal", id=...)`

---

## 场景四：执行财产线索调查

### 触发词
"查财产线索" / "查应收款" / "看有没有钱" / "执行调查" / "查对方公司有什么资产"

### 适用场景
对方公司是 **被执行人 / 被告 / 债务人**，你想知道它有没有**可执行的财产线索**。

### 核心思路
**找被执行人公司的"债权"比找它的"固定资产"更容易变现。**
一个公司欠你钱，但它可能也欠别人钱（应收款/中标款/胜诉款），这些债权就是财产线索。

### 工作流

#### 第 1 层：锁定主体 + 基础风险画像
```python
candidates = yd_ref.enterprise_search(name, top_k=5)
detail = yd_ref.get_company_detail(id=主体id)
writ_agg = yd_ref.enterprise_writ_agg(id=主体id)
exec_p = yd_ref.enterprise_executed_person(id=主体id)
exec_d = yd_ref.enterprise_executions(id=主体id)
```
先搞清楚：这家公司有多少执行案件、自己是原告多还是被告多。

#### 第 2 层：查"这家公司作为原告/申请执行人"的案件 → 找债权线索

这是财产线索调查最值钱的一步。从 `enterprise_writ_agg` 的聚合统计看：
- **诉讼身份**分布中"原告方/申请执行人"占比高 → 你可能能代位行使其胜诉债权
- 再从 `enterprise_writ_list` 筛选出该公司作为原告/申请人的案件

```python
# 先看诉讼身份分布
writ_agg = yd_ref.enterprise_writ_agg(id=主体id)
# 看 data 中的"诉讼身份"或"起诉方/应诉方"维度
# 再到涉诉文书列表找具体案件
writ_list = yd_ref.enterprise_writ_list(id=主体id, page_no=1)
# 筛选 title 或起诉方字段中包含该公司作为原告的案件
```

重点关注：
- 合同纠纷 → 可能有应收账款
- 工程款纠纷 → 可能有未结工程款
- 借贷纠纷 → 可能有未还借款
- 劳动争议（公司诉员工）→ 可能有竞业限制/赔偿金

#### 第 3 层：开庭公告 → 看正在发生的债权事件
```python
notices = yd_ref.enterprise_court_session_notice(id=主体id)
```
已开庭或即将开庭的案件 = 即将判决的债权。
- 查起诉方/应诉方：公司诉谁？
- 查案由：什么类型的债权？
- 查审理法院：在哪起诉的？

#### 第 4 层：法院公告 → 看是否有遗漏的诉讼
```python
court_notices = yd_ref.enterprise_court_notice(id=主体id)
```
法院公告里可能包含：
- 缺席判决 → 对方失联，该公司可能已经赢了
- 送达公告 → 案件在推进中
- 清算/破产公告 → 也可能在给自己清算

#### 第 5 层：股权冻结/出质 → 看是否有可供执行的股权资产
```python
frozen = yd_ref.enterprise_frozen_equity(id=主体id)
pledge = yd_ref.enterprise_pledge(id=主体id)
```
：该公司持有的**其他公司的股权** → 可以申请执行这些股权
重点看：`股权数额`、`被执行公司名称`（标的方）、`冻结法院`

#### 第 6 层：对外投资 → 看子公司/参股公司是否值钱
```python
out_invest = yd_ref.enterprise_out_invest(id=主体id)  # 或完整翻页
# out_invest_all = yd_ref._fetch_all_pages(lambda p: yd_ref.enterprise_out_invest(id=主体id, page_no=p), max_pages=20)
```
从 `enterprise_out_invest` 或 `get_company_detail` 返回的 `对外投资` 字段看：
- 有哪些子公司
- 持股比例
- 这些子公司本身有没有价值

### 财产线索汇总逻辑

汇总时按"变现难度"排序：

```
=== 财产线索（按变现难度排序）===

❶ 已胜诉/已判决债权（最容易）
- 作为原告已胜诉案件 X 件，金额约 XXX
- 对方被执行人：XXX公司
- 案号：[案号]

❷ 在诉/将开庭债权
- 作为原告在诉 X 件
- 主要案由：合同纠纷 / 工程款 / 借款
- 近期开庭：[日期] [法院]

❸ 持有的股权资产
- 对外投资 X 家公司
- 其中有股权冻结 Y 笔
- 有价值子公司：[名称 持股比例]

❹ 无形资产
- 商标 X 件 / 专利 X 件
- ICP 备案域名 X 个

❺ 已知债务压力（影响执行可行性）
- 被执行人 X 条 / 失信 X 条
- 自身债务也很多，需评估"顺位"
```

### 汇报示例

```
【财产线索调查】XXX有限公司

=== 主体概况 ===
被执行人案件：3 条（金额合计 120 万）
失信被执行人：1 条
自身涉诉：共 48 件（作为原告 35 件 / 作为被告 13 件）

=== 债权线索（按变现难度排序）===

❶ 已胜诉债权（最优线索）
→ 诉 XXX 公司合同纠纷（案号：XXXX），判决金额 80 万，已申请执行
→ 诉 XXX 公司工程款纠纷，判决金额 200 万

❷ 在诉案件
→ 近期开庭：YYYY-MM-DD，XXX 公司诉 XXX，合同纠纷，XXX法院

❸ 对外投资与股权
→ 持有 XX 公司 60% 股权（注册资本 500 万）
→ 持有 XX 公司 30% 股权（注册资本 1000 万）

❹ 建议
1. 优先对其已胜诉案件的对方债务人做代位执行
2. 核实其对外投资股权的实际价值和变现可能
3. 建议调取具体判决书确认金额和执行状态
```

---

## 企业尽调章节映射

做完整公司尽调时，不要一股脑全调接口；按章节调，省积分也更像律师工作底稿。

| 尽调章节 | 必调/建议接口 |
|---|---|
| 0 总览速查 | `enterprise_aggregation_summary` — 一条接口18个维度，省积分；后续按需深挖具体章节 |
| 1 主体资格 | `get_enterprise_base_info`、`enterprise_change_info`；建议 `enterprise_abnormal_operation`、`enterprise_serious_illegal` |
| 2 股权结构 | `get_enterprise_base_info`、`enterprise_pledge`、`enterprise_frozen_equity` |
| 3 治理组织 | `get_enterprise_base_info`（核心成员、分支机构） |
| 4 核心资产/IP | `enterprise_brand`、`enterprise_patent`、`enterprise_soft_right`；建议 `enterprise_works_right`、`enterprise_icp` |
| 5 业务合同 | 元典覆盖有限，只用经营范围辅助，仍需人工材料 |
| 6 财税 | `enterprise_corporate_tax` |
| 7 劳动人事 | 元典无直接覆盖，需人工材料 |
| 8 债权债务/担保 | `enterprise_guaranty`、`enterprise_pledge` |
| 9 诉讼行政执行 | `enterprise_writ_agg` 先看全貌，再调 `enterprise_writ_list`、`enterprise_executed_person`、`enterprise_executions`、`enterprise_punishment`；建议 `enterprise_court_notice`、`enterprise_court_session_notice`、`enterprise_frozen_equity` |
| 10 其他重要事项 | `enterprise_out_invest` |

### 底稿引用规范
1. API 数据**不列入“已获取材料清单”**，它是辅助核验数据，不是目标公司提交材料。
2. 在调查发现段首注明：`经查阅元典开放平台「接口名」接口（调用时间 YYYY-MM-DD HH:MM，原始数据见 缓存/文件名）……`
3. 元典数据与公司提供材料不一致时，按中/高风险提示；不得为了结论整齐而抹掉冲突。
4. 调用失败要留痕：接口、时间、原因、是否改用其他路径。

---

## 输出格式

### MD 格式（默认）

默认输出 Markdown 文档：
- 存放在 `~/Documents/知识库/raw/yuandian-cache/`（自动缓存）
- 同时输出到终端用于阅读
- 适合自己查看、保存到知识库

### 正式文件导出

本通用包不内置 PDF / DOCX 导出流程，也不绑定任何特定排版工具。用户如果需要正式文件，可以在本包生成的 Markdown 基础上自行配置导出工具。

---

## 通用汇报规则

1. **结论先行**：先给结论/风险等级/关键发现
2. **符号标记**（仅 MD 格式）：
   - ❌ 高风险 / 硬伤
   - ⚠️ 中风险 / 需关注
   - ℹ️ 信息参考
   - ✅ 积极信号
3. 对外正式文本应使用文字替代符号
4. **注明来源**：如"数据来源：元典企业信息，调用日期 YYYY-MM-DD"
5. **问用户才展开**：汇报后问"需要调具体判决/法规全文吗？"

---

## 缓存管理

### 位置
```text
~/Documents/知识库/raw/yuandian-cache/
├── SEARCH-{hash}.md    # 搜索结果
├── C-{id}_name.md      # 企业详情
├── L-{id}_name.md      # 法规详情
├── P/Q-{id}_name.md    # 案例详情
└── index.json
```

### 有效期
- 企业类：30 天
- 法规/案例：90 天
- 财产线索类：15 天（状态变化快，建议短效期）

---

## 已知坑

| 场景 | 坑 | 处理 |
|------|----|------|
| 查公司 | 名称有歧义 | 先用 `enterprise_search` 锁主体 |
| 查公司 | 聚合接口不接受名称 | `enterprise_aggregation_summary` 等聚合接口只接受 `id` 或 `tyshxydm`，给名字必须先模糊搜索拿到信用代码 |
| 查法规 | 精确名称命中通知外壳 | 看 content 有无附件正文 |
| 查案例 | 返回 `{"total","lst"}` 非列表 | 用 `_extract_items()` 标准化 |
| 查案例 | ay 参数 syntax error | 不用 ay，用 qw 替代 |
| 查案例 | xzqh_p 报错 | 必须传 `["江苏"]` 不是 `"江苏"` |
| 查详情 | code=500 程序处理异常 | 不重试，换路径 |
| 缓存 | 企业数据变化 | 企业类保持 30 天失效 |

---

## 与本地知识库的关系

- 查询结果自动缓存到 `~/Documents/知识库/raw/yuandian-cache/`
- 如需正式入库到知识库主结构，调用 `legal-kb` 的 ingest 流程
