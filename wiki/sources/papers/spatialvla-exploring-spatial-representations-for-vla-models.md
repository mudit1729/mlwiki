---
title: "SpatialVLA: Exploring Spatial Representations for VLA Models"
type: source-summary
status: active
updated: 2026-04-05
year: 2025
venue: arXiv
tags:
  - paper
  - robotics
  - vla
  - spatial-reasoning
  - 3d-perception
citations: 292
arxiv_id: "2501.15830"
---

# SpatialVLA: Exploring Spatial Representations for VLA Models

[Read on arXiv](https://arxiv.org/abs/2501.15830)

## Overview

SpatialVLA addresses a fundamental limitation of existing VLA models: they operate on 2D visual inputs despite robot manipulation requiring understanding of 3D spatial relationships. Developed by Shanghai AI Laboratory in collaboration with top Chinese universities, SpatialVLA introduces two core innovations -- Ego3D Position Encoding and Adaptive Action Grids -- to inject spatial awareness into the VLA framework. The model is trained on 1.1 million real-world robot demonstrations, achieving state-of-the-art zero-shot performance on SimplerEnv and 73% spatial accuracy on targeted spatial reasoning evaluations.

The key insight is that robot manipulation is inherently a 3D task: grasping requires understanding depth, relative positions, and object orientations that are ambiguous in 2D images. By converting monocular images into spatially-aware representations using estimated depth and 3D position encoding, SpatialVLA bridges the gap between 2D VLM pre-training and 3D robotic control.

## Key Contributions

- **Ego3D Position Encoding**: Transforms 2D image observations into spatially-aware representations by estimating depth, computing 3D positions in the robot's ego-centric frame, and applying sinusoidal encoding -- all without requiring explicit 3D sensors
- **Adaptive Action Grids**: Replaces uniform action discretization with Gaussian-distribution-based equal-probability intervals, concentrating resolution where actions are most likely and reducing quantization error
- **1.1M real episode pre-training**: Trained on one of the largest real-world robot datasets, spanning multiple embodiments and environments
- **Spatial Embedding Adaptation**: A lightweight post-training scheme that adapts pre-trained spatial embeddings to new robot setups without full retraining

## Architecture / Method

![SpatialVLA architecture with Ego3D encoding and adaptive action grids](https://paper-assets.alphaxiv.org/figures/2501.15830v5/x1.png)

```
  ┌──────────────────────────────────────────────────────────┐
  │                      SpatialVLA                          │
  │                                                          │
  │  ┌──────────┐     ┌───────────────────┐                  │
  │  │ RGB Image│────►│ Monocular Depth   │                  │
  │  └─────┬────┘     │ Estimator         │                  │
  │        │          └────────┬──────────┘                  │
  │        │                   │ per-pixel depth             │
  │        │                   ▼                             │
  │        │          ┌───────────────────┐                  │
  │        │          │ Back-project to   │                  │
  │        │          │ 3D (ego-centric)  │                  │
  │        │          └────────┬──────────┘                  │
  │        │                   │ 3D coordinates              │
  │        │                   ▼                             │
  │        │          ┌───────────────────┐                  │
  │        │          │ Sinusoidal 3D     │                  │
  │        │          │ Position Encoding │                  │
  │        │          └────────┬──────────┘                  │
  │        │                   │  Ego3D PE                   │
  │        ▼                   ▼                             │
  │  ┌──────────────────────────────┐                        │
  │  │ Vision Encoder               │                        │
  │  │ (patch embeds + Ego3D PE)    │                        │
  │  └──────────────┬───────────────┘                        │
  │                 │                                        │
  │  ┌──────────┐   │                                        │
  │  │ Task Text│───┤                                        │
  │  └──────────┘   ▼                                        │
  │          ┌──────────────┐                                │
  │          │ VLM Backbone  │                                │
  │          └──────┬───────┘                                │
  │                 ▼                                        │
  │  ┌──────────────────────────────┐                        │
  │  │ Adaptive Action Grids        │                        │
  │  │ (Gaussian equal-probability  │                        │
  │  │  bins per action dimension)  │──► Robot Actions       │
  │  └──────────────────────────────┘                        │
  └──────────────────────────────────────────────────────────┘
```

SpatialVLA's architecture augments a standard VLA pipeline with two key modules:

**Ego3D Position Encoding** works in three steps: (1) a monocular depth estimator predicts per-pixel depth from the RGB image, (2) depth values are back-projected into 3D coordinates using known camera intrinsics and the robot's ego-centric reference frame, (3) sinusoidal position encodings of the 3D coordinates are added to the image patch embeddings before they enter the VLM backbone. This gives the model explicit spatial information without requiring depth cameras or point clouds at inference time (only a learned depth estimator).

**Adaptive Action Grids** replace uniform discretization bins with bins derived from the Gaussian distribution of each action dimension in the training data. Bins are placed at equal-probability intervals of the fitted Gaussian, concentrating more bins around the mean (where most actions cluster) and fewer in the tails. This reduces quantization error for common actions while maintaining coverage of the full action range.

**Spatial Embedding Adaptation** enables transfer to new robots: when deploying to a new camera configuration or workspace, only the spatial embedding layers are fine-tuned while the rest of the model remains frozen, making adaptation fast and data-efficient.

## Results

| Benchmark | Metric | SpatialVLA | Previous SOTA | Improvement |
|-----------|--------|-----------|---------------|-------------|
| SimplerEnv (zero-shot) | Success rate | SOTA | - | New best |
| LIBERO | Success rate | Competitive | - | After adaptation |
| Franka tasks | Success rate | Strong | - | With spatial adaptation |
| WidowX (real-world) | Success rate | Strong | - | Real-world validation |
| Spatial accuracy | % correct | 73% | ~60% (baseline VLA) | +13% |

- State-of-the-art zero-shot performance on SimplerEnv, demonstrating that spatial representations improve generalization without task-specific fine-tuning
- Strong adaptation results on LIBERO, Franka, and real-world WidowX tasks using Spatial Embedding Adaptation
- Ablation studies confirm both Ego3D encoding and adaptive discretization contribute independently; combining them yields the best results
- Adaptive action grids provide statistically significant advantages over linear (uniform) discretization, particularly for fine-grained manipulation
- 73% spatial accuracy on targeted evaluations, substantially above baseline VLAs that lack explicit 3D reasoning

## Limitations

- Relies on a learned monocular depth estimator, which introduces errors in depth ambiguous scenes (reflective surfaces, transparent objects, thin structures)
- The Ego3D encoding assumes known camera intrinsics; deployment to new camera setups requires calibration
- Despite 1.1M episodes, the dataset is dominated by tabletop manipulation; spatial reasoning for navigation or aerial manipulation is not evaluated
- The Gaussian assumption for action distribution in adaptive grids may not hold for highly multimodal action spaces

## Connections

- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- SpatialVLA builds on the VLA paradigm established by OpenVLA, adding 3D spatial awareness
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] -- Lift-Splat-Shoot pioneered image-to-3D lifting for driving; SpatialVLA applies similar intuition to manipulation
- [[wiki/concepts/vision-language-action]] -- demonstrates that spatial representation is a critical design axis for VLAs
- [[wiki/concepts/perception]] -- monocular 3D perception for manipulation
- [[wiki/concepts/robotics]] -- spatial reasoning for dexterous manipulation
