---
title: Frontend Strategy
type: synthesis
status: draft
updated: 2026-04-05
tags:
  - frontend
  - hosting
  - obsidian
---

# Frontend Strategy

This page captures the hosting options for the wiki.

## Current recommendation

Use the included Flask app as the first hosted frontend.

Why:

- it matches the repo immediately,
- it can run on Railway without adding a build pipeline beyond Python dependencies,
- it is easy to extend with auth, richer search, or ingest actions later,
- it keeps markdown as the source of truth.

## Option comparison

### Flask viewer

Best when:

- the wiki will stay private or semi-private,
- custom workflows may be added later,
- Railway deployment simplicity matters,
- the markdown repo should remain the product surface.

### Quartz

Best when:

- the primary goal is a polished digital garden,
- Obsidian-style links, backlinks, graph view, and static hosting matter more than server-side custom logic,
- the site can be built as static output and deployed as a static service.

Quartz is probably the strongest Obsidian-native publishing frontend if the long-term goal is public read-only browsing.

### Flowershow

Best when:

- a richer docs/blog presentation is useful,
- Next.js-based site generation is acceptable,
- Obsidian-compatible publishing features are desired without building them from scratch.

### Obsidian Publish

Best when:

- managed publishing matters most,
- self-hosting is not required,
- Railway deployment is not a requirement.

## Recommended path

1. Start with Flask so the wiki is immediately readable and deployable.
2. If the vault becomes public-facing and mostly read-only, reevaluate Quartz.
3. If the product becomes more application-like, keep Flask and add search, auth, and source-ingest actions.

