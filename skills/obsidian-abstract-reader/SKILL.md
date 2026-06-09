---
name: obsidian-abstract-reader
description: Read, summarize, and screen PubMed abstract records for literature triage and Obsidian note creation. Use when the user provides PubMed IDs, PubMed URLs, DOIs, PubMed metadata, article titles with abstracts, or batches of PubMed records and asks for abstract reading, first-pass literature screening, quality scoring, journal-tier-aware ranking, Chinese or English summaries, keyword backlinks, or Obsidian literature notes.
---

# Obsidian Abstract Reader

Use this skill for first-pass screening of PubMed abstracts. Optimize for quick ranking and note creation, not full-text critical appraisal.

## Inputs

Accept one record or a batch:

- PMID list, PubMed URLs, DOI list, or pasted PubMed metadata.
- Title + abstract text.
- CSV, TSV, or Markdown tables containing fields such as `pmid`, `doi`, `title`, `journal`, `year`, `abstract`, `keywords`, or `mesh`.

For PMID lists, use `scripts/fetch_pubmed.py` when network access is available. For pasted abstracts or tables, parse the supplied content directly.

## Workflow

1. Extract metadata: title, PMID, DOI, journal, year, publication type, authors, abstract, author keywords, and MeSH terms.
2. If metadata is missing, mark it as `Not provided`; do not invent it.
3. Score the abstract with the first-pass rubric in `references/screening-rubric.md`.
4. Use `references/journal-tiers.md` for journal-level scoring. If the journal is not listed, assign a conservative provisional score and label it `journal tier unknown`.
5. Create keyword backlinks from article-provided keywords and MeSH terms. Do not score keywords. Use `references/obsidian-output.md` for backlink normalization and output templates.
6. For a single record, produce an Obsidian literature note unless the user asks for plain text.
7. For batches, produce a ranked screening table plus short notes for high-priority papers.

## Output Rules

- Use the user's language by default; if the user writes Chinese, summarize in Chinese while preserving English titles, journal names, and technical terms when useful.
- State that scores are abstract-level first-pass screening scores.
- Keep reasons brief and evidence-grounded.
- Separate facts from inference. Use wording such as `Abstract states...` and `Likely...` when interpreting.
- Do not provide medical diagnosis or treatment recommendations.
- Preserve the original abstract in a folded Obsidian callout for single-record notes.

## Batch Decisions

Use these labels:

- `Prioritize`: high score and clearly relevant abstract.
- `Read Abstract`: usable but not urgent.
- `Need Full Text`: important but abstract lacks methods, outcomes, or key result details.
- `Low Priority`: weak fit, older, low detail, or limited novelty.
- `Exclude`: not a research abstract, wrong topic, no usable abstract, or not relevant to the user's screening goal.

Default thresholds:

- `Prioritize`: 80-100
- `Read Abstract`: 65-79
- `Need Full Text`: 55-79 with important missing details
- `Low Priority`: 40-64
- `Exclude`: 0-39 or unusable

## Resources

- `references/screening-rubric.md`: first-pass scoring weights and caps.
- `references/journal-tiers.md`: journal-tier reference table and scoring guidance.
- `references/obsidian-output.md`: Obsidian note, batch table, and backlink templates.
- `scripts/fetch_pubmed.py`: fetch PubMed XML records by PMID and export normalized JSON or Markdown.
