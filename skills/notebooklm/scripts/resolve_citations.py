#!/usr/bin/env python3
"""Resolve [N] citations in NotebookLM answers to clickable [[wikilinks]].

Usage (nlm CLI output):
  python3 resolve_citations.py --qa /tmp/qa.json --sources /tmp/sources.json --slug my-notebook
  python3 resolve_citations.py --qa /tmp/qa.json --sources /tmp/sources.json \
    --slug my-notebook --title "My Q&A" \
    --output "Notes/NotebookLM/my-notebook/QA/2026-04-03 My Q&A.md" \
    --vault .

Input formats:
  --qa: nlm notebook query output: {value: {answer, references: [{source_id, citation_number, cited_text}]}}
  --sources: nlm source list output: [{id, title, type, url}]

Each [N] becomes [[Source#^anchor|[N]]] - click jumps to the cited line in the transcript.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def safe_filename(title):
    # Must match import_sources.py exactly
    safe = re.sub(r'[:*?"<>|]', '-', title)
    safe = re.sub(r'\s+', ' ', safe).strip()
    if len(safe) > 120:
        safe = safe[:120].rstrip(' -')
    return safe


def build_source_map(sources_file):
    with open(sources_file) as f:
        data = json.load(f)

    # nlm format: flat list [{id, title, type, url}]
    # old format: {sources: [{id, title, ...}]}
    if isinstance(data, list):
        sources = data
    else:
        sources = data.get("sources", [])

    mapping = {}
    for s in sources:
        title = s["title"].strip()
        if title == "- YouTube" or len(title) < 3:
            continue
        mapping[s["id"]] = safe_filename(title)
    return mapping


def expand_citation_spec(spec_text):
    numbers = []
    for part in spec_text.split(','):
        part = part.strip()
        if '-' in part:
            try:
                a, b = part.split('-', 1)
                numbers.extend(range(int(a.strip()), int(b.strip()) + 1))
            except ValueError:
                continue
        else:
            try:
                numbers.append(int(part))
            except ValueError:
                continue
    return numbers


def _detect_collapsed_citations(answer, references):
    """Check if answer citations all share one source_id despite naming multiple sources."""
    answer_cns = set(int(x) for x in re.findall(r'\[(\d+)\]', answer))
    if len(answer_cns) < 2:
        return False
    cn_to_sid = {r["citation_number"]: r["source_id"] for r in references}
    used_sids = set(cn_to_sid[n] for n in answer_cns if n in cn_to_sid)
    sections = _extract_section_titles(answer)
    return len(used_sids) == 1 and len(sections) >= 2


def _extract_section_titles(answer):
    """Extract *"episode title"* markers and their positions from answer text."""
    return [(m.start(), m.group(1).strip('"\u201c\u201d'))
            for m in re.finditer(r'\*["\u201c](.+?)["\u201d]\*', answer)]


def _fuzzy_match_title(extracted_title, source_map):
    """Match an extracted episode title to a source_id via substring overlap."""
    best_id = None
    best_score = 0
    for sid, raw_title in source_map.items():
        ext_low = extracted_title.lower()
        raw_low = raw_title.lower()
        if ext_low in raw_low or raw_low in ext_low:
            if len(raw_title) > best_score:
                best_score = len(raw_title)
                best_id = sid
            continue
        ext_words = set(re.findall(r'\w+', ext_low))
        raw_words = set(re.findall(r'\w+', raw_low))
        if not ext_words:
            continue
        overlap = len(ext_words & raw_words) / len(ext_words)
        if overlap > 0.5 and overlap * len(ext_words) > best_score:
            best_score = overlap * len(ext_words)
            best_id = sid
    return best_id


def _build_citation_section_map(answer, references, source_map):
    """When citations are collapsed, remap them using episode title sections."""
    sections = _extract_section_titles(answer)
    if len(sections) < 2:
        return None

    section_sources = []
    for pos, title in sections:
        sid = _fuzzy_match_title(title, source_map)
        section_sources.append((pos, sid))

    cite_positions = {}
    for m in re.finditer(r'\[(\d+(?:\s*[-,]\s*\d+)*)\]', answer):
        pos = m.start()
        for part in m.group(1).split(','):
            part = part.strip()
            if '-' in part:
                try:
                    a, b = part.split('-', 1)
                    for n in range(int(a.strip()), int(b.strip()) + 1):
                        if n not in cite_positions:
                            cite_positions[n] = pos
                except ValueError:
                    continue
            else:
                try:
                    n = int(part)
                    if n not in cite_positions:
                        cite_positions[n] = pos
                except ValueError:
                    continue

    remap = {}
    for cn, cpos in cite_positions.items():
        best_section_sid = None
        for spos, sid in reversed(section_sources):
            if spos <= cpos:
                best_section_sid = sid
                break
        if best_section_sid:
            remap[cn] = best_section_sid

    return remap if remap else None


def _make_anchor_id(cited_text):
    """Generate a stable anchor ID from cited_text content."""
    h = hashlib.md5(cited_text[:100].encode()).hexdigest()[:8]
    return "c-%s" % h


def _strip_anchors(text):
    """Remove previously injected anchor blocks (\n\n^c-...\n\n) for clean searching."""
    return re.sub(r'\n\n\^c-[0-9a-f]+\n\n', '', text)


def _find_text_position(content, cited_text):
    """Find the character position of cited_text in content via substring search.

    Tries full text first, then progressively shorter unique substrings.
    If anchors were previously injected in the content, strips them for matching
    then maps the position back to the real content.
    Returns char position or None.
    """
    # Normalize cited_text to match file conventions:
    # - nlm returns \xa0\n but files may have just \n
    # - Replace non-breaking spaces with regular spaces
    # Content stays as-is so returned positions are accurate
    norm_content = content.replace('\xa0', ' ')
    norm_cited = cited_text.replace('\xa0', ' ').strip()
    # Also try with whitespace before newlines collapsed (nlm artifact)
    norm_cited_collapsed = re.sub(r' +\n', '\n', norm_cited)

    if not norm_cited:
        return None

    # Try both normalizations: raw and with trailing spaces before \n collapsed
    # (nlm returns "text \nmore" but files may have "text\nmore")
    candidates = [norm_cited]
    if norm_cited_collapsed != norm_cited:
        candidates.append(norm_cited_collapsed)

    for cited in candidates:
        # Try direct search first (works when no anchors interrupt the passage)
        pos = norm_content.find(cited)
        if pos >= 0:
            return pos

        # Try shorter unique substrings
        for length in [200, 100, 60]:
            if len(cited) < length:
                continue
            snippet = cited[:length]
            pos = norm_content.find(snippet)
            if pos >= 0:
                second = norm_content.find(snippet, pos + 1)
                if second < 0:
                    return pos

    # Fallback: strip existing anchors from content and retry
    # This handles the case where a previous question's anchor was injected
    # in the middle of this question's cited_text passage
    clean = _strip_anchors(norm_content)
    if clean != norm_content:
        for cited in candidates:
            for length in [200, 100, 60]:
                if len(cited) < length:
                    continue
                snippet = cited[:length]
                clean_pos = clean.find(snippet)
                if clean_pos < 0:
                    continue
            # Map clean_pos back to real content position
            # Walk through content, skipping anchor blocks, counting real chars
            real_pos = 0
            clean_count = 0
            while clean_count < clean_pos and real_pos < len(norm_content):
                # Check if we're at an anchor block
                m = re.match(r'\n\n\^c-[0-9a-f]+\n\n', norm_content[real_pos:])
                if m:
                    real_pos += m.end()
                else:
                    real_pos += 1
                    clean_count += 1
            return real_pos

    return None


def _inject_inline_anchors(source_path, anchors_to_inject):
    """Inject ^anchor-id tags inline in the transcript at cited_text positions.

    anchors_to_inject: list of (anchor_id, file_position) tuples.

    Splits the content at each anchor position and inserts ^anchor-id on its own
    paragraph. Obsidian requires blank lines before AND after ^block-id for indexing,
    AND the block-id must reference a distinct paragraph (not a 90K char single line).
    """
    content = source_path.read_text()
    if not content:
        return 0

    # Strip old ## Cited Passages section if present (migration from old approach)
    t_idx = content.find("## Transcript")
    cp_idx = content.find("## Cited Passages")
    if cp_idx >= 0 and (t_idx < 0 or cp_idx > t_idx):
        content = content[:cp_idx].rstrip() + "\n"

    # Sort anchors by position descending so insertions don't shift later positions
    sorted_anchors = sorted(anchors_to_inject, key=lambda x: x[1], reverse=True)
    added = 0

    for anchor_id, file_pos in sorted_anchors:
        tag = "^%s" % anchor_id
        # Skip if anchor already exists anywhere in the file
        if tag in content:
            continue

        # Split content at the anchor position: insert a paragraph break + anchor
        # Don't strip whitespace - rstrip/lstrip can eat spaces between words,
        # which breaks future cited_text substring searches that span this split point.
        before = content[:file_pos]
        after = content[file_pos:]

        # Insert: \n\n^anchor-id\n\n between the two halves
        content = before + "\n\n" + tag + "\n\n" + after
        added += 1

    if added > 0:
        source_path.write_text(content)

    return added


def resolve_answer(answer, references, source_map, slug, vault=None):
    cn_map = {}
    for ref in references:
        cn = ref.get("citation_number")
        if cn is not None:
            cn_map[cn] = ref

    # Fix collapsed citations: all cited refs share one source_id
    remap = None
    if _detect_collapsed_citations(answer, references):
        remap = _build_citation_section_map(answer, references, source_map)
        if remap:
            print("REMAP: %d citations remapped via section titles" % len(remap), file=sys.stderr)

    sources_path = "Notes/NotebookLM/%s/Sources" % slug
    cited_sources = set()
    cited_numbers = set()

    # Build anchor map: citation_number -> (source_title, anchor_id, cited_text, original_source_title)
    anchor_map = {}
    seen_anchors = {}  # anchor_id -> first citation_number (dedup)
    for n, ref in cn_map.items():
        cited_text = ref.get("cited_text", "").strip()
        if not cited_text:
            continue
        remapped_sid = remap.get(n, ref["source_id"]) if remap else ref["source_id"]
        original_sid = ref["source_id"]
        anchor_id = _make_anchor_id(cited_text)

        # If two citations have the same anchor_id, they cite the same passage
        if anchor_id in seen_anchors:
            pass  # still create mapping so the link resolves
        seen_anchors[anchor_id] = n

        title = source_map.get(remapped_sid)
        original_title = source_map.get(original_sid)
        if title and cited_text:
            anchor_map[n] = (title, anchor_id, cited_text, original_title)

    def replace_citation(match):
        spec = match.group(1)
        numbers = expand_citation_spec(spec)
        links = []
        for n in numbers:
            if n not in anchor_map:
                links.append("[%d]" % n)
                continue
            title, anchor_id, _, original_title = anchor_map[n]
            cited_sources.add(title)
            cited_numbers.add(n)
            if title == original_title:
                links.append("[[%s/%s#^%s|[%d]]]" % (sources_path, title, anchor_id, n))
            else:
                links.append("[[%s/%s|[%d]]]" % (sources_path, title, n))
        return " ".join(links)

    resolved = re.sub(
        r'\[(\d+(?:\s*[-,]\s*\d+)*)\]',
        replace_citation,
        answer
    )

    # Inject inline anchors into source files
    if vault:
        # Group by ORIGINAL source file (where cited_text actually lives)
        by_source = {}
        for n in cited_numbers:
            title, anchor_id, cited_text, original_title = anchor_map[n]
            ref = cn_map[n]
            if original_title:
                by_source.setdefault(original_title, []).append((anchor_id, cited_text))

        total_added = 0
        for title, items in by_source.items():
            source_file = vault / sources_path / ("%s.md" % title)
            if not source_file.exists():
                print("SKIP: source file not found: %s" % source_file.name, file=sys.stderr)
                continue
            content = source_file.read_text()

            anchors = []
            seen_positions = set()
            for anchor_id, cited_text in items:
                file_pos = _find_text_position(content, cited_text)
                if file_pos is None:
                    print("MISS: could not find cited_text for ^%s in %s" % (anchor_id, title), file=sys.stderr)
                    continue
                # Dedup: don't place two anchors at the same position
                pos_bucket = file_pos // 200
                if pos_bucket in seen_positions:
                    continue
                seen_positions.add(pos_bucket)
                anchors.append((anchor_id, file_pos))

            if anchors:
                count = _inject_inline_anchors(source_file, anchors)
                total_added += count

        if total_added > 0:
            print("ANCHORS: %d injected across %d source files" % (total_added, len(by_source)), file=sys.stderr)

    stats = {
        "total_refs": len(references),
        "citations_in_answer": len(cited_numbers),
        "cited_sources": len(cited_sources),
        "total_sources": len(source_map),
    }

    return resolved, sorted(cited_sources), stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qa", required=True)
    parser.add_argument("--sources", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title")
    parser.add_argument("--notebook", help="Display name of notebook file, e.g. 'Lennys Podcast'")
    parser.add_argument("--output")
    parser.add_argument("--date")
    parser.add_argument("--vault", default=".")
    args = parser.parse_args()

    vault = Path(args.vault)
    source_map = build_source_map(args.sources)

    with open(args.qa) as f:
        qa_raw = json.load(f)

    # nlm format: {value: {answer, references, ...}}
    # old format: {answer, references, ...}
    if "value" in qa_raw:
        qa_data = qa_raw["value"]
    else:
        qa_data = qa_raw

    resolved, cited_sources, stats = resolve_answer(
        qa_data["answer"], qa_data["references"], source_map, args.slug, vault=vault
    )

    print("Citations: %d used, %d sources" % (stats['citations_in_answer'], stats['cited_sources']), file=sys.stderr)

    if not args.output:
        print(resolved)
        return

    if not args.title:
        print("ERROR: --title required for --output", file=sys.stderr)
        sys.exit(1)

    from datetime import date
    note_date = args.date or date.today().isoformat()
    sources_path = "Notes/NotebookLM/%s/Sources" % args.slug

    sources_list = "\n".join(
        "- [[%s/%s|%s]]" % (sources_path, t, t) for t in cited_sources
    )

    related_block = ""
    if args.notebook:
        related_block = '\nrelated:\n  - "[[Notes/NotebookLM/%s|%s]]"' % (args.notebook, args.notebook)

    content = """---
type: nlm-query
status: done
date: %s%s
---

# %s

%s

---

## Sources

%s
""" % (note_date, related_block, args.title, resolved, sources_list)

    output_path = vault / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    print("CREATED: %s (%d sources)" % (args.output, stats['cited_sources']), file=sys.stderr)


if __name__ == "__main__":
    main()
