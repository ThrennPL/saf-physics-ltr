#!/usr/bin/env python
"""ArXiv search helper for Cross-Reference agent."""

from __future__ import annotations

import argparse
from datetime import datetime
from typing import Iterable

import arxiv


def format_entry(result: arxiv.Result) -> str:
    authors = ", ".join(a.name for a in result.authors)
    published = result.published.strftime("%Y-%m-%d") if result.published else ""
    title = result.title.replace("\n", " ").strip()
    return f"| {result.get_short_id()} | {published} | {authors} | {title} | {result.entry_id} |"


def search_arxiv(query: str, max_results: int, categories: Iterable[str]) -> list[arxiv.Result]:
    cat_query = " OR ".join(f"cat:{c}" for c in categories) if categories else ""
    full_query = f"({query})" + (f" AND ({cat_query})" if cat_query else "")
    search = arxiv.Search(
        query=full_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    return list(search.results())


def main() -> int:
    parser = argparse.ArgumentParser(description="Search ArXiv and print a markdown table")
    parser.add_argument("query", help="Search query, e.g. 'CPT violation' or 'cat:hep-th'")
    parser.add_argument("--max", type=int, default=10, help="Max results")
    parser.add_argument("--cat", action="append", default=[], help="Category filter (repeatable)")
    args = parser.parse_args()

    results = search_arxiv(args.query, args.max, args.cat)
    print(f"# ArXiv search results ({datetime.utcnow().strftime('%Y-%m-%d')})")
    print(f"Query: {args.query}")
    if args.cat:
        print(f"Categories: {', '.join(args.cat)}")
    print()
    print("| ArXiv ID | Data | Autorzy | Tytul | URL |")
    print("|---|---|---|---|---|")
    for result in results:
        print(format_entry(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
