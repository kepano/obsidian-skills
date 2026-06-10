---
name: obsidian-literature-synthesis
description: >-
  Obsidian 文献知识提炼工作流。Use when Codex needs to turn Obsidian literature notes in 01 Papers into a reusable knowledge system: classify new papers, update MOC pages, concept notes, evidence matrices, Canvas maps, Bases views, and paper-writing arguments; also use when the user asks in Chinese for “文献从初筛到精读再到知识提炼”, “纳入知识体系”, “更新 MOC/概念页/证据矩阵/论文论点”, or “Obsidian 文献库流程”.
---

# Obsidian 文献知识提炼

用这个 skill 把 Obsidian 文献笔记从“单篇已读”推进到“可写论文的知识体系”。默认配合这些技能使用：`obsidian-abstract-reader` 做初筛，Zotero 插件做文献与 PDF 管理，`obsidian-markdown` 写笔记，`obsidian-cli` 操作 vault，`obsidian-bases` 做表格视图，`json-canvas` 做知识地图。

## 快速判断

- 用户要处理 PubMed/DOI/摘要并生成初筛笔记：先用 `obsidian-abstract-reader`。
- 用户要下载/导入 PDF、操作 Zotero、去重或附件：配合 Zotero 插件。
- 用户已有 `01 Papers` 精读笔记，想总结主题、概念、证据和论文论点：用本 skill。
- 用户要把新增文献继续纳入已有体系：用本 skill 的“增量纳入”流程。
- 用户要生成 Canvas 或 Bases：本 skill 负责设计信息结构，再调用 `json-canvas` 或 `obsidian-bases`。

## 标准目录约定

优先沿用 vault 中已有结构；若不存在再创建：

- `00 Inbox/`：待处理或尚未找到全文的文献笔记。
- `01 Papers/`：已纳入的精读文献笔记。
- `02 Concepts/`：可复用概念页，不堆单篇长摘要。
- `03 Synthesis/`：MOC、证据矩阵、论文论点、纳入流程。
- `Canvas/`：知识地图和研究框架图。
- `Bases/`：文献表格、进度表、证据库视图。
- `Attachments/PDFs/`：PDF 附件。
- `Other/`：非 Include 或低相关文献。

## 全流程

1. 初筛：读取摘要和元数据，创建 `00 Inbox` 文献笔记，写入 `decision`、`screening_score`、关键词和初筛理由。
2. 决策分流：`decision: Include` 的文献进入全文获取；非 Include 移入 `Other`。
3. PDF 与 Zotero：为 Include 文献查找 PDF，导入 Zotero 目标分类，优先保留有附件条目并去重。
4. 精读：有 PDF 或可读全文时，在文献笔记中追加全文精读、PDF 嵌入、Zotero item key、attachment key，并把 `status` 改为 `read`。
5. 移动：完成精读的文献从 `00 Inbox` 移入 `01 Papers`。
6. 知识提炼：把 `01 Papers` 的单篇结论提炼到 MOC、概念页、证据矩阵、论文论点和 Canvas。
7. 增量维护：每次新增文献，只更新受影响的概念页、矩阵和论点，不重建整个体系。

## 知识提炼结构

创建或维护这些核心文件：

- `03 Synthesis/<主题> MOC.md`：主题地图，只做导航和问题框架。
- `02 Concepts/<概念>.md`：概念定义、关键证据、对课题意义、可写入论文表达、待补问题。
- `03 Synthesis/筛查策略经济学证据矩阵.md`：横向比较文献的领域、国家、策略、经济学结论和关联概念。
- `03 Synthesis/论文讨论可用论点.md`：把证据整理成可直接服务论文讨论的论点。
- `03 Synthesis/新增文献纳入知识体系流程.md`：写清以后如何增量更新。
- `Canvas/<主题>知识地图.canvas`：可视化展示 MOC、概念、证据矩阵和论点之间的关系。

## 增量纳入规则

处理新增 `01 Papers` 文献时：

1. 读取文献标题、元数据、全文精读、PDF/Zotero 信息。
2. 判断文献的证据角色：支持、反驳、限定、方法学参考或提出新问题。
3. 选 1-3 个最相关概念页，追加一句话证据。
4. 在证据矩阵中新增一行。
5. 更新论文论点页：补充支撑证据、修正表述，或新增论点。
6. 必要时更新 MOC 的证据地图和 Canvas。
7. 校验 wikilink、Canvas JSON、文件路径和 `00 Inbox`/`01 Papers` 分流结果。

## 写作原则

- 文献笔记保留单篇精读，不承担综合综述。
- 概念页写可复用知识，避免复制文献摘要。
- 证据矩阵负责横向比较。
- 论文论点页负责把证据变成可写段落。
- MOC 负责导航，保持轻量。
- 明确区分原文事实、模型结果和自己的推论。

## 详细参考

需要完整中文操作手册时，读取 `references/workflow-zh.md`。