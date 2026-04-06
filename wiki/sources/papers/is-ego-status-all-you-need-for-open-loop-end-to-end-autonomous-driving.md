---
title: "Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving?"
type: source-summary
status: complete
updated: 2026-04-05
year: 2023
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - evaluation
  - benchmark
  - end-to-end
citations: ~199
arxiv_id: "2312.03031"
---

# Is Ego Status All You Need for Open-Loop End-to-End Autonomous Driving?

[Read on arXiv](https://arxiv.org/abs/2312.03031)

## Overview

This paper (CVPR 2024, NVIDIA / Nanjing University) delivers a "wake-up call" to the autonomous driving research community by demonstrating that simple baselines using only ego vehicle status (velocity, acceleration, heading) can match or outperform complex end-to-end driving models on the standard nuScenes open-loop planning benchmark. The paper shows that 73.9% of nuScenes driving scenarios are straightforward (going straight at near-constant speed), and current evaluation metrics fail to distinguish genuine scene understanding from trivial extrapolation of ego motion.

The authors introduce two minimal baselines -- Ego-MLP (a simple MLP on ego status) and BEV-Planner (adding minimal BEV features) -- that achieve competitive performance with state-of-the-art methods like UniAD and VAD, revealing fundamental flaws in how the community evaluates planning. They also propose a novel Curb Collision Rate (CCR) metric that better measures road boundary adherence.

## Key Contributions

- **Exposure of evaluation weakness**: Demonstrates that ego status alone (without any perception) achieves competitive open-loop planning on nuScenes, invalidating claims of scene understanding
- **Dataset bias analysis**: Reveals that 73.9% of nuScenes consists of straight driving, making L2 displacement error dominated by trivial scenarios
- **Ego-MLP baseline**: A simple MLP taking only ego velocity/acceleration/heading as input achieves results competitive with complex E2E models
- **BEV-Planner baseline**: Adding minimal BEV features to Ego-MLP provides marginal additional benefit, showing perception features are underutilized by planners
- **Curb Collision Rate (CCR)**: Novel metric measuring road boundary violations, providing a more meaningful signal than average L2 error
- **Call for closed-loop evaluation**: Argues the field must transition to closed-loop reactive simulation for meaningful planning evaluation

## Architecture / Method

![Ego-MLP and BEV-Planner](https://paper-assets.alphaxiv.org/figures/2312.03031v2/x1.png)

### Ego-MLP Baseline

The simplest baseline takes only ego vehicle status as input:
- **Input**: Ego velocity, acceleration, heading rate (no camera images, no LiDAR, no maps)
- **Architecture**: A small MLP (3-4 layers) that directly regresses future waypoints
- **Output**: Planned trajectory (T future waypoints in BEV)

This baseline achieves L2 errors competitive with UniAD on nuScenes, demonstrating that the benchmark can be largely solved by extrapolating current ego motion.

### BEV-Planner

Adds minimal visual features to the Ego-MLP:
- **Input**: Ego status + BEV features from a standard image backbone
- **Architecture**: Ego-MLP augmented with cross-attention to BEV features
- **Output**: Planned trajectory

The marginal improvement from BEV features over pure ego status is small, indicating that complex perception pipelines contribute surprisingly little to open-loop planning scores.

### Dataset Analysis

![Dataset distribution](https://paper-assets.alphaxiv.org/figures/2312.03031v2/x2.png)

The paper provides detailed analysis of nuScenes trajectory distributions:
- 73.9% of scenarios are near-straight driving
- Velocity distribution is heavily concentrated around typical urban speeds
- Challenging scenarios (sharp turns, stops, yielding) are underrepresented
- This bias means average L2 error is dominated by easy cases where ego extrapolation suffices

### Curb Collision Rate (CCR)

![CCR metric](https://paper-assets.alphaxiv.org/figures/2312.03031v2/x3.png)

A new metric that measures the percentage of planned trajectories that cross road boundaries:
- Requires the planner to understand road geometry, not just extrapolate motion
- Ego-MLP performs significantly worse on CCR than methods with perception, providing a more meaningful differentiation
- CCR better correlates with actual driving safety than average L2

## Results

| Method | L2 1s (m) | L2 3s (m) | Col. Rate (%) | CCR (%) |
|--------|-----------|-----------|---------------|---------|
| Ego-MLP (no vision) | ~0.5 | ~1.9 | ~0.7 | high |
| BEV-Planner | ~0.4 | ~1.8 | ~0.6 | moderate |
| UniAD | 0.48 | 1.93 | 0.71 | lower |
| VAD | 0.41 | 1.76 | 0.57 | lower |
| ST-P3 | 1.33 | 2.90 | 1.27 | - |

- **Ego-MLP matches complex E2E models** on average L2 error, invalidating the metric as a measure of scene understanding
- **Velocity perturbation experiments** show that small changes to ego status input dominate planning output changes, confirming over-reliance on ego motion
- **Feature analysis** reveals that learned features in complex models converge to representations dominated by ego status information
- **CCR provides better differentiation**: Methods with genuine perception features significantly outperform Ego-MLP on curb collision rate
- **Training dynamics** show Ego-MLP converges much faster than complex models, confirming the shortcut is easy to learn

![Feature analysis](https://paper-assets.alphaxiv.org/figures/2312.03031v2/x4.png)

## Limitations & Open Questions

- The paper identifies the problem but does not fully solve it -- closed-loop evaluation is suggested but not provided
- CCR requires map annotations which may not always be available
- The analysis is specific to nuScenes; other datasets (Waymo, CARLA) may have different bias profiles
- Does not propose a new architecture that provably uses perception features -- only exposes that current ones do not
- The fundamental tension between dataset realism (most driving IS easy) and benchmark utility remains unresolved

## Connections

- [[wiki/concepts/autonomous-driving]] -- evaluation methodology for E2E driving
- [[wiki/concepts/end-to-end-architectures]] -- critique of sequential E2E pipelines
- [[wiki/concepts/planning]] -- planning evaluation metrics and benchmarks
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, a primary target of the critique
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- VAD, another method shown to barely outperform Ego-MLP
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- the dataset whose evaluation is critiqued
- [[wiki/sources/papers/para-drive-parallelized-architecture-for-real-time-autonomous-driving]] -- concurrent work also evaluating on nuScenes
