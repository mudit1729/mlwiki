---
title: Research Thesis
type: synthesis
status: draft
updated: 2026-04-05
tags:
  - thesis
  - synthesis
confidence: medium
---

# Research Thesis

This page should evolve as the wiki matures. Updated with evidence from the AutoVLA corpus (18 papers, 2018–2025) and Ilya Top 30 analysis.

## Current thesis

The most important shift in autonomy research is not simply from modular to end-to-end. It is from hand-authored interfaces to learned shared representations, with explicit structure retained only where it carries operational value.

## Consequences

- Perception, prediction, and planning will increasingly share representation layers.
- Language will matter more as supervision, introspection, and task control than as a driver-facing interface.
- Robotics VLA work will transfer unevenly: representation and grounding ideas will transfer faster than action abstractions.
- Closed-loop evaluation will remain the decisive filter for meaningful progress.

## Evidence from AutoVLA corpus (new)

### Supporting the thesis

- **EMMA (Waymo, 2025)** demonstrates that unified "everything as language tokens" works at industry scale — planning, perception, and road graph understanding share a single representation.
- **ORION (2025)** retains structured decomposition (QT-Former → LLM reasoning → generative planner) but with learned interfaces between stages, not hand-authored ones.
- **Senna (2024)** shows that decoupled reasoning (natural language bridge) + E2E planning outperforms tightly-coupled approaches — supporting "explicit structure where operationally valuable."
- **DriveMoE (2025)** shows that expert specialization (MoE) outperforms monolithic models, suggesting some structural decomposition persists as valuable.

### Refining the thesis

- **Language as intermediate reasoning is emerging as a durable pattern**, more than just supervision. Senna's human-readable bridge, ORION's planning token, and DriveLM's Graph VQA all use language-like structure between perception and planning.
- **RL is becoming essential beyond imitation.** AlphaDrive (GRPO-based RL) and Alpamayo-R1 (multi-stage with RL) both show SFT has a ceiling. This parallels the LLM trajectory (pretraining → SFT → RLHF).
- **World models complement rather than replace VLAs.** WoTE uses BEV world models for trajectory safety verification, not as the primary planner. This suggests world models are a verification layer, not a planning replacement.

### Partially challenging the thesis

- **Alpamayo-R1 (NVIDIA)** achieved real-world deployment at 99ms latency — suggesting that the "end-to-end with retained structure" direction works in production, but required extensive engineering (causal grounding, multi-stage training, RL) beyond just learning shared representations.
- **SimLingo** won CARLA challenge with vision-only input, no LiDAR — suggesting that sensor simplification, not just representation sharing, may matter more than expected.

## Refined thesis (post-AutoVLA)

The shift from hand-authored to learned interfaces remains the core trend. But the AutoVLA evidence suggests a more specific formulation:

**The winning architecture is a foundation model backbone with language-structured intermediate reasoning, trained beyond imitation (via RL), and verified by physics-aware world models — with explicit modular structure retained at the reasoning-to-action boundary.**

## What could falsify this thesis

- Repeated evidence that pure direct control scales better than hybrid planning abstractions.
- Strong real-world wins from language-heavy runtime interfaces in driving.
- Evidence that explicit modularization remains superior even after large-scale multimodal pretraining.
- **NEW:** Evidence that SFT-only VLAs match RL-enhanced VLAs at scale (would weaken the RL claim).
- **NEW:** Evidence that world-model-based planners outperform VLA + world-model-verifier architectures (would change the complementarity claim).

## Connections to Ilya Top 30

The Ilya reading list's emphasis on compression (MDL, Kolmogorov complexity) and complexity theory (complexodynamics, coffee automaton) aligns with the thesis: the shift to learned representations is fundamentally about learning to compress the driving task into the right abstractions, rather than hand-engineering them.
