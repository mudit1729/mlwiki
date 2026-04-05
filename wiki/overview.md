---
title: Overview
type: overview
status: seed
updated: 2026-04-05
tags:
  - map
  - autonomy
  - ml
---

# Overview

This vault is organized around a practical question: how do machine learning, robotics, and foundation models change the design of real autonomy systems?

## Main axes

### System decomposition

The core autonomy decomposition remains [[wiki/concepts/perception]], [[wiki/concepts/prediction]], and [[wiki/concepts/planning]]. The wiki tracks both clean modular decompositions and modern attempts to collapse the stack into [[wiki/concepts/end-to-end-architectures]].

### Embodiment

[[wiki/concepts/robotics]] and [[wiki/concepts/autonomous-driving]] overlap but are not interchangeable. Robotics often has richer action spaces, more manipulation-centric tasks, and different safety envelopes; driving has extreme scale, partial observability, long-tail edge cases, and a tight connection between evaluation and deployment.

### Foundation-model influence

[[wiki/concepts/foundation-models]] and [[wiki/concepts/vision-language-action]] matter because they introduce reusable priors, language grounding, large-scale pretraining, and a new interface between perception and action. The wiki should treat transfer claims carefully: some translate cleanly, some are mostly narrative.

## What the wiki should answer well

- Which papers are actually foundational, and why?
- Which benchmarks are over-indexed relative to real deployment value?
- Where do modular systems still dominate?
- What does "end-to-end" mean in each paper, exactly?
- How should VLM/VLA progress in robotics be interpreted for autonomous driving?
- Which open problems are bottlenecked by data, simulation, evaluation, or architecture?

## Navigation

- Read [[wiki/taxonomies/research-map]] for the field breakdown.
- Read [[wiki/comparisons/modular-vs-end-to-end]] for the core systems debate.
- Read [[wiki/syntheses/research-thesis]] for the current high-level thesis.
- Read [[wiki/queries/open-questions]] for the active research agenda.

