---
title: "DriveTransformer: Unified Transformer for Scalable End-to-End Autonomous Driving"
tags: [autonomous-driving, transformer, end-to-end, planning]
status: active
type: paper
year: "2025"
venue: "ICLR 2025"
citations: 91
arxiv_id: "2503.07656"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2503.07656)**

## Overview

DriveTransformer represents a fundamental departure from existing end-to-end autonomous driving approaches. Rather than following sequential perception-prediction-planning pipelines with dense BEV representations, the framework implements three core principles: task parallelism, sparse representation, and streaming processing. This design directly addresses the limitations of prior methods like UniAD and VAD, which suffer from cumulative error propagation, training instability due to multi-stage optimization, and computational inefficiency from dense BEV processing.

The unified architecture operates through three attention mechanisms that replace the traditional sequential pipeline. Sensor Cross Attention connects task queries directly to raw sensor features, eliminating intermediate representation bottlenecks. Task Self-Attention enables simultaneous interaction among all driving task types -- detection, prediction, mapping, and planning -- rather than processing them sequentially. Temporal Cross Attention incorporates historical information through FIFO queues of past task queries with ego transformation and motion compensation, replacing the expensive storage and processing of historical BEV features.

The framework demonstrates superior scaling properties: decoder scaling provides greater planning improvements than backbone scaling, suggesting the interaction between tasks matters more than raw perception capacity. DriveTransformer achieves state-of-the-art closed-loop driving performance on the Bench2Drive simulation benchmark with significantly lower inference latency than competing methods.

## Key Contributions

- **Task parallelism:** All driving tasks (detection, prediction, mapping, planning) are processed simultaneously through shared attention, eliminating sequential error propagation
- **Sparse representation:** Task-specific queries replace dense BEV maps, reducing computation and memory while preserving task-relevant information
- **Streaming temporal processing:** FIFO queues of compact past task queries with ego-motion compensation replace expensive historical BEV feature storage
- **Unified training:** Single-stage end-to-end optimization replaces complex multi-stage training schedules
- **Favorable scaling laws:** Decoder scaling improves planning more than backbone scaling, revealing where compute is best allocated

## Architecture / Method

