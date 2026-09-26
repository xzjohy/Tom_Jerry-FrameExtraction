#!/usr/bin/env python3
"""Validate episode provenance, video-source and redistribution metadata."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "sources" / "episodes.json"
REQUIRED = {"id", "number", "title", "year", "metadata_source_url",
            "rights_status", "redistribution_allowed"}
RIGHTS = {"permission-required", "licensed", "public-domain", "unknown"}


def main():
    data = json.loads(PATH.read_text(encoding="utf-8"))
    errors, seen_ids, seen_numbers = [], set(), set()
    episodes = data.get("episodes", [])

    for i, ep in enumerate(episodes, 1):
        missing = REQUIRED - ep.keys()
        if missing:
            errors.append(f"episode #{i}: missing {sorted(missing)}")
        if ep.get("id") in seen_ids:
            errors.append(f"episode #{i}: duplicate id {ep.get('id')}")
        if ep.get("number") in seen_numbers:
            errors.append(f"episode #{i}: duplicate number {ep.get('number')}")
        if ep.get("rights_status") not in RIGHTS:
            errors.append(f"episode #{i}: invalid rights_status")
        if ep.get("redistribution_allowed") and ep.get("rights_status") not in {"licensed", "public-domain"}:
            errors.append(f"episode #{i}: redistribution requires licensed/public-domain status")
        if ep.get("video_source_url") and not ep.get("video_source_type"):
            errors.append(f"episode #{i}: video_source_type required when video_source_url is set")
        seen_ids.add(ep.get("id"))
        seen_numbers.add(ep.get("number"))

    expected = data.get("collection", {}).get("episode_count")
    if expected is not None and len(episodes) != expected:
        errors.append(f"catalog count {len(episodes)} != declared {expected}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"OK: {len(episodes)} episode records validated.")


if __name__ == "__main__":
    main()
