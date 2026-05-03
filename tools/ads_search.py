#!/usr/bin/env python
"""ADS search helper for Cross-Reference agent."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ADS_API_URL = "https://api.adsabs.harvard.edu/v1/search/query"


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def get_token() -> str | None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_env_file(env_path)
    return os.environ.get("ADS_API_TOKEN")


def format_entry(doc: dict) -> str:
    bibcode = doc.get("bibcode", "")
    year = str(doc.get("year", ""))
    authors = ", ".join(doc.get("author", []) or [])
    title_list = doc.get("title", []) or []
    title = title_list[0].replace("\n", " ").strip() if title_list else ""
    doi_list = doc.get("doi", []) or []
    doi = ", ".join(doi_list)
    url = f"https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract" if bibcode else ""
    return f"| {bibcode} | {year} | {authors} | {title} | {doi} | {url} |"


def search_ads(query: str, max_results: int, fields: Iterable[str]) -> list[dict]:
    params = {
        "q": query,
        "rows": max_results,
        "fl": ",".join(fields),
    }
    url = f"{ADS_API_URL}?{urlencode(params)}"
    token = get_token()
    if not token:
        raise RuntimeError("ADS_API_TOKEN missing. Set it in .env or environment.")
    request = Request(url, headers={"Authorization": f"Bearer {token}"})
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("response", {}).get("docs", [])


def main() -> int:
    parser = argparse.ArgumentParser(description="Search ADS and print a markdown table")
    parser.add_argument("query", help="Search query, e.g. 'CPT violation' or 'author:\"Smith, J\"'")
    parser.add_argument("--max", type=int, default=10, help="Max results")
    args = parser.parse_args()

    fields = ["bibcode", "title", "author", "year", "doi"]
    try:
        results = search_ads(args.query, args.max, fields)
    except (RuntimeError, HTTPError, URLError, TimeoutError) as exc:
        print(f"ADS search failed: {exc}", file=sys.stderr)
        return 2

    print(f"# ADS search results ({datetime.utcnow().strftime('%Y-%m-%d')})")
    print(f"Query: {args.query}")
    print()
    print("| ADS Bibcode | Rok | Autorzy | Tytul | DOI | URL |")
    print("|---|---|---|---|---|---|")
    for doc in results:
        print(format_entry(doc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())