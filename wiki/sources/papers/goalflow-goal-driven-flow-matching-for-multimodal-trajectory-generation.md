---
title: "GoalFlow: Goal-Driven Flow Matching for Multimodal Trajectory Generation"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - flow-matching
  - planning
  - trajectory-prediction
citations: ~25
arxiv_id: "2503.05689"
---

# GoalFlow: Goal-Driven Flow Matching for Multimodal Trajectory Generation

[Read on arXiv](https://arxiv.org/abs/2503.05689)

## Overview

GoalFlow (Horizon Robotics / HKU, CVPR 2025) introduces a goal-driven flow matching framework for multimodal trajectory generation in autonomous driving. The method achieves 90.3 PDMS on the NAVSIM benchmark -- the highest score reported at the time of publication -- while requiring only a single denoising step at inference, making it both accurate and extremely efficient.

Flow matching is a generative modeling framework that learns to transport samples from a simple prior distribution to the data distribution along straight-line paths, offering computational advantages over diffusion models. GoalFlow extends flow matching by conditioning the generation process on goal points, which provide high-level routing intent and help resolve the multimodality inherent in driving behavior. The combination of goal conditioning with flow matching enables the model to generate diverse, plausible trajectories aligned with navigation intent in a single forward pass.

## Key Contributions

- **Goal-driven flow matching for driving**: First application of conditional flow matching to trajectory planning with explicit goal conditioning, combining the efficiency of flow matching with interpretable goal-directed behavior
- **Single-step inference**: Unlike diffusion-based planners that need multiple denoising steps, GoalFlow generates high-quality trajectories in a single step, enabling very fast inference
- **90.3 PDMS on NAVSIM**: Establishes a new state-of-the-art on the NAVSIM benchmark, surpassing DiffusionDrive (88.1) and prior methods by a substantial margin
- **Goal-conditioned multimodality**: A vocabulary of clustered training-data endpoints (4096–8192 points) scored via Distance + DAC dual scoring naturally decomposes the multimodal trajectory distribution into mode-specific subproblems, improving both diversity and accuracy

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│              GoalFlow: Goal-Driven Flow Matching             │
│                                                             │
│  Multi-Camera Images + LiDAR                                │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────┐                           │
│  │  Transfuser-based BEV Encoder│                           │
│  │  (camera + LiDAR fusion)     │ ──► HD map seg, 3D bbox   │
│  └──────────────┬───────────────┘     (aux supervision)     │
│                 │                                           │
│                 │          Goal Point Vocabulary            │
│                 │       (N=4096-8192 clustered GT EPs)      │
│                 │                 │                         │
│                 │         ┌───────┴──────────────┐          │
│                 │         │ Dual Scoring:         │          │
│                 │         │  Distance Score       │          │
│                 │         │  DAC Score (shadow    │          │
│                 │         │  vehicle check)       │          │
│                 │         └───────┬──────────────┘          │
│                 │                 │ best goal g*             │
│                 └────────┬────────┘                         │
│                          ▼                                  │
│  ┌─────────────────────────────────────────┐                │
│  │   Flow Matching Trajectory Generator    │                │
│  │                                         │                │
│  │   x_0 ~ N(0, σ=0.1)  (128-256 samples) │                │
│  │     │                                   │                │
│  │     ▼                                   │                │
│  │   v_θ(x_0, t=0, c)  ◄── BEV features  │                │
│  │     │                     + goal g*     │                │
│  │     ▼  (single Euler step, 10.4ms)      │                │
│  │   x_1 = x_0 + v_θ   ──► trajectory     │                │
│  │                                         │                │
│  │   (shadow trajectory fallback if        │                │
│  │    goal appears unreliable)             │                │
│  └─────────────────────────────────────────┘                │
│                                                             │
│  Key: Single denoising step ──► 10.4ms inference            │
└─────────────────────────────────────────────────────────────┘
```

GoalFlow consists of three main components:

1. **Perception Module (Transfuser-based)**: Multi-view camera images and LiDAR data are fused into a Bird's Eye View (BEV) representation using a Transfuser-based architecture. Auxiliary supervision includes HD map segmentation and 3D bounding box detection tasks (both cross-entropy and L1 losses).

2. **Goal Point Construction Module**: A vocabulary of N candidate goal points (N=4096–8192) is built by clustering ground-truth trajectory endpoints from training data. At inference, each candidate is scored via a **dual scoring mechanism**:
   - *Distance Score*: softmax of negative Euclidean distance from the candidate to the ground-truth endpoint, measuring proximity.
   - *DAC Score (Drivable Area Compliance)*: binary evaluation placing a "shadow vehicle" at each candidate and checking whether it stays within the drivable area polygon.
   - Final selection uses weighted aggregation of both scores. A **shadow trajectory mechanism** defaults to non-guided trajectories when the best goal point appears unreliable.

3. **Flow Matching Trajectory Generator**: For each selected goal, a conditional flow matching model learns the velocity field v_θ(x_t, t) that transports a noisy sample x_0 ~ N(0, σ=0.1) to the data distribution along straight-line paths (x_t = (1-t)x_0 + t·x_1). The network encodes x_t, the time step, the goal point, and BEV features through Transformer attention layers. During inference 128–256 trajectory candidates are generated.

**Training losses** — three components:
- *Perception Loss*: cross-entropy for HD map segmentation and 3D bbox classification; L1 for locations.
- *Goal Loss*: cross-entropy supervising both the distance score and the DAC score predictions.
- *Planner Loss*: L1 minimizing the difference between predicted and ground-truth trajectory shifts.

**Inference**: GoalFlow evaluates the velocity field at t=0 and takes a single Euler step: x_1 = x_0 + v_θ(x_0, 0, c). Single-step inference runs in 10.4 ms (vs. 177.8 ms for multi-step), with only a 1.6% PDM score drop compared to the optimal multi-step result.

**Trajectory Selection**: The highest-scoring candidate (by the dual scoring mechanism) is selected; if the goal point appears unreliable the shadow trajectory mechanism falls back to non-guided generation.

## Results

| Method | PDMS (NAVSIM) | Steps | FPS |
|--------|--------------|-------|-----|
| GoalFlow | 90.3 | 1 | ~60 |
| DiffusionDrive | 88.1 | 2 | 45 |
| GenAD | 83.5 | 20 | ~3 |
| VAD | 80.8 | - | ~10 |
| UniAD | 79.2 | - | ~5 |

- **90.3 PDMS on NAVSIM**, +2.2 over DiffusionDrive and +9.5 over VAD
- Single-step inference at 10.4ms (6% of the 177.8ms multi-step baseline), with only 1.6% PDM drop
- Ablation progression: M0 base flow matching = 85.6, +Distance Score = 88.5, +DAC Score = 89.4, +Trajectory Scorer = 90.3
- Oracle goal points (GoalFlow†) reach 92.1 PDMS, approaching human driving ceiling of 94.8
- Goal vocabulary uses N=4096–8192 clustered endpoints; larger vocabularies and stronger image backbones consistently improve performance
- Flow matching outperforms diffusion for the single-step regime -- the straight-line interpolation paths enable better single-step approximation than DDIM/DDPM shortcuts
- Multimodal trajectory diversity is maintained through the goal point vocabulary: different selected goals produce distinct trajectory modes

## Limitations & Open Questions

- Open-loop evaluation on NAVSIM only; closed-loop simulation and real-world testing remain to be demonstrated
- The goal proposal module relies on accurate route information; degraded route inputs could significantly impact performance
- Single-step flow matching may sacrifice fine-grained trajectory quality compared to multi-step methods in complex scenarios
- The method's advantage over DiffusionDrive may partly stem from the goal conditioning rather than flow matching itself; ablations separating these factors would be valuable

## Connections

- [[wiki/concepts/autonomous-driving]] -- end-to-end trajectory planning
- [[wiki/concepts/planning]] -- generative trajectory planning with flow matching
- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] -- complementary diffusion-based approach on NAVSIM
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- vectorized planning baseline
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD modular E2E baseline
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- diffusion models, contrasted with flow matching
