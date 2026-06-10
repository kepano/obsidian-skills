# Obsidian Skills

用于 Obsidian vault 的 Agent Skills 集合，支持 Markdown、Bases、Canvas、文献初筛和文献知识提炼等工作流。

这些 skills 遵循 [Agent Skills specification](https://agentskills.io/specification)，可被 Claude Code、Codex、OpenCode 等兼容 Agent Skills 的工具使用。

> 注意：`nature-academic-search` 和 `nature-reader` 属于 nature skills 包，不属于本 Obsidian skills 包；本文只把它们列为“建议配合使用”的外部能力。

## 安装

### Marketplace

```text
/plugin marketplace add fx949494fx/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### npx skills

```text
npx skills add git@github.com:fx949494fx/obsidian-skills.git
```

如果更偏好 HTTPS：

```text
npx skills add https://github.com/fx949494fx/obsidian-skills
```

### 手动安装

#### Claude Code

将本仓库内容加入 Obsidian vault 根目录下的 `/.claude` 文件夹，或放入你为 Claude Code 配置的工作目录。更多说明见 [Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)。

#### Codex

将 `skills/` 目录复制到 Codex skills 路径，通常是 `~/.codex/skills`。

#### OpenCode

将整个仓库 clone 到 OpenCode skills 目录：

```sh
git clone https://github.com/fx949494fx/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

不要只复制内部的 `skills/` 文件夹；OpenCode 需要保留完整结构：

```text
~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md
```

重启 OpenCode 后会自动发现 skills。

## Skills

| Skill | 作用 |
|---|---|
| [obsidian-markdown](skills/obsidian-markdown) | 创建和编辑 [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)，包括 wikilinks、embeds、callouts、properties 等 Obsidian 扩展语法 |
| [obsidian-bases](skills/obsidian-bases) | 创建和编辑 [Obsidian Bases](https://help.obsidian.md/bases/syntax) (`.base`)，包括 views、filters、formulas 和 summaries |
| [json-canvas](skills/json-canvas) | 创建和编辑 [JSON Canvas](https://jsoncanvas.org/) (`.canvas`)，包括 nodes、edges、groups 和 connections |
| [obsidian-cli](skills/obsidian-cli) | 通过 [Obsidian CLI](https://help.obsidian.md/cli) 与 Obsidian vault 交互，包括插件和主题开发 |
| [defuddle](skills/defuddle) | 使用 [Defuddle](https://github.com/kepano/defuddle) 从网页中提取干净 Markdown，去除导航和页面噪声以节省上下文 |
| [obsidian-abstract-reader](skills/obsidian-abstract-reader) | 读取、评分和批量筛选 PubMed 摘要，生成带关键词回链的 Obsidian 文献初筛笔记 |
| [obsidian-literature-synthesis](skills/obsidian-literature-synthesis) | 将 `01 Papers` 中的精读文献提炼成 MOC、概念页、证据矩阵、Canvas 知识地图和论文讨论论点 |

## 文献从初筛到知识提炼的推荐流程

```text
检索/导入题录
  -> 摘要初筛
  -> decision 分流
  -> PDF/全文获取与 Zotero 管理
  -> 全文精读并进入 01 Papers
  -> 概念页/MOC/证据矩阵/论文论点
  -> Canvas/Bases 可视化与持续维护
```

### 推荐目录

```text
00 Inbox/              初筛后待处理文献，或暂缺全文文献
01 Papers/             已精读并纳入知识体系的文献
02 Concepts/           从文献中提炼出的概念页
03 Synthesis/          MOC、证据矩阵、论文论点、流程页
Attachments/PDFs/      PDF 附件
Bases/                 Obsidian Bases 视图
Canvas/                Obsidian Canvas 图谱
Other/                 非 Include 文献
```

### 阶段 1：摘要初筛

使用 [obsidian-abstract-reader](skills/obsidian-abstract-reader) 读取 PubMed ID、DOI、PubMed URL、题录或摘要文本，生成带 `decision` 和 `screening_score` 的 Obsidian 初筛笔记。

建议状态字段：

```yaml
decision: Include | Exclude | Maybe | Need Full Text
status: to-read | reading | read | synthesized
screening_score: 0-100
```

### 阶段 2：分流与全文获取

- `decision: Include`：进入 PDF 或全文获取。
- `decision: Need Full Text`：暂留 `00 Inbox`，等待 PDF 或可读全文。
- 非 Include：移入 `Other`。

可配合 Zotero 管理题录和 PDF 附件。去重时优先保留有附件的条目。

### 阶段 3：全文精读

有 PDF 或可读全文后，在文献笔记中追加统一的全文精读小节：

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

完成后将 `status` 改为 `read`，并把笔记移入 `01 Papers`。

### 阶段 4：知识体系提炼

使用 [obsidian-literature-synthesis](skills/obsidian-literature-synthesis) 将 `01 Papers` 中的精读笔记进一步提炼为：

- `03 Synthesis/<主题> MOC.md`：主题地图和研究问题框架。
- `02 Concepts/<概念>.md`：可复用概念页。
- `03 Synthesis/筛查策略经济学证据矩阵.md`：横向比较文献证据。
- `03 Synthesis/论文讨论可用论点.md`：把证据转化为论文讨论素材。
- `Canvas/<主题>知识地图.canvas`：可视化知识结构。

### 阶段 5：增量维护

每次新增文献进入 `01 Papers` 后：

1. 判断新文献支持、反驳、限定或补充哪些已有论点。
2. 选择 1-3 个概念页追加一句话证据。
3. 在证据矩阵中新增一行。
4. 必要时更新 MOC、论文论点页和 Canvas。
5. 校验 wikilink、Canvas 文件节点和目录分流结果。

## 建议配合使用的外部 Nature Skills

这些 skills 不属于本 Obsidian skills 包，只在需要时作为外部工具配合使用：

| 外部 skill | 建议用途 | 如何进入 Obsidian 流程 |
|---|---|---|
| `nature-academic-search` | 文献检索、PubMed/CrossRef/arXiv、RIS/BibTeX、题录管理 | 将检索结果、PMID/DOI 或 RIS/BibTeX 交给初筛与 Zotero 导入环节 |
| `nature-reader` | 从 PDF、DOI、publisher HTML 或粘贴全文生成结构化精读 | 将精读结果写入 `01 Papers` 的 `## 全文精读` 小节 |

## 常用请求

```text
请对这些 PubMed 文献做摘要初筛，并在 Obsidian 中生成初筛笔记。
```

```text
请对 decision 为 Include 的文献下载/导入 PDF 到 Zotero，精读后移动到 01 Papers。
```

```text
请把 01 Papers 中新增文献纳入知识体系，更新 MOC、概念页、证据矩阵和论文论点。
```

```text
请检查当前知识体系是否有断链、遗漏文献或需要新增概念页的地方。
```
