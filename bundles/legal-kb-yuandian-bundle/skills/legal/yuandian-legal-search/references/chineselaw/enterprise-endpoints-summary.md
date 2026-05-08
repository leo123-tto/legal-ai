# 企业信息接口速查（legal-due-diligence 视角）

> 完整接口文档及 CLI 用法见：[yuandian-legal-search skill](https://github.com/malnlda/yuandian-legal-search)
> 本文件仅作为 draft 阶段快速参考，供 LLM 知晓 raw/ 下各 JSON 文件的内容。

---

## 各子命令与 JSON 文件对应关系

| JSON 文件前缀 | 子命令 | 含义 | DD 章节 |
|---|---|---|---|
| `search-company_*` | search-company | 企业检索候选列表 | init |
| `get_enterprise_base_info_*` | get_enterprise_base_info | 基本信息+股东+核心成员+分支机构 | 1, 2, 3 |
| `enterprise_change_info_*` | enterprise_change_info | 变更记录（含历次法人/注册资本/经营范围变更） | 1 |
| `enterprise_brand_*` | enterprise_brand | 商标列表（名称/注册号/类别/有效期） | 4 |
| `enterprise_patent_*` | enterprise_patent | 专利列表 | 4 |
| `enterprise_soft_right_*` | enterprise_soft_right | 软件著作权列表 | 4 |
| `enterprise_works_right_*` | enterprise_works_right | 作品著作权列表 | 4 |
| `enterprise_icp_*` | enterprise_icp | 网站备案列表 | 4 |
| `enterprise_corporate_tax_*` | enterprise_corporate_tax | 欠税公告 | 6 |
| `enterprise_guaranty_*` | enterprise_guaranty | 对外担保 | 8 |
| `enterprise_pledge_*` | enterprise_pledge | 股权出质 | 2, 8 |
| `enterprise_frozen_equity_*` | enterprise_frozen_equity | 股权冻结 | 2, 9 |
| `enterprise_out_invest_*` | enterprise_out_invest | 对外投资 | 10 |
| `enterprise_abnormal_operation_*` | enterprise_abnormal_operation | 经营异常记录 | 1 |
| `enterprise_serious_illegal_*` | enterprise_serious_illegal | 严重违法记录 | 1, 9 |
| `enterprise_punishment_*` | enterprise_punishment | 行政处罚 | 9 |
| `enterprise_executed_person_*` | enterprise_executed_person | 被执行人 | 9 |
| `enterprise_executions_*` | enterprise_executions | 失信被执行人 | 9 |
| `enterprise_writ_agg_*` | enterprise_writ_agg | 涉诉统计（总量/案件类别/案由分布） | 9 |
| `enterprise_writ_list_*` | enterprise_writ_list | 涉诉文书列表 | 9 |
| `enterprise_court_notice_*` | enterprise_court_notice | 法院公告 | 9 |
| `enterprise_court_session_notice_*` | enterprise_court_session_notice | 开庭公告（反映未决诉讼）| 9 |

---

## 分页接口文件结构

所有分页接口文件均包含 `_meta` 字段，用于核验数据完整性：

```json
{
  "list": [ ... ],
  "_meta": {
    "fetched_pages": N,
    "fetched_items": M,
    "total": M,
    "fetched_at": "YYYY-MM-DDTHH:MM:SS"
  }
}
```

**核验要点**：`fetched_items == total` 表示数据完整；否则说明受 `--max-pages` 限制，数据不完整，应在底稿备注。
