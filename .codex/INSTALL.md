# Installing obsidian-skills for Codex

This guide explains how to install obsidian-skills using Codex native skill discovery.

## Quick Install (One-line)

Run this from anywhere — no need to clone the repo first:

macOS / Linux:

```bash
tmp_dir="$(mktemp -d)" && git clone --depth 1 https://github.com/Vinluo/obsidian-skills.git "$tmp_dir/obsidian-skills" && "$tmp_dir/obsidian-skills/scripts/install-skills-codex.sh" && rm -rf "$tmp_dir"
```

Windows (PowerShell):

```powershell
$tmp_dir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid()); New-Item -ItemType Directory -Path $tmp_dir | Out-Null; git clone --depth 1 https://github.com/Vinluo/obsidian-skills.git "$tmp_dir\obsidian-skills"; & "$tmp_dir\obsidian-skills\scripts\install-skills-codex.ps1"; Remove-Item -Recurse -Force $tmp_dir
```

## Install from Repo Root

If you have already cloned the repo:

macOS / Linux:

```bash
./scripts/install-skills-codex.sh
```

Windows (PowerShell):

```powershell
.\scripts\install-skills-codex.ps1
```

## What This Does

- Syncs all skills from `skills/` into `~/.agents/skills/obsidian-skills/`
- Skills are discovered automatically by Codex at next startup

## Verify

macOS / Linux:

```bash
ls -la ~/.agents/skills/obsidian-skills
```

Windows (PowerShell):

```powershell
Get-ChildItem "$HOME\.agents\skills\obsidian-skills"
```

Expected directories (one per skill):

- `defuddle`
- `json-canvas`
- `obsidian-bases`
- `obsidian-cli`
- `obsidian-markdown`

## Options

macOS / Linux:

```bash
# Preview without writing
./scripts/install-skills-codex.sh --dry-run

# Custom skills directory
./scripts/install-skills-codex.sh --skills-dir /custom/path/skills/obsidian-skills
```

Windows (PowerShell):

```powershell
# Preview without writing
.\scripts\install-skills-codex.ps1 -DryRun

# Custom skills directory
.\scripts\install-skills-codex.ps1 -SkillsDir C:\custom\path\skills\obsidian-skills
```

## Update

Re-run the install script to sync the latest skills:

macOS / Linux:

```bash
./scripts/install-skills-codex.sh
```

Windows (PowerShell):

```powershell
.\scripts\install-skills-codex.ps1
```

Or use the one-line command above to fetch and install the latest version.

## Uninstall

macOS / Linux:

```bash
rm -rf ~/.agents/skills/obsidian-skills
```

Windows (PowerShell):

```powershell
Remove-Item -Recurse -Force "$HOME\.agents\skills\obsidian-skills"
```
