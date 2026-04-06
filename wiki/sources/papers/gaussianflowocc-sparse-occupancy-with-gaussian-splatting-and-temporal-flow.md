---
title: "GaussianFlowOcc: Sparse and Weakly Supervised Occupancy Estimation using Gaussian Splatting and Temporal Flow"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: ICCV 2025
tags:
  - paper
  - autonomous-driving
  - perception
  - 3d-occupancy
  - gaussian-splatting
  - temporal
citations: 19
arxiv_id: "2502.17288"
---

# GaussianFlowOcc: Sparse and Weakly Supervised Occupancy Estimation using Gaussian Splatting and Temporal Flow

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2502.17288)**

## Overview

GaussianFlowOcc (ICCV 2025) introduces a transformative approach to 3D semantic occupancy estimation for autonomous driving by replacing traditional dense voxel grids with sparse 3D Gaussian distributions. The key insight is that most driving scenes are dominated by free space -- dense voxel grids waste computation on empty regions. By representing occupied space as a sparse collection of 3D Gaussians, the method achieves dramatically better efficiency while improving accuracy.

The method combines three innovations: (1) sparse Gaussian representation instead of dense voxels, (2) a Gaussian Transformer with induced attention to avoid expensive 3D convolutions, and (3) a temporal flow module that estimates 3D motion for each Gaussian to handle dynamic objects. Trained with only 2D pseudo-labels (no expensive 3D annotations), GaussianFlowOcc achieves 51%+ mIoU improvement and 50x faster inference than prior SOTA on Occ3D-nuScenes.

## Key Contributions

- **Sparse Gaussian occupancy representation**: Replaces dense voxel grids with collections of 3D Gaussian distributions, focusing computation only on occupied regions
- **Gaussian Transformer with induced attention**: Avoids expensive 3D convolutions by using inducing-point attention mechanisms that scale efficiently with the number of Gaussians
- **Temporal flow module**: Estimates 3D flow vectors for each Gaussian to model dynamic object motion across frames, improving temporal consistency
- **Weak supervision from 2D pseudo-labels**: Trains using only 2D semantic pseudo-labels projected from pre-trained models, eliminating the need for costly 3D voxel annotations
- **Extreme efficiency**: 50x faster inference than current SOTA with 29% accuracy improvement on Occ3D-nuScenes

## Architecture / Method

![GaussianFlowOcc method overview](https://paper-assets.alphaxiv.org/figures/2502.17288v4/img-1.jpeg)

The architecture consists of four main components:

**1. BEV Feature Extraction:** Multi-camera images are encoded into BEV features using a standard backbone (e.g., ResNet + LSS).

**2. Gaussian Initialization:** From BEV features, a set of 3D Gaussians is initialized. Each Gaussian has a 3D center position, covariance (shape/orientation), opacity, and semantic feature vector. Unlike dense voxels that cover the entire volume, Gaussians are placed only in regions likely to be occupied.

**3. Gaussian Transformer:** The core module refines Gaussian parameters through self-attention and cross-attention layers. To handle the potentially large number of Gaussians efficiently, the transformer uses an induced attention mechanism -- a small set of inducing points summarize the Gaussian population, reducing the quadratic attention cost.

![Gaussian Transformer architecture](https://paper-assets.alphaxiv.org/figures/2502.17288v4/img-5.jpeg)

![Induced attention mechanism](https://paper-assets.alphaxiv.org/figures/2502.17288v4/img-6.jpeg)

**4. Temporal Flow Module:** For multi-frame input, each Gaussian is assigned a 3D flow vector predicting its motion to the next timestep. This enables temporal alignment without requiring explicit object tracking or association. The flow is estimated via a temporal attention module that attends to previous-frame Gaussians.

![Temporal module effectiveness](https://paper-assets.alphaxiv.org/figures/2502.17288v4/img-10.jpeg)

For supervision, Gaussians are rendered into 2D views using differentiable Gaussian splatting and compared against 2D semantic pseudo-labels from a pre-trained segmentation model.

## Results

![Performance comparison](https://paper-assets.alphaxiv.org/figures/2502.17288v4/img-3.jpeg)

### Occ3D-nuScenes Benchmark

| Method | mIoU | Supervision | Inference Speed |
|---|---|---|---|
| SurroundOcc | ~30% | Full 3D | 1x |
| GaussianOcc | ~31% | Self-supervised | ~10x |
| GaussianFlowOcc | **~39%** | **2D pseudo-labels** | **~50x** |

The method achieves 51%+ improvement in mIoU over prior weakly-supervised methods while being 50x faster at inference. The temporal flow module contributes a significant portion of the improvement on dynamic object classes.

![Qualitative results](https://paper-assets.alphaxiv.org/figures/2502.17288v4/img-9.jpeg)

## Limitations

- Weakly supervised with 2D pseudo-labels, so accuracy is bounded by the quality of the pseudo-label generator
- Sparse Gaussian representation may miss thin structures or small objects that don't generate enough support in the initial placement
- Temporal flow assumes approximately rigid motion per Gaussian; deformable objects may not be well handled
- Currently benchmarked only on nuScenes; generalization to other datasets needs validation

## Connections

- Directly builds on the Gaussian occupancy paradigm from [[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting]] but adds temporal flow and weak supervision
- Complements [[wiki/sources/papers/gaussrender-learning-3d-occupancy-with-gaussian-rendering]] which uses Gaussians as a rendering loss rather than the core representation
- Related to [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]] which models occupancy evolution as a world model
- BEV backbone builds on [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]]
- Temporal reasoning connects to [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] (temporal BEV attention)
- Evaluated on [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] benchmarks
