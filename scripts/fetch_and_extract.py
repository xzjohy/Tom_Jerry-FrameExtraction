#!/usr/bin/env python3
"""Fetch one direct HTTP(S) media file, then run the frame extractor.

Use only direct media URLs that are accessible to your environment.
No DRM/access-control bypass is implemented.
"""
from __future__ import annotations
import argparse, subprocess, sys, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("episode_id")
    p.add_argument("--work",type=Path,default=ROOT/"work")
    p.add_argument("--count",type=int,default=50)
    p.add_argument("--trim-start",type=float,default=25)
    p.add_argument("--trim-end",type=float,default=20)
    a=p.parse_args()
    video_dir=a.work/"videos"; video_dir.mkdir(parents=True,exist_ok=True)
    suffix=Path(urllib.parse.urlparse(a.url).path).suffix or ".mp4"
    video=video_dir/f"{a.episode_id}{suffix}"
    req=urllib.request.Request(a.url,headers={"User-Agent":"Mozilla/5.0"})
    print(f"Downloading {a.url}")
    with urllib.request.urlopen(req) as src, video.open("wb") as dst:
        while True:
            block=src.read(1024*1024)
            if not block: break
            dst.write(block)
    out=a.work/"frames"/a.episode_id
    cmd=[sys.executable,str(ROOT/"scripts"/"extract_frames.py"),str(video),str(out),
         "--count",str(a.count),"--trim-start",str(a.trim_start),"--trim-end",str(a.trim_end)]
    raise SystemExit(subprocess.run(cmd).returncode)

if __name__=="__main__":
    import urllib.parse
    main()