![Paradigm Comparison](https://paper-assets.alphaxiv.org/figures/2503.07656v2/x1.png)

DriveTransformer (right) eliminates the sequential pipeline structure of UniAD-style systems (left) in favor of parallel task processing with shared attention.

![Architecture Overview](https://paper-assets.alphaxiv.org/figures/2503.07656v2/x2.png)

```
┌──────────────────────────────────────────────────────────────┐
│              DriveTransformer Architecture                     │
│                                                               │
│  Multi-Camera Images                                          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐          │
│  │Cam 1│ │Cam 2│ │Cam 3│ │Cam 4│ │Cam 5│ │Cam 6│          │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘          │
│     └───────┴───────┴───┬───┴───────┴───────┘              │
│                         ▼                                    │
│  ┌──────────────────────────────┐                            │
│  │     Image Backbone           │                            │
│  │     (Multi-scale features)   │                            │
│  └──────────────┬───────────────┘                            │
│                 ▼                                             │
│  ┌──────────────────────────────────────────────────┐       │
│  │           Unified Decoder (repeated L layers)     │       │
│  │                                                   │       │
│  │  Task Queries (all processed in parallel):        │       │
│  │  ┌──────┐ ┌──────┐ ┌───────┐ ┌────────┐         │       │
│  │  │Detect│ │ Map  │ │Predict│ │Planning│         │       │
│  │  └──┬───┘ └──┬───┘ └───┬───┘ └───┬────┘         │       │
│  │     │        │         │         │               │       │
│  │     ▼        ▼         ▼         ▼               │       │
│  │  ┌─────────────────────────────────────┐         │       │
│  │  │ 1. Sensor Cross-Attention           │         │       │
│  │  │    (queries attend to image feats)  │         │       │
│  │  ├─────────────────────────────────────┤         │       │
│  │  │ 2. Task Self-Attention              │         │       │
│  │  │    (all tasks interact mutually)    │         │       │
│  │  ├─────────────────────────────────────┤         │       │
│  │  │ 3. Temporal Cross-Attention         │         │       │
│  │  │    (FIFO queue of past queries      │         │       │
│  │  │     + ego-motion compensation)      │         │       │
│  │  └─────────────────────────────────────┘         │       │
│  └──────────────────────────────────────────────────┘       │
│                         ▼                                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │3D Detect │ │HD Map    │ │Motion    │ │GMM Planning  │   │
│  │Output    │ │Output    │ │Prediction│ │(multi-mode)  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

The architecture consists of a shared decoder with three attention types:

**Sensor Cross Attention:** Each task query (detection, mapping, planning) attends directly to multi-camera image features. This eliminates the BEV intermediate representation that creates an information bottleneck in prior systems.

**Task Self-Attention:** All task queries from all task types attend to each other simultaneously. Detection queries can inform planning queries directly; mapping queries and prediction queries interact without sequential ordering.

**Temporal Cross Attention:** Past task queries are stored in FIFO queues and transformed to the current ego coordinate frame. Agent tokens receive additional motion compensation using predicted velocities. This is far more efficient than storing full BEV features from past timesteps.

![Attention Mechanisms](https://paper-assets.alphaxiv.org/figures/2503.07656v2/x4.png)

Task-specific innovations include:
- **Shared agent queries** for detection and motion prediction (single query handles both)
- **Point-level mapping** with PointNet aggregation instead of dense rasterized maps
- **Multi-mode planning** with Gaussian Mixture Models to avoid dangerous trajectory averaging

## Results

![Scaling Analysis](https://paper-assets.alphaxiv.org/figures/2503.07656v2/x7.png)

| Benchmark | DriveTransformer | UniAD | VAD | Notes |
|-----------|-----------------|-------|-----|-------|
| Bench2Drive (closed-loop) | SOTA | -- | -- | Significantly lower latency |
| Decoder scaling | Large gains | -- | -- | More impactful than backbone scaling |
| Inference latency | Low | Higher | Higher | Sparse queries are faster |

The scaling analysis reveals a key insight: investing compute in the decoder (where tasks interact) yields greater planning improvements than investing in the backbone (raw perception capacity). This suggests that cross-task reasoning, not just better perception, is the bottleneck in end-to-end driving.

![Robustness](https://paper-assets.alphaxiv.org/figures/2503.07656v2/robustness.png)

The system maintains performance under various sensor corruption conditions, demonstrating robustness of the sparse representation approach.

## Limitations & Open Questions

- Evaluated primarily in simulation (Bench2Drive); real-world closed-loop deployment is not demonstrated
- The sparse representation may lose fine-grained scene details that matter for rare edge cases (e.g., small debris, unusual road markings)
- Whether the favorable decoder scaling law continues to hold at significantly larger model scales is unknown

## Connections

- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD is the primary baseline; DriveTransformer replaces UniAD's sequential pipeline with parallel task processing
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- VAD introduced vectorized representations; DriveTransformer pushes further toward sparse task queries
- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] -- TransFuser pioneered transformer-based sensor fusion for driving; DriveTransformer extends the transformer paradigm to all driving tasks
- [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] -- BEVFormer established dense BEV transformers; DriveTransformer argues for sparse alternatives
- [[wiki/sources/papers/attention-is-all-you-need]] -- The underlying transformer architecture that enables the unified attention-based design
- [[wiki/concepts/end-to-end-architectures]] -- Type 3 jointly trained system that pushes toward full task parallelism
- [[wiki/concepts/planning]] -- Novel multi-mode GMM planning within unified transformer
- [[wiki/concepts/autonomous-driving]] -- Demonstrates favorable scaling laws for E2E driving
