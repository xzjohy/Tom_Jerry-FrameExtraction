# Tom & Jerry Frame Extraction

A frame-extraction and static-API pipeline intended for e-paper / e-ink display projects.

> Use source videos only when you have permission to process and redistribute the resulting images. Repository access or online availability does not by itself grant redistribution rights. Non-commercial intent does not replace copyright permission.

## What it does

For each episode, the extractor ignores configurable opening/ending time, samples hundreds of candidates, removes near-duplicates using perceptual hashes, and selects up to 50 frames distributed across the episode.

Output example:

```text
frames/
  ep001-title/
    001_000045000ms.webp
    ...
    050_000420000ms.webp
    manifest.json
```

## Install

Python 3.10+ and OpenCV-compatible system libraries are recommended.

```bash
python -m pip install -r requirements.txt
```

## Extract one episode

Keep original videos outside Git. `sources/videos/` is ignored by default.

```bash
python scripts/extract_frames.py \
  sources/videos/episode.mp4 \
  frames/ep001-title \
  --count 50 \
  --trim-start 45 \
  --trim-end 30
```

The default 45-second opening and 30-second ending trims are adjustable per episode. Perceptual-hash filtering removes highly similar candidate frames before the final temporal selection.

## Source metadata

Register provenance in `sources/episodes.json` before publishing extracted images:

```json
{
  "episodes": [
    {
      "id": "ep001-title",
      "title": "Episode title",
      "year": 1940,
      "source_url": "https://example.invalid/source",
      "rights_status": "licensed | public-domain | permission-required",
      "license": "license name or notes"
    }
  ]
}
```

Validate it with:

```bash
python scripts/validate_sources.py
```

## Build the static API

After extraction:

```bash
python scripts/build_index.py
```

This generates `api/episodes.json`. Each frame record contains its timestamp, perceptual hash, filename, and repository-relative URL path, so a future HTTP API or CDN can consume the same data model.

## Repository layout

```text
.
├── api/
│   └── episodes.json
├── frames/
├── scripts/
│   ├── build_index.py
│   ├── extract_frames.py
│   └── validate_sources.py
├── sources/
│   └── episodes.json
├── .gitignore
├── requirements.txt
└── README.md
```

## Copyright

This project contains tooling and metadata. Do not add source video files or extracted copyrighted frames unless their license, public-domain status, or other authorization permits the intended use and redistribution.
