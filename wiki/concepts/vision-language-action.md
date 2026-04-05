---
title: Vision Language Action
type: concept
status: seed
updated: 2026-04-05
tags:
  - vla
  - vlm
  - multimodal
---

# Vision Language Action

This page tracks the bridge from multimodal understanding to action generation.

## Working definition

A VLA system consumes visual context and language-conditioned intent, then emits actions or action-relevant latent state. In robotics, actions may be motor commands or low-level policies. In driving, actions may be trajectories, waypoints, controls, or planner tokens.

## Important distinctions

- VLM vs VLA: understanding-only systems are not action models.
- language as supervision vs language as runtime interface,
- action tokens vs continuous controls,
- offline imitation vs interactive control.

## Driving-specific questions

- Does language add supervision, controllability, interpretability, or only presentation value?
- Can VLA-style pretraining reduce the amount of task-specific driving data needed?
- What is the right action abstraction for driving: controls, trajectories, anchors, or planner state?

## Related

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/sources/vla-and-driving]]

