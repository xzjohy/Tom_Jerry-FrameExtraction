#!/usr/bin/env python3
"""Summarize catalog readiness before extraction."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sources" / "episodes.json"

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    eps = data["episodes"]
    rights = Counter(e.get("rights_status", "missing") for e in eps)
    sourced = [e for e in eps if e.get("video_source_url")]
    redistributable = [e for e in eps if e.get("redistribution_allowed")]
    resolutions = Counter(e.get("resolution") or "unset" for e in sourced)
    print(f"Episodes: {len(eps)}")
    print(f"Video sources selected: {len(sourced)}/{len(eps)}")
    print(f"Redistribution-cleared: {len(redistributable)}/{len(eps)}")
    print("Rights:", dict(rights))
    print("Selected-source resolutions:", dict(resolutions))

if __name__ == "__main__":
    main()
