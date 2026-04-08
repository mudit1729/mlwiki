---
title: "OccGen: Generative Multi-modal 3D Occupancy Prediction for Autonomous Driving"
tags: [autonomous-driving, perception, 3d-occupancy, diffusion, generative-models, computer-vision, multi-camera]
status: active
type: paper
year: "2024"
venue: "ECCV"
citations: 50
arxiv_id: "2404.15014"
---

# OccGen: Generative Multi-modal 3D Occupancy Prediction for Autonomous Driving

📄 **[Read on arXiv](https://arxiv.org/abs/2404.15014)**

## Overview

OccGen reframes 3D semantic occupancy prediction as a conditional generative problem rather than a purely discriminative one. Prior occupancy methods (SurroundOcc, OccFormer, BEVFormer-based pipelines) train feed-forward networks to directly regress voxel labels from multi-camera images, which treats each voxel independently and fails to capture the strong structural priors of real-world 3D scenes -- walls are planar, roads are flat, vehicles have characteristic shapes. OccGen argues that modeling the joint distribution of 3D occupancy with a generative process can exploit these scene-level priors to produce more coherent and complete predictions, especially in occluded or ambiguous regions.

The core idea is to use a score-based diffusion model that operates on a coarse 3D occupancy representation. A multi-modal condition network (built on a BEV encoder processing multi-camera images) provides the conditioning signal. During inference, OccGen iteratively denoises a randomly initialized 3D occupancy volume, progressively refining it toward a plausible scene configuration that is consistent with the camera observations. A lightweight refinement stage then upsamples the coarse generative output to produce fine-grained voxel predictions.

OccGen achieves strong results on the Occ3D-nuScenes benchmark, demonstrating that the generative formulation improves over discriminative baselines -- particularly for rare and geometrically complex classes where structural priors matter most. The paper also shows that the diffusion framework gracefully integrates multi-modal conditioning (cameras, and optionally LiDAR), and that the iterative refinement produces visually more coherent occupancy maps compared to single-pass methods.

## Key Contributions

- **Generative occupancy formulation**: First paper to formulate 3D occupancy prediction as a conditional generative task using score-based diffusion, demonstrating that modeling the joint distribution of voxels captures scene-level structural priors that discriminative methods miss
- **Multi-modal condition network**: A flexible BEV-based conditioning architecture that encodes multi-camera images (and optionally LiDAR) into a spatial conditioning signal for the diffusion process, enabling plug-and-play sensor fusion
- **Coarse-to-fine generation pipeline**: A two-stage approach where diffusion operates at coarse resolution for computational efficiency, followed by a lightweight upsampling refinement network to recover fine-grained details
- **Progressive denoising for occupancy**: Demonstrates that iterative refinement through the diffusion reverse process produces more spatially coherent predictions than single-pass feed-forward methods, with particular gains on geometrically complex and rare classes
- **Strong Occ3D-nuScenes results**: Competitive or superior performance to existing discriminative methods, validating the generative paradigm for this task

## Architecture / Method

```
┌────────────────────────────────────────────────────────────┐
│  Multi-Camera Images ──► 2D Backbone ──► View Transformer  │
│  (optional LiDAR) ──► Voxelize ──────┐                     │
│                                       │ fuse                │
│                    BEV Conditioning ◄─┘                     │
└─────────────────────────┬──────────────────────────────────┘
                          │ spatial conditioning signal
                          │
┌─────────────────────────▼──────────────────────────────────┐
│            Conditional Diffusion Model                      │
│                                                             │
│  Training:  GT occ ──► add noise ──► 3D U-Net denoiser     │
│                                      (conditioned on BEV)   │
│                                                             │
│  Inference: Gaussian  ──► denoise ──► denoise ──► ... ──►  │
│             noise        step 1      step 2     (T steps)  │
│                          ▲                                  │
│                          │ cross-attention to BEV features  │
│                          │ at each resolution level         │
└─────────────────────────┬──────────────────────────────────┘
                          │ coarse occupancy
                          ▼
┌─────────────────────────────────────────────────────────────┐
│          Refinement Network                                  │
│  3D conv decoder + skip connections ──► upsample to full    │
│  resolution ──► fine-grained semantic occupancy              │
└─────────────────────────────────────────────────────────────┘
```

OccGen's pipeline consists of three main components:

**1. Multi-modal Condition Network.** Multi-camera images are processed through a 2D backbone (e.g., ResNet-50 or Swin Transformer) to extract multi-scale features. These are projected into BEV space using a view transformer (LSS-style depth-based lifting or cross-attention). The resulting BEV features serve as the spatial conditioning signal for the diffusion model. When LiDAR is available, point cloud features are voxelized and fused into the BEV conditioning via concatenation or cross-attention.

**2. Conditional Diffusion Model.** The core generative component operates on a coarse 3D occupancy volume. During training, ground-truth occupancy is encoded into a compact representation, noise is added according to the forward diffusion schedule, and a 3D U-Net denoiser learns to predict the noise (or the clean occupancy directly) conditioned on the BEV features. The denoiser uses cross-attention layers to incorporate the multi-modal BEV conditioning at each resolution level. Standard DDPM training with a simplified loss is used.

**3. Refinement Network.** The coarse occupancy output from the diffusion model is upsampled via a lightweight 3D convolutional decoder with skip connections, producing the final fine-grained semantic occupancy prediction at full resolution. Multi-scale supervision (similar to SurroundOcc) is applied during training.

During inference, OccGen starts from Gaussian noise and runs the reverse diffusion process for T steps (typically 10-20 with DDIM acceleration), conditioned on the encoded camera/LiDAR observations, producing a coarse occupancy volume that is then refined to full resolution.

## Results

OccGen was evaluated on the Occ3D-nuScenes benchmark:

| Method | mIoU | Type |
|--------|------|------|
| MonoScene | 6.06 | Discriminative |
| TPVFormer | 11.26 | Discriminative |
| SurroundOcc | 20.30 | Discriminative |
| OccFormer | 21.93 | Discriminative |
| **OccGen** | **~22-23** | **Generative (diffusion)** |

Key findings:
- The generative formulation provides the largest improvements on rare and geometrically complex classes (e.g., construction vehicles, bicycles, traffic cones) where scene-level priors matter most
- Multi-modal conditioning (camera + LiDAR) yields additional gains over camera-only, demonstrating the flexibility of the conditioning framework
- DDIM acceleration reduces inference to 10-20 denoising steps with minimal quality loss compared to full 1000-step sampling
- Qualitative results show visually more coherent and complete occupancy maps, with fewer spurious predictions in free space and better completion of occluded regions

## Limitations & Open Questions

- **Inference speed**: Even with DDIM acceleration, the iterative denoising process is significantly slower than single-pass discriminative methods. This limits real-time deployment for autonomous driving where latency is critical
- **Computational cost**: The 3D U-Net denoiser operating on volumetric representations is memory-intensive, compounding the existing cost of occupancy prediction
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
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] -- LSS depth-based view transform used in the condition network
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational DDPM framework that OccGen adapts to 3D occupancy
- [[wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising]] -- related use of diffusion for BEV feature denoising (training-only), complementary approach
- [[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin]] -- efficiency-focused occupancy method, highlighting the speed gap OccGen needs to close
- [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]] -- Mamba-based occupancy with linear complexity, another efficiency contrast
