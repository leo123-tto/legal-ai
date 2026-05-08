<!-- Archived from skill `yuandian-api-reference` during umbrella consolidation. Original path: generic-local-skill/yuandian-api-reference -->

---
name: yuandian-api-reference
description: 元典开放平台完整 API 接口说明书。覆盖法律法规、法条、案例、企业信息全部 30+ 接口的路径、参数、返回、已知坑。
tags: [yuandian, api, legal, enterprise, reference]
---

# 元典 API 接口说明书

> 基于用户整理的原档 + 实战踩坑积累
> 更新日期：2026-04-29
> Base URL：`https://open.chineselaw.com/open`
> 认证：`X-Api-Key` 请求头

## 先说结论

1. **先检索，后详情**。不要在检索结果能解决问题时调详情接口。
2. **企业优先 GET，法规/案例 POST**。混合用会 405。
3. **id 优先于名称**。传 `id` 最稳，传 `fgmc`/`名称` 容易命中通知外壳或异常。
4. **本地过滤优于接口过滤**。接口做第一层筛选，本地做第二层。

## 接口总览

### A. 法律法规组（POST）
| 接口 | 用途 |
|------|------|
| `rh_fg_search` | 法规关键词检索 |
| `rh_fg_detail` | 法规详情 |
| `rh_ft_search` | 法条关键词检索 |
| `rh_ft_detail` | 法条详情 |
| `law_vector_search` | 法规语义检索 |

### B. 案例文书组（POST + GET）
| 接口 | 用途 |
|------|------|
| `rh_qwal_search` | 权威案例关键词检索 |
| `rh_ptal_search` | 普通案例关键词检索 |
| `rh_case_details` | 案例详情（GET） |
| `case_vector_search` | 案例语义检索 |

### C. 企业信息组（全部 GET）
**定位：** `rh_enterpriseSearch`、`rh_company_info`、`rh_company_detail`、`rh_enterpriseBaseInfo`

**工商治理/投融资：** `rh_enterpriseChangeInfo`、`rh_enterprisePledge`、`rh_enterpriseFrozenEquity`、`rh_enterpriseGuaranty`、`rh_enterpriseOutInvest`

**诉讼执行：** `rh_enterpriseWritAgg`、`rh_enterpriseWritList`、`rh_enterpriseCourtSessionNotice`、`rh_enterpriseCourtNotice`、`rh_enterpriseExecutions`、`rh_enterpriseExecutedPerson`

**行政合规：** `rh_enterprisePunishment`、`rh_enterpriseAbnormalOperation`、`rh_enterpriseSeriousIllegal`、`rh_enterpriseCorporateTax`

**知产资产：** `rh_enterpriseBrand`、`rh_enterprisePatent`、`rh_enterpriseSoftRight`、`rh_enterpriseWorksRight`、`rh_enterpriseIcp`

**聚合总览：** `rh_enterpriseAggregationSummary` — 18个维度一站式统计汇总，省积分

---

## 一、法律法规接口

### 1. `search_fagui(keyword=, search_mode=, fgmc=, sxx=, xljb_1=, fbrq_start/end=, ssrq_start/end=, top_k=10)`
**路径：** `POST /rh_fg_search`
**最常用的法规入口。**

| 参数 | 说明 |
|------|------|
| `keyword` | 关键词搜索 |
| `search_mode` | `AND` / `OR` |
| `fgmc` | 精确法规名称过滤 |
| `sxx` | 时效性：`现行有效`、`失效` |
| `xljb_1` | 效力级别：法律/司法解释/行政法规/部门规章/地方性法规/地方司法文件/地方政府规章/地方规范性文件 |
| `fbrq_start/end` | 发布日期范围（YYYY-MM-DD） |
| `ssrq_start/end` | 实施日期范围 |
| `top_k` | 返回条数，最大 50 |

**用法：**
- 已知精确标题：`fgmc=精确名称` + `sxx=现行有效` + `xljb_1=对应级别` + `top_k=3~5`
- 主题检索：`keyword="关键词 组合"` + `search_mode="AND"` + `xljb_1=...`
- **别只丢简称**（"盗窃罪解释" → 命中通知）

### 2. `get_fagui_detail(id=, fgmc=, refer_date=)`
**路径：** `POST /rh_fg_detail`

