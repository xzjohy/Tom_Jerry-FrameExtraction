#!/usr/bin/env python3
"""Extract representative frames from one video.

Pipeline:
1. Ignore configurable intro/outro margins.
2. Sample a larger candidate pool across the remaining duration.
3. Remove visually near-identical frames with perceptual hashing.
4. Select up to N temporally distributed frames.
5. Save deterministic filenames and metadata.

Only process source videos you have permission to use.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import imagehash
import numpy as np
from PIL import Image


def phash_bgr(frame: np.ndarray) -> imagehash.ImageHash:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return imagehash.phash(Image.fromarray(rgb))


def read_frame(cap: cv2.VideoCapture, t: float):
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, frame = cap.read()
    return frame if ok else None


def extract(video: Path, output: Path, count: int, trim_start: float,
            trim_end: float, hash_distance: int, candidates: int) -> dict:
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0
    duration = total_frames / fps if fps > 0 else 0.0
    start = max(0.0, trim_start)
    end = max(start, duration - max(0.0, trim_end))
    if end <= start:
        raise ValueError("Trim settings leave no usable video.")

    output.mkdir(parents=True, exist_ok=True)
    sample_times = np.linspace(start, end, max(candidates, count * 4), endpoint=False)

    unique = []
    hashes = []
    for t in sample_times:
        frame = read_frame(cap, float(t))
        if frame is None:
            continue
        h = phash_bgr(frame)
        if hashes and min(h - old for old in hashes) <= hash_distance:
            continue
        hashes.append(h)
        unique.append((float(t), frame, str(h)))

    cap.release()
    if not unique:
        raise RuntimeError("No usable frames found.")

    # Pick temporally distributed items from the de-duplicated candidate pool.
    pick_n = min(count, len(unique))
    indices = np.linspace(0, len(unique) - 1, pick_n).round().astype(int)
    chosen = [unique[i] for i in indices]

    records = []
    for seq, (t, frame, h) in enumerate(chosen, 1):
        filename = f"{seq:03d}_{int(round(t * 1000)):09d}ms.webp"
        cv2.imwrite(str(output / filename), frame, [cv2.IMWRITE_WEBP_QUALITY, 90])
        records.append({"index": seq, "timestamp": round(t, 3), "file": filename, "phash": h})

    manifest = {
        "source_file": video.name,
        "duration": round(duration, 3),
        "trim_start": trim_start,
        "trim_end": trim_end,
        "requested_count": count,
        "frame_count": len(records),
        "frames": records,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--count", type=int, default=50)
    p.add_argument("--trim-start", type=float, default=45.0)
    p.add_argument("--trim-end", type=float, default=30.0)
    p.add_argument("--hash-distance", type=int, default=6)
    p.add_argument("--candidates", type=int, default=500)
    args = p.parse_args()
    manifest = extract(args.video, args.output, args.count, args.trim_start,
                       args.trim_end, args.hash_distance, args.candidates)
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
