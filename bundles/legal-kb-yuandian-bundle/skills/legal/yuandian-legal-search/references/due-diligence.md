<!-- Archived from skill `yuandian-due-diligence` during umbrella consolidation. Original path: generic-local-skill/yuandian-due-diligence -->

---
name: yuandian-due-diligence
description: 元典增强版中国法律尽职调查技能。用于公司法律尽调项目初始化、底稿逐章撰写、完整性检查、尽调报告生成；对接 yuandian-legal-search / yuandian-api-reference 获取企业工商、诉讼、执行、知识产权等辅助数据。
tags: [yuandian, due-diligence, legal, company, report, working-paper]
related_skills: [yuandian-legal-search, yuandian-api-reference, md-to-pdf-macos]
---

# 元典增强版法律尽职调查

> 来源吸收：法律元力 `legal-due-diligence` 的好结构。  
> 本地改造：不依赖 Claude Code 路径，不单独安装 `yd-enterprise-info`；统一调用我们已有的 `yuandian-legal-search` / `yuandian-api-reference`。

## 结论

这是一个**独立技能**，不要塞进 `yuandian-legal-search`。  
理由很简单：`yuandian-legal-search` 是数据检索层；本技能是项目管理、底稿和报告生产层。混在一起会变成一锅粥。

## 触发词

“尽职调查”“尽调”“法律尽调”“DD报告”“尽调报告”“底稿”“写第X章底稿”“生成尽调报告”“检查底稿”。

## 总流程

```text
init 初始化项目 → collect/yuandian 拉取辅助数据 → draft 逐章写底稿 → check 完整性检查 → report 生成报告 → pdf 可选转 PDF
```

## 模式一：init 初始化项目

### 必要输入
- `project_path`：项目路径
- `target_company`：目标公司全称
- `client_name`：委托人名称

### 可选输入
- `base_date`：调查基准日，默认当天
- `purpose`：调查目的，如股权收购、投资入股、融资、并购
- `law_firm`：律师事务所
- `lawyers`：经办律师
- `uscc`：统一社会信用代码

### 执行
使用本技能脚本：
```bash
python3 scripts/init_project.py \
  --path /path/to/project \
  --target "目标公司全称" \
  --client "委托人名称" \
  --base-date YYYY-MM-DD \
  --purpose "股权收购" \
  --law-firm "律师事务所" \
  --lawyers "经办律师" \
  --uscc "统一社会信用代码"
```

### 项目结构
```text
项目目录/
├── project-info.md
├── working-paper.md          # 10章合一底稿
├── raw/
│   └── chineselaw/           # 元典原始 JSON 留痕
└── report/
```

## 模式二：yuandian / collect 拉取元典辅助数据

先加载 `yuandian-legal-search`。如果用户只给公司名，先 `enterprise_search` 锁定主体；有 USCC 时直接用 USCC。

### 章节 → 元典接口映射

| 尽调章节 | 必调/建议接口 |
|---|---|
| 1 主体资格 | `get_enterprise_base_info`、`enterprise_change_info`；建议 `enterprise_abnormal_operation`、`enterprise_serious_illegal` |
| 2 股权结构 | `get_enterprise_base_info`、`enterprise_pledge`、`enterprise_frozen_equity` |
| 3 治理组织 | `get_enterprise_base_info`（核心成员、分支机构） |
| 4 核心资产/IP | `enterprise_brand`、`enterprise_patent`、`enterprise_soft_right`；建议 `enterprise_works_right`、`enterprise_icp` |
| 5 业务合同 | 元典覆盖有限，只用经营范围/ICP备案辅助，主要依赖材料 |
| 6 财税 | `enterprise_corporate_tax`；行政处罚中筛税务处罚 |
| 7 劳动人事 | 元典无直接覆盖，可从涉诉文书筛劳动争议 |
| 8 债权债务/担保 | `enterprise_guaranty`、`enterprise_pledge`、`enterprise_frozen_equity` |
| 9 诉讼行政执行 | `enterprise_writ_agg`、`enterprise_writ_list`、`enterprise_executed_person`、`enterprise_executions`、`enterprise_punishment`；建议 `enterprise_court_notice`、`enterprise_court_session_notice` |
| 10 其他重要事项 | `enterprise_out_invest` |

