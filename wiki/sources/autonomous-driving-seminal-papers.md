---
title: Autonomous Driving Seminal Papers
type: source-program
status: active
updated: 2026-04-05
tags:
  - sources
  - driving
  - seminal
---

# Autonomous Driving Seminal Papers

Goal: build a durable corpus of high-impact autonomous driving papers, prioritizing papers with strong citation footprints, lasting conceptual importance, or clear influence on later systems.

## Collection rule

Use citation count as a filter, not a definition. The corpus should include:

- papers that exceed roughly 1000 citations,
- papers that introduced a durable concept even if newer or less cited,
- benchmark or system papers that reshaped evaluation or architecture choices.

## Seed list by area

### Perception

- PointNet
- PointNet++
- VoxelNet
- PointPillars
- SECOND
- PV-RCNN
- CenterPoint
- Lift, Splat, Shoot
- BEVFormer
- DETR3D

### Prediction

- DESIRE
- Social LSTM
- Trajectron / Trajectron++
- CoverNet
- MultiPath
- LaneGCN
- VectorNet
- TNT
- MTR

### Planning / system

- ChauffeurNet
- Conditional Imitation Learning
- Learning by Cheating
- TransFuser
- TCP
- VAD
- UniAD

### Evaluation / benchmarks / data

- KITTI
- nuScenes
- Waymo Open Dataset
- Argoverse / Argoverse 2
- CARLA

## Ingest priorities

1. Build dataset and benchmark pages first because they anchor later method comparisons.
2. Ingest one canonical paper per cluster before adding near-duplicates.
3. Maintain explicit notes on whether each paper supports modular, hybrid, or e2e interpretations.

## Already seeded in batch 01

- [[wiki/sources/papers/end-to-end-learning-for-self-driving-cars]]
- [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]]
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]]
- [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]]
- [[wiki/sources/papers/learning-by-cheating]]
- [[wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation]]
- [[wiki/sources/papers/learning-lane-graph-representations-for-motion-forecasting]]
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]]
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]]
- [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]]
- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]]
- [[wiki/sources/papers/planning-oriented-autonomous-driving]]
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]]
