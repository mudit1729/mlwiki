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

