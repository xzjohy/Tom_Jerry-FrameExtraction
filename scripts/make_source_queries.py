#!/usr/bin/env python3
"""Generate human-review search queries for each episode.

This does not download video and does not bypass access controls.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sources" / "episodes.json"
OUT = ROOT / "sources" / "source_queries.csv"

def main():
    episodes = json.loads(DATA.read_text(encoding="utf-8"))["episodes"]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","title","year","official_query","archive_query"])
        w.writeheader()
        for e in episodes:
            title = e["title"]
            w.writerow({
                "id": e["id"],
                "title": title,
                "year": e["year"],
                "official_query": f'Tom and Jerry "{title}" Warner Bros official',
                "archive_query": f'Tom and Jerry "{title}" {e["year"]} restoration',
            })
    print(f"Wrote {len(episodes)} queries to {OUT}")

if __name__ == "__main__":
    main()
