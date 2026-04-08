---
title: "Drive-OccWorld: Driving in the Occupancy World"
type: source-summary
status: complete
updated: 2026-04-05
year: 2024
venue: "AAAI 2025"
tags:
  - paper
  - autonomous-driving
  - world-model
  - 3d-occupancy
  - planning
  - bev
  - prediction
citations: 49
arxiv_id: "2408.14197"
---

# Drive-OccWorld: Driving in the Occupancy World

📄 **[Read on arXiv](https://arxiv.org/abs/2408.14197)**

## Overview

Drive-OccWorld introduces a vision-centric 4D occupancy forecasting world model that directly integrates with end-to-end planning. The core premise is that current end-to-end driving models lack sufficient "world knowledge" for forecasting dynamic environments, leading to poor generalization and safety robustness. By building an explicit world model that predicts future 3D occupancy states, the system can "think ahead" multiple steps before committing to a trajectory.

The framework operates through an auto-regressive architecture with three main components: a history encoder that builds BEV representations from multi-view cameras, a memory queue with novel conditional normalization that maintains temporal context while addressing semantic discrimination and motion awareness, and a world decoder that predicts future BEV embeddings conditioned on ego actions. The predicted future states feed into an occupancy-based planner that evaluates candidate trajectories against agent safety, road safety, and learned cost functions.

A key capability is action-controllable generation: the model can simulate different future scenarios based on various ego actions (velocity, steering angle, trajectory waypoints, high-level commands), functioning as a neural simulator. Drive-OccWorld achieves 9.4% improvement in occupancy forecasting, 33% reduction in L2 planning error at 1-second horizon compared to UniAD, and demonstrates strong results on the AAAI 2024 benchmark.

## Key Contributions

- **4D occupancy world model for planning:** First system to directly integrate vision-centric 4D occupancy forecasting with end-to-end planning through auto-regressive prediction
- **Semantic-Conditional Normalization:** Addresses "ray-shaped patterns" in BEV embeddings through adaptive affine transformations based on voxel-wise semantic predictions
- **Motion-Conditional Normalization:** Accounts for ego-vehicle and agent movements through ego-pose transformation and predicted 3D backward centripetal flow
- **Action-controllable generation:** Supports conditioning on velocity, steering angle, trajectory waypoints, and high-level commands via unified Fourier embeddings, enabling neural simulation
- **Occupancy-based planning:** Evaluates candidate trajectories using a three-component cost function (Agent-Safety, Road-Safety, Learned-Volume) that reasons about predicted future occupancy

## Architecture / Method

```
┌──────────────────────────────────────────────────────────────┐
│                     Drive-OccWorld                            │
│                                                              │
│  Multi-view   ┌───────────────────┐                          │
│  Cameras ────►│  History Encoder  │                          │
│               │  (BEVFormer)      │                          │
│               └────────┬──────────┘                          │
│                        │ BEV embeddings                      │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────┐         │
│  │         Memory Queue + Conditional Norm         │         │
│  │  ┌─────────────────┐  ┌─────────────────────┐  │         │
│  │  │  Semantic-Cond.  │  │   Motion-Cond.      │  │         │
│  │  │  Normalization   │  │   Normalization     │  │         │
│  │  │  (fix ray-shape  │  │   (ego-pose xform   │  │         │
│  │  │   artifacts)     │  │   + 3D flow)        │  │         │
│  │  └─────────────────┘  └─────────────────────┘  │         │
│  └────────────────────┬────────────────────────────┘         │
│                       │                                      │
│  Ego Actions ────┐    │                                      │
│  (vel, steer,    │    ▼                                      │
│   waypoints)  ┌──┴────────────────────────────┐              │
│  Fourier emb. │       World Decoder           │              │
│  ────────────►│  (deform. self-attn +         │              │
│               │   temporal cross-attn +       │ Auto-        │
│               │   conditional cross-attn)     │ regressive   │
│               └───────────┬───────────────────┘ loop         │
│                           │ Future BEV embeddings            │
│                           ▼                                  │
│               ┌───────────────────────┐                      │
│               │ Occupancy Decoder     │                      │
│               │ ──► 3D semantic occ.  │                      │
│               │ ──► 3D flow           │                      │
│               └───────────┬───────────┘                      │
│                           ▼                                  │
│               ┌───────────────────────┐                      │
│               │ Occupancy Planner     │                      │
│               │ Cost = Agent-Safety   │                      │
│               │      + Road-Safety    │                      │
│               │      + Learned-Volume │                      │
│               └───────────┬───────────┘                      │
│                           ▼                                  │
│                   Best Trajectory                             │
└──────────────────────────────────────────────────────────────┘
```

![Drive-OccWorld system architecture](https://paper-assets.alphaxiv.org/figures/2408.14197v3/x2.png)

The architecture consists of three main stages operating in an auto-regressive loop:

**History Encoder:** Processes multi-view camera images using a BEVFormer-based architecture to extract multi-view geometry features and transform them into Bird's-Eye-View embeddings that capture spatial relationships across the scene.

**Memory Queue with Conditional Normalization:** Accumulates historical BEV features with two novel normalization mechanisms:
- *Semantic-Conditional Normalization:* Applies adaptive affine transformations based on per-voxel semantic predictions, addressing the ray-shaped artifacts that arise from perspective projection into BEV space
- *Motion-Conditional Normalization:* Incorporates ego-pose transformation matrices and predicted 3D backward centripetal flow to make the representation motion-aware

**World Decoder:** An auto-regressive transformer using deformable self-attention, temporal cross-attention, and conditional cross-attention to predict future BEV embeddings. Action conditioning is achieved through Fourier embeddings of ego actions (velocity, steering, trajectory waypoints, or high-level commands).

**Occupancy-Based Planner:** The predicted future BEV embeddings are decoded into semantic occupancy volumes and 3D flow. Candidate trajectories are evaluated using:
- *Agent-Safety Cost:* Penalizes trajectories that intersect with predicted occupied voxels
- *Road-Safety Cost:* Penalizes trajectories that leave drivable surface
- *Learned-Volume Cost:* A learned cost function that captures complex safety patterns beyond explicit rules

![Action-controllable generation](https://paper-assets.alphaxiv.org/figures/2408.14197v3/x5.png)

## Results

![Qualitative forecasting results](https://paper-assets.alphaxiv.org/figures/2408.14197v3/x4.png)

### Occupancy Forecasting

| Method | mIoU (weighted) | VPQ (flow) |
|---|---|---|
| Baseline | -- | -- |
| **Drive-OccWorld** | **+9.4% improvement** | **+5.1% improvement** |

### Planning Performance (nuScenes)

| Method | L2 @ 1s | L2 @ 2s | L2 @ 3s | Collision Rate |
|---|---|---|---|---|
| UniAD | 0.48 | 0.96 | 1.65 | -- |
| **Drive-OccWorld** | **0.32** | **0.75** | -- | Competitive |

Drive-OccWorld achieves a 33% reduction in L2 error at 1-second horizon (0.32 vs 0.48) and 22% reduction at 2-second horizon compared to UniAD. Ablation studies validate all normalization components, confirm cross-attention superiority for action conditioning, and show that each cost function component contributes to planning quality. The action-controllable generation demonstrates consistent and interpretable behavior across different ego actions.

## Limitations & Open Questions

- **Computational cost of 4D occupancy:** Predicting full 3D occupancy volumes at multiple future timesteps is computationally expensive; real-time deployment may require aggressive optimization or sparse representations
- **Autoregressive error accumulation:** Multi-step predictions may degrade over longer horizons as errors compound through the auto-regressive loop
- **Limited to camera-only input:** The BEVFormer-based encoder processes only camera images; fusion with LiDAR could improve depth accuracy for occupancy prediction

## Connections

- Extends the world model paradigm explored in [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] (WoTE) with explicit 4D occupancy forecasting
- BEV encoder builds on [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] (BEVFormer) spatial cross-attention
- Planning approach complements trajectory-based methods like [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) and [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] (VAD) with occupancy-based reasoning
- Occupancy prediction connects to the broader scene representation discussion in [[wiki/concepts/perception]] -- occupancy handles irregular objects that detection-based systems miss
- Evaluated on [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] (nuScenes)
