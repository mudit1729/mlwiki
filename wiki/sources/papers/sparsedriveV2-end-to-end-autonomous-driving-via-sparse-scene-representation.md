---
title: "SparseDriveV2: Scoring is All You Need for End-to-End Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-25
year: 2026
venue: arXiv
tags:
  - paper
  - autonomous-driving
  - end-to-end
  - sparse-representation
  - planning
citations: 0
arxiv_id: "2603.29163"
paper-faithfullness: audited-fixed
---

# SparseDriveV2: Scoring is All You Need for End-to-End Autonomous Driving

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2603.29163)**

## Overview

SparseDriveV2 by Sun et al. (2026) pushes the performance boundary of scoring-based trajectory planning by demonstrating that "scoring is all you need" -- given sufficient coverage of the action space, a simple score-and-select approach outperforms complex generative planners. The core innovation is a scalable trajectory vocabulary that factorizes spatiotemporal trajectories into geometric paths and velocity profiles, enabling combinatorial explosion of candidates (1024 paths x 256 velocities = 262,144 total) while remaining computationally tractable.

SparseDriveV2 achieves 92.0 PDMS and 90.1 EPDMS on NAVSIM using a lightweight ResNet-34 backbone, and 89.15 Driving Score with 70.00% Success Rate on Bench2Drive using a ResNet-50 backbone with all six cameras. The paper presents a systematic scaling study (using Hydra-MDP as a baseline) showing that planning performance improves consistently as trajectory anchors increase in density, without saturation before computational limits -- suggesting that larger vocabularies will yield further gains.

## Key Contributions

- **Factorized trajectory vocabulary**: Decomposes spatiotemporal trajectories into independent geometric paths (spatial) and velocity profiles (temporal), enabling 262,144 candidates from only 1024+256=1280 base elements
- **Scaling law for trajectory anchors**: Demonstrates that planning performance improves consistently as vocabulary density increases, with no saturation observed before memory limits
- **Two-stage scalable scoring**: Coarse factorized scoring with progressive filtering (128/64 → 20/20) prunes the 262K candidates to 400 composed trajectories, followed by fine-grained trajectory re-conditioning scoring
- **Metric supervision training**: Multi-task objectives including metric-based losses for safety, progress, comfort, and rule compliance aligned with the PDMS evaluation metric
- **92.0 PDMS on NAVSIM v1, 90.1 EPDMS on NAVSIM v2**: New state-of-the-art on NAVSIM with ResNet-34; also achieves 89.15 Driving Score / 70.00% Success Rate on Bench2Drive with ResNet-50

## Architecture / Method

