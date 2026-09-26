#!/usr/bin/env python3
"""Build api/episodes.json from per-episode manifests and source metadata."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_META = ROOT / "sources" / "episodes.json"
FRAMES = ROOT / "frames"
OUTPUT = ROOT / "api" / "episodes.json"


def main():
    source = json.loads(SOURCE_META.read_text(encoding="utf-8"))
    metadata = {e["id"]: e for e in source.get("episodes", [])}
    episodes = []

    for manifest_path in sorted(FRAMES.glob("*/manifest.json")):
        episode_id = manifest_path.parent.name
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        item = dict(metadata.get(episode_id, {}))
        item["id"] = episode_id
        item["frame_count"] = manifest["frame_count"]
        item["frames"] = [
            {
                **frame,
                "url_path": f"frames/{episode_id}/{frame['file']}",
            }
            for frame in manifest["frames"]
        ]
        episodes.append(item)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps({"version": 1, "episodes": episodes}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT} with {len(episodes)} episodes.")


if __name__ == "__main__":
    main()
