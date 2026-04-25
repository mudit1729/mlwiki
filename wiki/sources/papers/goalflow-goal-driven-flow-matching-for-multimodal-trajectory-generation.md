---
title: "GoalFlow: Goal-Driven Flow Matching for Multimodal Trajectory Generation"
type: source-summary
status: complete
updated: 2026-04-25
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
paper-faithfullness: audited-fixed
---

# GoalFlow: Goal-Driven Flow Matching for Multimodal Trajectory Generation

[Read on arXiv](https://arxiv.org/abs/2503.05689)

## Overview

GoalFlow (Horizon Robotics / HKU, CVPR 2025) introduces a goal-driven flow matching framework for multimodal trajectory generation in autonomous driving. The method achieves 90.3 PDMS on the NAVSIM benchmark with 5 inference steps, while its fastest single-step setting runs in 10.4 ms and scores 88.9 PDMS. The result is best read as a strong accuracy-efficiency tradeoff rather than a simultaneous one-step SOTA claim.

Flow matching is a generative modeling framework that learns to transport samples from a simple prior distribution to the data distribution along straight-line paths, offering computational advantages over diffusion models. GoalFlow extends flow matching by conditioning the generation process on goal points, which provide high-level routing intent and help resolve the multimodality inherent in driving behavior. The combination of goal conditioning with flow matching enables the model to generate diverse, plausible trajectories aligned with navigation intent in a small number of inference steps.

## Key Contributions

- **Goal-driven flow matching for driving**: First application of conditional flow matching to trajectory planning with explicit goal conditioning, combining the efficiency of flow matching with interpretable goal-directed behavior
- **Fast few-step inference**: GoalFlow reaches its best reported score with 5 steps and also supports a 10.4 ms single-step mode with a modest score drop
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
│  │     ▼  (one-step mode: 10.4ms)          │                │
│  │   x_1 = x_0 + v_θ   ──► trajectory     │                │
│  │                                         │                │
│  │   (shadow trajectory fallback if        │                │
│  │    goal appears unreliable)             │                │
│  └─────────────────────────────────────────┘                │
│                                                             │
│  Key: 5-step best score; 1-step fastest mode                │
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

**Inference**: GoalFlow can evaluate the velocity field at t=0 and take a single Euler step: x_1 = x_0 + v_θ(x_0, 0, c). The paper's timestep ablation reports 90.3 PDMS at 5 steps / 49.0 ms, 89.9 PDMS at 20 steps / 177.8 ms, and 88.9 PDMS at 1 step / 10.4 ms.

**Trajectory Selection**: The highest-scoring candidate (by the dual scoring mechanism) is selected; if the goal point appears unreliable the shadow trajectory mechanism falls back to non-guided generation.

## Results

| Method / setting | PDMS (NAVSIM) | Steps | Inference time |
|--------|--------------|-------|-----|
| GoalFlow best reported | 90.3 | 5 | 49.0 ms |
| GoalFlow single-step mode | 88.9 | 1 | 10.4 ms |
| GoalFlow 20-step mode | 89.9 | 20 | 177.8 ms |
| DiffusionDrive | 88.1 | - | - |

- **90.3 PDMS on NAVSIM** at 5 inference steps, +2.2 over DiffusionDrive
- Single-step inference runs in 10.4 ms and scores 88.9 PDMS, a 1.6% relative drop from the 5-step best setting
- Ablation progression: M0 base flow matching = 85.6, +Distance Score = 88.5, +DAC Score = 89.4, +Trajectory Scorer = 90.3
- Oracle goal points (GoalFlow†) reach 92.1 PDMS, approaching human driving ceiling of 94.8
- Goal vocabulary uses N=4096–8192 clustered endpoints; larger vocabularies and stronger image backbones consistently improve performance
- Flow matching enables strong short-horizon inference because straight-line interpolation paths are easier to approximate with few steps than iterative diffusion trajectories
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
