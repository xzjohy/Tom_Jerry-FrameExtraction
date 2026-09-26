#!/usr/bin/env python3
"""Validate that source metadata contains provenance and reuse information."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "sources" / "episodes.json"
REQUIRED = {"id", "title", "source_url", "rights_status"}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    errors = []
    seen = set()
    for i, ep in enumerate(data.get("episodes", []), 1):
        missing = REQUIRED - ep.keys()
        if missing:
            errors.append(f"episode #{i}: missing {sorted(missing)}")
        if ep.get("id") in seen:
            errors.append(f"episode #{i}: duplicate id {ep.get('id')}")
        seen.add(ep.get("id"))
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(seen)} episode source records validated.")


if __name__ == "__main__":
    main()
