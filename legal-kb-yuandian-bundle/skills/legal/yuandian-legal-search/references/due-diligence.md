# 元典辅助法律尽职调查流程

本文件用于把元典企业信息、诉讼执行、知识产权、行政合规等数据，作为公司法律尽职调查的辅助线索写入项目底稿和 Markdown 报告。它不是独立安装包；由 `yuandian-legal-search` 在需要做尽调项目时按需读取。

## 适用场景

- 初始化公司法律尽调项目。
- 按章节拉取元典辅助数据。
- 根据材料和 API 结果撰写底稿。
- 检查底稿完整性。
- 从底稿生成 Markdown 版尽调报告。

## 总流程

```text
init 初始化项目 -> collect 拉取辅助数据 -> draft 逐章写底稿 -> check 完整性检查 -> report 生成 Markdown 报告
```

## 模式一：init 初始化项目

### 必要输入

- `project_path`：项目路径。
- `target_company`：目标公司全称。
- `client_name`：委托人名称。

### 可选输入

- `base_date`：调查基准日，默认当天。
- `purpose`：调查目的，如股权收购、投资入股、融资、并购。
- `law_firm`：律师事务所。
- `lawyers`：经办律师。
- `uscc`：统一社会信用代码。

### 执行

```bash
python3 scripts/init_project.py \
  --path /path/to/project \
  --target "目标公司全称" \
  --client "委托人名称" \
  --base-date YYYY-MM-DD \
  --purpose "股权收购" \
  --law-firm "XX律师事务所" \
  --lawyers "张三,李四" \
  --uscc 91110108MA0074PN30
```

### 项目结构

```text
项目目录/
├── project-info.md
├── working-paper.md
├── raw/
│   └── chineselaw/
└── report/
```

## 模式二：collect 拉取元典辅助数据

先加载 `yuandian-legal-search`。如果用户只给公司名，先用 `enterprise_search` 锁定主体；有 USCC 时可直接用 USCC。

### 章节与接口映射

| 尽调章节 | 必调/建议接口 |
|---|---|
| 1 主体资格 | `get_enterprise_base_info`、`enterprise_change_info`；建议 `enterprise_abnormal_operation`、`enterprise_serious_illegal` |
| 2 股权结构 | `get_enterprise_base_info`、`enterprise_pledge`、`enterprise_frozen_equity` |
| 3 治理组织 | `get_enterprise_base_info`（核心成员、分支机构） |
| 4 核心资产/IP | `enterprise_brand`、`enterprise_patent`、`enterprise_soft_right`；建议 `enterprise_works_right`、`enterprise_icp` |
| 5 业务合同 | 元典覆盖有限，只用经营范围/ICP备案辅助，主要依赖用户材料 |
| 6 财税 | `enterprise_corporate_tax`；行政处罚中筛税务处罚 |
| 7 劳动人事 | 元典无直接覆盖，可从涉诉文书筛劳动争议 |
| 8 债权债务/担保 | `enterprise_guaranty`、`enterprise_pledge`、`enterprise_frozen_equity` |
| 9 诉讼行政执行 | `enterprise_writ_agg`、`enterprise_writ_list`、`enterprise_executed_person`、`enterprise_executions`、`enterprise_punishment`；建议 `enterprise_court_notice`、`enterprise_court_session_notice` |
| 10 其他重要事项 | `enterprise_out_invest` |

### 元典数据使用纪律

1. API 数据只作辅助核验和线索，不替代目标公司原始材料。
2. API JSON 放入 `项目目录/raw/chineselaw/`，保留调用时间、接口名、主体标识。
3. API 数据不得列入底稿的“已获取材料清单”。
4. 写入调查发现时注明：`经查阅元典开放平台「接口名」接口（调用时间 YYYY-MM-DD HH:MM，原始数据见 raw/chineselaw/文件名）……`
5. 元典数据与公司材料冲突时，必须作为中/高风险提示或待核验事项。
6. 分页数据检查 `_meta.fetched_items == _meta.total`；不一致时在律师备忘注明数据可能不完整。
7. 分页接口可能消耗积分；快速体检只取关键页，完整尽调再用 `_fetch_all_pages(..., max_pages=20)`。
8. 调用失败要留痕：接口、时间、原因、是否改用其他路径。

## 模式三：draft 撰写底稿

### 必要输入

- `chapter`：章节编号 1-10 或章节名称。
- `materials`：材料路径或用户粘贴文本。
- `project_path`：项目路径，若上下文已有可省略。

### 步骤

1. 读取 `references/section-guide.md` 中对应章节，不要全量加载浪费上下文。
2. 检查 `project_path/raw/chineselaw/` 是否有相关元典 JSON；有就整合，没有就提示可补拉。
3. 阅读用户材料。
4. 按底稿六段结构写入 `working-paper.md` 对应章节。
5. 发现与意见分离：调查发现只写事实，风险提示再写评价。

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

- 每项发现必须注明来源。
- 金额、日期、比例、案号、证照编号必须精确引用。
- 缺失材料必须进入 `X.3`，并说明影响。
- 风险等级可用：高 / 中 / 低。
- 律师备忘可以记录疑点，最终报告中应删除内部过程性内容。

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

- 10 章是否齐全。
- 每章六段是否完整。
- 是否有 `[待撰写]`、空表、占位符。
- 高风险是否进入最终风险汇总。
- 元典数据是否注明来源且未混入材料清单。

## 模式五：report 生成报告

### 步骤

1. 读取 `references/report-standards.md`。
2. 读取 `assets/report-template.md`。
3. 读取 `working-paper.md`。
4. 按“底稿 -> 报告”转化规则生成 Markdown 报告，写入 `report/法律尽职调查报告_目标公司_YYYYMMDD.md`。

### 底稿 -> 报告转化

| 底稿部分 | 报告对应 | 处理 |
|---|---|---|
| 调查范围与方法 | 各章调查范围 | 简化，去掉内部过程 |
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

## 正式文件导出

本通用包不内置 PDF / DOCX 导出流程，也不绑定任何特定排版工具。用户要求正式版时，先生成 Markdown 报告；如需 PDF / DOCX，由使用者在自己的环境中另行配置导出工具。

## 支撑文件

- `references/section-guide.md`：10 章调查要点、红旗风险、标准发现语言。
- `references/report-standards.md`：报告结构、声明、语言规范、格式规范。
- `references/chineselaw/enterprise-endpoints-summary.md`：企业信息接口与章节映射速查。
- `assets/working-paper-template.md`：10 章合一底稿模板。
- `assets/report-template.md`：报告模板。
- `scripts/init_project.py`：初始化项目脚本。
