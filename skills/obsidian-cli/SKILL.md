---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

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

### Notes

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian prepend file="My Note" content="Header line"
obsidian delete file="My Note"
obsidian open file="My Note"
obsidian move path="old/note.md" file="new/note.md"
obsidian rename file="Old Name" name="New Name"
```

### Search

```bash
obsidian search query="search term" limit=10
obsidian search:context query="search term" limit=10
obsidian search:open query="search term"
```

### Daily notes

```bash
obsidian daily
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian daily:prepend content="# Morning thoughts"
obsidian daily:path
```

### Properties

```bash
obsidian property:set name="status" value="done" file="My Note"
obsidian property:read name="status" file="My Note"
obsidian property:remove name="status" file="My Note"
obsidian properties sort=count counts
```

### Tasks

```bash
obsidian tasks daily todo
obsidian task file="My Note" line=5 toggle
```

### Tags and links

```bash
obsidian tags sort=count counts
obsidian tag name="my-tag"
obsidian backlinks file="My Note"
obsidian links file="My Note"
obsidian orphans
obsidian deadends
obsidian unresolved
```

### Files and folders

```bash
obsidian files
obsidian folders
obsidian file file="My Note"
obsidian folder path="My Folder"
obsidian recents
obsidian random
obsidian random:read
obsidian wordcount file="My Note"
```

### Templates

```bash
obsidian templates
obsidian template:read name="My Template"
obsidian template:insert name="My Template"
```

### Bookmarks

```bash
obsidian bookmarks
obsidian bookmark file="My Note" title="Important"
```

### Commands

```bash
obsidian commands
obsidian command id="workspace:close"
obsidian hotkeys
obsidian hotkey id="workspace:close"
```

### Workspace

```bash
obsidian workspace
obsidian tabs
obsidian tab:open
obsidian outline
obsidian reload
obsidian restart
```

### Vault

```bash
obsidian vault
obsidian vaults
obsidian version
```

Use `--copy` on any command to copy output to clipboard. Use `silent` to prevent files from opening. Use `total` on list commands to get a count.

## Bases (databases)

```bash
obsidian bases
obsidian base:query file="My Base" view="All"
obsidian base:create file="My Base" view="All" name="New Item"
obsidian base:views file="My Base"
```

## Plugins and themes

```bash
obsidian plugins
obsidian plugins:enabled
obsidian plugin id="dataview"
obsidian plugin:enable id="dataview"
obsidian plugin:disable id="dataview"
obsidian plugin:install id="dataview"
obsidian plugin:uninstall id="dataview"
obsidian plugins:restrict
obsidian themes
obsidian theme
obsidian theme:set name="Minimal"
obsidian theme:install name="Minimal"
obsidian theme:uninstall name="Minimal"
obsidian snippets
obsidian snippets:enabled
obsidian snippet:enable name="custom"
obsidian snippet:disable name="custom"
```

## Sync

```bash
obsidian sync:status
obsidian sync
obsidian sync:history path="note.md"
obsidian sync:read path="note.md" version=3
obsidian sync:restore path="note.md" version=3
obsidian sync:deleted
obsidian sync:open
obsidian diff path="note.md"
```

## History (file recovery)

```bash
obsidian history:list
obsidian history path="note.md"
obsidian history:read path="note.md" version=3
obsidian history:restore path="note.md" version=3
obsidian history:open
```

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

Debug with Chrome DevTools Protocol:

```bash
obsidian dev:debug
obsidian dev:cdp method="Runtime.evaluate" params='{"expression": "app.vault.getName()"}'
```

Run `obsidian help` to see additional developer commands including CDP and debugger controls.
