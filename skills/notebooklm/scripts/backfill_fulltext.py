#!/usr/bin/env python3
"""Backfill source files with fulltext content from NotebookLM.

Usage:
  cd ~/projects/notebooklm-loader && uv run python3 \
    /path/to/backfill_fulltext.py \
    --notebook <notebook-id> \
    --slug <slug> \
    --vault /path/to/vault \
    --concurrency 10
"""
import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path


def safe_filename(title):
    safe = re.sub(r'[/:*?"<>|]', '-', title)
    safe = re.sub(r'\s+', ' ', safe).strip()
    if len(safe) > 120:
        safe = safe[:120].rstrip(' -')
    return safe


success = 0
failed = 0
skipped = 0


async def fetch_and_write(client, sem, notebook_id, source, sources_dir):
    global success, failed, skipped
    sid = source["id"]
    title = source["title"].strip()
    filename = safe_filename(title) + ".md"
    filepath = sources_dir / filename

    if not filepath.exists():
        skipped += 1
        return

    content = filepath.read_text()
    if "## Transcript" in content:
        skipped += 1
        return

    async with sem:
        try:
            ft = await client.sources.get_fulltext(notebook_id, sid)
            if not ft.content or len(ft.content) < 100:
                failed += 1
                print(f"  EMPTY: {filename}", file=sys.stderr)
                return

            # Append transcript section
            new_content = content.rstrip() + "\n\n## Transcript\n\n" + ft.content + "\n"
            filepath.write_text(new_content)
            success += 1
            print(f"  OK: {filename} ({len(ft.content)} chars)")
        except Exception as e:
            failed += 1
            print(f"  FAIL: {filename} | {str(e)[:80]}", file=sys.stderr)


async def main():
    from notebooklm import NotebookLMClient

    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--vault", default=".")
    parser.add_argument("--concurrency", type=int, default=10)
    parser.add_argument("--sources-json", help="Path to source list JSON (skips API call)")
    args = parser.parse_args()

    vault = Path(args.vault)
    sources_dir = vault / "Notes/NotebookLM" / args.slug / "Sources"

    client = await NotebookLMClient.from_storage()
    async with client:
        if args.sources_json:
            with open(args.sources_json) as f:
                source_list = json.load(f)["sources"]
        else:
            raw = await client.sources.list(args.notebook)
            source_list = [{"id": s.id, "title": s.title or ""} for s in raw]

        total = len(source_list)
        print(f"Backfilling {total} sources (concurrency={args.concurrency})")

        sem = asyncio.Semaphore(args.concurrency)
        tasks = [
            fetch_and_write(client, sem, args.notebook, s, sources_dir)
            for s in source_list
        ]
        await asyncio.gather(*tasks)

    print(f"\nDone: {success} written, {skipped} skipped, {failed} failed")

if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(main())
    print(f"Elapsed: {time.time() - t0:.0f}s")
