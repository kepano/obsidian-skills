# Import Notebook Workflow

Import all sources from a NotebookLM notebook into the vault as linked `notebook-source` files with AI-generated guides, plus a dashboard.

## Inputs

- **notebook-id**: from `notebooklm list`
- **notebook-slug**: short kebab-case name (e.g. `lennys-podcast`)
- **dashboard-title**: human-readable title (e.g. `Lenny's Podcast Research`)

If user doesn't specify, derive from `notebooklm status` output.

## Step 1: Verify Auth

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm status
```

If auth error, run [workflows/auth.md](auth.md) first.

## Step 2: Set Notebook Context

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm use {notebook-id}
```

## Step 3: Export Source List

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm source list --json > /tmp/notebooklm-sources.json
```

Inspect the JSON. Key fields per source: `id`, `title`, `type`, `url`, `created_at`.

**FORMAT NOTE:** `nlm source list --json` returns a flat array `[{id, title, type, url}]`. The `import_sources.py` script expects a wrapper `{notebook_id: "...", sources: [...]}` with `type` as `SourceType.YOUTUBE` etc. If using `nlm` output, wrap it first:

```python
import json
sources = json.load(open("/tmp/notebooklm-sources.json"))
TYPE_MAP = {"youtube": "SourceType.YOUTUBE", "web": "SourceType.WEB_PAGE", "pdf": "SourceType.PDF"}
wrapped = {"notebook_id": "{notebook-id}", "sources": [{
    **s, "type": TYPE_MAP.get(s.get("type",""), f"SourceType.{s.get('type','WEB_PAGE').upper()}"),
    "created_at": s.get("created_at", "")
} for s in sources]}
json.dump(wrapped, open("/tmp/notebooklm-sources-wrapped.json", "w"))
```

## Step 4: Create Folder Structure

```bash
mkdir -p "Notes/NotebookLM/{notebook-slug}/Sources"
mkdir -p "Notes/NotebookLM/{notebook-slug}/QA"
```

## Step 5: Create Source Files

```bash
python3 .claude/skills/notebooklm/scripts/import_sources.py \
  --sources /tmp/notebooklm-sources.json \
  --slug {notebook-slug} \
  --dashboard "{dashboard-title}"
```

Add `--skip-guides` to skip AI source guide fetching (faster, can add later).

This creates one `.md` file per source with proper frontmatter and `related` linking to dashboard.

## Step 6: Create Dashboard

Create `Notes/Dashboards/{dashboard-title}.md` using the dashboard template from `Templates/Types/dashboard.md`.

Add these Dataview queries:

```markdown
## Sources

\```dataview
TABLE source_type AS "Type", url AS "URL", date AS "Added"
FROM "Notes/NotebookLM/{notebook-slug}/Sources"
WHERE type = "notebook-source"
SORT date DESC
\```

## Q&A Log

\```dataview
TABLE date AS "Date", source AS "Source"
FROM "Notes/NotebookLM/{notebook-slug}/QA"
WHERE type = "reference"
SORT date DESC
\```
```

## Step 7: Verify

```bash
ls "Notes/NotebookLM/{notebook-slug}/Sources/" | wc -l
obsidian open path="Notes/Dashboards/{dashboard-title}.md" newtab
```

## Output

- Source files in `Notes/NotebookLM/{notebook-slug}/Sources/`
- Dashboard at `Notes/Dashboards/{dashboard-title}.md`
- Empty `QA/` folder ready for ask workflow
