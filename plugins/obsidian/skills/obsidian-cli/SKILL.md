---
name: obsidian-cli
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## Before using the CLI

Run `obsidian help` to check availability. If the command is missing, explain how to turn on the CLI using https://help.obsidian.md/cli. The `obsidian` command ships with the Obsidian installer; don't install the unrelated npm package `obsidian-cli`. If it can't find Obsidian, ask the user to open the desktop app, then retry. In a sandboxed shell the same message can mean the sandbox blocked the CLI's local socket.

The CLI exits with status 0 even when a command fails, so read its output before reporting that a command succeeded.

Quote parameters for the current shell, and pass note text as literal argument data, never as executable shell syntax.

## Command reference

Run `obsidian help` to see all available commands. This is always up to date. Full docs: https://help.obsidian.md/cli

## Syntax

**Parameters** take a value with `=`. Quote values with spaces:

```bash
obsidian create name="My Note" content="Hello world"
```

**Flags** are boolean switches with no value:

```bash
obsidian create name="My Note" open overwrite
```

Use `overwrite` only when replacing an existing file is intended.

Opening is opt-in: pass `open` to open the file, and add `newtab` to open it in a new tab. There is no `silent` flag.

In `content=`, `\n` becomes a newline and `\t` a tab. Every `\n` and `\t` is converted and there's no escape, so text such as the LaTeX `\theta` or the path `C:\notes` is corrupted. Write content that contains backslashes, or is longer than about 4 KB, directly to the note's file instead.

A dot in a file name is read as the start of an extension. When a name contains a dot, include the extension: `create name="Meeting 2026.11.06.md"`, `rename name="v1.2 notes.md"`, `move to="Archive 2026.10/Note.md"`.

## File targeting

Many commands accept `file` or `path` to target a file. Without either, the active file is used.

- `file=<name>` — resolves like a wikilink (name only, no path needed). `.md` is optional; other file types need their extension, e.g. `file="Projects.base"`. Aliases don't resolve.
- `path=<path>` — exact path from vault root, e.g. `folder/note.md`

## Vault targeting

Without `vault=`, commands target the vault that contains the current directory, then the most recently focused vault. `vault=<name>` only works as the first parameter; anywhere else it's ignored:

```bash
obsidian vault="My Vault" search query="test"
```

Use `vault=` when the user has selected a vault. If the target is unclear and the user has several vaults, ask which one before changing files.

## Common patterns

```bash
obsidian read file="My Note"
obsidian create name="New Note" template="Template"   # a template replaces content=
obsidian create name="New Note" content="# Hello" open  # also open in Obsidian
obsidian append file="My Note" content="New line"
obsidian rename path="folder/note.md" name="New name"
obsidian move path="folder/note.md" to="archive/"
obsidian delete path="folder/note.md"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

Use `rename` and `move`, not filesystem `mv` or `obsidian eval`, so Obsidian can update links to the file. If other notes link to it and Settings → Files and links → Automatically update internal links is off, Obsidian asks in a dialog and the command waits until someone answers. `delete` moves the file to the trash; don't pass `permanent` unless the user asks for it. Prefer `create` and `append` over `eval` for writing note bodies.

Use `total` on list commands to get a count.

**Output options placement:** `--copy`, `--json`, `--md`, `--tsv`, and `--csv` only work **after** the command name. Putting them before the command (or before `vault=`) fails — often as `Command "--copy" not found` — because the first token is treated as the command. Prefer `vault=` first when used; put double-dash options last:

```bash
obsidian tasks todo total --copy
obsidian vault="My Vault" search query="TODO" --copy
obsidian tasks todo format=json   # many list commands also accept format=
# Wrong: obsidian --copy vault="My Vault" tasks todo
```

## Plugin development

### Develop/test cycle

Turn on console capture once with `obsidian dev:debug on`, so messages from the reload are kept. After making code changes to a plugin or theme, follow this workflow:

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
   obsidian dev:screenshot
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **Check console output** for warnings or unexpected logs:
   ```bash
   obsidian dev:console level=error
   ```

`dev:screenshot` saves to a temporary file and prints its path. A relative `path=` saves inside the vault.

### Additional developer commands

Run JavaScript in the app context (prefer dedicated commands like `rename`, `move`, `create`, and `append` for vault mutations):

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
