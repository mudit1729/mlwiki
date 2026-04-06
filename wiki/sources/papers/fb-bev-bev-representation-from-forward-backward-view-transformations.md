---
title: "FB-BEV: BEV Representation from Forward-Backward View Transformations"
tags: [autonomous-driving, perception, bev, transformer, computer-vision]
status: active
type: paper
year: "2023"
venue: "ICCV"
citations: 150
arxiv_id: "2308.02236"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2308.02236)**

## Overview

FB-BEV addresses a fundamental tension in camera-based BEV perception for autonomous driving: **forward projection** methods (like Lift-Splat-Shoot) generate BEV features by explicitly predicting depth and projecting 2D image features into 3D, while **backward projection** methods (like BEVFormer) start from BEV queries and sample image features via cross-attention. Each paradigm has distinct strengths -- forward methods preserve fine-grained image detail but suffer from depth estimation errors, while backward methods handle geometric ambiguity more gracefully but can miss details due to sparse sampling. FB-BEV proposes that these two view transformation directions are complementary, not competing, and unifies them in a single framework.

The core insight is a **forward-backward view transformation** module that combines the strengths of both paradigms. The forward branch lifts image features into BEV space via depth-based projection (similar to LSS), while the backward branch uses deformable cross-attention from BEV queries to image features (similar to BEVFormer). A learned fusion mechanism merges both BEV representations, allowing the network to leverage dense depth-based features and attention-based features simultaneously. The paper also introduces a **3D pre-training strategy** using LiDAR-supervised depth estimation and 3D object detection to bootstrap the forward branch, significantly improving convergence and final performance.

FB-BEV achieved state-of-the-art results on the nuScenes 3D detection and BEV segmentation benchmarks at the time of publication, demonstrating that the forward-backward combination consistently outperforms either direction alone. The work by Zhiqi Li, Zhiding Yu, Wenhai Wang, Anima Anandkumar, Tong Lu, and Jose Alvarez (NVIDIA / Nanjing University) was published at ICCV 2023, and its unified view transformation framework influenced subsequent BEV perception systems.

## Key Contributions

- **Unified forward-backward view transformation**: Combines depth-based forward projection (LSS-style) and query-based backward projection (BEVFormer-style) in a single module, demonstrating their complementarity rather than treating them as competing paradigms
- **Forward-backward feature fusion**: A learned attention-based mechanism merges the two BEV feature maps, allowing the model to adaptively weight forward vs. backward features depending on the spatial location and scene context
- **3D pre-training strategy**: Uses LiDAR-supervised depth prediction and 3D detection as pre-training tasks for the forward branch, providing strong geometric priors that improve both convergence speed and final accuracy
- **Systematic ablation of view transformation**: Provides the first rigorous comparison of forward vs. backward vs. combined view transformations under controlled experimental conditions, isolating the contribution of each direction
- **State-of-the-art nuScenes performance**: Achieves leading results on nuScenes 3D detection (NDS and mAP) and BEV segmentation among camera-only methods at time of publication

## Architecture / Method

FB-BEV takes surround-view multi-camera images as input and produces a unified BEV feature map for downstream 3D detection and segmentation tasks. The architecture consists of four major components:

**Image backbone**: A shared image encoder (ResNet-50 or ResNet-101 with FPN) extracts multi-scale features from each of the N=6 surround-view camera images independently, producing feature maps at multiple resolutions.

**Forward view transformation (2D-to-3D)**: Following the LSS paradigm, the forward branch predicts a categorical depth distribution over D discrete bins for each pixel in the image feature maps. Each pixel's feature is "lifted" into 3D by computing the outer product of the depth distribution and the context feature, then accumulated onto a BEV grid via pillar-based sum pooling. This produces a forward BEV feature map `B_fwd` of shape `(B, C, H_bev, W_bev)`.

**Backward view transformation (3D-to-2D)**: Following BEVFormer, the backward branch maintains learnable BEV queries on the same spatial grid. Each BEV query generates 3D reference points at multiple heights, projects them onto camera image planes, and aggregates features via multi-scale deformable cross-attention. Temporal self-attention optionally incorporates previous-frame BEV features aligned by ego-motion. This produces a backward BEV feature map `B_bwd` of shape `(B, C, H_bev, W_bev)`.

