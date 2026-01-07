# Obsidian Skills for Claude Code

Claude Code skills for creating and editing Obsidian vault files.

## Skills included

| Skill | Description | File Types |
|-------|-------------|------------|
| [obsidian-markdown](./skills/obsidian-markdown/) | Obsidian Flavored Markdown with wikilinks, embeds, callouts, and properties | `.md` |
| [obsidian-bases](./skills/obsidian-bases/) | Database-like views with filters, formulas, and summaries | `.base` |
| [json-canvas](./skills/json-canvas/) | Infinite canvas with nodes, edges, and groups | `.canvas` |

## Installation

### As a Claude Code Plugin (Recommended)

Run the following commands in a Claude Code session:

```
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

### Manual installation

Clone or copy this repository into your project's `.claude/plugins/` directory:

```bash
# Option 1: Clone into plugins directory
mkdir -p .claude/plugins
git clone https://github.com/kepano/obsidian-skills.git .claude/plugins/obsidian

# Option 2: Add as git submodule
git submodule add https://github.com/kepano/obsidian-skills.git .claude/plugins/obsidian
```

## Usage

Once installed, Claude Code will automatically use these skills when working with Obsidian files. The skills provide:

- **Syntax guidance** for Obsidian-specific features (wikilinks, callouts, embeds)
- **Schema documentation** for `.base` and `.canvas` file formats
- **Best practices** for structuring notes and databases
- **Complete function references** for Bases formulas

## Documentation

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Obsidian Bases](https://help.obsidian.md/bases)
- [JSON Canvas Spec](https://jsoncanvas.org/)
