---
title: "SparseDrive: End-to-End Autonomous Driving via Sparse Scene Representation"
type: source-summary
status: complete
updated: 2026-04-05
year: 2024
venue: ICRA 2025
tags:
  - paper
  - autonomous-driving
  - end-to-end
  - sparse-representation
  - planning
citations: 181
arxiv_id: "2405.19620"
---

# SparseDrive: End-to-End Autonomous Driving via Sparse Scene Representation

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2405.19620)**

## Overview

SparseDrive by Sun et al. (ICRA 2025) proposes a paradigm shift from dense BEV-based end-to-end driving to fully sparse scene representations. The core argument is that dense BEV grids are wasteful: most cells are empty, and the computation spent on them doesn't contribute to planning quality. SparseDrive represents the entire driving scene using sparse instance features, anchor boxes, and polylines -- handling detection, tracking, prediction, and planning in a unified sparse framework.

The key insight is that motion prediction and planning share three overlooked similarities: both require modeling high-order bidirectional interactions among agents, both need rich semantic and geometric scene understanding, and both are inherently multi-modal problems with uncertainty. SparseDrive exploits these parallels through a symmetric sparse perception module and a parallel motion planner that handles prediction and planning jointly.

SparseDrive surpasses prior SOTA on nuScenes across all metrics, especially the safety-critical collision rate, while maintaining much higher training and inference efficiency than dense alternatives.

## Key Contributions

- **Fully sparse scene representation**: Replaces dense BEV grids with sparse instance features (anchor boxes for agents, polylines for map elements), scaling computation with scene complexity rather than spatial resolution
- **Symmetric sparse perception**: A unified architecture that handles 3D detection, online mapping, and multi-object tracking through symmetric query-based modules
- **Parallel motion planner**: Jointly handles motion prediction and ego planning through a shared architecture, exploiting the structural similarities between forecasting other agents and planning ego motion
- **Hierarchical planning selection**: Multi-modal trajectory generation with safety-aware selection that considers collision avoidance and traffic rule compliance
- **State-of-the-art efficiency**: Faster training and inference than dense BEV alternatives while achieving better performance

## Architecture / Method

![SparseDrive detection visualization](https://paper-assets.alphaxiv.org/figures/2405.19620v2/avoidance1.jpg)

```
  Multi-Camera Images (6x)
         │
         ▼
  ┌──────────────────┐
  │  Image Backbone   │  (ResNet-50/101)
  │  (Multi-View)     │
  └────────┬─────────┘
           │ multi-view features
           ▼
  ┌──────────────────────────────────────────────────┐
  │        Symmetric Sparse Perception               │
  │                                                  │
  │  ┌──────────────────┐  ┌──────────────────────┐  │
  │  │  Agent Queries    │  │  Map Queries         │  │
  │  │  (anchor boxes)   │  │  (anchor polylines)  │  │
  │  └────────┬─────────┘  └────────┬─────────────┘  │
  │           │  deformable          │  deformable    │
  │           │  cross-attn          │  cross-attn    │
  │           ▼                      ▼                │
  │  ┌────────────────┐  ┌────────────────────────┐  │
  │  │ 3D Detection   │  │ Online Mapping         │  │
  │  │ + Tracking      │  │ (lanes, edges, xwalks) │  │
  │  └────────┬───────┘  └────────┬───────────────┘  │
  └───────────┼───────────────────┼──────────────────┘
              └─────────┬─────────┘
                        ▼
  ┌──────────────────────────────────────────────────┐
  │          Parallel Motion Planner                 │
  │                                                  │
  │  ┌────────────────┐     ┌────────────────────┐   │
  │  │ Agent Motion   │     │ Ego Planning       │   │
  │  │ Prediction     │     │ (multi-modal)      │   │
  │  │ (multi-modal)  │     │                    │   │
  │  └────────┬───────┘     └────────┬───────────┘   │
  │           │                      │               │
  │           └──────────┬───────────┘               │
  │                      ▼                           │
  │           ┌─────────────────────┐                │
  │           │ Hierarchical Select │                │
  │           │ (safety + progress  │                │
  │           │  + rule compliance) │                │
  │           └────────┬────────────┘                │
  └────────────────────┼─────────────────────────────┘
                       ▼
                 Final Trajectory
```

SparseDrive consists of three main modules:

**1. Image Backbone + Sparse Feature Extraction:** Multi-camera images are processed by a backbone (ResNet-50/101). Instead of constructing a dense BEV grid, sparse 3D queries (anchor boxes for agents, anchor polylines for map elements) attend to multi-view image features via deformable cross-attention. Each query extracts features relevant to its spatial location from the images directly.

**2. Symmetric Sparse Perception:** Agent queries and map queries are processed through symmetric transformer layers. Agent queries predict 3D bounding boxes, velocities, and attributes. Map queries predict polylines (lane boundaries, road edges, crosswalks). Both use the same attention mechanism, allowing weight sharing and unified training. Temporal information is incorporated by propagating queries across frames for tracking.

**3. Parallel Motion Planner:** This is the core innovation. Rather than predicting agent futures and then planning separately, SparseDrive uses a shared architecture:
- **Agent motion prediction**: Agent queries attend to map context and other agents, producing multi-modal future trajectory distributions
- **Ego planning**: Ego queries attend to the same scene context and produce multi-modal ego trajectory candidates
- **Hierarchical selection**: Multiple trajectory candidates are scored based on safety (collision checking against predicted agent trajectories), progress (distance toward goal), and traffic rule compliance. The best candidate is selected as the final plan

The parallel design means prediction and planning share intermediate representations and can be trained jointly end-to-end.

## Results

### nuScenes Benchmark

**SparseDrive-B (ResNet101, 512×1408 input):**

| Metric | UniAD | VAD | SparseDrive-B |
|---|---|---|---|
| Detection mAP | 38.0 | -- | **49.6** (+11.6 vs UniAD) |
| Multi-Object Tracking AMOTA | 35.9 | -- | **50.1** (+14.2 vs UniAD) |
| Online Mapping mAP | 47.6 | 47.6 | **56.2** (+8.6 vs VAD) |
| Planning L2 (m) | 1.03 | 0.72 | **0.58** |
| Collision Rate | 0.31% | 0.21% | **0.06%** |

**SparseDrive-S (ResNet50, 256×704):** Achieves 9.0 FPS versus 1.8 FPS for UniAD.

SparseDrive achieves the best results across all metrics, with a particularly notable 71.4% reduction in collision rate compared to VAD. Training is 4.8× faster (SparseDrive-B) and 7.2× faster (SparseDrive-S) than UniAD, with inference 4.1× and 5.0× faster respectively.

## Limitations

- Sparse representation relies on good query initialization; if initial anchors miss objects, they cannot be recovered
- The parallel planner assumes that prediction and planning share sufficient structure for joint modeling; adversarial or highly unpredictable scenarios may violate this assumption
- Evaluated primarily in open-loop on nuScenes; closed-loop performance needs validation
- Multi-modal trajectory selection uses hand-designed scoring criteria rather than learned selection

## Connections

- Extends the vectorized paradigm from [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] to a fully sparse framework
- Directly evolved into [[wiki/sources/papers/sparsedriveV2-end-to-end-autonomous-driving-via-sparse-scene-representation]] which adds trajectory vocabulary scaling
- Query-based perception builds on [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] (deformable attention)
- Joint prediction-planning design relates to [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) but is fully sparse
- Map encoding connects to [[wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation]] (vectorized map representation)
- Evaluated on [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]]
- Benchmarked on [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] (NAVSIM) in V2
