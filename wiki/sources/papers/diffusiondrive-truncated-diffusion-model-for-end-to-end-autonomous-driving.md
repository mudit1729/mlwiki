---
title: "DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - diffusion
  - end-to-end
  - planning
citations: ~50
arxiv_id: "2411.15139"
paper-faithfullness: audited-solid
---

# DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2411.15139)

## Overview

DiffusionDrive (HUST/Horizon Robotics, CVPR 2025 Highlight) proposes a truncated diffusion model for end-to-end autonomous driving that achieves real-time inference while preserving the multimodal trajectory generation benefits of diffusion models. Standard diffusion models require many denoising steps starting from pure Gaussian noise, making them too slow for real-time driving. DiffusionDrive's key insight is to begin the reverse diffusion process not from random noise but from an anchored set of trajectory priors derived from the training data, dramatically reducing the number of denoising steps needed.

The method achieves 88.1 PDMS on the NAVSIM benchmark with only 2 denoising steps at 45 FPS, demonstrating that diffusion-based planning can meet real-time requirements without sacrificing trajectory quality or multimodality.

## Key Contributions

- **Truncated diffusion policy**: Starts denoising from an anchored Gaussian distribution centered around K-means clustered trajectory priors instead of pure Gaussian noise, reducing required denoising steps from ~20 to just 2
- **Anchored trajectory initialization**: K-means clustering on training trajectories produces K=20 anchor trajectories that serve as starting points, capturing the multimodal distribution of driving behaviors
- **Efficient Cascade Diffusion Decoder**: A cascaded decoder with spatial cross-attention to BEV and perspective view (PV) features via deformable attention, plus agent/map cross-attention
- **Real-time diffusion planning**: Achieves 45 FPS on an NVIDIA 4090 with 2 denoising steps, making diffusion models practical for deployment in autonomous driving
- **NAVSIM SOTA**: 88.1 PDMS on NAVSIM with a ResNet-34 backbone, establishing a new state-of-the-art at time of publication

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                      DiffusionDrive                         │
│                                                             │
│  Multi-camera    ┌──────────────────┐                       │
│  Images ────────►│  Scene Encoder   │                       │
│                  │  (ResNet-34 +    │                       │
│                  │   BEV + PV feat.)│                       │
│                  └────────┬─────────┘                       │
│                           │ BEV + PV features               │
│                           ▼                                 │
│  ┌──────────────┐   ┌──────────────────────────────────┐    │
│  │ K=20 Anchor  │   │ Cascade Diffusion Decoder        │    │
│  │ Trajectories ├──►│                                  │    │
│  │ (K-means     │   │  Noised anchors   Scene feats.   │    │
│  │  clusters)   │   │       │               │          │    │
│  └──────────────┘   │       ▼               ▼          │    │
│                     │  ┌─────────────────────────────┐ │    │
│  Forward diffusion  │  │ Deformable spatial cross-   │ │    │
│  truncated at       │  │ attention (BEV + PV) plus   │ │    │
│  T_trunc << T       │  │ agent/map cross-attention,  │ │    │
│                     │  │ timestep modulation, MLPs   │ │    │
│                     │  │ for score + offset          │ │    │
│                     │  └───────────┬─────────────────┘ │    │
│                     │              │ × 2 denoise steps │    │
│                     │              │ × 4 cascade stages│    │
│                     │              ▼                    │    │
│                     │  ┌───────────────────────┐       │    │
│                     │  │ K refined trajectories│       │    │
│                     │  │ + confidence scores   │       │    │
│                     │  └───────────┬───────────┘       │    │
│                     └──────────────┼────────────────────┘    │
│                                    ▼                        │
│                        Highest-confidence trajectory        │
│                          (45 FPS, 2 steps)                  │
└─────────────────────────────────────────────────────────────┘
```

DiffusionDrive consists of three main components:

1. **Scene Encoder**: A sensor-fusion backbone (ResNet-34 for the main NAVSIM result) produces both BEV and perspective-view (PV) features that the decoder attends to.

2. **Anchor Trajectory Set**: The training trajectory distribution is clustered via K-means into K=20 anchor trajectories. These anchors span the space of common driving behaviors (straight, left turn, right turn, lane changes at various speeds) and define an anchored Gaussian distribution that replaces the standard zero-mean Gaussian prior. At inference time, up to 20 noisy samples drawn around these anchors are used as starting points for the truncated diffusion process; the number of samples can be adjusted without retraining.

3. **Efficient Cascade Diffusion Decoder (~60M parameters)**: Instead of the standard forward diffusion process that adds noise until reaching pure Gaussian, the forward process is truncated at a small timestep T_trunc << T. The reverse process starts from the noised anchor trajectories and denoises for only 2 steps. Each decoder layer uses deformable spatial cross-attention to BEV and PV features, agent/map cross-attention, timestep modulation, and MLP heads that predict a confidence score and a coordinate offset for each trajectory. The decoder is cascaded over 4 stages (found to be the optimal balance in ablations). The trajectory with the highest predicted confidence is selected as the final plan.

The truncation strategy works because the anchor trajectories are already close to the target distribution -- they only need small refinements rather than generation from scratch. This is analogous to how warm-starting optimization from a good initial point requires fewer iterations.

**Training**: The model is trained with an L1 reconstruction loss on the denoised trajectories plus a binary cross-entropy classification loss on the per-trajectory confidence scores (which supervise proximity to the ground-truth trajectory).

## Results

| Method | PDMS (NAVSIM) | Steps | FPS |
|--------|--------------|-------|-----|
| **DiffusionDrive (ResNet-34)** | **88.1** | 2 | 45 |
| Transfuser (single-mode baseline) | 84.0 | - | 60 |
| Vanilla diffusion policy | 84.6 | 20 | 7 |
| Truncated diffusion (ablation) | 85.7 | 2 | 27 |
| UniAD | 83.4 | - | - |
| Hydra-MDP (challenge winner) | 86.5 | - | - |

- 88.1 PDMS on NAVSIM with a ResNet-34 backbone, surpassing prior methods including Hydra-MDP
- On nuScenes (open-loop), reports 0.57 m average L2 error and 0.08% collision rate
- Only 2 denoising steps required (vs. 20 for vanilla diffusion policy)
- 45 FPS real-time inference on an NVIDIA 4090, roughly 6x faster than a vanilla diffusion adaptation (7 FPS)
- Reaches 74% mode diversity, avoiding the mode collapse observed with vanilla diffusion
- Anchor count and number of sampled noises can be tuned at inference without retraining for a flexible diversity-quality tradeoff

## Limitations & Open Questions

- The K=20 anchor trajectory set is fixed after training -- it may not cover truly novel scenarios outside the training distribution
- K-means clustering assumes Euclidean distance in trajectory space, which may not capture semantic differences between driving behaviors
- NAVSIM evaluation uses a non-reactive simulator with PDMS metrics; fully reactive closed-loop performance remains to be validated
- The method relies on a good BEV/PV representation; perception errors propagate directly to planning quality

## Connections

- [[wiki/concepts/autonomous-driving]] -- end-to-end driving planning
- [[wiki/concepts/planning]] -- diffusion-based trajectory planning
- [[wiki/concepts/end-to-end-architectures]] -- full perception-to-planning pipeline
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- baseline comparison on NAVSIM
- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] -- earlier E2E driving baseline
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational diffusion model framework
