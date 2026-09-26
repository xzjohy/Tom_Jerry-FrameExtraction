#!/usr/bin/env python3
"""Batch-extract episodes from a local/private video directory.

Expected filename matching: filenames begin with 001..114, e.g.
001 Puss Gets the Boot.mkv
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"sources"/"episodes.json"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("video_dir",type=Path)
    p.add_argument("--output",type=Path,default=ROOT/"work"/"frames")
    p.add_argument("--count",type=int,default=50)
    p.add_argument("--trim-start",type=float,default=25)
    p.add_argument("--trim-end",type=float,default=20)
    a=p.parse_args()
    eps={int(e["number"]):e for e in json.loads(CATALOG.read_text(encoding="utf-8"))["episodes"]}
    videos=[]
    for f in a.video_dir.iterdir():
        if not f.is_file(): continue
        m=re.match(r"^\s*(\d{1,3})\D",f.name)
        if m and int(m.group(1)) in eps: videos.append((int(m.group(1)),f))
    if not videos: raise SystemExit("No numbered episode files found.")
    failures=[]
    for n,f in sorted(videos):
        ep=eps[n]; out=a.output/ep["id"]
        cmd=[sys.executable,str(ROOT/"scripts"/"extract_frames.py"),str(f),str(out),
             "--count",str(a.count),"--trim-start",str(a.trim_start),"--trim-end",str(a.trim_end)]
        print(f"[{n:03d}/114] {ep['title']} <- {f.name}")
        r=subprocess.run(cmd)
        if r.returncode: failures.append(n)
    print(f"Finished: {len(videos)-len(failures)}/{len(videos)} successful.")
    if failures: raise SystemExit(f"Failed episode numbers: {failures}")

if __name__=="__main__": main()
