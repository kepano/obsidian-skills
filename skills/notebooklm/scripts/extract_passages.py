#!/usr/bin/env python3
"""Extract cited_text passages from Q&A JSONs and append to source files.

Usage:
  python3 extract_passages.py --qa /tmp/qa-1.json /tmp/qa-2.json \
    --sources /tmp/sources.json --slug my-notebook

Reads all Q&A JSONs, deduplicates cited_text chunks per source (first 100 chars as key),
and appends a ## Cited Passages section to each source file with ### Passage 1, 2, etc.

Incremental - appends new passages to sources that already have a ## Cited Passages section.
"""
import argparse
import json
import re
import sys
from pathlib import Path

VAULT = Path.cwd()


def safe_filename(title: str) -> str:
    """Same logic as import_sources.py."""
    title = re.sub(r'[/:*?"<>|]', '-', title)
    title = re.sub(r'\s+', ' ', title).strip()
    if len(title) > 120:
        title = title[:120].rstrip(' -')
    return title


def main():
    parser = argparse.ArgumentParser(description="Extract cited passages into source files")
    parser.add_argument("--qa", nargs="+", required=True, help="Q&A JSON files")
    parser.add_argument("--sources", required=True, help="Sources JSON file")
    parser.add_argument("--slug", required=True, help="Notebook slug")
    args = parser.parse_args()

    # Build source_id -> title mapping
    with open(args.sources) as f:
        sources_data = json.load(f)

    source_titles = {}
    for s in sources_data["sources"]:
        title = s["title"].strip()
        if title == "- YouTube" or len(title) < 3:
            continue
        source_titles[s["id"]] = title

    # Collect unique chunks per source across all QA files
    # Key: source_id -> list of unique cited_text (deduped by first 100 chars)
    source_chunks: dict[str, list[str]] = {}
    seen_keys: dict[str, set[str]] = {}

    for qa_file in args.qa:
        with open(qa_file) as f:
            data = json.load(f)
        for ref in data["references"]:
            ct = ref.get("cited_text", "").strip()
            if not ct:
                continue
            sid = ref["source_id"]
            if sid not in source_titles:
                continue
            dedup_key = ct[:100]
            if sid not in seen_keys:
                seen_keys[sid] = set()
                source_chunks[sid] = []
            if dedup_key not in seen_keys[sid]:
                seen_keys[sid].add(dedup_key)
                source_chunks[sid].append(ct)

    print(f"Sources with passages: {len(source_chunks)}", file=sys.stderr)

    sources_dir = VAULT / "Notes/NotebookLM" / args.slug / "Sources"
    updated = 0
    skipped = 0

    for sid, chunks in source_chunks.items():
        title = source_titles[sid]
        filename = safe_filename(title) + ".md"
        filepath = sources_dir / filename

        if not filepath.exists():
            print(f"  MISSING: {filename}", file=sys.stderr)
            skipped += 1
            continue

        content = filepath.read_text()
        if "## Cited Passages" in content:
            # Parse existing passages to find what's already there
            existing_keys = set()
            existing_count = 0
            for m in re.finditer(r'### Passage (\d+)\n\n(.+?)(?=\n### Passage |\Z)', content, re.DOTALL):
                existing_count = max(existing_count, int(m.group(1)))
                existing_keys.add(m.group(2).strip()[:100])

            # Find new chunks not already in the file
            new_chunks = [c for c in chunks if c[:100] not in existing_keys]
            if not new_chunks:
                print(f"  CURRENT: {filename} ({existing_count} passages, no new)", file=sys.stderr)
                skipped += 1
                continue

            # Append new passages after existing ones
            new_passages = ""
            for i, chunk in enumerate(new_chunks, existing_count + 1):
                new_passages += f"\n### Passage {i}\n\n{chunk}\n"

            filepath.write_text(content.rstrip() + "\n" + new_passages)
            print(f"  APPENDED: {filename} (+{len(new_chunks)} passages, {existing_count + len(new_chunks)} total)", file=sys.stderr)
            updated += 1
        else:
            # Build new passages section
            passages = "\n## Cited Passages\n"
            for i, chunk in enumerate(chunks, 1):
                passages += f"\n### Passage {i}\n\n{chunk}\n"

            filepath.write_text(content.rstrip() + "\n" + passages)
            print(f"  CREATED: {filename} ({len(chunks)} passages)", file=sys.stderr)
            updated += 1

    print(f"\nDone: {updated} updated, {skipped} skipped", file=sys.stderr)

    # Output passage mapping as JSON for resolve_citations to use
    mapping = {}
    for sid, chunks in source_chunks.items():
        mapping[sid] = {}
        for i, chunk in enumerate(chunks, 1):
            mapping[sid][chunk[:100]] = i
    json.dump(mapping, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
