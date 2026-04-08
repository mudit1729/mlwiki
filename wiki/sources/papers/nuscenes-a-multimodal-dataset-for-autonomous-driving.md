---
title: nuScenes: A Multimodal Dataset for Autonomous Driving
type: source-summary
status: complete
updated: 2026-04-05
year: 2020
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - benchmark
  - dataset
citations: 7791
---

📄 **[Read on arXiv](https://arxiv.org/abs/1903.11027)**

## Overview

nuScenes is a large-scale multimodal dataset for autonomous driving that provides synchronized data from 6 cameras (360-degree coverage), 1 LiDAR, 5 radars, GPS, and IMU collected across 1000 driving scenes in Boston and Singapore. Each scene is 20 seconds long with keyframe annotations at 2 Hz, yielding approximately 1.4 million 3D bounding box annotations across 23 object classes. The dataset was created by Motional (formerly nuTonomy) and released in 2019, quickly becoming the de facto benchmark for 3D object detection, tracking, and BEV-centric perception in autonomous driving research.

What distinguishes nuScenes from prior datasets like KITTI (which provided only front-facing stereo camera and single LiDAR) is its full 360-degree sensor coverage and the diversity of its collection environments. Boston provides North American urban driving conditions while Singapore adds tropical weather, left-hand traffic, and dense urban scenarios with many vulnerable road users. This geographic diversity, combined with the full sensor suite, made nuScenes the first dataset that could credibly evaluate surround-view perception systems operating in varied conditions.

Beyond 3D detection, nuScenes catalyzed multiple research directions: BEV segmentation (LSS, BEVFormer), 3D multi-object tracking (the nuScenes tracking challenge), motion prediction (nuScenes-prediction split), and planning-oriented architectures (UniAD, VAD). The nuScenes Detection Score (NDS) metric, which combines mAP with true positive metrics for translation, scale, orientation, velocity, and attribute errors, became the standard evaluation protocol and influenced metric design in subsequent benchmarks.

## Key Contributions

- **Full 360-degree multimodal sensor suite**: 6 cameras, 1 32-beam LiDAR, 5 radars, GPS, and IMU with precise cross-sensor calibration and time synchronization, enabling research on sensor fusion at scale
- **Large-scale 3D annotations**: ~1.4M annotated 3D bounding boxes across 23 object classes with attributes (e.g., vehicle state, pedestrian pose) and visibility levels, annotated at 2 Hz keyframes
- **nuScenes Detection Score (NDS)**: A composite metric that goes beyond mAP to penalize errors in translation, scale, orientation, velocity, and attribute prediction, providing a more holistic evaluation of 3D detection quality
- **Geographic and condition diversity**: Data collected in Boston and Singapore across day/night, rain/dry conditions, providing distribution diversity that single-city datasets cannot match
- **Public benchmark and leaderboard**: An open evaluation server with held-out test set annotations, fostering reproducible comparisons and driving community-wide progress

## Architecture / Method

![nuScenes multimodal sensor data: camera images, radar, lidar, and semantic maps with 3D bounding boxes](https://paper-assets.alphaxiv.org/figures/1903.11027v5/img-0.jpeg)

![Challenging scenarios in nuScenes: nighttime, rain, complex urban, diverse objects with 3D annotations](https://paper-assets.alphaxiv.org/figures/1903.11027v5/img-1.jpeg)

nuScenes is a dataset contribution, not an algorithmic one. The key design decisions are:

**Sensor configuration**: Six cameras provide full 360-degree coverage with minimal overlap. The 32-beam Velodyne LiDAR captures ~34K points per sweep at 20 Hz. Five Continental radars provide long-range velocity measurements. All sensors are precisely calibrated with known extrinsic transformations.

**Annotation protocol**: Professional annotators label 3D bounding boxes on accumulated LiDAR point clouds (5 sweeps) projected into a unified coordinate frame. Each box has class label, 3D size, position, orientation, velocity (derived from tracking), and semantic attributes. Quality is ensured through multi-round review.

**Dataset splits**: 700 training scenes, 150 validation scenes, 150 test scenes. The test set annotations are held out and evaluation requires submission to the public server. A mini-split of 10 scenes is provided for rapid prototyping.

**Evaluation metrics**: The primary 3D detection metric is NDS = (1/2) * [mAP + (1/5) * sum(1 - min(TP_metric, 1))], where TP metrics are mean errors in translation (mATE), scale (mASE), orientation (mAOE), velocity (mAVE), and attribute (mAAE). This penalizes detections that are correctly localized but poorly characterized.

**Prediction and planning extensions**: The nuScenes-prediction split provides 2-second future trajectories for agents, and the map expansion provides HD map layers (lanes, crosswalks, boundaries), enabling motion forecasting and planning research.

## Results

![Distribution of object classes and attributes in nuScenes](https://paper-assets.alphaxiv.org/figures/1903.11027v5/img-4.jpeg)

| Method | NDS | mAP | Notes |
|--------|-----|-----|-------|
| Megvii (top) | 63.3% | 52.8% | Best at time of paper |
| PointPillars (LiDAR) | 45.3% | 30.5% | LiDAR baseline |
| MonoDIS (camera) | 38.4% | 30.4% | Camera-only baseline |

| Condition | Impact on mAP |
|-----------|--------------|
| Nighttime (LiDAR) | 36% reduction |
| Nighttime (camera) | 55-58% reduction |
| 1 vs 10 LiDAR sweeps | NDS: 31.8% vs 44.8% |

- At release, the PointPillars baseline achieved 30.5 NDS and 16.0 mAP on the test set, establishing initial performance reference points
- By 2023, top-performing methods exceeded 75 NDS, demonstrating the dataset's ability to drive sustained progress
- The dataset enabled the discovery that camera-only methods (BEVFormer, BEVDet) could approach LiDAR-based performance when using BEV representations, a finding that would not have been possible without the full 360-degree camera coverage
- nuScenes tracking and prediction challenges revealed that multi-object tracking in 3D remains significantly harder than 2D, with identity switches and fragmentation being dominant failure modes
- Cross-dataset evaluation (training on nuScenes, testing on Waymo or vice versa) revealed significant domain gaps, motivating research in domain adaptation for 3D perception

## Limitations & Open Questions

- The 32-beam LiDAR is sparser than the 64-beam sensors used in newer datasets (Waymo Open, Argoverse 2), potentially understating the performance of LiDAR-dependent methods
- Annotation at 2 Hz (vs. the 20 Hz sensor rate) means that intermediate frames lack labels, requiring interpolation for methods that operate at full sensor rate
- The dataset does not include raw driver actions (steering, throttle, brake), limiting its direct applicability to end-to-end driving research without additional annotation efforts (addressed by nuPlan)

## Connections

- [[wiki/concepts/perception]] -- nuScenes is the primary benchmark for 3D perception research
- [[wiki/concepts/autonomous-driving]] -- foundational dataset for the AD research community
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] -- LSS pioneered camera-to-BEV on nuScenes
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD evaluates on nuScenes
- [[wiki/concepts/prediction]] -- nuScenes-prediction enables motion forecasting research

