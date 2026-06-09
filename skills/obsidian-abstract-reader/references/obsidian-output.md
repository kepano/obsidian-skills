# Obsidian Output

Use Obsidian-flavored Markdown with YAML frontmatter, wikilinks, and folded callouts.

## Keyword Backlinks

Use article-provided keywords first:

1. Author keywords.
2. MeSH terms.
3. If neither is available, infer 3-8 terms from title and abstract and label them `inferred`.

Do not score keywords.

Normalize keyword backlinks:

- Title-case plain biomedical phrases: `risk factors` -> `[[Risk Factors]]`.
- Remove MeSH subheading separators: `COVID-19/diagnosis` -> `[[COVID-19 Diagnosis]]`.
- Preserve useful abbreviations as aliases: `CVD` -> `[[Cardiovascular Diseases|CVD]]` when the expansion is clear from context.
- Keep disease names and gene/protein symbols readable; do not over-normalize specialized terms.
- If a keyword is unsafe as a note title, make a clean title and keep the original text beside it.

## Single-Record Template

```markdown
---
title: "{{title}}"
pmid: "{{pmid}}"
doi: "{{doi}}"
journal: "{{journal}}"
year: "{{year}}"
publication_type: "{{publication_type}}"
screening_score: {{total_score}}
decision: "{{decision}}"
keywords:
{{keyword_yaml}}
---

# {{title}}

> [!summary] First-pass conclusion
> {{one_sentence_takeaway}}

## Screening Score

| Dimension | Score | Reason |
|---|---:|---|
| Journal level | {{journal_score}}/25 | {{journal_reason}} |
| Recency | {{recency_score}}/15 | {{recency_reason}} |
| Method completeness | {{method_score}}/25 | {{method_reason}} |
| Scientific rigor | {{rigor_score}}/20 | {{rigor_reason}} |
| Novelty | {{novelty_score}}/15 | {{novelty_reason}} |
| Total | {{total_score}}/100 | {{decision}} |

## Metadata

- PMID: {{pmid}}
- DOI: {{doi}}
- Journal: {{journal}}
- Year: {{year}}
- Publication type: {{publication_type}}

## Keyword Backlinks

{{keyword_links}}

## Abstract Summary

### Research Question

{{research_question}}

### Methods and Population

{{methods_population}}

### Main Results

{{main_results}}

### First-Pass Value

{{screening_value}}

### Full-Text Checks

{{full_text_checks}}

> [!abstract]- Original Abstract
> {{original_abstract}}
```

## Batch Table

```markdown
| Rank | PMID | Year | Journal | Title | Score | Journal | Recent | Method | Rigor | Novelty | Decision | Keyword backlinks | Reason |
|---:|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | {{pmid}} | {{year}} | {{journal}} | {{title}} | {{total}} | {{journal_score}} | {{recency_score}} | {{method_score}} | {{rigor_score}} | {{novelty_score}} | {{decision}} | {{keyword_links_inline}} | {{short_reason}} |
```

After the table, add:

- `Top priority`: 3-10 papers worth reading first.
- `Need full text`: papers that may be important but lack abstract detail.
- `Keyword map`: a compact list of frequently appearing backlinks across the batch.
