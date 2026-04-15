#!/usr/bin/env python3
"""Import NotebookLM sources into vault as notebook-source files.

Usage:
  python3 import_sources.py --sources /tmp/sources.json --slug my-notebook --dashboard "Dashboard Title"
  python3 import_sources.py --sources /tmp/sources.json --slug my-notebook --dashboard "Dashboard Title" --skip-guides

Creates one .md file per source with frontmatter + AI-generated source guide.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path.cwd()  # Expected to run from vault root

# Map NotebookLM type strings to our source_type values
TYPE_MAP = {
    "SourceType.YOUTUBE": "youtube",
    "SourceType.WEB_PAGE": "web",
    "SourceType.PDF": "pdf",
    "SourceType.TEXT": "text",
    "SourceType.GOOGLE_DOCS": "gdocs",
    "SourceType.GOOGLE_SLIDES": "gslides",
}


def safe_filename(title: str) -> str:
    """Make title safe for filesystem."""
    title = re.sub(r'[/:*?"<>|]', '-', title)
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 120:
        title = title[:120].rstrip(' -')
    return title


def fetch_guide(source_id: str) -> tuple[str, list[str], list[str]]:
    """Fetch AI-generated source guide. Returns (summary, topics, keywords)."""
    try:
        result = subprocess.run(
            ["notebooklm", "source", "guide", source_id, "--json"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            return "", [], []
        data = json.loads(result.stdout)
        return data.get("summary", ""), data.get("topics", []), data.get("keywords", [])
    except Exception:
        return "", [], []


def main():
    parser = argparse.ArgumentParser(description="Import NotebookLM sources into vault")
    parser.add_argument("--sources", required=True, help="Path to notebooklm source list JSON")
    parser.add_argument("--slug", required=True, help="Notebook slug (kebab-case folder name)")
    parser.add_argument("--dashboard", required=True, help="Dashboard title for related links")
    parser.add_argument("--skip-guides", action="store_true", help="Skip fetching AI source guides")
    args = parser.parse_args()

    with open(args.sources) as f:
        data = json.load(f)

    notebook_id = data.get("notebook_id", "")
    sources = data["sources"]
    sources_dir = VAULT / "Notes/NotebookLM" / args.slug / "Sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    dashboard_path = f"Notes/Dashboards/{args.dashboard}"

    created = 0
    skipped = 0

    for source in sources:
        title = source["title"].strip()
        source_id = source["id"]
        source_type = TYPE_MAP.get(source["type"], "web")
        url = source.get("url") or ""
        date = source.get("created_at", "")[:10]

        # Skip sources with garbage titles (multi-URL web pages etc.)
        if title == "- YouTube" or len(title) < 3:
            print(f"  SKIP: '{title}' (bad title)")
            skipped += 1
            continue

        filename = safe_filename(title) + ".md"
        filepath = sources_dir / filename

        if filepath.exists():
            print(f"  EXISTS: {filename}")
            skipped += 1
            continue

        # Fetch guide if not skipped
        guide_text = ""
        keywords = []
        if not args.skip_guides:
            print(f"  Fetching guide: {title[:60]}...")
            summary, topics, keywords = fetch_guide(source_id)
            if summary:
                guide_text = summary
                if topics:
                    guide_text += "\n\n### Topics\n\n" + ", ".join(topics)
                print(f"    OK: {len(summary)} chars, {len(keywords)} keywords")
            else:
                print(f"    WARN: no guide returned")

        # Build topics frontmatter
        topics_yaml = ""
        if keywords:
            topics_yaml = "topics:\n" + "\n".join(f'  - "[[{k}]]"' for k in keywords) + "\n"

        content = f"""---
type: notebook-source
source_id: "{source_id}"
notebook_id: "{notebook_id}"
url: "{url}"
source_type: {source_type}
status: active
date: {date}
{topics_yaml}related:
  - "[[{dashboard_path}]]"
---

# {title}

## Source Guide

{guide_text}
"""

        filepath.write_text(content)
        print(f"  CREATED: {filename}")
        created += 1

    print(f"\nDone: {created} created, {skipped} skipped")


if __name__ == "__main__":
    main()
