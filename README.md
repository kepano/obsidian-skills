Agent Skills for use with Obsidian.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code and Codex CLI.

## Installation

### Marketplace

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### npx skills

```
npx skills add git@github.com:kepano/obsidian-skills.git
```

### Manually

#### Claude Code

Add the contents of this repo to a `/.claude` folder in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex CLI

**Option 1 — Tell Codex to install (recommended):**

```
Fetch and follow instructions from https://raw.githubusercontent.com/kepano/obsidian-skills/main/.codex/INSTALL.md
```

**Option 2 — One-line script install:**

macOS / Linux:

```bash
tmp_dir="$(mktemp -d)" && git clone --depth 1 https://github.com/kepano/obsidian-skills.git "$tmp_dir/obsidian-skills" && "$tmp_dir/obsidian-skills/scripts/install-skills-codex.sh" && rm -rf "$tmp_dir"
```

Windows (PowerShell):

```powershell
$tmp_dir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid()); New-Item -ItemType Directory -Path $tmp_dir | Out-Null; git clone --depth 1 https://github.com/kepano/obsidian-skills.git "$tmp_dir\obsidian-skills"; & "$tmp_dir\obsidian-skills\scripts\install-skills-codex.ps1"; Remove-Item -Recurse -Force $tmp_dir
```

**Option 3 — From the repo root:**

macOS / Linux:

```bash
./scripts/install-skills-codex.sh
```

Windows (PowerShell):

```powershell
.\scripts\install-skills-codex.ps1
```

This installs all skills into `~/.agents/skills/obsidian-skills/`. Restart Codex to discover them. See [`.codex/INSTALL.md`](.codex/INSTALL.md) for options including `--dry-run` and custom target directories.

#### OpenCode

Clone the entire repo into the OpenCode skills directory (`~/.opencode/skills/`):

```sh
git clone https://github.com/kepano/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

Do not copy only the inner `skills/` folder — clone the full repo so the directory structure is `~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md`.

OpenCode auto-discovers all `SKILL.md` files under `~/.opencode/skills/`. No changes to `opencode.json` or any config file are needed. Skills become available after restarting OpenCode.

## Skills

| Skill | Description |
|-------|-------------|
| [obsidian-markdown](skills/obsidian-markdown) | Create and edit [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown) (`.md`) with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax |
| [obsidian-bases](skills/obsidian-bases) | Create and edit [Obsidian Bases](https://help.obsidian.md/bases/syntax) (`.base`) with views, filters, formulas, and summaries |
| [json-canvas](skills/json-canvas) | Create and edit [JSON Canvas](https://jsoncanvas.org/) files (`.canvas`) with nodes, edges, groups, and connections |
| [obsidian-cli](skills/obsidian-cli) | Interact with Obsidian vaults via the [Obsidian CLI](https://help.obsidian.md/cli) including plugin and theme development |
| [defuddle](skills/defuddle) | Extract clean markdown from web pages using [Defuddle](https://github.com/kepano/defuddle-cli), removing clutter to save tokens |