**核心规则：优先传 `id`，别优先传 `fgmc`。**
因为直接 `fgmc` 可能：
- 命中错版本
- 命中通知外壳（"关于印发《XX》的通知"）
- 直接返回 `程序处理异常`

**最稳流程：** `search_fagui` 拿候选 → 本地筛 → 用 `id` 调详情

**通知外壳处理：** 检查 `content` 里是否有完整附件正文：
- 有 → 提取正文保留
- 只有发文壳 → 不入库

### 3. `search_fatiao(keyword=, search_mode=, fgmc=, ...)`
**路径：** `POST /rh_ft_search`
按法条内容关键词搜索。适合：
- 要规则点，不是整部法规
- `rh_fg_search` 找不到时用法条反推

### 4. `get_fatiao_detail(id=, fgmc=, ftnum=, refer_date=)`
**路径：** `POST /rh_ft_detail`
已知法规名+条号时取具体条文。

### 5. `law_vector_search(query=, rewrite_flag=True, effect1=, sxx="现行有效", top_k=10)`
**路径：** `POST /law_vector_search`
按问题/语义搜法规，不知精确标题时用。

**`effect1` 可用值：** 法律、司法解释、行政法规、部门规章、地方性法规、地方司法文件、地方政府规章、地方规范性文件

**适合：** 找"审理指南""裁判指引"这类主题材料

---

## 二、案例文书接口

### 1. `search_qwal(qw=, title=, ah=, ay=, jbdw=, xzqh_p=, ja_start/end=, top_k=10)`
**路径：** `POST /rh_qwal_search`
搜权威案例（指导性/典型案例/公报案例）。

**核心原则：检索结果里的 `content` 往往已够用。**
有裁判要旨/典型意义 → 直接入库摘要版。只有 content 太短才调详情。

**已知坑：** `ay` 参数传中文常报 syntax error，靠 `qw` 做关键词匹配。
`xzqh_p` 必须传列表 `["江苏"]`，不能传字符串。

**返回结构（重要）：** 案例检索统一返回 `{"total": 总数, "lst": [...]}`，不是平铺列表。
代码中用工具函数标准化：
```python
from yuandian_api import _extract_items, _extract_total
items = _extract_items(data)   # → 列表
total = _extract_total(data)   # → 总数
```
`lst` 中每条的关键字段：`id`、`title`、`ah`（案号）、`cprq`（裁判日期）、`jbdw`（判决单位）、`ay`（案由数组）、`xzqh_p`（省）、`xzqh_c`（市）、`cj`（法院层级）、`spcx`（审判程序）。

### 2. `search_ptal(qw=, fxgc=, title=, ah=, ay=, jbdw=, xzqh_p=, wszl=, ajlb=, ja_start/end=, yyft=, ft_search_mode=, top_k=10)`
**路径：** `POST /rh_ptal_search`
搜普通案例。

**最关键的判断：** 检索结果里有 `本院认为` / `裁判分析` / `应当认定` / `不予支持`，且长度够 → 直接入库，不调详情。

**用法：**
- 民商事：`xzqh_p=["江苏"]` + `wszl=判决书` + `ja_start=近三年`
- 执行程序：`wszl=裁定书` 也可接受

### 3. `get_case_detail(type="qwal"|"ptal", id=, ah=)`
**路径：** `GET /rh_case_details`
调案例全文。**别名烧分，只在检索结果不够用时才调。**

**最值字段：**
- 普通案例：`content`、`fxgc`、`pjjg`、`cmss`、`yyft`、`jbdw`、`ay`、`wszl`
- 权威案例：`content`、`title`、`ah`、`jbdw`、`ay`、`cprq`

### 4. `case_vector_search(query=, rewrite_flag=True, xzqh_p=, xzqh_c=, cj=, fayuan=, wszl=, dianxing=, ja_start/end=, top_k=10)`
**路径：** `POST /case_vector_search`
按语义搜案例——适合"我知道问题，不知道案号/标题"。

**实战建议：**
- 地域先卡 `xzqh_p=["江苏"]`
- 普通案例卡近三年
- 执行程序可以放低文书种类限制

---

## 三、企业信息接口（全部 GET）

### 通用规则
- 大多数支持 `id` 或 `tyshxydm`，不能同时为空
- 分页参数：`pageNo`（默认 1），每页约 30-50 条
- 判断翻页用 `hasMore`，不要自己算
- 返回结构：`code=200` 成功，`code=404` 未找到，`code=500` 参数异常

