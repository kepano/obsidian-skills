# Journal Tier Reference

Use this file as a conservative starting table for first-pass journal scoring. Do not treat journal tier as a substitute for article-level quality.

Source basis: SCImago Journal Rank Medicine 2024 lists top medicine journals and Q1 quartiles, with metrics based on Scopus data as of March 2025: https://www.scimagojr.com/journalrank.php?area=2700&ord=desc&order=h

Also consider publisher journal metrics pages when available. Many publishers warn that citation metrics are not direct measures of article quality; keep this caution in the score reason.

## Scoring Bands

| Band | Journal score | Meaning |
|---|---:|---|
| T0 | 23-25 | Elite general medical, multidisciplinary biomedical, or clearly field-defining journal. |
| T1 | 20-22 | Field-leading specialty journal or major society journal. |
| T2 | 16-19 | Strong specialty journal, high-quality clinical or translational journal. |
| T3 | 12-15 | Standard peer-reviewed PubMed-indexed journal or unknown but credible journal. |
| T4 | 6-11 | Low-information, weakly matched, very narrow, or uncertain journal. |
| Unknown | 12-15 | Use when journal is absent from this table but appears PubMed-indexed and peer reviewed. |

If the journal is not listed, assign `Unknown` rather than guessing a high tier. If the abstract is from a case-report journal, methods journal, protocol journal, or narrative-review venue, score the journal normally but apply the article-type cap from `screening-rubric.md`.

## Starter Table

| Journal | Band | Suggested score | Notes |
|---|---|---:|---|
| New England Journal of Medicine | T0 | 25 | Elite general medical journal. |
| The Lancet | T0 | 25 | Elite general medical journal. |
| JAMA | T0 | 24 | Elite general medical journal. |
| BMJ | T0 | 23 | Elite general medical journal. |
| Nature Medicine | T0 | 25 | Elite translational and clinical medicine journal. |
| Nature | T0 | 24 | Elite multidisciplinary journal; apply topic relevance carefully. |
| Science | T0 | 24 | Elite multidisciplinary journal; apply topic relevance carefully. |
| Cell | T0 | 23 | Elite biomedical journal; often mechanistic or translational. |
| Annals of Internal Medicine | T1 | 22 | Leading internal medicine journal. |
| JAMA Internal Medicine | T1 | 22 | Leading internal medicine journal. |
| Lancet Global Health | T1 | 22 | Leading global health journal. |
| Lancet Public Health | T1 | 22 | Leading public health journal. |
| Lancet Oncology | T1 | 22 | Leading oncology journal. |
| Journal of Clinical Oncology | T1 | 22 | Leading oncology journal. |
| Nature Reviews Cancer | T1 | 22 | Leading review journal; apply review/article-type cap when needed. |
| Cancer Research | T1 | 20 | Major oncology research journal. |
| Circulation | T1 | 22 | Leading cardiovascular journal. |
| Journal of the American College of Cardiology | T1 | 22 | Leading cardiovascular journal. |
| European Heart Journal | T1 | 22 | Leading cardiovascular journal. |
| Blood | T1 | 21 | Leading hematology journal. |
| Gastroenterology | T1 | 21 | Leading gastroenterology journal. |
| Hepatology | T1 | 20 | Leading liver disease journal. |
| Journal of Clinical Investigation | T1 | 21 | Leading translational medicine journal. |
| Journal of Experimental Medicine | T1 | 20 | Leading biomedical research journal. |
| Immunity | T1 | 21 | Leading immunology journal. |
| Nature Immunology | T1 | 21 | Leading immunology journal. |
| Nature Reviews Immunology | T1 | 22 | Leading review journal; apply review/article-type cap when needed. |
| Lancet Neurology | T1 | 22 | Leading neurology journal. |
| Neurology | T2 | 19 | Strong specialty journal. |
| JAMA Neurology | T1 | 21 | Leading neurology journal. |
| Lancet Respiratory Medicine | T1 | 22 | Leading respiratory journal. |
| American Journal of Respiratory and Critical Care Medicine | T1 | 21 | Leading respiratory and critical care journal. |
| Lancet Psychiatry | T1 | 22 | Leading psychiatry journal. |
| JAMA Psychiatry | T1 | 21 | Leading psychiatry journal. |
| Diabetes Care | T1 | 21 | Leading diabetes journal. |
| JAMA Oncology | T1 | 21 | Leading oncology journal. |
| JAMA Cardiology | T1 | 21 | Leading cardiovascular journal. |
| PLOS Medicine | T1 | 20 | Strong general medical open-access journal. |
| eClinicalMedicine | T2 | 18 | Strong clinical medicine journal. |
| BMJ Medicine | T2 | 18 | Strong general medical journal. |
| BMC Medicine | T2 | 18 | Strong general medical journal. |
| Clinical Infectious Diseases | T1 | 21 | Leading infectious diseases journal. |
| The Journal of Infectious Diseases | T2 | 19 | Strong infectious diseases journal. |
| Emerging Infectious Diseases | T2 | 19 | Strong infectious diseases journal. |
| American Journal of Epidemiology | T2 | 18 | Strong epidemiology journal. |
| Epidemiology | T2 | 18 | Strong epidemiology journal. |
| International Journal of Epidemiology | T1 | 20 | Leading epidemiology journal. |

## Matching Rules

- Match case-insensitively.
- Treat common abbreviations as aliases when obvious: `N Engl J Med` -> `New England Journal of Medicine`; `JAMA Intern Med` -> `JAMA Internal Medicine`; `J Clin Oncol` -> `Journal of Clinical Oncology`.
- If journal title contains a family name such as `Lancet`, `JAMA`, `Nature`, or `BMJ`, do not automatically assign T0. Match the exact journal when possible; otherwise use T1 or T2 conservatively.
- If the journal is not found, write `Unknown journal tier; provisional score`.
