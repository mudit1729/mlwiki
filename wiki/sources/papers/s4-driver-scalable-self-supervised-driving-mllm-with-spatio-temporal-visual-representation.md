---
title: "S4-Driver: Scalable Self-Supervised Driving MLLM with Spatio-Temporal Visual Representation"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: "CVPR"
tags:
  - paper
  - autonomous-driving
  - self-supervised
  - multimodal
  - language-model
  - perception
  - planning
citations: 16
arxiv_id: "2505.24139"
---

# S4-Driver: Scalable Self-Supervised Driving MLLM with Spatio-Temporal Visual Representation

📄 **[Read on arXiv](https://arxiv.org/abs/2505.24139)**

## Overview

S4-Driver is a self-supervised framework that adapts Multimodal Large Language Models (MLLMs) for autonomous vehicle motion planning. The system processes multi-view camera imagery to predict future trajectories directly, addressing two fundamental challenges: MLLMs' reliance on 2D representations when operating in 3D space, and the limited scale of annotated training data in public driving datasets.

The core insight is that annotation-free training can match or exceed supervised approaches when combined with architectural innovations that transform MLLMs' 2D visual representations into effective 3D spatio-temporal reasoning. Built on PaLI3-5B, S4-Driver introduces a hierarchical coarse-to-fine planning strategy using "meta-decisions" (high-level acceleration behavior descriptions generated through heuristics), a novel sparse 3D volume representation, and multi-frame temporal fusion -- all without requiring human annotations for perception or prediction tasks.

S4-Driver represents a paradigm shift toward annotation-free autonomous driving that can leverage vast unlabeled driving data. By eliminating dependence on expensive human labeling for perception and prediction tasks, the framework dramatically reduces the cost and time required to develop capable autonomous driving systems, demonstrating clear scaling benefits on datasets 100x larger than nuScenes.

## Key Contributions

- **Self-supervised MLLM for driving:** Achieves state-of-the-art motion planning without any human annotation for perception or prediction, using only raw driving data and self-supervised objectives
- **3D spatio-temporal visual representation:** Transforms 2D MLLM features into 3D volumes through dense volume projection, sparse volume representation, and local feature aggregation with relative position bias
- **Hierarchical meta-decision planning:** Introduces coarse-to-fine planning with heuristic-generated meta-decisions describing future acceleration behavior, eliminating annotation requirements
- **Multi-decoding strategy:** Generates K=16 plausible trajectories and averages them to counteract the conservative prediction problem inherent in imitation learning
- **Scalability validation:** Demonstrates consistent improvement with data scale on WOMD (100x larger than nuScenes), validating the self-supervised approach at scale

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                     S4-Driver Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │
│  │ Multi-View  │  │ Historical  │  │ Behavior Command   │   │
│  │ Cameras     │  │ Ego States  │  │ (meta-decision)    │   │
│  └─────┬──────┘  └─────┬──────┘  └─────────┬──────────┘   │
│        │               │                    │              │
│        ▼               │                    │              │
│  ┌───────────────┐     │                    │              │
│  │ PaLI3-5B      │     │                    │              │
│  │ Vision Encoder │     │                    │              │
│  └─────┬─────────┘     │                    │              │
│        │               │                    │              │
│        ▼               │                    │              │
│  ┌────────────────────────────────────┐     │              │
│  │  3D Spatio-Temporal Visual Module  │     │              │
│  │  ┌──────────────────────────────┐  │     │              │
│  │  │ Dense Volume Projection      │  │     │              │
│  │  │         ▼                    │  │     │              │
│  │  │ Sparse Volume Representation │  │     │              │
│  │  │         ▼                    │  │     │              │
│  │  │ Local Feature Aggregation    │  │     │              │
│  │  │   (3D position bias)         │  │     │              │
│  │  │         ▼                    │  │     │              │
│  │  │ Multi-Frame Temporal Fusion  │  │     │              │
│  │  └──────────────────────────────┘  │     │              │
│  └──────────────┬─────────────────────┘     │              │
│                 │                            │              │
│                 ▼                            ▼              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            PaLI3-5B Language Decoder                  │  │
│  │   Coarse: Meta-decision ("accelerating forward")     │  │
│  │   Fine:   Trajectory Waypoints (K=16 decoded)        │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         ▼                                  │
│               ┌──────────────────┐                         │
│               │ Averaged Planned │                         │
│               │    Trajectory    │                         │
│               └──────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

![S4-Driver architecture overview](https://paper-assets.alphaxiv.org/figures/2505.24139v2/F.png)

The architecture processes multi-view camera images, historical ego-vehicle states, and behavior commands through PaLI3-5B as a unified text interface. The key innovation is the 3D Spatio-Temporal Visual Representation module:

**Dense Volume Projection** projects 2D image features from the MLLM's vision encoder into 3D feature volumes centered on the ego-vehicle, creating a volumetric representation of the surrounding scene.

**Sparse Volume Representation** learns to retain only relevant voxels through adaptive sparse features. Ablation studies show the sparse volumes concentrate on semantically important regions (front area, road center), dramatically reducing computational cost while preserving planning-relevant information.

**Local Feature Aggregation** injects relative 3D position bias into attention mechanisms, enabling the MLLM to perform genuine 3D spatial reasoning rather than relying on implicit 2D heuristics.

**Multi-Frame Temporal Fusion** incorporates temporal information by ego-motion compensating historical frames and fusing multi-frame features, giving the model awareness of scene dynamics.

The hierarchical planning approach first generates coarse meta-decisions (e.g., "accelerating forward") then refines these into precise trajectory waypoints, decomposing the planning problem into manageable subtasks.

## Results

| Benchmark | Metric | S4-Driver | Comparison |
|---|---|---|---|
| nuScenes | Avg L2 (1-3s) | **0.31m** | OmniDrive: 0.33m, VAD: 0.37m, UniAD: 0.66m |
| WOMD | ADE@5s | **0.693** | Vanilla PaLI: 0.798, MotionLM: 0.697 |
| WOMD | bADE@5s | **0.928** | Vanilla PaLI: 1.069 |
| WOMD (scaled) | ADE@5s | **0.655** | Demonstrates scaling benefit |
| WOMD (scaled) | bADE@5s | **0.830** | Clear improvement with more data |

On nuScenes, S4-Driver achieves 0.31m average L2 error across 1-3 second horizons, outperforming all supervised baselines including OmniDrive (0.33m) and VAD (0.37m). On the proprietary WOMD-Planning-ADE benchmark (100x larger than nuScenes), it performs competitively against MotionLM (0.697 vs 0.693 ADE@5s) despite using only raw camera inputs versus MotionLM's richer inputs.

Meta-decision accuracy ranges 67-85% across driving behaviors. Ablation studies confirm that each component (sparse volumes, temporal fusion, multi-decoding, stronger backbones) contributes measurably, and that stronger MLLM backbones yield significant gains on large datasets.

## Limitations & Open Questions

- **Proprietary large-scale data:** The strongest results (S4-Driver*) rely on a large internal dataset not publicly available, making full reproduction difficult
- **Meta-decision heuristics:** The coarse planning stage relies on hand-designed heuristics for meta-decision generation; learning these end-to-end could improve performance
- **Closed-loop evaluation absent:** All evaluation is open-loop; the gap between open-loop metrics and closed-loop driving competence remains untested

## Connections

- Extends the MLLM-for-driving paradigm explored by [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] but eliminates the need for annotations
- Competes directly with supervised end-to-end systems like [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] and [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD)
- The BEV representation builds on the lift-splat paradigm from [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]]
- Self-supervised scaling philosophy parallels [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- more data improves performance predictably
