---
title: "GenAD: Generative End-to-End Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2024
venue: ECCV
tags:
  - paper
  - autonomous-driving
  - end-to-end
  - generative
  - trajectory-prediction
citations: ~189
arxiv_id: "2402.11502"
---

# GenAD: Generative End-to-End Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2402.11502)

## Overview

GenAD (ECCV 2024) reframes end-to-end autonomous driving as a generative modeling problem, simultaneously generating future trajectories for all traffic participants rather than following the traditional sequential perception-prediction-planning pipeline. The core insight is that jointly modeling ego and agent trajectories in a shared latent space captures interactions more naturally than cascaded modules.

The framework uses instance-centric scene representations with map-aware tokens, a VAE-based trajectory prior model that captures the structural properties of realistic vehicle trajectories, and a GRU-based temporal decoder for progressive waypoint generation. GenAD achieves state-of-the-art L2 displacement error of 0.91m, collision rate of 0.43%, and runs at 6.7 FPS on an RTX 3090.

## Key Contributions

- **Generative driving paradigm**: Recasts E2E driving as joint generative modeling of all agent trajectories rather than sequential perception-then-planning
- **Instance-centric scene representation**: Map-aware instance tokens with self-attention for ego-agent interaction modeling, replacing dense BEV grid representations
- **Trajectory prior via VAE**: Learns a latent prior that captures structural properties of realistic vehicle trajectories (smoothness, kinematic feasibility), providing strong inductive bias for generation
- **Progressive waypoint decoding**: GRU-based temporal model generates trajectories step-by-step, enabling autoregressive refinement at each timestep
- **State-of-the-art planning**: 0.91m L2, 0.43% collision rate on nuScenes -- best results at time of publication

## Architecture / Method

![GenAD paradigm comparison](https://paper-assets.alphaxiv.org/figures/2402.11502v3/img-0.jpeg)

GenAD consists of three primary components:

### 1. Instance-Centric Scene Representation

Multi-camera images are processed through a backbone and BEV encoder. Rather than using the full BEV grid directly, GenAD extracts instance-level tokens:
- **Map tokens**: Encode road topology, lane boundaries, and traffic elements
- **Agent tokens**: Represent each detected traffic participant
- **Ego token**: Represents the ego vehicle

These tokens interact through self-attention layers that model ego-agent and agent-agent relationships, with map tokens providing contextual grounding.

### 2. Trajectory Prior Modeling (VAE)

![Detailed architecture](https://paper-assets.alphaxiv.org/figures/2402.11502v3/img-1.jpeg)

A Variational Autoencoder learns a structured latent space of realistic trajectories:
- **Encoder**: Maps ground-truth trajectories to a latent distribution during training
- **Decoder**: Reconstructs trajectories from latent samples
- **Prior network**: Learns to predict the latent distribution from scene features alone (used at inference)

The VAE prior ensures generated trajectories satisfy physical constraints (smooth curvature, feasible velocities) without explicit kinematic modeling.

### 3. Latent Future Trajectory Generation

A GRU-based temporal decoder progressively generates waypoints:
- Takes the sampled latent code and scene features as input
- Generates waypoints autoregressively, conditioning each step on previously generated points
- Produces trajectories for both ego and surrounding agents simultaneously
- The joint generation captures interaction effects (e.g., yielding, following)

![Trajectory generation process](https://paper-assets.alphaxiv.org/figures/2402.11502v3/img-2.jpeg)

**Training** uses a multi-objective loss combining:
- VAE reconstruction and KL divergence losses for the trajectory prior
- Planning loss (L2 to ground truth ego trajectory)
- Auxiliary losses for perception (detection, map segmentation) to regularize the BEV features

## Results

| Method | L2 1s (m) | L2 3s (m) | Avg L2 (m) | Col. Rate (%) | FPS |
|--------|-----------|-----------|------------|---------------|-----|
| GenAD | **0.36** | **1.83** | **0.91** | **0.43** | 6.7 |
| UniAD | 0.48 | 1.93 | 1.03 | 0.71 | ~2 |
| VAD-Tiny | 0.46 | 1.76 | 0.93 | 0.57 | ~8 |
| ST-P3 | 1.33 | 2.90 | 1.93 | 1.27 | - |

![Qualitative results](https://paper-assets.alphaxiv.org/figures/2402.11502v3/img-3.jpeg)

- **0.91m average L2** displacement error -- SOTA on nuScenes planning at time of publication
- **0.43% collision rate** -- lowest among E2E methods
- **6.7 FPS** on RTX 3090 -- faster than UniAD (~2 FPS) due to efficient instance-centric design
- Ablations confirm that ego-agent interaction modeling and the VAE trajectory prior each provide significant improvements
- Removing the generative prior degrades collision rate substantially, confirming the value of learned trajectory structure

## Limitations & Open Questions

- Open-loop evaluation on nuScenes; the generative approach may particularly benefit from closed-loop validation where trajectory diversity matters
- The VAE prior assumes unimodal posterior per scenario; a more expressive generative model (e.g., diffusion) could better capture multimodal futures
- GRU-based decoding may struggle with very long-horizon predictions
- Runtime (6.7 FPS) is improved over UniAD but not yet real-time
- The instance-centric representation may lose fine-grained spatial information compared to dense BEV features

## Connections

- [[wiki/concepts/autonomous-driving]] -- generative E2E driving paradigm
- [[wiki/concepts/end-to-end-architectures]] -- generative vs. discriminative E2E approaches
- [[wiki/concepts/planning]] -- trajectory generation as planning
- [[wiki/concepts/prediction]] -- joint ego-agent trajectory prediction
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, primary sequential baseline
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- VAD comparison
- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] -- later diffusion-based generative planning
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- evaluation dataset
