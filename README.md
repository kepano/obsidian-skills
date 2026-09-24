Agent Skills for use with Obsidian.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code, Codex, and Open Code.

## Installation

### Claude Code marketplace

From terminal:

```sh
claude plugin marketplace add kepano/obsidian-skills
claude plugin install obsidian@obsidian-skills
```

From within a Claude Code session:

```sh
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### Codex marketplace

```sh
codex plugin marketplace add kepano/obsidian-skills
codex plugin add obsidian@obsidian-skills
```

### npx skills

```sh
npx skills add git@github.com:kepano/obsidian-skills.git
```

Instead of ssh, if you prefer to use https:

```sh
npx skills add https://github.com/kepano/obsidian-skills
```

### Manually

#### Claude Code

Add the contents of this repo to a `/.claude` folder in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex

Copy the `plugins/obsidian/skills/` directory into your Codex skills path (typically `~/.agents/skills`). See the [Agent Skills specification](https://agentskills.io/specification) for the standard skill format.

#### OpenCode

Clone the entire repo into the OpenCode skills directory (`~/.opencode/skills/`):

```sh
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

Do not copy only the inner `skills/` folder — clone the full repo so the directory structure is `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`.

OpenCode auto-discovers all `SKILL.md` files under `~/.opencode/skills/`. No changes to `opencode.json` or any config file are needed. Skills become available after restarting OpenCode.

## Release maintenance

Update the plugin version across Claude and Codex metadata with:

```sh
./scripts/bump-version.sh patch
```

The script also accepts `major`, `minor`, or an explicit version like `1.1.0`.

## Skills

| Skill                                                          | Description                                                                                                                                                                                |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [obsidian-markdown](plugins/obsidian/skills/obsidian-markdown) | Create and edit [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown) (`.md`) with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax |
| [obsidian-bases](plugins/obsidian/skills/obsidian-bases)       | Create and edit [Obsidian Bases](https://help.obsidian.md/bases/syntax) (`.base`) with views, filters, formulas, and summaries                                                             |
| [json-canvas](plugins/obsidian/skills/json-canvas)             | Create and edit [JSON Canvas](https://jsoncanvas.org/) files (`.canvas`) with nodes, edges, groups, and connections                                                                        |
| [obsidian-cli](plugins/obsidian/skills/obsidian-cli)           | Interact with Obsidian vaults via the [Obsidian CLI](https://help.obsidian.md/cli) including plugin and theme development                                                                  |
| [defuddle](plugins/obsidian/skills/defuddle)                   | Extract clean markdown from web pages using [Defuddle](https://github.com/kepano/defuddle), removing clutter to save tokens                                                                |
| [knap](plugins/obsidian/skills/knap)                           | Render Markdown templates from JSON or CSV data using [Knap](https://github.com/obsidianmd/knap), including batch file generation                                                          |
