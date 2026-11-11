# Obsidian

Skills for working with Obsidian vaults: Obsidian Markdown, Bases, Canvas, the Obsidian CLI, Obsidian Headless, web pages, and templates.

## Install

In Claude Code:

```
/plugin install obsidian --marketplace obsidianmd/obsidian-skills
```

In Codex, run `codex plugin marketplace add obsidianmd/obsidian-skills`, then install Obsidian from the plugin directory.

In Cursor, install Obsidian from the [Cursor Marketplace](https://cursor.com/marketplace).

## Requirements

The CLI skill runs the `obsidian` command, which needs the Obsidian desktop app installed, running, and with the CLI turned on. See https://help.obsidian.md/cli for setup. It needs a host that can run local commands, such as Claude Code, Codex, Cursor, or a desktop app session on your computer.

The Markdown, Bases, and Canvas skills only describe file formats, so they also work in chat.

Web extraction uses [Defuddle](https://github.com/kepano/defuddle), which fetches the page you ask for. Template rendering uses [Knap](https://github.com/obsidianmd/knap), which needs Node.js 20 or later. Sync and Publish use [Obsidian Headless](https://help.obsidian.md/headless), which needs Node.js 22 or later and a Sync or Publish subscription, and runs without the desktop app. None of these tools is bundled. When one is missing, the skill asks before installing it from npm.

## Included skills

- obsidian-cli: search, read, create, and manage notes through the running app.
- obsidian-headless: sync and publish vaults from the command line without the app.
- obsidian-markdown: Obsidian links, properties, callouts, and embeds.
- obsidian-bases: Bases files, views, filters, formulas, and summaries.
- json-canvas: Canvas files with nodes, edges, groups, and connections.
- defuddle: extract readable Markdown from public web pages.
- knap: render templates from structured data.

## Scope

This plugin contains skills only, with no MCP server, hooks, or background processes. Using it can bring vault content you ask about into the conversation, and that content is processed by the AI model you use, not only on your computer.

Source: https://github.com/obsidianmd/obsidian-skills
