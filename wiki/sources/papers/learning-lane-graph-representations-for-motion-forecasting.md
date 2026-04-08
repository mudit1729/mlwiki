---
title: Learning Lane Graph Representations for Motion Forecasting
type: source-summary
status: seed
updated: 2026-04-05
year: 2020
venue: ECCV
tags:
  - paper
  - autonomous-driving
  - prediction
  - lanegcn
citations: 750
---

📄 **[Read on arXiv](https://arxiv.org/abs/2007.13732)**

# Learning Lane Graph Representations for Motion Forecasting

## Overview

LaneGCN introduces a graph neural network architecture for motion forecasting in autonomous driving that operates directly on the lane graph structure of HD maps. Rather than rasterizing the map into a bird's-eye-view image (losing topological information) or using simple polyline encodings (losing connectivity), LaneGCN represents lanes as nodes in a graph with four types of edges capturing different spatial relationships: predecessor, successor, left neighbor, and right neighbor. This structured representation allows the model to propagate information along the lane topology, enabling the network to reason about where agents can physically go based on road structure.

The model combines lane graph convolutions for map encoding with actor-map interaction modules that allow agent features and map features to exchange information. Actor features are first extracted from past trajectories, then fused with lane features through cross-attention-like mechanisms. The fused features are decoded into multi-modal trajectory predictions with associated confidence scores.

LaneGCN became one of the most influential and durable papers in motion forecasting, establishing the paradigm of explicit graph-based map reasoning for prediction. Its lane graph representation was adopted or adapted by numerous subsequent works including HiVT, LaPred, and TNT. The paper demonstrated that respecting the topological structure of road networks -- rather than treating the map as just another image -- provides substantial benefits for predicting how vehicles, pedestrians, and cyclists will move through structured environments.

## Key Contributions

- **Lane graph representation:** Encodes HD map lanes as a graph with four edge types (predecessor, successor, left neighbor, right neighbor), preserving topological connectivity that rasterization destroys
- **Lane graph convolution (LaneConv):** A specialized graph neural network layer that propagates features along lane topology, with separate kernels for each edge type and dilated graph convolutions to capture long-range lane dependencies
- **Actor-map fusion modules:** Four interaction blocks (ActorNet, MapNet, Actor2Map, Map2Actor) that enable bidirectional information flow between agent trajectory features and map structure features
- **Multi-modal trajectory prediction:** Outputs K trajectory hypotheses with associated confidence scores, handling the inherent multimodality of future motion (an agent at an intersection could go straight, turn left, or turn right)
- **Argoverse benchmark results:** State-of-the-art on the Argoverse motion forecasting benchmark at time of publication, with strong performance maintained over subsequent years

## Architecture / Method

```
┌─────────────────────────────────────────────────────────┐
│                  LaneGCN Architecture                    │
│                                                         │
│  ┌─────────────────┐     ┌──────────────────────┐       │
│  │ Actor Histories  │     │  HD Map Lane Graph    │       │
│  │ (2s @ 10Hz)      │     │  (centerlines + topo) │       │
│  └────────┬────────┘     └──────────┬───────────┘       │
│           ▼                         ▼                   │
│  ┌─────────────────┐     ┌──────────────────────┐       │
│  │   ActorNet       │     │      MapNet           │       │
│  │ (1D Conv on      │     │ (LaneConv layers      │       │
│  │  displacement    │     │  with 4 edge types:   │       │
│  │  vectors)        │     │  pred, succ, left,    │       │
│  └────────┬────────┘     │  right + dilation)    │       │
│           │               └──────────┬───────────┘       │
│           │                          │                   │
│           ▼                          ▼                   │
│  ┌──────────────────────────────────────────────┐       │
│  │            Fusion Modules                     │       │
│  │  ┌──────────┐              ┌──────────┐       │       │
│  │  │Actor2Map │──► spatial ──►│Map2Actor │       │       │
│  │  │attention │   attention  │attention │       │       │
│  │  └──────────┘              └──────────┘       │       │
│  │  (actors attend to          (lanes updated    │       │
│  │   nearby lanes)              by nearby actors)│       │
│  └──────────────────────┬───────────────────────┘       │
│                         ▼                               │
│  ┌──────────────────────────────────────────────┐       │
│  │            Prediction Header                  │       │
│  │  Fused actor features ──► K trajectories      │       │
│  │                          (3s horizon)         │       │
│  │                       ──► K confidence scores │       │
│  │  Loss: regression (smooth L1) + classification│       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

LaneGCN's architecture consists of four main modules that process information in sequence.

ActorNet encodes each actor's past trajectory (observed positions over the last 2 seconds at 10 Hz) using a 1D convolutional network. The trajectory is represented as a sequence of displacement vectors, and the 1D convolutions extract temporal features at multiple scales. The output is a feature vector for each actor capturing its motion history.

MapNet encodes the lane graph. Each lane segment is represented as a node with initial features derived from the lane's geometry (centerline coordinates, lane width, speed limit, turn direction). LaneConv layers propagate information through the graph using four types of edges: predecessor (lane continuations), successor (following lanes), left neighbor, and right neighbor. Dilated graph convolutions extend the receptive field along lanes, allowing the network to reason about distant but topologically connected road structure. Multiple rounds of message passing build up rich lane features.

Actor2Map and Map2Actor modules perform bidirectional fusion. Actor2Map attention allows each actor to attend to nearby lane features, pulling in relevant map context based on spatial proximity and heading alignment. Map2Actor attention allows lane features to be updated based on nearby actors, incorporating traffic context into the map representation. These fusion modules use spatial attention where the attention weights depend on the relative spatial positions and headings of actors and lanes.

The prediction header takes each actor's fused feature and generates K trajectory hypotheses (each a sequence of 2D coordinates over a 3-second future horizon) along with K confidence scores. The training loss combines a regression loss (smooth L1 on the trajectory closest to ground truth) with a classification loss on the confidence scores.

## Results

- State-of-the-art on the Argoverse motion forecasting benchmark at publication, with minADE (minimum average displacement error over K predictions) of 1.35m and minFDE (final displacement error) of 2.97m for K=6 predictions
- The lane graph representation significantly outperforms rasterized map baselines, demonstrating that topological structure provides information beyond what spatial images capture
- Ablation studies confirm that all four edge types contribute positively, with successor and predecessor edges being most important (capturing lane continuation) and neighbor edges providing complementary lateral context
- The dilated LaneConv layers are critical for long-range reasoning -- removing dilation significantly degrades prediction accuracy for long trajectories and complex maneuvers
- Multi-modal predictions correctly capture diverse future behaviors at decision points (intersections, lane changes, merges), with the confidence scores appropriately concentrating on the most likely modes

## Limitations & Open Questions

- Requires high-definition maps with accurate lane connectivity, which are expensive to create and maintain and may not be available in all deployment environments
- The graph representation assumes a fixed lane topology -- dynamic changes to road structure (construction, temporary closures) are not handled
- Pedestrian and cyclist prediction may not benefit as much from lane graph structure since these agents are less constrained by lane topology

## Connections

- [[wiki/concepts/prediction]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/sources/papers/neural-message-passing-for-quantum-chemistry]]
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]]
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]]

