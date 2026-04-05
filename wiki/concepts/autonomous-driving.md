---
title: Autonomous Driving
type: concept
status: seed
updated: 2026-04-05
tags:
  - autonomy
  - driving
---

# Autonomous Driving

Autonomous driving is the central application domain of this wiki.

## Canonical decomposition

The traditional stack decomposes into [[wiki/concepts/perception]], [[wiki/concepts/prediction]], and [[wiki/concepts/planning]], with mapping, localization, control, and safety overlays.

## What makes driving distinct

- safety-critical operation at high speed,
- long-tail edge cases,
- severe train/deploy distribution mismatch,
- multi-agent interaction,
- partial observability,
- dependence on evaluation protocols that often fail to match deployment conditions.

## Recurring research tensions

- modular vs [[wiki/concepts/end-to-end-architectures]],
- map-heavy vs map-light systems,
- imitation vs reinforcement vs planning-heavy training,
- open-loop metric progress vs closed-loop reliability,
- human-readable intermediate representations vs latent internal state.

## Adjacent pages

- [[wiki/concepts/robotics]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/autonomous-driving-seminal-papers]]

