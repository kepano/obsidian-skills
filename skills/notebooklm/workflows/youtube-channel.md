# YouTube Channel Loader Workflow

Bulk-load all videos from a YouTube channel into a NotebookLM notebook. No external dependencies. Uses InnerTube API for video discovery + notebooklm-py async API for parallel upload.

## Inputs

- **channel_url**: YouTube channel URL (e.g. `https://www.youtube.com/@LennysPodcast`)
- **notebook_name**: Name for the NotebookLM notebook
- **count**: Number of most recent videos to load (default: 200, max: 300 per notebook)

## Step 1: Scrape Channel Videos

```bash
python3 .claude/skills/notebooklm/scripts/load_channel.py scrape \
  --channel "https://www.youtube.com/@ChannelName" \
  --output /tmp/channel-videos.json
```

This:
1. Resolves the channel handle to a channel ID via page HTML
2. Uses InnerTube browse API to paginate through all videos
3. Follows continuation tokens until all videos are fetched
4. Saves JSON array: `[{id, title, length, views, published, url}, ...]`
5. Videos are ordered most recent first

No API key needed. No external dependencies. Pure stdlib.

## Step 2: Create Notebook

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm create "{notebook_name}"
```

Note the notebook ID from the output.

## Step 3: Load Videos

```bash
cd ~/projects/notebooklm-loader && uv run python3 \
  scripts/load_channel.py load \
  --videos /tmp/channel-videos.json \
  --notebook {notebook-id} \
  --count {count} \
  --concurrency 20
```

This:
1. Reads the video list JSON
2. Opens async NotebookLM client (uses `~/.notebooklm/storage_state.json`)
3. Fires `add_url` for each video with 20 concurrent requests
4. Reports progress and saves errors to `/tmp/channel-load-errors.json`

**Performance:** ~200 videos in ~75 seconds with concurrency=20.

## Step 4: Fetch Transcript Content

**CRITICAL:** Source files created by import are empty stubs. Citations will ALL fail unless you fetch the actual transcript content first.

```bash
# Fetch content for all sources (threaded, ~2 min for 200 sources)
python3 /tmp/fetch_transcripts.py
```

Or inline:
```python
import json, subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCES_DIR = Path("Notes/NotebookLM/{notebook-slug}/Sources")
sources = json.load(open("/tmp/nlm-sources.json"))

# Build source_id -> file mapping
id_to_file = {}
for f in SOURCES_DIR.glob("*.md"):
    for line in f.read_text().split("\n"):
        if line.startswith("source_id:"):
            sid = line.split('"')[1]
            id_to_file[sid] = f
            break

def fetch(sid):
    r = subprocess.run(["nlm", "source", "content", sid, "--json"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0: return sid, None
    return sid, json.loads(r.stdout).get("value", {}).get("content", "")

with ThreadPoolExecutor(max_workers=10) as ex:
    for future in as_completed(ex.submit(fetch, s["id"]) for s in sources if s["id"] in id_to_file):
        sid, content = future.result()
        if content:
            f = id_to_file[sid]
            f.write_text(f.read_text() + f"\n## Transcript\n\n{content}\n")
```

`nlm source content <id> --json` returns `{value: {content: "..."}}`. Some sources may return empty if still processing on NotebookLM's end (retry after a few minutes).

## Step 5: Verify

```bash
cd ~/projects/notebooklm-loader && uv run notebooklm use {notebook-id}
cd ~/projects/notebooklm-loader && uv run notebooklm source list --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} sources loaded')"
```

## Step 6 (Optional): Import to Vault

Follow [workflows/import.md](import.md) to create vault source files and a dashboard.

## Limits

- **300 sources per notebook.** For channels with 300+ videos, create multiple notebooks (e.g. `channel-part-1`, `channel-part-2`).
- **Some videos may fail** if they're private, deleted, or region-locked. Check `/tmp/channel-load-errors.json`.
- **Processing time:** After upload, NotebookLM indexes each video server-side. This takes a few minutes. Sources may show as "processing" initially.

## Example: Full Pipeline

```bash
# 1. Scrape
python3 .claude/skills/notebooklm/scripts/load_channel.py scrape \
  --channel "https://www.youtube.com/@LennysPodcast" \
  --output /tmp/lennys-videos.json

# 2. Create notebook
cd ~/projects/notebooklm-loader && uv run notebooklm create "Lenny's Podcast"
# -> 2a18a53d-be60-4951-af17-8b7303dc097e

# 3. Load 200 most recent
cd ~/projects/notebooklm-loader && uv run python3 \
  /path/to/load_channel.py load \
  --videos /tmp/lennys-videos.json \
  --notebook 2a18a53d-be60-4951-af17-8b7303dc097e \
  --count 200

# 4. Ask questions
cd ~/projects/notebooklm-loader && uv run notebooklm use 2a18a53d-...
cd ~/projects/notebooklm-loader && uv run notebooklm ask "What are the top product management frameworks discussed?"
```
