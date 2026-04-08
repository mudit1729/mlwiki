---
title: "MomAD: Don't Shake the Wheel - Momentum-Aware Planning in End-to-End Autonomous Driving"
tags: [autonomous-driving, planning, end-to-end, trajectory-prediction]
status: active
type: paper
year: "2025"
venue: "CVPR"
citations: 60
arxiv_id: "2503.03125"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2503.03125)**

## Overview

End-to-end autonomous driving systems suffer from a critical limitation: temporal inconsistency. Current systems operate in a "one-shot" manner, making trajectory predictions based solely on the current perception frame. This leads to vehicle trembling (unstable consecutive predictions), vulnerability to temporary occlusions, and safety concerns from abrupt trajectory changes. MomAD (Momentum-Aware Driving) addresses these challenges by incorporating two types of "momentum" into end-to-end planning.

The framework introduces Trajectory Momentum (ensuring temporal coherence by selecting candidate trajectories that align with previously executed paths) and Perception Momentum (enriching current planning with historical context to improve long-horizon understanding). Two novel technical components implement these concepts: Topological Trajectory Matching (TTM) uses Hausdorff distance to select temporally consistent trajectory candidates, while the Momentum Planning Interactor (MPI) uses LSTM-based historical query fusion with cross-attention to inject perception momentum into planning.

MomAD achieves state-of-the-art results on nuScenes (0.60m L2 error, 0.09% collision rate) and introduces a new Trajectory Prediction Consistency (TPC) metric measuring planning stability. In closed-loop evaluation on Bench2Drive, it improves success rate by 16.3% over VAD and 8.4% over SparseDrive, with 7.2% better trajectory smoothness.

## Key Contributions

- Identifies temporal inconsistency as a critical but overlooked failure mode in end-to-end driving planners
- Introduces two forms of momentum: trajectory momentum (temporal coherence in trajectory selection) and perception momentum (historical context enrichment)
- Topological Trajectory Matching (TTM) module using Hausdorff distance for temporally consistent multi-modal trajectory selection
- Momentum Planning Interactor (MPI) with LSTM-based surrogate query and cross-attention for historical context fusion
- New Trajectory Prediction Consistency (TPC) metric and Turning-nuScenes dataset for evaluating planning stability

## Architecture / Method

```
┌───────────────────────────────────────────────────────────────┐
│                    MomAD Architecture                          │
│                                                               │
│  Multi-view ──► Sparse Perception ──► Instance Features       │
│  Images         Backbone              (agents + map)          │
│                                           │                   │
│                          ┌────────────────┴───────────────┐   │
│                          │                                │   │
│                          ▼                                ▼   │
│               ┌───────────────────┐          ┌─────────────┐  │
│               │ Trajectory Momentum│          │  Perception │  │
│               │ (TTM)             │          │  Momentum   │  │
│               │                   │          │  (MPI)      │  │
│               │ K candidates ──►  │          │             │  │
│               │ Hausdorff dist.   │          │ Hist. query │  │
│               │ vs. history ──►   │          │   ──► LSTM  │  │
│               │ Best-aligned      │          │   ──► Cross │  │
│               │ selection         │          │      Attn.  │  │
│               └────────┬──────────┘          └──────┬──────┘  │
│                        │                            │         │
│                        └──────────┬─────────────────┘         │
│                                   ▼                           │
│                        ┌────────────────────┐                 │
│                        │  Refined Trajectory │                 │
│                        │  (temporally smooth)│                 │
│                        └────────────────────┘                 │
└───────────────────────────────────────────────────────────────┘
```

![Architecture](https://paper-assets.alphaxiv.org/figures/2503.03125v3/img-0.jpeg)

MomAD builds upon sparse perception backbones (similar to SparseDrive) with a momentum-aware planning module. Multi-view images are processed into instance features for road agents and map elements.

**Topological Trajectory Matching (TTM):**
1. Generate K multi-modal candidate trajectories for the current timestep
2. Transform candidates and historical optimal trajectory into a common coordinate system via rotation and translation matrices
3. Apply Hausdorff distance to measure alignment -- captures maximum deviation between trajectory sets, ensuring both local and global alignment while being less sensitive to point density variations
4. Select the candidate best aligned with historical execution path

**Momentum Planning Interactor (MPI):**
1. Combine historical planning queries with their scores via element-wise multiplication
2. Process through LSTM to create a surrogate multi-modal query capturing temporal evolution
3. Cross-attention: current query attends to historical surrogate query
4. Generate refined trajectories using enriched query combined with current instance features

**Robust Instance Denoising:** Training-time controlled perturbations to instance features teach the model to filter perception noise.

## Results

![Results](https://paper-assets.alphaxiv.org/figures/2503.03125v3/img-2.jpeg)

### nuScenes (Open-Loop)

| Model | L2 Error (m) | Collision (%) | TPC (m) |
|-------|-------------|--------------|---------|
| UniAD | 1.03 | 0.31 | -- |
| VAD | 0.72 | 0.12 | -- |
| SparseDrive | 0.68 | 0.11 | 0.81 |
| **MomAD** | **0.60** | **0.09** | **0.54** |

### Turning-nuScenes (6-second horizon)

| Metric | Improvement vs SparseDrive |
|--------|--------------------------|
| Collision rate | -26% |
| TPC | -33.45% (better consistency) |
| L2 error | -25.30% |

### Bench2Drive (Closed-Loop)

| Model | Success Rate | Comfortness |
|-------|-------------|-------------|
| VAD | baseline | baseline |
| SparseDrive | +8.4% vs VAD | -- |
| **MomAD** | **+16.3% vs VAD** | **+7.2%** |

Inference speed: 7.8 FPS on RTX 4090.

## Limitations & Open Questions

- The LSTM-based historical query fusion adds sequential dependency that may limit parallelization and real-time performance at higher frame rates
- Evaluation on Bench2Drive closed-loop is encouraging but the gap between closed-loop simulation and real-world deployment remains unaddressed
- Whether momentum-aware planning composes well with VLA systems (which have their own temporal reasoning through autoregressive generation) is unexplored

## Connections

- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- VAD baseline; MomAD improves +16.3% success rate in closed-loop
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD baseline; MomAD addresses temporal consistency gap in joint E2E systems
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] -- Complementary approach: Senna addresses reasoning, MomAD addresses temporal consistency
- [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] -- Both address trajectory quality verification, from different angles (world model vs momentum)
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] -- Bench2Drive closed-loop evaluation environment
