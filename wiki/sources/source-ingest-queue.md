---
title: Source Ingest Queue
type: source-program
status: active
updated: 2026-04-05
tags:
  - sources
  - queue
---

# Source Ingest Queue

This is the master queue for source collection and ingest.

## Acquisition lanes

1. [[wiki/sources/ilya-top-30]]
2. [[wiki/sources/autonomous-driving-seminal-papers]]
3. [[wiki/sources/vla-and-driving]]
4. [[wiki/sources/llm-seminal-papers]]

## Intake workflow

For each source:

1. Save the raw artifact to `raw/inbox/` or `raw/papers/`.
2. Normalize filename to `year-short-title.pdf` when possible.
3. Create or update the matching `wiki/sources/` page.
4. Route updates into concept pages and comparisons.
5. Record unresolved questions that the source creates.

## Notes

- Citation-count thresholds should be verified at ingest time.
- For source discovery, use paper graphs and citations to expand outward from canonical papers rather than scraping arbitrary lists.
- If AlphaXiv-specific tooling is unavailable, use arXiv, OpenReview, Semantic Scholar, OpenAlex, and project pages.

