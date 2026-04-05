# AGENTS.md

This repo is a persistent LLM-maintained research wiki for machine learning, autonomous driving, robotics, vision-language-action systems, end-to-end architectures, perception, prediction, and planning.

The agent is not acting as a chatbot. It is acting as the maintainer of a markdown knowledge base.

## Core responsibilities

1. Maintain `wiki/` as the durable knowledge layer.
2. Treat `raw/` as immutable source material.
3. Keep `index.md` current enough to navigate the vault.
4. Append concise, parseable entries to `log.md`.
5. Prefer updating existing pages over creating duplicates.
6. Record uncertainty, disagreement, and superseded claims explicitly.

## Directory structure

- `raw/`
  - Immutable source inputs.
  - `raw/inbox/` is the drop zone for new source files.
  - `raw/papers/` is the long-term local paper store.
  - `raw/assets/` stores downloaded images and figures.
- `wiki/`
  - `concepts/` canonical topic pages.
  - `sources/` source summaries, reading queues, and acquisition plans.
  - `comparisons/` direct comparisons between methods, paradigms, or benchmarks.
  - `syntheses/` higher-level theses and evolving research narratives.
  - `queries/` answers worth preserving.
  - `taxonomies/` maps, ontologies, and evaluation frameworks.
- `templates/`
  - Reusable markdown skeletons.

## Page conventions

### Frontmatter

Use YAML frontmatter when useful. Preferred keys:

- `title`
- `type`
- `status`
- `tags`
- `updated`
- `source_count`
- `confidence`

### Linking

- Prefer Obsidian-style wikilinks: `[[page-name]]`.
- Link important mentions the first time they appear in a page.
- Add backlinks by updating both sides when the relation is materially important.

### Naming

- Use lowercase kebab-case filenames.
- Keep filenames semantic, not conversational.
- Prefer one canonical page per concept.

## Source handling rules

1. Never modify files under `raw/`.
2. When a source is ingested, create or update a corresponding page under `wiki/sources/`.
3. Distinguish clearly between:
   - direct source claims,
   - the wiki's synthesis,
   - open questions,
   - contradictions with prior sources.
4. If citation counts matter, verify them from a current source at ingest time rather than hard-coding them from memory.
5. If an external skill such as AlphaXiv is unavailable, fall back to arXiv abstracts, project pages, OpenReview, Semantic Scholar, and the local raw source itself.

## Ingest workflow

When the user asks to ingest a source:

1. Read `index.md` and the most relevant existing wiki pages first.
2. Read the new source from `raw/`.
3. Write or update the source summary.
4. Update related concept pages.
5. Update comparisons or syntheses if the source changes a broader conclusion.
6. Update `index.md`.
7. Append a log entry using this format:

`## [YYYY-MM-DD] ingest | Short Source Title`

Then include 2-5 bullets summarizing what changed.

## Query workflow

When the user asks a research question:

1. Start from `index.md`.
2. Read the smallest set of relevant pages that can answer the question well.
3. Answer with citations to wiki pages and sources where possible.
4. If the answer produces durable value, store it in `wiki/queries/` or `wiki/comparisons/`.
5. Update `index.md` and `log.md` if a new page is created.

## Lint workflow

When asked to lint the wiki, check for:

- duplicate concept pages,
- orphan pages,
- dead-end source summaries that never influenced a concept page,
- stale benchmark claims,
- ambiguous terminology around e2e, modular, hybrid, VLM, VLA, world model, and planner,
- missing canonical pages for recurring ideas.

## Domain-specific rules

### Autonomous driving

- Always separate open-loop and closed-loop claims.
- Always note required inputs: cameras, lidar, radar, maps, routes, language, privileged state.
- Record whether a method is modular, hybrid, or e2e.
- Record whether results depend on simulation, offline logs, intervention data, or real-world deployment.

### Perception / prediction / planning

- Keep task definitions explicit.
- Distinguish benchmark performance from operational usefulness.
- Prefer comparisons that surface assumptions and failure modes, not just metrics.

### VLM / VLA / robotics transfer

- Note what transfers cleanly from robotics to driving and what breaks because of speed, safety, partial observability, or scale.
- Track embodiment assumptions separately from general multimodal reasoning claims.

### LLMs and foundation models

- Record whether a paper contributes architecture, training recipe, scaling law, alignment method, tool use, multimodal capability, or downstream systems insight.
- Link LLM pages into driving pages only when the transfer mechanism is concrete.

## Frontend rules

- The Flask app is a viewer, not the source of truth.
- The wiki lives in markdown; the app should stay thin and stateless.
- New UI features should improve reading, navigation, search, and synthesis browsing before adding product complexity.