**Forward-backward fusion**: The two BEV feature maps are fused via a learned mechanism. Specifically, channel-wise concatenation followed by attention-based gating produces the final unified BEV representation `B_fused`. The gating mechanism allows the model to adaptively rely more on forward features in regions where depth estimation is confident (nearby, well-textured) and backward features where depth is ambiguous (distant, textureless).

**3D pre-training**: Before end-to-end training, the forward branch is pre-trained with explicit depth supervision from LiDAR point cloud projections and auxiliary 3D object detection. This bootstraps accurate depth distributions, which improves the quality of the forward BEV features and stabilizes training of the full model.

Task-specific heads (a DETR-style head for 3D detection, convolutional decoder for BEV segmentation) operate on the fused BEV features.

## Results

FB-BEV was evaluated on the nuScenes dataset for both 3D object detection and BEV map segmentation.

### 3D Object Detection (nuScenes val)

| Method | Backbone | NDS | mAP |
|--------|----------|-----|-----|
| **FB-BEV** | ResNet-101 | **62.4** | **54.2** |
| BEVFormer v2 | ResNet-101 | 61.7 | 52.8 |
| BEVFormer | ResNet-101 | 56.9 | 48.1 |
| BEVDet4D | Swin-B | 56.9 | 45.1 |
| BEVDepth | ResNet-101 | 53.5 | 41.2 |
| PETR v2 | ResNet-101 | 58.2 | 49.0 |

### Ablation: Forward vs. Backward vs. Combined

| View Transform | NDS | mAP |
|---------------|-----|-----|
| Forward only (LSS-style) | 58.1 | 47.9 |
| Backward only (BEVFormer-style) | 59.3 | 49.5 |
| Forward + Backward (FB-BEV) | **62.4** | **54.2** |

The combined forward-backward approach consistently outperforms either direction alone, confirming the complementarity thesis. The improvement is largest for distant objects and occluded regions, where the backward attention branch compensates for depth estimation failures in the forward branch.

### Effect of 3D Pre-training

| Pre-training | NDS | mAP |
|-------------|-----|-----|
| No pre-training | 59.8 | 50.1 |
| Depth pre-training only | 61.2 | 52.4 |
| Depth + 3D det pre-training | **62.4** | **54.2** |

The 3D pre-training strategy provides a +2.6 NDS improvement, with explicit depth supervision being the dominant factor. This suggests that accurate depth initialization is critical for the forward branch to provide useful complementary information to the backward branch.

## Limitations & Open Questions

- **Computational cost**: Running both forward and backward branches approximately doubles the view transformation compute compared to using either alone; the paper does not extensively analyze latency-accuracy trade-offs for deployment
- **LiDAR dependency for pre-training**: The 3D pre-training strategy relies on LiDAR point clouds for depth supervision, creating a dependency on multi-modal data during the training phase even though inference is camera-only
- **Fixed fusion strategy**: The forward-backward fusion uses a learned gating mechanism, but the paper does not explore dynamic routing where some regions might skip one branch entirely for efficiency
- **Temporal modeling**: The temporal component follows BEVFormer's single-frame recurrence; more sophisticated temporal fusion (multi-frame, learned alignment) could further improve performance
- **Generalization beyond nuScenes**: Results are demonstrated only on nuScenes; transfer to other datasets and camera configurations is not evaluated

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] -- FB-BEV's forward branch builds directly on the LSS lift-splat paradigm for depth-based 2D-to-3D projection
- [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] -- FB-BEV's backward branch adopts BEVFormer's deformable cross-attention mechanism and temporal self-attention
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD uses BEVFormer as its perception backbone; FB-BEV's improved BEV features could serve as a drop-in replacement
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- VAD builds on BEV perception for vectorized end-to-end driving
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- Primary evaluation benchmark
- [[wiki/concepts/perception]] -- FB-BEV advances the BEV perception paradigm central to modern driving stacks