![SparseDriveV2 framework overview](https://paper-assets.alphaxiv.org/figures-normalized/figures/2603.29163v1/high_level.png)

```
  ┌───────────────────────────────────────────────────────────┐
  │              Factorized Trajectory Vocabulary              │
  │                                                           │
  │  ┌─────────────────────┐    ┌──────────────────────────┐  │
  │  │ Geometric Paths     │    │ Velocity Profiles        │  │
  │  │ (1024 anchors)      │    │ (256 anchors)            │  │
  │  │ [straight, turn,    │    │ [accel, decel, const,    │  │
  │  │  lane change, ...]  │    │  stop, ...]              │  │
  │  └─────────┬───────────┘    └──────────┬───────────────┘  │
  └────────────┼───────────────────────────┼──────────────────┘
               │                           │
               ▼                           ▼
  ┌───────────────────────────────────────────────────────────┐
  │  Stage 1: Coarse Factorized Scoring                       │
  │  Score paths independently ──► 128 paths (layer 1) → 20  │
  │  Score velocities independently ──► 64 vels (layer 1) → 20│
  │  262,144 candidates ──► 400 composed trajectories         │
  └──────────────────────────┬────────────────────────────────┘
                             │
                             ▼
  ┌───────────────────────────────────────────────────────────┐
  │  Stage 2: Fine-Grained Scoring                            │
  │  Compose path + velocity ──► full trajectory              │
  │  Trajectory re-conditioning via scene interaction modules │
  │  400 ──► Best trajectory                                  │
  └──────────────────────────┬────────────────────────────────┘
                             │
                             ▼
  ┌───────────────────────────────────────────────────────────┐
  │  Metric Supervision: Safety + Progress + Comfort + Rules  │
  └───────────────────────────────────────────────────────────┘
```

The architecture extends [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] with a fundamentally new planning module:

**Backbone:** SparseDriveV2 uses a lightweight ResNet-34 (21.8M parameters) for NAVSIM experiments and ResNet-50 for Bench2Drive experiments.

**Factorized Vocabulary Construction:** Instead of directly discretizing the full trajectory space, SparseDriveV2 separates trajectories into two independent components:
- **Geometric paths** (1024 anchors): Describe the spatial shape of the trajectory (straight, left turn, lane change, etc.) as sequences of 2D waypoints
- **Velocity profiles** (256 anchors): Describe the temporal progression along a path (accelerate, decelerate, constant speed, stop)
- **Composition**: Any path can be combined with any velocity profile, yielding 1024 x 256 = 262,144 spatiotemporal trajectory candidates

![Trajectory factorization](https://paper-assets.alphaxiv.org/figures-normalized/figures/2603.29163v1/x1.png)

**Two-Stage Scoring Pipeline:**
- **Stage 1 (Coarse)**: Score paths and velocities independently using scene feature interactions via deformable aggregation modules. Progressive filtering retains top 128 paths and 64 velocities in the first decoder layer, then refines to top 20 paths and 20 velocities in the second layer, yielding 400 final composed trajectory hypotheses.
- **Stage 2 (Fine)**: Compose the selected paths and velocities into full trajectories. Each composed trajectory undergoes trajectory re-conditioning through additional scene interaction modules to account for spatiotemporal dependencies. Select the highest-scoring trajectory as the final plan.

![Scaling study](https://paper-assets.alphaxiv.org/figures-normalized/figures/2603.29163v1/efficiency.png)

**Metric Supervision:** Training losses are directly aligned with the PDMS evaluation metric, including sub-losses for:
- **Safety**: Collision probability with predicted agent trajectories
- **Progress**: Distance traveled toward the navigation goal
- **Comfort**: Smoothness of acceleration and jerk profiles
- **Rule compliance**: Lane keeping, speed limit adherence, traffic signal obedience

## Results

### NAVSIM v1 Benchmark

| Method | PDMS |
|---|---|
| UniAD | ~75 |
| VAD | ~78 |
| SparseDrive (V1) | ~85 |
| **SparseDriveV2** | **92.0** |

### NAVSIM v2 Benchmark

| Metric | Score |
|---|---|
| EPDMS (corrected protocol) | 90.1 |
| EPDMS* (original protocol) | 86.7 |
| Ego Progress | 91.1 |

### Bench2Drive Benchmark

| Metric | Score |
|---|---|
| Driving Score | 89.15 |
| Success Rate | 70.00% |
| Multi-Ability (mean) | 67.67 |

### Scaling Behavior

The motivating scaling study of Hydra-MDP shows performance gains from 1,024 to 16,384 anchors without saturation, suggesting insufficient action space coverage -- not inherent approach limitations -- constrained prior static vocabulary methods. In SparseDriveV2, scaling vocabulary from 512×128 to 1024×256 anchors improves EPDMS from 88.7 to 90.1.

![Qualitative navigation results](https://paper-assets.alphaxiv.org/figures-normalized/figures/2603.29163v1/navigation.png)

## Limitations

- The 262K vocabulary, while efficient through factorization, still requires significant memory and compute for scoring
- Factorized scoring in Stage 1 may prune good trajectories if path quality depends on velocity (e.g., a tight turn requires specific speed)
- The vocabulary is pre-defined and fixed; novel maneuvers not represented in the vocabulary cannot be executed
- Evaluated on NAVSIM v1, NAVSIM v2, and Bench2Drive; performance on fully closed-loop simulators (e.g., CARLA) is not reported
- The "scoring is all you need" claim assumes sufficient vocabulary coverage, which may not hold in out-of-distribution scenarios

## Connections

- Direct successor to [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] (SparseDrive V1), extending the sparse representation with factorized trajectory scaling
- Achieves SOTA on [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] (NAVSIM benchmark)
- The scoring-based planning contrasts with generative approaches like [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] (EMMA) which generates trajectories as tokens
- Trajectory vocabulary concept relates to [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] (MomAD) temporal consistency approach
- Vectorized scene representation builds on [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] (VAD)
- Planning evaluation connects to the benchmark design of [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] (CARLA closed-loop)
