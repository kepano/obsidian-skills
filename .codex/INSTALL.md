# Installing obsidian-skills for Codex

This guide explains how to install obsidian-skills using Codex native skill discovery.

## Quick Install (One-line)

Run this from anywhere — no need to clone the repo first:

```bash
tmp_dir="$(mktemp -d)" && git clone --depth 1 https://github.com/Vinluo/obsidian-skills.git "$tmp_dir/obsidian-skills" && "$tmp_dir/obsidian-skills/scripts/install-skills-codex.sh" && rm -rf "$tmp_dir"
```

## Install from Repo Root

If you have already cloned the repo:

```bash
./scripts/install-skills-codex.sh
```

## What This Does

- Syncs all skills from `skills/` into `~/.agents/skills/obsidian-skills/`
- Skills are discovered automatically by Codex at next startup

## Verify

```bash
ls -la ~/.agents/skills/obsidian-skills
```

Expected directories (one per skill):

- `defuddle`
- `json-canvas`
- `obsidian-bases`
- `obsidian-cli`
- `obsidian-markdown`

## Options

```bash
# Preview without writing
./scripts/install-skills-codex.sh --dry-run

# Custom skills directory
./scripts/install-skills-codex.sh --skills-dir /custom/path/skills/obsidian-skills
```

## Update

Re-run the install script to sync the latest skills:

```bash
./scripts/install-skills-codex.sh
```

Or use the one-line command above to fetch and install the latest version.

## Uninstall

```bash
rm -rf ~/.agents/skills/obsidian-skills
```
