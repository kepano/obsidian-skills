# SmartForestTech Knowledge Vault

This is an Obsidian vault, not a code project. All files are plain markdown.
Always use [[wikilinks]] for internal links — never convert them to standard markdown links.
When you encounter a [[wikilink]], resolve it by searching for the matching .md file.

## Owner
Tim Webster — independent product developer.
Products span land management tech (LandPlan platform) and personal projects.

## Vault Purpose
Central knowledge base for all products Tim is developing. Acts as second brain
feeding Claude Code sessions in separate code repos.

## Folder Structure

raw/          Drop zone for unprocessed source material. Never edit files here.
              Subfolders: articles/, my-notes/, landplan/, directive/, fun-projects/

wiki/         Compiled, cross-linked knowledge. Claude maintains this.
  platforms/
    landplan/ The LandPlan platform (three products — see below)
      roadmap/   Epics, milestones, release plans
      backlog/   Feature ideas, issues, priorities
      help/      End-user documentation and tutorials
  projects/
    directive/    Process documentation app (React/Vite/TS + Node/Express)
    capo/         CAPO whitepaper and concept development
    midi-looper/  Raspberry Pi MIDI looper (Python/Kivy)
    tinkergis/    TinkerGIS desktop app (Tauri/Rust/Leaflet)
    home-assistant/ Home Assistant / Raspberry Pi configs
  concepts/     Shared ideas, patterns, architectural decisions
  entities/     Tools, APIs, services, people
  meta/
    index.md    Master page index — always update after ingest
    log.md      Ingest and change history — always append, never overwrite
    hot.md      Recent context cache — update at end of every session

## LandPlan Platform
Three products sharing GIS/land/forestry domain. Code lives at:
/Users/timwebster/Documents/code/landplan/landplan
Document each product under wiki/platforms/landplan/ with its own subfolder once product names are defined.

## Conventions
- Frontmatter on every wiki page: title, tags, created, updated, status
- Status values: seedling | growing | evergreen | archived
- Tags use kebab-case: #land-management #raspberry-pi #react
- Roadmap items frontmatter: status (idea/planned/in-progress/done), priority (1-3), epic
- Help files: second-person ("you"), step-by-step, link to related concepts
- Never write to raw/ — only read from it during ingest

## Reading Order for New Sessions
1. Read wiki/meta/hot.md first (~500 tokens of recent context)
2. If more context needed, read wiki/meta/index.md
3. Then drill into the relevant product subfolder
4. Only read specific wiki pages when directly relevant

## Anti-Patterns
- Do NOT treat this as a code project
- Do NOT convert [[wikilinks]] to [text](url) format
- Do NOT empty log.md or index.md — always append
- Do NOT read the entire vault on every session
