# Ask Notebook Workflow

Ask a NotebookLM notebook a question and save the answer as a vault reference note with `[N]` citations linked to source files.

## Inputs

- **question**: The question to ask
- **title**: Short title for the Q&A note
- **notebook-slug**: Which notebook folder to use
- **notebook-id**: Full UUID of the notebook (from `nlm notebook list`)
- **dashboard-title** (optional): Dashboard to link to via `related`

## Step 1: Verify Auth

```bash
nlm auth status
```

If auth error, run `nlm auth login` (browser flow).

## Step 2: Get Sources

```bash
nlm source list {notebook-id} --json > /tmp/nlm-sources.json
```

## Step 3: Ask the Question

**Delegate to a Haiku sub-agent** to keep JSON out of main context:

```
Agent(model="haiku", prompt="""
1. Run: nlm notebook query {notebook-id} "{question}" --json > /tmp/qa-output.json
2. Return: answer length, citation count, sources_used count
""")
```

Or directly:
```bash
nlm notebook query {notebook-id} "{question}" --json > /tmp/qa-output.json
```

## Step 4: Resolve Citations

```bash
cd /path/to/vault && python3 .claude/skills/notebooklm/scripts/resolve_citations.py \
  --qa /tmp/qa-output.json \
  --sources /tmp/nlm-sources.json \
  --slug {notebook-slug} \
  --title "{title}" \
  --notebook "{Notebook Display Name}" \
  --output "Notes/NotebookLM/{notebook-slug}/QA/{date} {title}.md" \
  --vault .
```

The `--notebook` flag sets the `related` wikilink to the notebook index file (e.g. `--notebook "Lennys Podcast"` links to `[[Notes/NotebookLM/Lennys Podcast]]`).

This replaces `[N]` with `[[Source#^anchor|[N]]]` wikilinks. Click opens the source file and jumps to the cited passage.

## Step 5: Verify

```bash
obsidian open path="Notes/NotebookLM/{notebook-slug}/QA/{date} {title}.md" newtab
```

**CRITICAL: Click 2-3 citation links in Obsidian to verify they jump to the correct passage.** The resolver reporting "N anchors injected" does NOT mean they work. Obsidian block references can silently fail if formatting is wrong.

## Cross-Source Citation Handling

NotebookLM's API returns the same `source_id` for all citations in cross-source synthesis answers. The resolver detects this and remaps citations by parsing `*"episode title"*` section markers in the answer text and fuzzy-matching them to source titles. This works automatically. No single-source workaround needed.

## Anchor Placement

Anchors are placed via substring search: the resolver finds the `cited_text` passage in the source file and inserts a `^c-XXXXXXXX` block ID on its own line with blank lines before and after (required by Obsidian for block indexing). Anchor IDs are derived from MD5 hash of the cited_text content, so they're stable across runs.

## Output

- Q&A note at `Notes/NotebookLM/{notebook-slug}/QA/{date} {title}.md`
- Inline `[N]` rendered as clickable `[[Source#^anchor|[N]]]` links to cited passages in source files
- Sources list at bottom
