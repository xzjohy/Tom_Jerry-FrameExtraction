# Source policy

This directory separates **episode identity** from **video provenance**.

- `metadata_source_url`: evidence for title/year/order.
- `video_source_url`: the exact video selected for processing.
- `rights_status`: whether frame redistribution is licensed, public-domain, unknown, or permission-required.
- `redistribution_allowed`: must stay false unless the selected source has a verified basis for redistribution.

## Source priority

1. Rights-cleared / licensed high-resolution master.
2. Official Warner Bros. / WB Kids / Warner Classics source for reference and quality comparison.
3. Other lawful source with explicit reuse terms.
4. User-supplied source that the user is authorized to process.

A streaming page being publicly viewable does **not** make its video or extracted frames redistributable.

## Quality target

Preferred source: 1080p or better, original aspect ratio, no burned-in subtitles, logos, borders, or interpolation. Avoid AI-upscaled copies when a genuine restoration/master is available.
