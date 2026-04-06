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

This wiki tracks the convergence of machine learning, robotics, and foundation models into real autonomy systems — spanning 120+ papers from 2012 to 2026. The field has undergone three major shifts: from modular perception-prediction-planning pipelines ([[wiki/sources/papers/planning-oriented-autonomous-driving|UniAD]], [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving|VAD]]) to unified end-to-end architectures ([[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving|DriveTransformer]], [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving|DiffusionDrive]]); from imitation learning to RL-based planning ([[wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving|CarPlanner]], [[wiki/sources/papers/pi06-a-vla-that-learns-from-experience|π₀.₆]]); and from task-specific models to generalist Vision-Language-Action agents ([[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control|π₀]], [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots|GR00T N1]], [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world|Gemini Robotics]]).

## Main axes

### System decomposition

The core autonomy decomposition remains [[wiki/concepts/perception]], [[wiki/concepts/prediction]], and [[wiki/concepts/planning]]. UniAD ([[wiki/sources/papers/planning-oriented-autonomous-driving]]) unified these into one framework and won CVPR 2023 Best Paper. Since then, the field has moved further toward collapsing the stack: [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving|DriveTransformer]] (ICLR 2025) parallelizes all tasks in a single transformer, while [[wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving|DriveGPT]] (Waymo, ICML 2025) proved that LLM-style scaling laws hold for driving behavior models. See [[wiki/concepts/end-to-end-architectures]] for the full trajectory.

### Embodiment

[[wiki/concepts/robotics]] and [[wiki/concepts/autonomous-driving]] overlap but are not interchangeable. In 2025, dual-system VLA architectures independently emerged across Google DeepMind ([[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world|Gemini Robotics]]), Physical Intelligence ([[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control|π₀]]/[[wiki/sources/papers/pi05-a-vision-language-action-model-with-open-world-generalization|π₀.₅]]), NVIDIA ([[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots|GR00T N1]]), and Figure AI (Helix) — all separating slow VLM reasoning (7–10 Hz) from fast motor control (120–200 Hz). On the driving side, the same dual-system pattern appears in [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving|Senna]] and [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving|EMMA]].

### Foundation-model influence

[[wiki/concepts/foundation-models]] and [[wiki/concepts/vision-language-action]] are now central. [[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model|PaLM-E]] (562B, ICML 2023) and [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control|RT-2]] (CoRL 2023) established that web-scale VLMs can directly control robots. By 2025, [[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai|Cosmos]] provides world-model infrastructure, [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model|OpenVLA]] democratized 7B VLAs with 970K real demonstrations, and [[wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics|SmolVLA]] proved 450M-parameter VLAs can compete with 10× larger models.

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

