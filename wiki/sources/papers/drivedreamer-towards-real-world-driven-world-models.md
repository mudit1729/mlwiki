---
title: "DriveDreamer: Towards Real-World-Driven World Models for Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2023
venue: ECCV
tags:
  - paper
  - autonomous-driving
  - world-model
  - generation
  - video-prediction
citations: ~452
arxiv_id: "2309.09777"
---

# DriveDreamer: Towards Real-World-Driven World Models for Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2309.09777)

## Overview

DriveDreamer (ECCV 2024) is the first world model built entirely from real-world driving data, addressing fundamental limitations of prior approaches that relied on simulated environments. The system uses a diffusion-based architecture called Auto-DM (Autonomous-Driving Diffusion Model) to learn controllable video generation from real driving scenarios, enabling both high-fidelity driving video synthesis and action-conditioned future prediction.

The two-stage training pipeline progressively builds understanding: first learning static structural constraints (HD maps, 3D bounding boxes), then advancing to dynamic future prediction. DriveDreamer achieves an average L2 trajectory error of 0.29m in open-loop planning and reduces collision rates by approximately 21% compared to baselines, while also generating synthetic training data that significantly improves downstream 3D object detection.

## Key Contributions

- **First real-world-driven world model**: Entirely trained on real driving data rather than simulated environments, capturing the complexity of actual road scenarios
- **Auto-DM architecture**: Diffusion model with three conditional input types -- spatially aligned conditions (HD Maps), position conditions (3D bounding boxes), and text prompts for environmental attributes
- **Two-stage progressive training**: Stage 1 learns structural understanding from static scene elements; Stage 2 extends to temporal future prediction with action conditioning
- **Controllable generation**: Supports video generation conditioned on traffic layout, text descriptions, and driving actions simultaneously
- **Data augmentation utility**: Synthetic data from DriveDreamer measurably improves 3D object detection training, demonstrating practical value beyond planning

## Architecture / Method

![DriveDreamer overview](https://paper-assets.alphaxiv.org/figures/2309.09777v2/img-0.jpeg)

DriveDreamer's Auto-DM architecture integrates three types of conditional inputs into a diffusion denoising process:

1. **Spatially Aligned Conditions**: HD map rasterizations provide road topology and lane structure, encoded via a spatial encoder and injected into the diffusion UNet through cross-attention layers.

2. **Position Conditions**: 3D bounding boxes of traffic participants are projected into BEV (Bird's Eye View) and image planes, providing object-level layout constraints. These are encoded separately and fused with the map conditions.

3. **Text Prompts**: Natural language descriptions of environmental attributes (weather, time of day, traffic density) are encoded with a text encoder and provide global scene-level conditioning.

![Training pipeline](https://paper-assets.alphaxiv.org/figures/2309.09777v2/img-1.jpeg)

**Stage 1 -- Structural Understanding**: The model learns to generate single frames conditioned on HD maps and 3D boxes, ensuring spatial consistency and structural adherence to road layouts.

**Stage 2 -- Future Prediction**: The model extends to temporal sequences, learning to predict future frames conditioned on the current scene and planned driving actions. This enables action-conditioned video rollouts for planning evaluation.

![Auto-DM architecture](https://paper-assets.alphaxiv.org/figures/2309.09777v2/img-3.jpeg)

For planning, DriveDreamer generates multiple future rollouts conditioned on candidate action sequences, then selects the best trajectory based on predicted outcomes. This "imagination-based" planning approach parallels model-based RL.

## Results

| Metric | DriveDreamer | DriveGAN | Improvement |
|--------|-------------|----------|-------------|
| L2 trajectory error (m) | 0.29 | - | SOTA |
| Collision rate reduction | ~21% | baseline | significant |
| FID (video quality) | superior | baseline | - |
| 3D detection (w/ synthetic data) | improved | - | measurable |

- **Open-loop planning**: 0.29m average L2 error on nuScenes, competitive with specialized planners
- **Video generation quality**: Significantly outperforms DriveGAN in FID and structural adherence metrics
- **Data augmentation**: Adding DriveDreamer-generated synthetic data to 3D detection training improves detection performance, validating the realism of generated scenes
- **Controllability**: Successfully generates diverse scenarios by varying text prompts and traffic layouts

![Comparison results](https://paper-assets.alphaxiv.org/figures/2309.09777v2/img-5.jpeg)

## Limitations & Open Questions

- Open-loop evaluation only; closed-loop performance in reactive simulation is not validated
- HD map dependency limits applicability to map-free driving scenarios
- Video generation resolution and temporal horizon are constrained by computational cost
- The relationship between video generation quality and downstream planning performance is not fully characterized
- Single-camera generation; multi-view consistency for surround-view driving is not addressed

## Connections

- [[wiki/concepts/autonomous-driving]] -- world models for autonomous driving
- [[wiki/concepts/planning]] -- imagination-based planning via world model rollouts
- [[wiki/concepts/prediction]] -- future scene prediction for driving
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational diffusion model framework
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- primary evaluation dataset
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- E2E driving baseline
- [[wiki/sources/papers/end-to-end-learning-for-self-driving-cars]] -- pioneering E2E driving approach
