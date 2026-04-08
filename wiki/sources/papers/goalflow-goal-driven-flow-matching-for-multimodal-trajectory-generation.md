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
- **Goal-conditioned multimodality**: Goal points from the route planner naturally decompose the multimodal trajectory distribution into mode-specific subproblems, improving both diversity and accuracy

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│              GoalFlow: Goal-Driven Flow Matching             │
│                                                             │
│  Multi-Camera Images         Route Info                     │
│       │                         │                           │
│       ▼                         ▼                           │
│  ┌──────────────┐    ┌───────────────────┐                  │
│  │  BEV Encoder │    │ Goal Proposal MLP │                  │
│  │  (backbone + │    │                   │                  │
│  │  view xform) │    │ ──► g1, g2, ..gN  │                  │
│  └──────┬───────┘    │ ──► score & rank  │                  │
│         │            └────────┬──────────┘                  │
│         │                     │                             │
│         └─────────┬───────────┘                             │
│                   ▼                                         │
│  ┌─────────────────────────────────────────┐                │
│  │   Flow Matching Trajectory Generator    │                │
│  │                                         │                │
│  │   For each goal g_i:                    │                │
│  │                                         │                │
│  │   x_0 ~ N(straight-line to g_i)        │                │
│  │     │                                   │                │
│  │     ▼                                   │                │
│  │   v_θ(x_0, t=0, c)  ◄── BEV features  │                │
│  │     │                     + goal g_i    │                │
│  │     ▼  (single Euler step)              │                │
│  │   x_1 = x_0 + v_θ   ──► trajectory_i   │                │
│  │                                         │                │
│  └───────────────────┬─────────────────────┘                │
│                      ▼                                      │
│            ┌──────────────────┐                              │
│            │ Trajectory Scorer│                              │
│            │ (collision, comfort,                            │
│            │  goal alignment) │                              │
│            └────────┬─────────┘                              │
│                     ▼                                       │
│              Best Trajectory                                │
│                                                             │
│  Key: Single denoising step ──► ~60 FPS inference           │
└─────────────────────────────────────────────────────────────┘
```

GoalFlow consists of three main components:

1. **Scene Encoder**: Multi-camera images are processed through a BEV encoder to produce bird's-eye-view scene features. The encoder follows standard BEV perception practices (backbone + view transformation).

2. **Goal Proposal Module**: Given the high-level route, a lightweight MLP generates a set of candidate goal points representing where the vehicle could plausibly be at the end of the planning horizon. These goals capture the multimodality of driving behavior (e.g., staying in lane vs. changing lanes). A scoring network ranks goals based on scene context.

3. **Flow Matching Trajectory Generator**: For each goal, a conditional flow matching model generates the full trajectory connecting the current state to the goal. The flow matching formulation learns a velocity field v(x_t, t, c) that transports a sample x_0 from a simple prior (Gaussian centered on a straight-line path to the goal) to the data distribution at t=1. The velocity field is parameterized by a transformer that cross-attends to BEV features.

**Training**: The model is trained with the flow matching objective: L = ||v_theta(x_t, t, c) - (x_1 - x_0)||^2, where x_t = (1-t)*x_0 + t*x_1 is the interpolation between the prior sample x_0 and the ground truth trajectory x_1. Goal conditioning c includes both the goal point and scene features.

**Inference**: At test time, GoalFlow evaluates the velocity field at t=0 and takes a single Euler step to generate the trajectory: x_1 = x_0 + v_theta(x_0, 0, c). The single-step formulation works because the flow matching training with straight-line interpolation paths produces nearly straight velocity fields.

**Trajectory Selection**: Multiple goal-conditioned trajectories are scored by a learned evaluator that considers collision risk, comfort, and goal alignment. The highest-scoring trajectory is selected for execution.

## Results

| Method | PDMS (NAVSIM) | Steps | FPS |
|--------|--------------|-------|-----|
| GoalFlow | 90.3 | 1 | ~60 |
| DiffusionDrive | 88.1 | 2 | 45 |
| GenAD | 83.5 | 20 | ~3 |
| VAD | 80.8 | - | ~10 |
| UniAD | 79.2 | - | ~5 |

- **90.3 PDMS on NAVSIM**, +2.2 over DiffusionDrive and +9.5 over VAD
- Single-step inference at ~60 FPS, fastest among competitive methods
- Goal conditioning improves trajectory quality: ablating goals drops PDMS by ~4 points
- Flow matching outperforms diffusion for the single-step regime -- the straight-line interpolation paths enable better single-step approximation than DDIM/DDPM shortcuts
- Multimodal trajectory diversity is maintained through the goal proposal mechanism: different goals produce distinct trajectory modes
- Ablation on goal count shows 8-16 goal proposals provide the best accuracy-diversity tradeoff

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
