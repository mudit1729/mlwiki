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
---

# LAW: Enhancing End-to-End Autonomous Driving with Latent World Model

[Read on arXiv](https://arxiv.org/abs/2406.08481)

## Overview

LAW (CASIA, ICLR 2025) introduces a self-supervised latent world model that enhances end-to-end autonomous driving by learning to predict future latent states of the driving environment. Rather than predicting future observations directly in pixel or BEV space (which is computationally expensive and prone to compounding errors), LAW learns a compact latent representation of the world and trains a dynamics model to predict future latent states. This latent world model is used as an auxiliary training objective that enriches the driving policy's scene understanding without adding inference overhead.

The key insight is that a model that can predict what will happen next in latent space necessarily has a deeper understanding of scene dynamics, agent interactions, and physical constraints -- all of which are valuable for planning even if the world model itself is not used at inference time. LAW achieves state-of-the-art results across three benchmarks: nuScenes, NAVSIM, and CARLA, demonstrating the generality of the approach.

## Key Contributions

- **Self-supervised latent world model**: A dynamics model in latent space that predicts future scene states, trained entirely self-supervised without requiring ground-truth future labels
- **Auxiliary training objective**: The world model serves as a representation learning mechanism during training; it can be discarded at inference time, adding zero computational overhead to the driving policy
- **Multi-benchmark SOTA**: Achieves state-of-the-art results on nuScenes (planning metrics), NAVSIM (PDMS), and CARLA (driving score), demonstrating broad applicability
- **Latent dynamics learning**: The latent world model captures temporal dynamics, agent interactions, and environmental constraints in a compressed space, providing richer gradients for the planning module

## Architecture / Method

LAW augments a standard end-to-end driving architecture with a latent world model branch:

1. **Scene Encoder**: Multi-camera images are encoded into BEV features using a standard BEV encoder (e.g., BEVFormer-style with spatial cross-attention). The BEV features at each timestep form the basis for both planning and world modeling.

2. **Latent Space Construction**: BEV features are projected into a lower-dimensional latent space z_t via a learned encoder E. This latent space is designed to be compact yet information-rich, capturing the essential state of the driving scene.

3. **Latent World Model**: A temporal dynamics model predicts future latent states: z_{t+1} = f(z_t, a_t), where a_t is the ego action at time t. The dynamics model is implemented as a transformer that attends over the current latent state and action sequence to predict the next latent state. The prediction is trained with a contrastive or reconstruction loss against the actual future latent state z_{t+1} = E(BEV_{t+1}).

4. **Planning Head**: The standard planning module takes the enriched BEV features (which have been shaped by the world model's training signal) and outputs future waypoints. At inference time, only the scene encoder and planning head are used.

**Training**: Multi-task learning with three losses: (1) planning loss (L2 on waypoints), (2) latent prediction loss (MSE or contrastive between predicted and actual future latent states), (3) optional perception losses (3D detection, map segmentation). The latent prediction loss provides a self-supervised signal that does not require any additional annotations.

**Key Design Choices**:
- Latent space dimensionality is kept small (e.g., 256-512) to prevent the world model from memorizing rather than understanding
- Multi-step prediction (predicting 2-4 steps ahead) is more effective than single-step prediction
- Stop-gradient on the target latent state prevents representational collapse

## Results

| Benchmark | LAW | Previous SOTA | Metric |
|-----------|-----|---------------|--------|
| nuScenes | 0.28m | 0.31m (VAD) | L2 @ 3s |
| nuScenes | 0.18% | 0.22% (VAD) | Collision Rate |
| NAVSIM | 87.5 | 85.2 | PDMS |
| CARLA | 78.3 | 71.8 | Driving Score |

- **nuScenes**: 0.28m average L2 displacement at 3s horizon (previous SOTA: 0.31m), 18% reduction in collision rate compared to VAD
- **NAVSIM**: 87.5 PDMS, competitive with concurrent methods
- **CARLA**: 78.3 driving score in closed-loop evaluation, +6.5 over previous best, demonstrating strong closed-loop transfer
- **Ablation -- world model importance**: Removing the latent world model branch degrades performance by 8-12% across all benchmarks, confirming its value as a representation learning mechanism
- Multi-step prediction (3 steps ahead) outperforms single-step by ~3%, indicating that longer-horizon dynamics modeling provides richer training signal
- The latent world model adds zero inference latency since it is discarded after training
- Visualization shows that the latent space learns meaningful structure: similar driving scenarios cluster together, and latent trajectories reflect physical plausibility

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
