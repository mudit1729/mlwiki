---
title: Lift, Splat, Shoot: Encoding Images From Arbitrary Camera Rigs by Implicitly Unprojecting to 3D
type: source-summary
status: seed
updated: 2026-04-05
year: 2020
venue: ECCV
tags:
  - paper
  - autonomous-driving
  - perception
  - bev
citations: 1510
---

📄 **[Read on arXiv](https://arxiv.org/abs/2008.05711)**

## Overview

Lift, Splat, Shoot (LSS) introduced a differentiable pipeline for transforming multi-camera images into a unified bird's-eye view (BEV) representation without requiring LiDAR. The core insight is a three-step process: "lift" each pixel into a frustum of 3D points by predicting a categorical depth distribution, "splat" these 3D features into a voxel grid on the BEV plane using sum-pooling, and then "shoot" -- plan motion trajectories directly from the BEV features. This approach works with arbitrary camera configurations because the geometry is handled through known camera intrinsics and extrinsics rather than learned implicitly.

Before LSS, camera-based 3D perception either relied on explicit depth estimation (monocular 3D detection) or projected 3D anchors onto images (FCOS3D, DETR3D). LSS showed that a learned depth distribution per pixel, combined with an outer product with image features, creates a rich 3D representation that can be efficiently accumulated on a BEV grid. This became the dominant paradigm for camera-only BEV perception in autonomous driving, directly enabling BEVDet, BEVDepth, BEVFusion, and the perception backbone of Tesla's Autopilot as described in their AI Day presentations.

The paper also demonstrated that the resulting BEV features are directly useful for downstream planning, not just perception. By predicting a cost map in BEV space and performing template-based trajectory selection, LSS showed the potential for end-to-end camera-to-planning pipelines that bypass explicit 3D bounding box detection entirely.

## Key Contributions

- **Lift operation**: Predicts a categorical distribution over D discrete depth bins for each pixel and takes the outer product with the image feature vector, creating a point cloud of context-weighted features in 3D frustum space
- **Splat operation**: Efficiently accumulates 3D frustum features onto a 2D BEV grid using pillar-based sum pooling, leveraging cumulative sum tricks for GPU-efficient voxelization
- **Camera-rig agnostic**: The architecture handles arbitrary numbers of cameras with arbitrary intrinsics/extrinsics at inference time without retraining, since geometry is encoded through known calibration parameters
- **End-to-end planning from cameras**: Demonstrates trajectory planning directly from BEV features via a learned cost volume, bypassing the need for explicit 3D object detection
- **Interpretable depth predictions**: The predicted depth distributions can be visualized and validated against LiDAR ground truth, providing transparency into what the model learns

## Architecture / Method

![Overview of the Lift-Splat-Shoot architecture](https://paper-assets.alphaxiv.org/figures/2008.05711/img-3.jpeg)

![Depth distribution visualization showing learned depth predictions](https://paper-assets.alphaxiv.org/figures/2008.05711/img-2.jpeg)

The architecture takes N camera images as input, each with known intrinsic matrix K and extrinsic pose [R|t]. For each image, a shared backbone (EfficientNet-B0) extracts features at 1/8 resolution. Two prediction heads produce (1) a context feature vector c of dimension C for each pixel and (2) a softmax depth distribution alpha over D discrete depth bins (e.g., D=41 bins from 4m to 45m at 1m intervals).

For each pixel, the outer product of alpha (D x 1) and c (1 x C) yields a D x C frustum feature tensor. Each depth bin maps to a known 3D point via the camera intrinsics and extrinsics. The "splat" step places all frustum features from all cameras into a 3D voxel grid (X x Y x Z) and collapses the Z dimension via sum pooling to produce a BEV feature map of size X x Y x C.

A BEV encoder (ResNet-18) processes the BEV features. For the planning ("shoot") task, the model predicts a per-pixel cost on the BEV grid and selects the lowest-cost trajectory from a template library of kinematically feasible paths.

Training uses binary cross-entropy for BEV semantic segmentation (vehicle, road, lane) and a planning loss based on expert trajectory imitation. The entire pipeline is differentiable and trained end-to-end.

## Results

![Robustness to camera configuration changes demonstrating camera-rig-agnostic design](https://paper-assets.alphaxiv.org/figures/2008.05711/img-5.jpeg)

![Qualitative results on nuScenes: BEV segmentation from multi-camera input](https://paper-assets.alphaxiv.org/figures/2008.05711/img-7.jpeg)

- On the nuScenes dataset, LSS achieves competitive performance on vehicle and map segmentation tasks from camera-only input, outperforming baselines and establishing the baseline for the BEV perception paradigm. Achieves competitive performance compared to LiDAR methods at close distances
- The model generalizes across different camera configurations: demonstrates robustness to camera dropout and calibration errors, with performance degrading gracefully when cameras are removed at test time. Enables zero-shot transfer across different camera configurations and datasets, validating the camera-rig-agnostic design
- Depth distribution predictions correlate well with LiDAR-derived ground truth depths, showing the network learns meaningful geometry
- The planning module demonstrates feasible trajectory prediction from BEV features, though quantitative planning metrics were not the paper's primary focus
- Inference runs at approximately 35 FPS on a single GPU, making it practical for real-time autonomous driving applications

## Limitations & Open Questions

- The discrete depth binning introduces quantization error, particularly at long range where bins are sparse; later work (BEVDepth) showed that explicit depth supervision from LiDAR dramatically improves the depth predictions
- The sum-pooling splat operation loses information about vertical structure (height), which matters for objects like trucks vs. cars; 3D voxel representations or height-aware pooling could address this
- The paper does not address temporal fusion across frames, which is critical for velocity estimation and handling occlusions; subsequent work (BEVFormer, SOLOFusion) added temporal modeling on top of the LSS framework

## Connections

- [[wiki/concepts/perception]] -- LSS is a foundational camera-based perception method
- [[wiki/concepts/planning]] -- demonstrates end-to-end camera-to-planning via BEV
- [[wiki/concepts/autonomous-driving]] -- core method in modern AV perception stacks
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD builds on BEV representations pioneered by LSS
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- primary evaluation benchmark

