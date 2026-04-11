---
title: "OccGen: Generative Multi-modal 3D Occupancy Prediction for Autonomous Driving"
tags: [autonomous-driving, perception, 3d-occupancy, diffusion, generative-models, computer-vision, multi-camera]
status: active
updated: 2026-04-11
type: paper
year: "2024"
venue: "ECCV"
citations: 50
arxiv_id: "2404.15014"
paper-faithfullness: audited-fixed
---

# OccGen: Generative Multi-modal 3D Occupancy Prediction for Autonomous Driving

📄 **[Read on arXiv](https://arxiv.org/abs/2404.15014)**

## Overview

OccGen reframes 3D semantic occupancy prediction as a conditional generative problem rather than a purely discriminative one. Prior occupancy methods (SurroundOcc, OccFormer, BEVFormer-based pipelines) train feed-forward networks to directly regress voxel labels from multi-camera images, which treats each voxel independently and fails to capture the strong structural priors of real-world 3D scenes -- walls are planar, roads are flat, vehicles have characteristic shapes. OccGen argues that modeling the joint distribution of 3D occupancy with a generative process can exploit these scene-level priors to produce more coherent and complete predictions, especially in occluded or ambiguous regions.

The core idea is to use a diffusion model that operates on a 3D occupancy representation. A multi-modal condition network encodes multi-camera images (and optionally LiDAR) into spatial conditioning features. During inference, OccGen iteratively denoises a randomly initialized 3D occupancy volume using DDIM, progressively refining it toward a plausible scene configuration consistent with the camera observations. A progressive refinement decoder with stacked deformable attention layers produces the final semantic occupancy predictions.

OccGen achieves strong results on the nuScenes-Occupancy benchmark (22.0% mIoU multi-modal, 14.5% camera-only, 16.8% LiDAR-only), demonstrating that the generative formulation improves over discriminative baselines -- particularly for rare and geometrically complex classes where structural priors matter most. The paper also shows that the diffusion framework gracefully integrates multi-modal conditioning (cameras, and optionally LiDAR), and that the iterative refinement produces visually more coherent occupancy maps compared to single-pass methods. A distinctive property of the generative approach is the ability to provide uncertainty estimates alongside predictions.

## Key Contributions

- **Generative occupancy formulation**: First paper to formulate 3D occupancy prediction as a conditional generative task using score-based diffusion, demonstrating that modeling the joint distribution of voxels captures scene-level structural priors that discriminative methods miss
- **Multi-modal condition network**: A flexible BEV-based conditioning architecture that encodes multi-camera images (and optionally LiDAR) into a spatial conditioning signal for the diffusion process, enabling plug-and-play sensor fusion
- **Progressive refinement decoder**: Six stacked refinement layers with 3D deformable cross-attention and self-attention, using DDIM with a cosine noise schedule to iteratively denoise the occupancy volume; the denoising process inherently models coarse-to-fine refinement without a separate upsampling stage
- **Progressive denoising for occupancy**: Demonstrates that iterative refinement through the diffusion reverse process produces more spatially coherent predictions than single-pass feed-forward methods, with particular gains on geometrically complex and rare classes
- **Uncertainty estimation**: As a generative model, OccGen natively provides uncertainty estimates alongside occupancy predictions, a capability discriminative methods cannot offer
- **Strong nuScenes-Occupancy results**: 22.0% mIoU (multi-modal), 14.5% (camera-only), 16.8% (LiDAR-only), with relative mIoU improvements of 9.5%, 13.3%, and 6.3% respectively over the prior state-of-the-art

## Architecture / Method

```
┌────────────────────────────────────────────────────────────┐
│            Conditional Encoder (two-stream)                 │
│                                                             │
│  Camera: 2D Backbone+FPN ──► Gumbel-Softmax hard           │
│                               2D-to-3D view transform       │
│                                              │              │
│  LiDAR:  VoxelNet + 3D sparse conv ─────────┤              │
│                                  geometry mask fuse         │
└─────────────────────────┬──────────────────────────────────┘
                          │ multi-modal conditioning features
                          │
┌─────────────────────────▼──────────────────────────────────┐
│         Progressive Refinement Decoder (DDIM)               │
│                                                             │
│  Training:  GT occ ──► add noise (cosine schedule)         │
│                                                             │
│  Inference: Gaussian noise                                  │
│             ──► [Layer 1: 3D deformable cross-attn +        │
│                           self-attn + time embed]           │
│             ──► [Layer 2] ──► ... ──► [Layer 6]            │
│                 ▲ conditioned on multi-modal features        │
│                                                             │
│  Loss: cross-entropy + lovász-softmax + affinity + depth    │
└─────────────────────────┬──────────────────────────────────┘
                          │
                          ▼
              Semantic Occupancy Volume
```

OccGen's pipeline consists of three main components:

**1. Multi-modal Condition Network (Conditional Encoder).** A two-stream architecture encodes multi-modal inputs. The camera stream processes images through a pre-trained 2D backbone with Feature Pyramid Network and projects them into 3D using a novel hard 2D-to-3D view transformation based on Gumbel-Softmax for deterministic depth assignment (not the LSS soft-distribution approach). The LiDAR stream uses VoxelNet with 3D sparse convolutions. When both modalities are available, a geometry mask derived from LiDAR is used to refine camera features, enabling cross-modal fusion.

**2. Progressive Refinement Decoder.** The core generative component applies diffusion denoising using the multi-modal encoded features as conditions. Rather than a 3D U-Net, it uses six stacked refinement layers with 3D deformable cross-attention and self-attention mechanisms that operate on multi-scale noise maps with time embeddings from the diffusion module. DDIM (Denoising Diffusion Implicit Models) with a cosine noise schedule is used for both training and inference. The training loss combines cross-entropy, lovász-softmax, affinity (geometric and semantic), and depth supervision.

**3. Inference.** OccGen starts from Gaussian noise and runs DDIM reverse diffusion (with asymmetric time intervals, td=1), conditioned on the encoded multi-modal observations, progressively denoising to produce a semantic occupancy volume. The denoising process inherently models coarse-to-fine refinement of the dense 3D occupancy map.

## Results

OccGen was evaluated primarily on the nuScenes-Occupancy benchmark:

| Method | Setting | mIoU | Type |
|--------|---------|------|------|
| OpenOccupancy (Baseline) | Multi-modal | 15.1 | Discriminative |
| CONet | Multi-modal | 20.1 | Discriminative |
| **OccGen** | **Multi-modal** | **22.0** | **Generative (diffusion)** |
| C-CONet | Camera-only | 12.8 | Discriminative |
| **C-OccGen** | **Camera-only** | **14.5** | **Generative (diffusion)** |
| L-CONet | LiDAR-only | 15.8 | Discriminative |
| **L-OccGen** | **LiDAR-only** | **16.8** | **Generative (diffusion)** |

OccGen also achieves 13.74% mIoU on SemanticKITTI (vs OccFormer 13.46%).

Key findings:
- OccGen relatively improves mIoU by 9.5% (multi-modal), 13.3% (camera-only), and 6.3% (LiDAR-only) on the nuScenes-Occupancy benchmark vs. the prior state-of-the-art
- The generative formulation provides the largest improvements on rare and geometrically complex classes where structural priors matter most
- Multi-modal conditioning (camera + LiDAR) yields additional gains over unimodal, demonstrating the flexibility of the conditioning framework
- As a generative model, OccGen can produce uncertainty estimates alongside predictions -- a capability unavailable in discriminative baselines
- Comparable inference latency (~357-400ms) to single-forward discriminative methods despite iterative denoising
- Qualitative results show visually more coherent and complete occupancy maps, with better completion of occluded regions

## Limitations & Open Questions

- **Inference speed**: Despite using DDIM and achieving comparable latency to some discriminative baselines (~357-400ms), the iterative denoising process still exceeds real-time requirements for safety-critical autonomous driving deployment
- **Computational cost**: The stacked 3D deformable attention refinement layers operating on volumetric representations are memory-intensive, compounding the existing cost of occupancy prediction
- **Limited temporal modeling**: OccGen operates on single-frame observations without explicit temporal aggregation; combining diffusion-based occupancy with temporal world models (OccWorld, Drive-OccWorld) is an open direction
- **Scaling to higher resolutions**: The coarse-to-fine strategy helps, but scaling diffusion to very fine voxel resolutions (e.g., 0.1m) remains challenging
- **How many denoising steps are truly needed?** Recent work on truncated diffusion (DiffusionDrive) and single-step flow matching (GoalFlow) suggests that full multi-step denoising may be unnecessary -- could occupancy prediction benefit from similar truncation?

## Connections

Related papers in the wiki:

- [[wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving]] -- foundational discriminative occupancy method that OccGen builds upon and compares against
- [[wiki/sources/papers/occformer-dual-path-transformer-for-vision-based-3d-semantic-occupancy-prediction]] -- efficient dual-path transformer baseline for discriminative occupancy
- [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]] -- alternative efficient occupancy representation using sparse Gaussians (ECCV 2024 peer)
- [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]] -- generative occupancy world model using VQ-VAE + GPT (ECCV 2024 peer); generative but for forecasting rather than perception
- [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] -- 4D occupancy forecasting world model extending OccWorld ideas
- [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] -- BEV feature extraction backbone used in OccGen's condition network
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] -- LSS soft-depth approach that OccGen contrasts against; OccGen replaces it with a Gumbel-Softmax hard 2D-to-3D view transform for deterministic depth assignment
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational DDPM framework that OccGen adapts to 3D occupancy
- [[wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising]] -- related use of diffusion for BEV feature denoising (training-only), complementary approach
- [[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin]] -- efficiency-focused occupancy method, highlighting the speed gap OccGen needs to close
- [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]] -- Mamba-based occupancy with linear complexity, another efficiency contrast
