# Obsidian 文献从初筛到知识提炼全流程

## 目标

把文献从“找到一篇、读完一篇”变成一个持续增长的研究知识系统。最终产物不是一堆孤立笔记，而是：文献库、概念网络、证据矩阵、可写作论点和可视化知识地图。

注意：`nature-academic-search` 和 `nature-reader` 属于 nature skills 包，不属于 Obsidian skills 包。本手册只建议在检索和全文阅读环节与它们配合使用。

## Obsidian 流程内技能

| 阶段 | 主要 skill/插件 | 用法 |
|---|---|---|
| 摘要初筛 | `obsidian-abstract-reader` | 对 PubMed/DOI/摘要打分，生成 `decision`、`screening_score` 和初筛笔记 |
| Obsidian 写作 | `obsidian-markdown` | 生成 wikilink、callout、PDF embed、frontmatter、概念页 |
| Vault 操作 | `obsidian-cli` 或 Obsidian MCP | 批量读取、移动、搜索、更新笔记 |
| Zotero 管理 | Zotero 插件 | 导入文献、导入 PDF、读取附件、去重，优先保留有附件条目 |
| 知识提炼 | `obsidian-literature-synthesis` | 从 `01 Papers` 提炼 MOC、概念页、矩阵和论文论点 |
| 表格视图 | `obsidian-bases` | 为文献库创建可筛选的数据库视图 |
| 知识地图 | `json-canvas` | 创建 `.canvas` 研究框架图和证据图谱 |

## 建议配合使用的外部 Nature Skills

| 外部 skill | 建议用途 | 输出如何进入本流程 |
|---|---|---|
| `nature-academic-search` | 文献检索、PubMed/CrossRef/arXiv、RIS/BibTeX、题录管理 | 将检索结果、PMID/DOI 或 RIS/BibTeX 交给初筛与 Zotero 导入环节 |
| `nature-reader` | 从 PDF、DOI、publisher HTML 或粘贴全文生成结构化精读 | 将精读结果写入 `01 Papers` 的 `## 全文精读` 小节 |

## 目录规范

```text
00 Inbox/              待处理文献和暂缺全文文献
01 Papers/             已精读并纳入的文献
02 Concepts/           概念页
03 Synthesis/          MOC、证据矩阵、论文论点、流程页
Attachments/PDFs/      PDF 附件
Bases/                 Obsidian Bases 视图
Canvas/                Obsidian Canvas 图谱
Other/                 非 Include 文献
```

## 阶段 1：初筛

输入可以是 PMID、DOI、PubMed 链接、题录表或摘要文本。

每篇初筛笔记至少包含：

```yaml
---
title: ...
pmid: ...
doi: ...
journal: ...
year: ...
screening_score: 0
decision: Include | Exclude | Maybe | Need Full Text
status: to-read
---
```

初筛笔记建议包含：研究问题、方法与人群、主要结果、初筛价值、全文核查要点。

## 阶段 2：决策分流

- `decision: Include`：进入 PDF/全文获取。
- `decision: Need Full Text`：暂留 `00 Inbox`，等待 PDF 或可读全文。
- 非 Include：移入 `Other`。

不要因为暂时没有 PDF 就删除文献。若能读取 HTML/PMC 全文，也可以完成精读后进入 `01 Papers`。

## 阶段 3：PDF 与 Zotero

1. 将 PDF 放入 `Attachments/PDFs/`。
2. 导入 Zotero 指定分类。
3. 为文献笔记写入：
   - PDF embed：`![[Attachments/PDFs/xxx.pdf]]`
   - Zotero item key
   - Zotero attachment key
4. Zotero 去重时优先保留有附件条目。
5. 无附件重复条目可移入 Zotero 回收站，但操作前应备份数据库或使用可恢复方式。

## 阶段 4：全文精读

普通 PDF/HTML 可直接阅读；需要高质量全文对照、图表感知或论文深读时，可以建议配合外部 `nature-reader`。

精读小节建议统一为：

```markdown
## 全文精读（YYYY-MM-DD）

![[Attachments/PDFs/xxx.pdf]]

- Zotero item key: `...`
- Zotero attachment key: `...`
- PDF: `Attachments/PDFs/xxx.pdf`

### 一句话结论

### 研究设计与人群

### 关键结果

### 对本课题的启发

### 方法学评价
```

完成后把 `status` 改为 `read`，并移入 `01 Papers`。

## 阶段 5：知识提炼

从 `01 Papers` 提炼四层结构：

1. MOC：主题地图，回答“这个课题有哪些核心问题”。
2. 概念页：回答“这个概念是什么，有哪些证据支持”。
3. 证据矩阵：横向比较文献。
4. 论文论点页：把证据改写成可用于论文讨论的论点。

## 概念页模板

```markdown
---
type: concept
topic: ...
status: seed | active
created: YYYY-MM-DD
tags:
  - concept
---
# 概念名

## 核心定义

## 关键证据

- [[01 Papers/文献A|文献A]]：一句话证据。

## 对本课题的意义

## 可写入论文的表达

## 待补问题
```

## MOC 模板

```markdown
---
type: MOC
topic: ...
status: active
created: YYYY-MM-DD
tags:
  - MOC
---
# 主题 MOC

## 这个页面怎么用

## 核心研究问题

## 知识节点

## 证据地图

## 写作出口

## 维护规则
```

## 证据矩阵模板

```markdown
| 文献 | 领域 | 国家/地区 | 策略或对象 | 经济学/政策结论 | 关联知识节点 |
|---|---|---|---|---|---|
| [[01 Papers/文献A|文献A]] |  |  |  |  | [[02 Concepts/概念]] |
```

## 论文论点页模板

```markdown
# 论文讨论可用论点

## 论点1：...

### 支撑证据

- [[01 Papers/文献A|文献A]]：...

### 可写入论文

...

## 下一步需要补强的证据
```

## 新增文献增量纳入

每次有新文献进入 `01 Papers`：

1. 读取新增文献的全文精读。
2. 判断证据角色：支持、反驳、限定、方法学参考、提出新问题。
3. 选择 1-3 个概念页。
4. 更新证据矩阵。
5. 更新论文论点页。
6. 必要时更新 MOC 和 Canvas。
7. 校验 wikilink 和 Canvas。

## 质量检查

- `00 Inbox` 中不应残留已精读且有全文的 Include 文献。
- `01 Papers` 中每篇应有 `status: read` 或明确阅读状态。
- 概念页不能只有文献列表，必须有自己的定义和可写入论文表达。
- 证据矩阵应覆盖所有与主题有关的 `01 Papers` 文献。
- 论文论点页应区分证据、推论和待补证据。
- Canvas 的文件节点路径必须存在，边引用不能断。

## 常用用户请求

- “请把 01 Papers 中新增文献纳入知识体系。”
- “请更新 MOC、概念页、证据矩阵和论文论点。”
- “请为这个课题生成 Obsidian Canvas 知识地图。”
- “请检查哪些文献还没有被纳入概念页。”
- “请根据这些文献生成论文讨论部分的论点。”