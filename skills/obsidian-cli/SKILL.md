---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## Prerequisites

The `obsidian` binary ships with the **installer**, not with the auto-updated asar bundle. If `which obsidian` returns nothing, the user is most likely missing one of these:

1. **Installer is too old.** Obsidian on macOS has two version numbers: the asar bundle (shown in Settings → About) auto-updates, but the installer at `/Applications/Obsidian.app` does **not**. The in-app "check for updates" only covers the asar — it can report "you are on the latest version" while the installer is multiple versions behind. CLI binary requires installer ≥ 1.10. Check via:

   ```bash
   defaults read /Applications/Obsidian.app/Contents/Info.plist CFBundleShortVersionString
   ```

   If old, download the latest from <https://obsidian.md/download> and reinstall (vault data is unaffected).

2. **CLI not enabled.** Settings → General → Advanced → toggle "Enable command line interface" ON. This installs the shim to `/usr/local/bin/`.

3. **PATH not refreshed.** Open a new terminal after enabling.

### Health check

```bash
which obsidian \
  && obsidian vault \
  && obsidian dev:screenshot path=/tmp/obs.png
```

If all three succeed, the CLI is ready.

### Fallback when CLI is unavailable

When the CLI cannot be installed (older Obsidian, restricted host, etc.), most vault operations are still doable via direct file access:

- Read / edit notes: read or edit the `.md` file directly
- Toggle core plugins: edit `.obsidian/core-plugins.json` and ask the user to reload (`Cmd+P → Reload app without saving`)
- Open a file: `open "obsidian://open?vault=<name>&file=<url-encoded-path>"`

Note: direct file edits won't trigger Obsidian's index refresh until the vault reloads.

## Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" silent overwrite
```

For multiline content use `\n` for newline and `\t` for tab.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path or extension needed)
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Commands target the most recently focused vault by default. Use `vault=<name>` as the first parameter to target a specific vault:

```bash
obsidian vault="My Vault" search query="test"
```

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Plugin development

### Develop/test cycle

After making code changes to a plugin or theme, follow this workflow:

1. **Reload** the plugin to pick up changes:
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **Check for errors** — if errors appear, fix and repeat from step 1:
   ```bash
   obsidian dev:errors
   ```
3. **Verify visually** with a screenshot or DOM inspection:
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

### Additional developer commands

Run JavaScript in the app context:

```bash
obsidian eval code="app.vault.getFiles().length"
```

Inspect CSS values:

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

Toggle mobile emulation:

```bash
obsidian dev:mobile on
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