### C1. 企业定位（先找主体）

#### `enterprise_search(name, top_k=10)`
**路径：** `GET /rh_enterpriseSearch`
**积分：** 1 积分
按名称关键词搜企业候选列表。**查公司第一步，也是唯一支持模糊查询的入口。** 不传全称会返回多个候选，需要确认目标企业后拿 `id` 或 `tyshxydm`。
返回：`id`、`企业名称`、`统一社会信用代码`

**重要：聚合接口、详情接口等只接受 `id` 或 `tyshxydm`，不接受名称。** 给名字查公司必须先走这里。

#### `get_company_info(name, num=2)`
**路径：** `GET /rh_company_info`
按名称直接拿聚合详情列表。重接口，适合名称明确时。
`num` 最大 50，但 `>50` 会被重置为 10。

#### `get_company_detail(id=, tyshxydm=)`
**路径：** `GET /rh_company_detail`
企业聚合全景——工商登记、股东、分支、对外投资、涉诉摘要、风险标签。**适合做企业尽调第一眼总览。**

#### `get_enterprise_base_info(id=, tyshxydm=)`
**路径：** `GET /rh_enterpriseBaseInfo`
轻量基础版——工商信息 + 股东 + 核心成员 + 分支机构。

### C2. 工商与治理

#### `enterprise_change_info(id=, tyshxydm=, page_no=1)`
企业变更记录。**非常值钱的接口。** 可看出法人是否频繁换、经营范围是否突变、股东结构是否动过。

#### `enterprise_pledge(id=, tyshxydm=, page_no=1)`
股权出质。关键字段：`登记日`、`状态`、`出质股权数额`、`出质人`、`质权人`

#### `enterprise_frozen_equity(id=, tyshxydm=, page_no=1)`
股权冻结。**比出质更硬的信号。** 关键字段：`执行法院`、`执行裁定文书号`、`股权数额`、`冻结开始/结束时间`

#### `enterprise_guaranty(id=, tyshxydm=, page_no=1)`
对外担保。关键字段：`债权人`、`债务人`、`主债权数额`、`保证方式`

#### `enterprise_out_invest(id=, tyshxydm=, page_no=1)`
对外投资。**尽调第10章和执行财产线索的高价值接口。** 关键字段通常包括：`被投资企业名称`、`统一社会信用代码`、`出资比例`、`出资金额`、`经营状态`。用于识别子公司/参股公司、关联资产、可供执行的股权价值。

#### 自动翻页工具：`_fetch_all_pages(func, max_pages=20)`
企业列表接口普遍分页且每页计费。需要完整清单时用：
```python
all_brand = _fetch_all_pages(lambda page_no: enterprise_brand(tyshxydm=USCC, page_no=page_no), max_pages=20)
all_cases = _fetch_all_pages(lambda page_no: enterprise_writ_list(id=ID, page_no=page_no), max_pages=5)
```
默认最多 20 页，`max_pages=0` 才不限制。判断翻页仍以接口返回的 `hasMore` 为准。

### C3. 诉讼与执行风险

#### `enterprise_writ_agg(id=, tyshxydm=)`
**涉诉聚合统计——先看轮廓，再看明细。** 按案件类别、一级/二级案由、文书种类、审判程序、法院层级、结案年份、地域、诉讼身份、对方当事人身份等多维度聚合。

**核心价值：** 能快速看出——原告多还是被告多、执行案件是否集中、近两年风险上升还是下降。

#### `enterprise_writ_list(id=, tyshxydm=, page_no=1)`
涉诉文书列表。关键字段：`文书id`、`标题`、`案号`、`案由`、`起诉方`、`应诉方`、`裁判结果`

#### `enterprise_court_session_notice(id=, tyshxydm=, page_no=1)`
开庭公告——看**正在发生的事**。

#### `enterprise_court_notice(id=, tyshxydm=, page_no=1)`
法院公告——送达/缺席风险线索。

#### `enterprise_executions(id=, tyshxydm=, page_no=1)`
**失信被执行人——明确高风险信号。** 关键字段：`失信被执行人`、`执行依据文书号`、`执行标的`、`履行情况`、`立案时间`、`失信行为具体情形`

