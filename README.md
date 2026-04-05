# ML Wiki

A pattern for building a persistent research wiki for machine learning, autonomous driving, robotics, VLA systems, end-to-end architectures, perception, prediction, and planning.

This repo is an idea file and working scaffold. It is designed to be used directly with an LLM agent such as Codex or Claude Code. The high-level pattern stays stable; the exact workflow, page formats, and ingestion rules should evolve with the domain.

## The core idea

Most research workflows with LLMs still look like retrieval over a pile of PDFs, notes, and bookmarks. The model re-discovers the same facts on every question, re-synthesizes the same comparisons, and forgets the work as soon as the chat ends. That is expensive and fragile for deep domains like autonomous driving or robotics, where good answers usually require connecting models, datasets, benchmarks, failure modes, and historical context across many sources.

This repo is set up around a different idea: the LLM maintains a persistent markdown wiki that sits between the raw papers and the user. When a new paper, article, benchmark sheet, or project page is added, the LLM does not just index it for later retrieval. It reads it, extracts the durable claims, updates existing concept pages, strengthens or revises comparisons, records open disagreements, and links the source into the broader research map.

The wiki is the compounding artifact. The synthesis is stored once and improved over time. Cross-references, contradictions, benchmark context, and evolving theses stay in the wiki instead of being recreated from scratch in every chat.

## Why this is useful for this domain

Autonomous driving, robotics, and modern foundation-model work are unusually cross-cutting:

- Perception papers depend on sensor assumptions, labeling regimes, and evaluation choices.
- Prediction and planning papers often differ more in problem framing and deployment assumptions than in the headline metric.
- End-to-end stacks borrow ideas from imitation learning, world models, transformers, multimodal pretraining, and control.
- Vision-language-action work spans general robotics and driving-specific instruction grounding, which makes terminology inconsistent across subfields.

A persistent wiki is useful because it can capture those cross-cutting links explicitly:

- which papers are foundational versus merely popular,
- which ideas transfer from robotics to driving and which do not,
- which claims depend on simulation, privileged inputs, HD maps, closed-loop evaluation, or offline replay,
- which architectures are modular, hybrid, or genuinely end-to-end.

## Architecture

There are three layers:

### 1. Raw sources

`raw/` holds immutable inputs: papers, clipped articles, benchmark pages, interview transcripts, project notes, figures, and datasets metadata. The LLM reads from these files but should never rewrite them.

### 2. The wiki

`wiki/` holds LLM-maintained markdown pages. These are the actual knowledge base: overviews, concept pages, comparisons, taxonomies, source summaries, synthesis pages, and query outputs worth keeping.

### 3. The schema

`AGENTS.md` tells the LLM how to behave as the wiki maintainer: directory conventions, page templates, citation rules, ingest workflow, query workflow, and lint expectations. This file is the control surface for the system.

## Operations

### Ingest

One source at a time is usually best for this domain. A typical ingest pass:

1. Read the raw source.
2. Write or update a source-summary page in `wiki/sources/`.
3. Update the relevant concept pages.
4. Update one or more comparison or synthesis pages if the source changes a broader thesis.
5. Update `index.md`.
6. Append a concise entry to `log.md`.

### Query

The LLM answers questions primarily from the wiki rather than directly from the raw corpus. If the answer reveals a durable comparison, new taxonomy, benchmark note, or synthesis, it should be written back into the wiki as a first-class page.

### Lint

Periodic maintenance should look for:

- stale benchmark claims,
- modular/e2e terminology drift,
- orphan pages,
- missing backlinks,
- concepts that appear in many pages but do not yet have their own canonical page,
- places where a web search or new paper would materially improve the wiki.

## Indexing and logging

Two files are special:

- `index.md` is the content catalog. It is the first file the LLM should read when orienting itself.
- `log.md` is the chronological history of ingests, syntheses, and maintenance passes.

This gives the system a lightweight navigation layer before any custom retrieval tooling is needed.

## Initial source program

The starting corpus in this scaffold focuses on six acquisition lanes:

1. Ilya's recommended or "top papers" reading list.
2. Seminal autonomous driving papers with durable impact in perception, prediction, and planning.
3. Vision-language and vision-language-action papers relevant to autonomous driving.
4. Seminal LLM and foundation-model papers that inform modern e2e stacks.
5. High-signal robotics VLA papers that transfer into driving.
6. Benchmark and system papers that expose real deployment constraints.

The repo already includes queue pages for these lanes in `wiki/sources/`.

## Frontend

This repo includes a lightweight Flask app for local browsing and Railway deployment. The goal is not to replace Obsidian as an editing environment; it is to provide a clean hosted viewer for reading, linking, search, and sharing.

Obsidian is still the best local IDE for the wiki itself. For hosting, the best option depends on priorities:

- if you want a static, Obsidian-native digital garden, Quartz is usually the cleanest fit;
- if you want managed publishing with minimal ops, Obsidian Publish is the simplest but not Railway-native;
- if you want a custom app layer and future authenticated workflows, the Flask app in this repo is the most extensible starting point.

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Then open `http://127.0.0.1:8080`.

## Deploy to Railway

This repo is prepared for Railway with:

- `requirements.txt`
- `Procfile`
- `runtime.txt`

The default process is `gunicorn app:app --bind 0.0.0.0:${PORT:-8080}`.

## Note

This scaffold is intentionally opinionated but incomplete. It gives the wiki a strong initial shape and enough infrastructure to start ingesting papers immediately. The correct next step is to use the repo with an LLM agent, ingest sources incrementally, and let the structure co-evolve with the research program.
