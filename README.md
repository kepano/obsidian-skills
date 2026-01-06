Claude Skills for use with Obsidian.

## Installation

### Vault-scoped (recommended for shared vaults)

Copy the `skills/` folder to `.claude/skills/` in the root of your Obsidian vault (or whichever folder you're using with Claude Code). See more in the [official Claude Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

### User-scoped (via plugin)

Install as a Claude Code plugin to make skills available across all your vaults:

```bash
claude marketplace add kepano/obsidian-skills
claude plugin install obsidian-skills
```

## Skills

### Create and edit Obsidian-compatible plain text files

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown) `.md`
- [Obsidian Bases](https://help.obsidian.md/bases/syntax) `.base`
- [JSON Canvas](https://jsoncanvas.org/) `.canvas`
