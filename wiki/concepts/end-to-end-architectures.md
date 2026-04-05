---
title: End to End Architectures
type: concept
status: seed
updated: 2026-04-05
tags:
  - e2e
  - systems
---

# End to End Architectures

This page tracks what "end-to-end" means across the literature.

## Warning

"End-to-end" is overloaded. Papers use it to mean at least four different things:

1. direct perception-to-control,
2. perception-to-trajectory with no explicit modular planner,
3. shared latent backbone with multiple supervised heads,
4. a system trained jointly even if it still exposes interpretable intermediate structure.

## Useful classification

- Modular: explicit intermediate representations with separately optimized components.
- Hybrid: shared representation plus structured heads or differentiable interfaces.
- End-to-end: action-centric training objective with minimal manually designed interfaces.

## What to track per paper

- required inputs,
- output type,
- training objective,
- whether intermediate supervision exists,
- open-loop and closed-loop evaluation,
- sim-only or real-world evidence.

## Related

- [[wiki/comparisons/modular-vs-end-to-end]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/planning]]

