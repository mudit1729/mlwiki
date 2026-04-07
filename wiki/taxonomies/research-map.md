---
title: Research Map
type: taxonomy
status: active
updated: 2026-04-05
tags:
  - taxonomy
  - map
---

# Research Map

Use this page to decide where new material belongs.

## Layer 1: Application domain

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/robotics]]
- [[wiki/concepts/machine-learning]]

## Layer 2: Stack component

- [[wiki/concepts/perception]]
- [[wiki/concepts/prediction]]
- [[wiki/concepts/planning]]

## Layer 3: Paradigm

- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/concepts/foundation-models]]

## Layer 4: Evaluation and deployment questions

For each new source, tag at least:

- open-loop vs closed-loop,
- simulation vs real-world,
- map dependence,
- sensor assumptions,
- action abstraction,
- data regime,
- deployment evidence.

## Source programs

| Program | Papers | Status |
|---------|--------|--------|
| [[wiki/sources/ilya-top-30]] | 30 | All ingested |
| [[wiki/sources/vla-and-driving]] | 25 (6 general VLA + 19 AutoVLA) | Active |
| [[wiki/sources/autonomous-driving-seminal-papers]] | 14 ingested, many queued | Active |
| [[wiki/sources/llm-seminal-papers]] | 8 ingested | Active |

## Routing guide for new papers

**If the paper is about...** → **Route to:**

- Language + driving action → [[wiki/sources/vla-and-driving]] + tag `vla`
- Driving perception/prediction/planning (no language) → [[wiki/sources/autonomous-driving-seminal-papers]]
- LLM/VLM architecture (not driving-specific) → [[wiki/sources/llm-seminal-papers]]
- Foundational ML / Ilya-adjacent → [[wiki/sources/ilya-top-30]]
- Generative models (diffusion, flow matching, VAE) → [[wiki/concepts/foundation-models]] under diffusion models section
- Robotics VLA → [[wiki/sources/vla-and-driving]] under general VLA section

## VLA sub-taxonomy (from AutoVLA analysis)

Papers in the VLA-driving space can be classified along these axes:

```
Language Role:        supervision ←→ reasoning ←→ runtime control ←→ action output
Action Space:         controls ←→ waypoints ←→ planner tokens ←→ language tokens
Architecture:         VLM+planner ←→ decoupled ←→ true VLA ←→ MoE
Evaluation:           open-loop ←→ closed-loop sim ←→ real-world
Training:             IL only ←→ IL+SFT ←→ IL+RL ←→ GRPO
```
