#!/usr/bin/env python3
"""Check a private/local extraction archive for completeness."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"sources"/"episodes.json"
def main():
 p=argparse.ArgumentParser();p.add_argument("frames_dir",type=Path);p.add_argument("--target",type=int,default=50);a=p.parse_args()
 eps=json.loads(CATALOG.read_text(encoding="utf-8"))["episodes"];ok=0
 for e in eps:
  d=a.frames_dir/e["id"]; m=d/"manifest.json"
  if not m.exists(): print(f"MISSING {e['number']:03d} {e['title']}");continue
  data=json.loads(m.read_text(encoding="utf-8")); n=data.get("frame_count",0)
  if n==a.target: ok+=1
  else: print(f"INCOMPLETE {e['number']:03d} {e['title']}: {n}/{a.target}")
 print(f"Complete: {ok}/{len(eps)} episodes ({ok*a.target} frames)")
if __name__=="__main__":main()