#### `enterprise_executed_person(id=, tyshxydm=, page_no=1)`
**被执行人——注意区分失信和执行。** 被执行人不一定失信，失信是更重一层。

### C4. 行政与合规风险

#### `enterprise_punishment(id=, tyshxydm=, page_no=1)`
行政处罚。不只看有没有处罚，看处罚类型和依据（市监/税务/环保/网信含义差很大）。

#### `enterprise_abnormal_operation(id=, tyshxydm=, page_no=1)`
经营异常。一次异常不一定致命，反复列入、长期不移出就是问题。

#### `enterprise_serious_illegal(id=, tyshxydm=, page_no=1)`
严重违法。**比经营异常更重——信用与监管层硬伤。**

#### `enterprise_corporate_tax(id=, tyshxydm=, page_no=1)`
欠税公告。补一块税务信用信息，对交易相对方核验挺值。

### C5. 知识产权与线上资产

- `enterprise_brand()` — 商标
- `enterprise_patent()` — 专利
- `enterprise_soft_right()` — 软著
- `enterprise_works_right()` — 作品著作权
- `enterprise_icp()` — 网站备案

### C6. 企业聚合总览

#### `enterprise_aggregation_summary(id=, tyshxydm=)`
**路径：** `GET /rh_enterpriseAggregationSummary`
**积分：** ~10 积分
**参数限制：仅支持 `id` 或 `tyshxydm`（统一社会信用代码），不支持企业名称。** 如果只拿到名字，必须先走 `enterprise_search` 锁定主体。

**一次性拉取18个维度的统计汇总：** 对外投资、商标、专利、软著、作品著作权、网站备案、变更记录、失信被执行人、被执行人、开庭公告、法院公告、股权冻结、行政处罚、股权出质、对外担保、经营异常、欠税公告、严重违法。非年度统计取 top 20。

**核心价值：** 一个接口代替 C2-C5 十几个单独调用，省大量积分。适合尽调第一眼总览、快速风险扫描。每个维度返回统计聚合（分类 count + 总数），不返回明细。明细仍需走 C2-C5 各子接口。

**标准链路：** 给名字 → `enterprise_search`（1积分）模糊匹配 → 确认目标拿 `tyshxydm` → `enterprise_aggregation_summary` → 18维度总览一次到位。

---

## 四、标准工作流

### 找法规全文
1. `search_fagui`（精确标题或主题）
2. 本地筛标题/效力级别/时效性/通知外壳
3. 高置信 → `get_fagui_detail(id)`

### 找权威案例包
1. `search_qwal` 或 `case_vector_search`
2. 看 content 是否已有要旨
3. 有 → 直接入库；不够 → `get_case_detail(type="qwal")`

### 找普通案例
1. `search_ptal`（卡地域/案由/年份/文书种类）
2. 看 content/fxgc 是否有实质裁判分析
3. 有 → 直接入库；不够再拉详情

### 做公司快速风险体检
1. `enterprise_search` → 锁定主体
2. `enterprise_aggregation_summary` → 一条接口拉18个维度统计总览（省积分首选）
3. 需要明细再按需调：`get_company_detail` / `enterprise_writ_agg` / `enterprise_executed_person` / `enterprise_executions` 等

---

## 五、已知坑（重要）

| 问题 | 表现 | 处理 |
|------|------|------|
| 积分爆炸 | 分页接口每页计费；全量翻页可能几十页 | 默认只拉必要页；需要全量时用 `_fetch_all_pages(..., max_pages=20)`，明确再设 0 |
| 通知外壳 | 标题含"关于印发……的通知" | 看 content 有无完整正文 |
| 程序处理异常 | code=500 | 不要连续重试，换路径 |
| 案例内容空心 | content 只有"驳回上诉" | 跳过，没必要拉详情 |
| ay 参数报错 | syntax error | 别用 ay，用 qw 替代 |
| xzqh_p 格式 | 必须传列表 | `["江苏"]` ✅，`"江苏"` ❌ |
| 非 JSON 响应 | 偶发返回 HTML | 加 try-except 保护 |
| 鉴权失败 | 401 | 检查 API key，中止任务 |

## 六、积分消耗

- 每次 API 调用约 10 积分
- 检索积分消耗低，详情接口更贵
- 当前免费期（2026年上半年），后续可能收费
