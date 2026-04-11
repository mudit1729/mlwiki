---
title: "LAW: Enhancing End-to-End Autonomous Driving with Latent World Model"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: ICLR
tags:
  - paper
  - autonomous-driving
  - world-model
  - self-supervised
  - end-to-end
citations: ~40
arxiv_id: "2406.08481"
paper-faithfullness: audited-solid
---

# LAW: Enhancing End-to-End Autonomous Driving with Latent World Model

[Read on arXiv](https://arxiv.org/abs/2406.08481)

## Overview

LAW (CASIA, ICLR 2025) introduces a self-supervised latent world model that enhances end-to-end autonomous driving by learning to predict future latent states of the driving environment. Rather than predicting future observations directly in pixel or BEV space (which is computationally expensive and prone to compounding errors), LAW learns a compact latent representation of the world and trains a dynamics model to predict future latent states. This latent world model is used as an auxiliary training objective that enriches the driving policy's scene understanding without adding inference overhead.

The key insight is that a model that can predict what will happen next in latent space necessarily has a deeper understanding of scene dynamics, agent interactions, and physical constraints -- all of which are valuable for planning even if the world model itself is not used at inference time. LAW achieves state-of-the-art results across three benchmarks: nuScenes, NAVSIM, and CARLA, demonstrating the generality of the approach.

## Key Contributions

- **Self-supervised latent world model**: A dynamics model in latent space that predicts next-frame visual features, trained entirely self-supervised using MSE against actual future latents -- no ground-truth future labels required
- **Action-aware future prediction**: Ego vehicle trajectories are explicitly incorporated into the latent world model input (A_t = MLP(Concat(V_t, e_{W_t}))), enabling the model to account for the ego's own actions when predicting future scene states
- **Universal framework compatibility**: LAW is compatible with both perception-free (perspective-view latents) and perception-based (BEV latents) end-to-end driving architectures
- **Auxiliary training objective**: The world model serves as a representation learning mechanism during training; it is discarded at inference time, adding zero computational overhead to the driving policy
- **Multi-benchmark SOTA**: Achieves state-of-the-art results on nuScenes (planning metrics), NAVSIM (PDMS: 84.6), and CARLA (driving score: 70.1), demonstrating broad applicability

## Architecture / Method

```
┌─────────────────────────────────────────────────────────┐
│                   LAW Architecture                       │
│                                                         │
│  ┌────────────────┐                                     │
│  │ Multi-Camera    │                                     │
│  │ Images (t)      │                                     │
│  └───────┬────────┘                                     │
│          ▼                                              │
│  ┌────────────────┐                                     │
│  │ Image Backbone  │  (Swin-T / ResNet-34)               │
│  │ + View Attn     │  → Visual Latents V_t               │
│  └───────┬────────┘                                     │
│          │                                              │
│     ┌────┴─────────────────────┐                        │
│     ▼                          ▼                        │
│  ┌──────────────┐    ┌───────────────────┐              │
│  │ Waypoint Head │    │ Action-Aware      │              │
│  │ W_t (traj)    │───►│ Latents           │              │
│  └──────┬───────┘    │ A_t=MLP(V_t,e_Wt) │              │
│         │            └────────┬──────────┘              │
│         │                     ▼                         │
│         │            ┌───────────────────┐              │
│         │            │ Latent World Model│              │
│         │            │ (Transformer      │              │
│         │            │  blocks)          │              │
│         │            │ V̂_{t+1}=LWM(A_t) │              │
│         │            └────────┬──────────┘              │
│         │                     ▼                         │
│         │            ┌───────────────────┐              │
│         │            │  L_latent = MSE   │              │
│         │            │ (V̂_{t+1}, V_{t+1})│              │
│         │            └───────────────────┘              │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ L_waypoint   │  L_total = L_waypoint + L_latent      │
│  │ (traj loss)  │           (+ L_percep if perc-based)  │
│  └──────────────┘                                       │
│                                                         │
│  Inference: only Backbone + Waypoint Head (no LWM)      │
└─────────────────────────────────────────────────────────┘
```

LAW augments a standard end-to-end driving architecture with a latent world model branch. Two variants are described:

**Perception-Free Variant** (nuScenes, NAVSIM, CARLA):
- Image backbone (Swin-Transformer-Tiny for nuScenes; ResNet-34 for NAVSIM and CARLA) processes multi-view camera images into perspective-view latent features V_t via a view attention mechanism
- Learnable waypoint queries predict the ego vehicle's future trajectory W_t
- Action-aware latents are formed: A_t = MLP(Concat(V_t, e_{w_t})), fusing visual features with the flattened trajectory embedding
- Stacked transformer blocks (the latent world model) predict the next frame's visual features: V̂_{t+1} = LWM(A_t)
- Latent loss: L_latent = MSE(V̂_{t+1}, V_{t+1})

**Perception-Based Variant**:
- BEV queries project image features into a flattened BEV feature map, supporting intermediate perception tasks (motion prediction, map construction)
- Same latent world model is applied on top of BEV features
- Training on nuScenes uses a two-stage approach: initial perception training, then joint fine-tuning

**Training**: Total loss = L_waypoint + L_latent (+ perception losses for perception-based variants). The latent prediction loss is purely self-supervised, requiring no additional annotations beyond the ego trajectory.

**Key Design Choices**:
- Optimal prediction horizon is 1.5 seconds (validated through ablation); shorter windows are insufficient, longer windows degrade performance
- Explicitly conditioning on the ego trajectory (action-aware latents) is crucial; using visual latents alone provides substantially less benefit
- Transformer blocks for the latent world model significantly outperform linear projections and MLP-only architectures

## Results

| Benchmark | Setting | LAW | Previous SOTA | Metric |
|-----------|---------|-----|---------------|--------|
| nuScenes | Perception-based | 0.49m | 0.72m (VAD), 1.03m (UniAD) | Avg L2 |
| nuScenes | Perception-based | 0.19% | — | Avg Collision Rate |
| nuScenes | Perception-free | 0.61m | 0.71m (w/o LAW) | Avg L2 |
| nuScenes | Perception-free | 0.30% | 0.41% (w/o LAW) | Avg Collision Rate |
| NAVSIM | Perception-free | 84.6 | 84.0 (PARA-Drive, TransFuser) | PDMS |
| CARLA | Perception-free | 70.1 | 65.9 (DriveAdapter), 65.0 (ThinkTwice) | Driving Score |

- **nuScenes (perception-based)**: 0.49m average L2 (vs. 0.72m VAD, 1.03m UniAD), 0.19% average collision rate
- **nuScenes (perception-free)**: 0.61m average L2 and 0.30% collision rate, compared to 0.71m / 0.41% without the latent world model
- **NAVSIM**: 84.6 PDMS, surpassing PARA-Drive and TransFuser (both 84.0)
- **CARLA**: 70.1 driving score in closed-loop evaluation, vs. 65.9 (DriveAdapter) and 65.0 (ThinkTwice)
- **Ablation -- world model importance**: Adding the latent task reduces nuScenes perception-free L2 from 0.71m to 0.61m and collision rate from 0.41% to 0.30%
- **Ablation -- prediction horizon**: A 1.5-second window is optimal; shorter windows are insufficient and longer windows degrade performance
- The latent world model adds zero inference latency since it is discarded after training

## Limitations & Open Questions

- The world model is used only for training, not inference -- using it for test-time lookahead or planning could further improve performance but at computational cost
- The latent space may lose fine-grained spatial information needed for precise maneuvers (parking, tight gaps)
- Multi-step prediction accumulates errors in latent space; how far ahead the model can reliably predict is limited
- The approach requires temporal sequences during training, which may complicate training data pipelines compared to single-frame methods

## Connections

- [[wiki/concepts/autonomous-driving]] -- end-to-end driving with world models
- [[wiki/concepts/planning]] -- world-model-enhanced planning
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, modular E2E baseline
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- VAD baseline comparison
- [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] -- complementary occupancy-based world model for driving
- [[wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation]] -- related world model approach
