---
title: "GaussRender: Learning 3D Occupancy with Gaussian Rendering"
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
  - gaussian-rendering
citations: 13
arxiv_id: "2502.05040"
paper-faithfullness: audited-clean
---

# GaussRender: Learning 3D Occupancy with Gaussian Rendering

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2502.05040)**

## Overview

GaussRender by Chambon et al. (Valeo AI / Sorbonne, ICCV 2025) introduces a plug-and-play training-time module that improves 3D occupancy prediction by enforcing projective consistency between predicted 3D voxels and their 2D camera projections. The key idea is simple but effective: project both predicted and ground-truth 3D occupancy grids into 2D camera views using differentiable Gaussian splatting, then penalize configurations where the projections disagree. This catches 3D errors that volumetric losses miss -- a prediction can have correct voxel occupancy but produce physically impossible 2D projections.

GaussRender is architecture-agnostic, requiring no modifications to the base occupancy model and adding zero inference-time cost (the rendering is only used during training). It integrates with TPVFormer, SurroundOcc, and Symphonies, consistently improving performance on SurroundOcc-nuScenes, Occ3D-nuScenes, and SSCBench-KITTI360 benchmarks. The improvements are particularly strong on surface-sensitive metrics (RayIoU), suggesting that the projective consistency loss encourages more physically coherent 3D predictions.

## Key Contributions

- **Plug-and-play projective consistency loss**: A training-time module that can be added to any 3D occupancy model without architectural changes and with zero inference overhead
- **Voxel Gaussianization**: Converts occupied voxels into spherical Gaussian primitives with learned opacities for efficient differentiable rendering
- **Strategic camera placement**: Uses both fixed Bird's-Eye View cameras and dynamically positioned virtual viewpoints to maximize the supervision signal from different perspectives
- **Architecture-agnostic improvements**: Demonstrates consistent gains across TPVFormer (+3.75 mIoU), SurroundOcc, and Symphonies on multiple benchmarks

## Architecture / Method

![GaussRender qualitative results](https://paper-assets.alphaxiv.org/figures/2502.05040v3/qualitative_0_0.png)

```
┌──────────────────────────────────────────────────────────────────┐
│            GaussRender: Training-Time Module                      │
│                                                                   │
│  ┌───────────────────────────────────────────────────┐            │
│  │  Any Base Occupancy Model                          │            │
│  │  (TPVFormer / SurroundOcc / Symphonies)            │            │
│  └──────────────────────┬────────────────────────────┘            │
│                         │                                         │
│              Predicted 3D Voxel Grid                              │
│                         │                                         │
│         ┌───────────────┴───────────────┐                         │
│         ▼                               ▼                         │
│  ┌──────────────┐              ┌──────────────┐                   │
│  │ Standard 3D   │              │ Voxel         │                   │
│  │ Occupancy     │              │ Gaussianize   │                   │
│  │ Loss (CE +    │              │ (each voxel   │                   │
│  │ Lovasz)       │              │ ──► spherical │                   │
│  └──────┬───────┘              │ Gaussian)     │                   │
│         │                      └───────┬──────┘                   │
│         │                              │                          │
│         │         ┌────────────────────┤                          │
│         │         │                    │                          │
│         │         ▼                    ▼                          │
│         │  ┌─────────────┐    ┌──────────────┐                    │
│         │  │ GT Voxels    │    │ Pred Voxels   │                    │
│         │  │ Gaussianized │    │ Gaussianized  │                    │
│         │  └──────┬──────┘    └──────┬───────┘                    │
│         │         │                  │                             │
│         │         ▼                  ▼                             │
│         │  ┌───────────────────────────────────┐                  │
│         │  │  Differentiable Gaussian Splatting  │                  │
│         │  │  from virtual cameras:              │                  │
│         │  │  - Fixed BEV camera (top-down)      │                  │
│         │  │  - Dynamic cameras (Elevated+Around) │                  │
│         │  └───────────────┬───────────────────┘                  │
│         │                  │                                      │
│         │         2D rendered semantic maps                        │
│         │         (pred vs GT)                                    │
│         │                  │                                      │
│         │         ┌────────▼────────┐                             │
│         │         │ Projective       │                             │
│         │         │ Consistency Loss  │                             │
│         │         └────────┬────────┘                             │
│         │                  │                                      │
│         └──────────┬───────┘                                      │
│                    ▼                                              │
│           Total Training Loss                                     │
│           (removed at inference -- zero overhead)                  │
└──────────────────────────────────────────────────────────────────┘
```

The GaussRender module operates as follows:

**Voxel Gaussianization:** Each occupied voxel in the predicted 3D grid is converted into a spherical Gaussian primitive. The Gaussian center is placed at the voxel center, the covariance is set proportional to voxel size (spherical), and opacity is predicted by the base model or learned. Semantic class labels are assigned to each Gaussian based on the voxel's predicted class.

**Camera Placement:** To render the Gaussians into 2D, virtual cameras are placed at strategic viewpoints. The system uses: (1) a fixed Bird's-Eye View orthographic camera looking down, which captures the spatial layout of the scene; and (2) dynamic virtual cameras placed using an "Elevated + Around" strategy — cameras are lifted along the z-axis and translated randomly in the xy-plane, covering both visible and occluded regions from varied perspectives.

**Gaussian Rendering + Loss:** Both the predicted voxel grid and the ground-truth voxel grid are Gaussianized and rendered into 2D semantic maps from each camera viewpoint using a fast differentiable Gaussian splatting rasterizer. The loss penalizes pixel-wise disagreements between the predicted and ground-truth rendered maps. Because Gaussian splatting naturally handles occlusion through depth-sorted alpha compositing, the loss correctly accounts for visibility.

The total training loss is the standard 3D occupancy loss (cross-entropy + lovasz) plus the GaussRender projective consistency loss. The module adds ~10-14% training overhead but accelerates convergence by 17%, so the net wall-clock cost is modest. At inference time, the GaussRender module is completely removed.

## Results

### SurroundOcc-nuScenes

| Base Model | IoU (base) | IoU (+GaussRender) | mIoU (base) | mIoU (+GaussRender) |
|---|---|---|---|---|
| TPVFormer | 30.86 | **32.05 (+1.19)** | 17.10 | **20.85 (+3.75)** |
| SurroundOcc | 34.71 | **35.48 (+0.77)** | 20.30 | **22.26 (+1.96)** |
| Symphonies | 32.41 | **33.05 (+0.64)** | 19.24 | **20.88 (+1.64)** |

GaussRender provides consistent improvements across all base models, with particularly strong gains on mIoU (per-class metric) and RayIoU (surface accuracy metric). The gains are largest for TPVFormer, suggesting the projective consistency loss helps most when the base model has weaker 3D structure.

## Limitations

- Training-time only module -- does not improve inference-time model capacity
- Gaussian rendering quality depends on voxel resolution; very fine structures may not be well captured by spherical Gaussians
- Virtual camera placement heuristics may not be optimal for all scene types
- Currently demonstrated only on voxel-based occupancy models; extending to other 3D representations (point clouds, meshes) would require adaptation

## Connections

- Directly complements [[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting]] which uses Gaussians as the core representation rather than as a training loss
- Related to [[wiki/sources/papers/gaussianflowocc-sparse-occupancy-with-gaussian-splatting-and-temporal-flow]] which also applies Gaussian splatting to occupancy
- Occupancy prediction connects to [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] (4D occupancy world model)
- [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]] uses Gaussians for world-model-based streaming occupancy
- [[wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting]] applies Gaussian splatting to BEV perception
- Evaluated on [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] benchmarks
