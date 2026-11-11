---
name: ob-cli
description: Use the `ob` command line tool to work with Obsidian services for local vaults, especially Obsidian Sync and Obsidian Publish. Use when the user wants to log into Obsidian from the terminal, inspect or configure remote sync/publish targets, sync a vault headlessly, publish vault changes, or automate these service workflows without opening the Obsidian app UI.
---

# Obsidian `ob` CLI

Use `ob` for headless access to Obsidian services tied to a local vault path.

`ob` is especially useful when the Obsidian desktop app is not running or is not available at all, such as on a VPS, CI runner, remote server, or other headless environment.

## Install and docs

Install `ob` with:

```bash
npm install -g obsidian-headless
```

If installation details need verification or the user hits platform-specific issues, use the official headless documentation:

- https://obsidian.md/help/headless

Do not guess alternate package names or unofficial install methods.

Use this skill when the task is about:

- Logging into an Obsidian account from the terminal
- Connecting a local vault to Obsidian Sync or Obsidian Publish
- Running or checking sync for a vault
- Publishing vault changes from the command line
- Inspecting or changing sync/publish configuration for a vault

Do not use this skill for note editing, search, task management, or plugin/theme debugging inside the app. Use the `obsidian` CLI skill for those workflows when the desktop app is running.

If the desktop app is unavailable, manipulate the vault files directly with standard agent or Unix tools and the `obsidian-markdown` skill as needed. Treat `ob` as the service-side tool for Sync and Publish, not as the primary editor for note contents.

## Quick check

Start with:

```bash
ob --help
```

If the user needs the exact flags for a subcommand, prefer `ob <command> --help` over memory.

## Path model

Most `ob` commands target a local vault by filesystem path:

```bash
ob sync --path "/path/to/vault"
ob publish --path "/path/to/vault"
```

If `--path` is omitted, `ob` uses the current directory. Set the shell `workdir` to the vault root when possible.

## Core workflows

### Account login

Check login status or authenticate:

```bash
ob login
ob login --email "user@example.com"
```

Use `--password` and `--mfa` only when the task explicitly requires non-interactive auth handling.

### Sync setup

List available vaults first if needed:

```bash
ob sync-list-remote
ob sync-list-local
```

Connect a local vault to Sync:

```bash
ob sync-setup --vault "Vault Name or ID" --path "/path/to/vault"
```

Important setup/config options:

- `--password` for the end-to-end encryption password
- `--device-name` to label this client in sync history
- `--config-dir` when the vault uses a nonstandard config folder instead of `.obsidian`

### Run sync

One-shot sync:

```bash
ob sync --path "/path/to/vault"
```

Continuous sync:

```bash
ob sync --path "/path/to/vault" --continuous
```

Check state first when diagnosing:

```bash
ob sync-status --path "/path/to/vault"
```

### Sync configuration

Use `sync-config` when the user wants to change how sync behaves for a vault:

```bash
ob sync-config --path "/path/to/vault" --mode pull-only
ob sync-config --path "/path/to/vault" --excluded-folders "Templates,Attachments/tmp"
```

Notable flags:

- `--conflict-strategy merge|conflict`
- `--mode bidirectional|pull-only|mirror-remote`
- `--excluded-folders`
- `--file-types image,audio,video,pdf,unsupported`
- `--configs` for Obsidian config categories to sync
- `--device-name`
- `--config-dir`

Use extra care with `mirror-remote`, which reverts local changes to match the remote state.

### Publish setup

List sites:

```bash
ob publish-list-sites
```

Connect a vault to a Publish site:

```bash
ob publish-setup --site "site-slug-or-id" --path "/path/to/vault"
```

### Publish changes

Preview before changing anything:

```bash
ob publish --path "/path/to/vault" --dry-run
```

Publish without confirmation only when the task is explicitly automated or unattended:

```bash
ob publish --path "/path/to/vault" --yes
```

Include files without a publish flag only when the user asks for a broad publish:

```bash
ob publish --path "/path/to/vault" --all
```

### Publish configuration

Configure include/exclude folders:

```bash
ob publish-config --path "/path/to/vault" --includes "Notes,Docs"
ob publish-config --path "/path/to/vault" --excludes "Private,Drafts"
```

Adjust site options:

```bash
ob publish-site-options --path "/path/to/vault" --site-name "My Site"
```

Common `publish-site-options` flags:

- `--index-file`
- `--logo`
- `--show-navigation`
- `--show-search`
- `--show-backlinks`
- `--show-outline`
- `--show-hover-preview`
- `--show-theme-toggle`
- `--default-theme light|dark`
- `--nav-order`
- `--nav-hidden`

## Decision guide

Use `ob` when the task is service-oriented and path-based:

- "Set this vault up with Obsidian Sync"
- "Run sync for this vault"
- "Publish these vault changes"
- "Configure which folders Publish includes"
- "Check whether this machine is linked to the right remote vault"

Use the `obsidian` CLI instead when the task is app-oriented:

- Read or edit note contents
- Search notes, backlinks, tags, tasks, or properties
- Create daily notes
- Reload plugins or inspect the Obsidian UI

Use direct filesystem tools plus `obsidian-markdown` when the task is content-oriented but the desktop app is not available:

- Editing notes on a VPS or remote shell
- Creating or reorganizing vault files in CI or automation
- Bulk-fixing Markdown, wikilinks, frontmatter, or embeds without a running app
- Preparing vault content locally before running `ob sync` or `ob publish`

## Safety and verification

- Prefer `--dry-run` for publish previews when available.
- Prefer status/list commands before mutating setup in an already-configured vault.
- When a vault path is ambiguous, inspect the filesystem first instead of guessing.
- When a command could change remote state, confirm the target path/site/vault name from command output before proceeding.

## Reference

- Headless Obsidian docs: https://obsidian.md/help/headless
