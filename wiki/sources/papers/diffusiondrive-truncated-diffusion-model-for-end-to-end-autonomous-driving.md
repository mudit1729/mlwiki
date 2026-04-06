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
---

# DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2411.15139)

## Overview

DiffusionDrive (HUST/Horizon Robotics, CVPR 2025 Highlight) proposes a truncated diffusion model for end-to-end autonomous driving that achieves real-time inference while preserving the multimodal trajectory generation benefits of diffusion models. Standard diffusion models require many denoising steps starting from pure Gaussian noise, making them too slow for real-time driving. DiffusionDrive's key insight is to begin the reverse diffusion process not from random noise but from an anchored set of trajectory priors derived from the training data, dramatically reducing the number of denoising steps needed.

The method achieves 88.1 PDMS on the NAVSIM benchmark with only 2 denoising steps at 45 FPS, demonstrating that diffusion-based planning can meet real-time requirements without sacrificing trajectory quality or multimodality.

## Key Contributions

- **Truncated diffusion**: Starts denoising from a set of anchored trajectory priors instead of pure Gaussian noise, reducing required denoising steps from ~20-50 to just 2
- **Anchored trajectory initialization**: K-means clustering on training trajectories produces a diverse set of anchor trajectories that serve as starting points, capturing the multimodal distribution of driving behaviors
- **Real-time diffusion planning**: Achieves 45 FPS with 2 denoising steps, making diffusion models practical for deployment in autonomous driving
- **NAVSIM SOTA**: 88.1 PDMS on NAVSIM, establishing a new state-of-the-art at time of publication

## Architecture / Method

DiffusionDrive consists of three main components:

1. **Scene Encoder**: A BEV (Bird's Eye View) encoder processes multi-camera images and produces scene features. The encoder follows standard BEV perception pipelines with a backbone (e.g., ResNet-50 or Swin-T) and BEV projection.

2. **Anchor Trajectory Set**: The training trajectory distribution is clustered via K-means into K anchor trajectories (e.g., K=128). These anchors span the space of common driving behaviors (straight, left turn, right turn, lane changes at various speeds). At inference time, all K anchors are used as starting points for the truncated diffusion process.

3. **Truncated Diffusion Denoiser**: Instead of the standard forward diffusion process that adds noise until reaching pure Gaussian, the forward process is truncated at a small timestep T_trunc (e.g., T_trunc=5 out of T=1000). The reverse process starts from the noised anchor trajectories at T_trunc and denoises for only 2 steps. A transformer-based denoiser cross-attends between trajectory tokens and BEV scene features to produce refined trajectories. The best trajectory is selected via a learned scoring head.

The truncation strategy works because the anchor trajectories are already close to the target distribution -- they only need small refinements rather than generation from scratch. This is analogous to how warm-starting optimization from a good initial point requires fewer iterations.

**Training**: The model is trained with the standard diffusion denoising objective but only over the truncated range [0, T_trunc], with an additional trajectory scoring loss to learn which denoised anchor best matches the ground truth.

## Results

| Method | PDMS (NAVSIM) | Steps | FPS |
|--------|--------------|-------|-----|
| DiffusionDrive | 88.1 | 2 | 45 |
| VAD | 80.8 | - | ~10 |
| GenAD (full diffusion) | 83.5 | 20 | ~3 |
| Transfuser | 81.3 | - | ~15 |

- 88.1 PDMS on NAVSIM, surpassing prior methods by a significant margin
- Only 2 denoising steps required (vs. 20+ for standard diffusion planners)
- 45 FPS real-time inference, 10-15x faster than full diffusion baselines
- Maintains multimodal trajectory diversity through the anchor set -- different anchors capture different driving modes (e.g., lane change vs. straight)
- Ablations show that increasing anchor count K improves performance up to ~128, after which returns diminish
- Truncation timestep T_trunc=5 provides the best speed-quality tradeoff

## Limitations & Open Questions

- The anchor trajectory set is fixed after training -- it may not cover truly novel scenarios outside the training distribution
- K-means clustering assumes Euclidean distance in trajectory space, which may not capture semantic differences between driving behaviors
- Evaluation on NAVSIM is open-loop; closed-loop performance in reactive simulation remains to be validated
- The method relies on a good BEV representation; perception errors propagate directly to planning quality

## Connections

- [[wiki/concepts/autonomous-driving]] -- end-to-end driving planning
- [[wiki/concepts/planning]] -- diffusion-based trajectory planning
- [[wiki/concepts/end-to-end-architectures]] -- full perception-to-planning pipeline
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- baseline comparison on NAVSIM
- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] -- earlier E2E driving baseline
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational diffusion model framework
