> **Skills updated August 3, 2026.** This fork was reviewed against all 171 English pages in the official Obsidian Help documentation at commit `1d26fe9d22673ba476c77919800ce514dc0907e0` (July 30, 2026).

# Obsidian Skills

Agent Skills for use with Obsidian.

These skills follow the [Agent Skills specification](https://agentskills.io/specification) so they can be used by any skills-compatible agent, including Claude Code, Codex, and Open Code.

## What changed in this fork

- Added `obsidian-help`, a documentation map covering all 171 reviewed English Obsidian Help pages and routing app-level questions to the right official topic.
- Updated Markdown guidance for configured internal-link styles, Windows-safe vault paths, properties, embeds, and Obsidian 1.13 callout CSS.
- Corrected Bases date arithmetic to use milliseconds, added `random()`, and documented current views, map coordinates, and embedded Base blocks.
- Updated CLI guidance for Obsidian 1.12+, including activation, vault selection precedence, current command groups, and safer command use.
- Aligned Canvas IDs with the JSON Canvas 1.0 specification: IDs must be unique strings; 16-character hexadecimal IDs remain a recommendation, not a requirement.

This repository is a documentation-reviewed fork of [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills).

## Installation

### Marketplace

```
/plugin marketplace add GatienBoquet/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### npx skills

```
npx skills add git@github.com:GatienBoquet/obsidian-skills.git
```

Instead of ssh, if you prefer to use https:

```
npx skills add https://github.com/GatienBoquet/obsidian-skills
```

### Manually

#### Claude Code

Add the contents of this repo to a `/.claude` folder in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

#### Codex

Copy the `skills/` directory into your Codex skills path (typically `~/.codex/skills`). See the [Agent Skills specification](https://agentskills.io/specification) for the standard skill format.

#### OpenCode

Clone the entire repo into the OpenCode skills directory (`~/.opencode/skills/`):

```sh
git clone https://github.com/GatienBoquet/obsidian-skills.git ~/.opencode/skills/obsidian-skills
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
| [obsidian-help](skills/obsidian-help) | Navigate current official Obsidian workflows using a reviewed feature map and a page-by-page coverage inventory |
| [defuddle](skills/defuddle) | Extract clean markdown from web pages using [Defuddle](https://github.com/kepano/defuddle), removing clutter to save tokens |
