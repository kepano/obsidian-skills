#!/usr/bin/env python3
"""Fetch PubMed records by PMID and export normalized JSON or Markdown.

Uses NCBI EFetch XML through the public E-utilities endpoint.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch PubMed article metadata by PMID.")
    parser.add_argument("pmids", nargs="*", help="PMIDs to fetch.")
    parser.add_argument("--input", "-i", help="Text file containing PMIDs, one per line or mixed text.")
    parser.add_argument("--output", "-o", help="Output path. Defaults to stdout.")
    parser.add_argument("--format", choices=("json", "md"), default="json", help="Output format.")
    parser.add_argument("--email", help="Email parameter for NCBI usage attribution.")
    parser.add_argument("--api-key", help="NCBI API key.")
    parser.add_argument("--batch-size", type=int, default=100, help="PMIDs per request.")
    parser.add_argument("--delay", type=float, default=0.34, help="Delay between requests in seconds.")
    return parser.parse_args()


def collect_pmids(args: argparse.Namespace) -> list[str]:
    chunks = list(args.pmids)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            chunks.append(handle.read())
    text = "\n".join(chunks)
    seen = set()
    pmids = []
    for pmid in re.findall(r"\b\d{5,9}\b", text):
        if pmid not in seen:
            seen.add(pmid)
            pmids.append(pmid)
    return pmids


def fetch_batch(pmids: list[str], email: str | None, api_key: str | None) -> str:
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    if email:
        params["email"] = email
    if api_key:
        params["api_key"] = api_key
    url = f"{EFETCH_URL}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read().decode("utf-8")


def text_content(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return " ".join("".join(element.itertext()).split())


def first_text(root: ET.Element, path: str) -> str:
    return text_content(root.find(path))


def article_year(article: ET.Element) -> str:
    paths = [
        ".//JournalIssue/PubDate/Year",
        ".//ArticleDate/Year",
        ".//DateCompleted/Year",
        ".//DateRevised/Year",
    ]
    for path in paths:
        value = first_text(article, path)
        if value:
            return value
    medline_date = first_text(article, ".//JournalIssue/PubDate/MedlineDate")
    match = re.search(r"\b(19|20)\d{2}\b", medline_date)
    return match.group(0) if match else ""


def article_doi(article: ET.Element) -> str:
    for article_id in article.findall(".//ArticleId"):
        if article_id.attrib.get("IdType", "").lower() == "doi":
            return text_content(article_id)
    return ""


def article_authors(article: ET.Element) -> list[str]:
    authors = []
    for author in article.findall(".//AuthorList/Author"):
        collective = first_text(author, "CollectiveName")
        if collective:
            authors.append(collective)
            continue
        last = first_text(author, "LastName")
        initials = first_text(author, "Initials")
        if last:
            authors.append(f"{last} {initials}".strip())
    return authors


def article_abstract(article: ET.Element) -> str:
    parts = []
    for abstract_text in article.findall(".//Abstract/AbstractText"):
        label = abstract_text.attrib.get("Label") or abstract_text.attrib.get("NlmCategory")
        body = text_content(abstract_text)
        if body and label:
            parts.append(f"{label}: {body}")
        elif body:
            parts.append(body)
    return "\n".join(parts)


def article_keywords(article: ET.Element) -> list[str]:
    values = []
    for keyword in article.findall(".//KeywordList/Keyword"):
        value = text_content(keyword)
        if value:
            values.append(value)
    return dedupe(values)


def article_mesh(article: ET.Element) -> list[str]:
    values = []
    for descriptor in article.findall(".//MeshHeading/DescriptorName"):
        value = text_content(descriptor)
        if value:
            values.append(value)
    return dedupe(values)


def publication_types(article: ET.Element) -> list[str]:
    return dedupe([text_content(node) for node in article.findall(".//PublicationTypeList/PublicationType") if text_content(node)])


def dedupe(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        key = value.casefold()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def parse_records(xml_text: str) -> list[dict[str, object]]:
    root = ET.fromstring(xml_text)
    records = []
    for article in root.findall(".//PubmedArticle"):
        pmid = first_text(article, ".//MedlineCitation/PMID")
        record = {
            "pmid": pmid,
            "doi": article_doi(article),
            "title": first_text(article, ".//ArticleTitle"),
            "journal": first_text(article, ".//Journal/Title") or first_text(article, ".//Journal/ISOAbbreviation"),
            "journal_abbrev": first_text(article, ".//Journal/ISOAbbreviation"),
            "year": article_year(article),
            "authors": article_authors(article),
            "publication_types": publication_types(article),
            "keywords": article_keywords(article),
            "mesh_terms": article_mesh(article),
            "abstract": article_abstract(article),
            "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
        }
        records.append(record)
    return records


def to_markdown(records: list[dict[str, object]]) -> str:
    lines = []
    for record in records:
        lines.extend(
            [
                f"## {record.get('title') or 'Untitled'}",
                "",
                f"- PMID: {record.get('pmid', '')}",
                f"- DOI: {record.get('doi', '')}",
                f"- Journal: {record.get('journal', '')}",
                f"- Year: {record.get('year', '')}",
                f"- Publication types: {', '.join(record.get('publication_types', []))}",
                f"- Keywords: {', '.join(record.get('keywords', []))}",
                f"- MeSH: {', '.join(record.get('mesh_terms', []))}",
                "",
                str(record.get("abstract") or "No abstract."),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    pmids = collect_pmids(args)
    if not pmids:
        print("No PMIDs found.", file=sys.stderr)
        return 2

    records = []
    for start in range(0, len(pmids), args.batch_size):
        batch = pmids[start : start + args.batch_size]
        xml_text = fetch_batch(batch, args.email, args.api_key)
        records.extend(parse_records(xml_text))
        if start + args.batch_size < len(pmids):
            time.sleep(args.delay)

    if args.format == "json":
        output = json.dumps(records, ensure_ascii=False, indent=2)
    else:
        output = to_markdown(records)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(output)
            if not output.endswith("\n"):
                handle.write("\n")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