### 元典数据使用纪律
1. API 数据只作辅助核验和线索，不替代目标公司原始材料。
2. API JSON 放 `项目目录/raw/chineselaw/`，保留调用时间、接口名、主体标识。
3. API 数据**不列入 §X.2 已获取材料清单**。
4. 写入 §X.4 调查发现时注明：`经查阅元典开放平台「接口名」接口（调用时间 YYYY-MM-DD HH:MM，原始数据见 raw/chineselaw/文件名）……`
5. 元典数据与公司材料冲突，§X.5 必须作为中/高风险提示。
6. 分页数据检查 `_meta.fetched_items == _meta.total`；不一致就在 §X.6 律师备忘注明数据可能不完整。
7. 分页接口每页约 10 积分。默认先取关键页，完整尽调再用 `_fetch_all_pages(..., max_pages=20)`，不要手贱无限翻页。

## 模式三：draft 撰写底稿

### 必要输入
- `chapter`：章节编号 1-10 或章节名称
- `materials`：材料路径或用户粘贴文本
- `project_path`：项目路径，若上下文已有可省略

### 步骤
1. 读取 `references/section-guide.md` 中对应章节，不要全量加载浪费上下文。
2. 检查 `project_path/raw/chineselaw/` 是否有相关元典 JSON；有就整合，没有就提示可补拉。
3. 阅读用户材料。
4. 按底稿六段结构写入 `working-paper.md` 对应章节。
5. 发现与意见分离：§X.4 只写事实，§X.5 才写风险评价。

### 每章底稿六段结构
```markdown
## 第X章 章节名称

### X.1 调查范围与方法
### X.2 已获取材料清单
### X.3 未获取/待补充材料
### X.4 调查发现
### X.5 风险提示
### X.6 律师备忘
```

### 底稿硬规则
- 每项发现必须注明来源：“经查阅[文件名称]，……”
- 金额、日期、比例、案号、证照编号必须精确引用。
- 缺失材料必须进 §X.3，并说明影响。
- 风险等级：🔴 高 / 🟡 中 / 🟢 低。
- §X.6 律师备忘可以直说疑点，最终报告里删除。

## 模式四：check 完整性检查

读取 `working-paper.md`，输出：
```markdown
# 尽调底稿完整性检查报告

## 总览
| 章节 | 状态 | 已获取材料 | 缺失材料 | 风险数量 |

## 缺失材料汇总
## 风险汇总
## 后续工作建议
```

重点检查：
- 10 章是否齐全；
- 每章六段是否完整；
- 是否有 `[待撰写]`、空表、占位符；
- 高风险是否进入最终风险汇总；
- 元典数据是否注明来源且未混入材料清单。

## 模式五：report 生成尽调报告

### 步骤
1. 读取 `references/report-standards.md`。
2. 读取 `assets/report-template.md`。
3. 读取 `working-paper.md`。
4. 按“底稿 → 报告”转化规则生成报告，写入 `report/法律尽职调查报告_目标公司_YYYYMMDD.md`。

### 底稿 → 报告转化
| 底稿部分 | 报告对应 | 处理 |
|---|---|---|
| 调查范围与方法 | 各章“调查范围” | 简化，去掉内部过程 |
| 已获取材料清单 | 附件文件清单 | 汇总 |
| 未获取/待补充材料 | 声明与限定条件 | 转为限制性表述 |
| 调查发现 | 基本情况/调查结果 | 精炼为客户可读事实 |
| 风险提示 | 律师意见 + 重大风险提示 | 增加法律分析和建议 |
| 律师备忘 | 不体现 | 删除 |

### 报告语言
- 用“本所律师”“目标公司”“委托人”。
- 不用“我、我们、看了一下、合法合规、保证、绝对、没问题”。
- 无法核实时写：`因未获取[材料]，本所律师无法就此事项发表意见。`
- 高风险写：`本所律师特别提请委托人关注：……`
- 中风险写：`本所律师提示委托人注意：……`

## 模式六：PDF 输出

用户要求“生成 PDF / 发客户 / 正式版”时加载 `md-to-pdf-macos`，把报告 MD 转 PDF。  
默认不要放桌面，除非用户明确要求；优先放项目 `report/` 目录。

## 支撑文件

- `references/section-guide.md`：10章调查要点、红旗风险、标准发现语言。
- `references/report-standards.md`：报告结构、声明、语言规范、格式规范。
- `references/external-apis.md`：元典辅助数据使用规范。
- `assets/working-paper-template.md`：10章合一底稿模板。
- `assets/report-template.md`：报告模板。
- `scripts/init_project.py`：初始化项目脚本。

## 我的本地改造原则

1. 数据层继续用 `yuandian-legal-search`，不新增重复 API 客户端。
2. 报告层独立成 skill，避免污染检索技能。
3. 所有项目材料收敛到案件/项目目录，不默认丢桌面。
4. 保留底稿与报告两阶段：底稿真实，报告克制。好报告不是把底稿美颜，是把事实和风险讲清楚。
