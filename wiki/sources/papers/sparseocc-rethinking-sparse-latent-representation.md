---
title: "SparseOcc: Rethinking Sparse Latent Representation for Vision-Based Semantic Occupancy Prediction"
tags: [autonomous-driving, perception, 3d-occupancy, computer-vision, sparse-representation, transformer]
status: active
type: paper
year: "2024"
venue: "CVPR"
citations: 50
arxiv_id: "2404.09502"
---

# SparseOcc: Rethinking Sparse Latent Representation for Vision-Based Semantic Occupancy Prediction

📄 **[Read on arXiv](https://arxiv.org/abs/2404.09502)**

## Overview

Dense 3D occupancy prediction from multi-view cameras has become a key perception task for autonomous driving, but most methods process the full voxel volume -- including the vast majority of voxels that are empty. SparseOcc rethinks this by operating exclusively on non-empty (occupied) voxels in a sparse latent space, dramatically reducing computational cost while actually improving prediction quality. The core observation is that real-world driving scenes are inherently sparse: typically only 5-15% of voxels in the perception volume are occupied, yet dense methods expend equal computation on empty and occupied regions.

The method introduces three novel components that work together: (1) a **Sparse Latent Diffuser** that propagates features among sparse voxels using decomposed orthogonal sparse convolutions along the X, Y, and Z axes, avoiding full 3D convolutions; (2) a **Sparse Feature Pyramid** that constructs multi-scale representations from the sparse voxels, combining coarse global context with fine-grained local detail; and (3) a **Sparse Transformer Head** that performs contextual reasoning on sparse data through self-attention among non-empty voxels. The sparse voxels are stored in COO (coordinate) format throughout, enabling memory-efficient processing.

On the nuScenes-Occupancy benchmark, SparseOcc achieves a **74.9% reduction in FLOPs** compared to dense baselines while improving mIoU from 12.8% to 14.1%. This is a notable result: the sparse method is not just more efficient but also more accurate, likely because removing the distraction of empty-space processing allows the network to focus representational capacity on the occupied regions that actually matter for downstream planning. The approach demonstrates that sparse processing is not merely a computational shortcut but a fundamentally better inductive bias for occupancy prediction.

## Key Contributions

- **Sparse latent representation for occupancy:** First method to process only non-empty voxels throughout the entire occupancy prediction pipeline, using COO-format sparse tensors for memory efficiency
- **Sparse Latent Diffuser:** Feature propagation via decomposed orthogonal sparse convolutions along three axes, enabling efficient information flow between occupied voxels without full 3D convolutions
- **Multi-scale Sparse Feature Pyramid:** Constructs coarse-to-fine sparse feature hierarchies, combining global scene context (from coarser levels) with local geometric detail (from finer levels)
- **Sparse Transformer Head:** Self-attention restricted to non-empty voxels for contextual reasoning, avoiding the quadratic cost of attending over the full volume
- **Simultaneous efficiency and accuracy gains:** 74.9% FLOP reduction with improved mIoU (12.8% to 14.1%), showing that sparsity is a better inductive bias, not just a compression trick

## Architecture / Method

![SparseOcc architecture overview](https://paper-assets.alphaxiv.org/figures/2404.09502/img-1.jpeg)

The SparseOcc pipeline processes multi-view camera images through three stages:

**1. Initial Sparse Representation:** Multi-view images are processed through a standard 2D backbone (e.g., ResNet-50) and view transformer to produce an initial 3D feature volume. A mask prediction module identifies which voxels are likely occupied, and only these voxels are retained in COO format -- a sparse tensor storing `(coordinates, features)` pairs for non-empty locations only. This initial sparsification step is critical: it discards the ~85-95% of voxels that are empty before any expensive 3D processing begins.

**2. Sparse Latent Diffuser:** The sparse voxel features are refined through decomposed sparse convolutions. Rather than applying full 3D convolutions (which would require densifying the representation), the Diffuser applies sparse convolutions independently along each axis (X, Y, Z) in an orthogonal decomposition. This enables efficient feature propagation: information flows between nearby occupied voxels along each dimension separately, then the results are combined. The decomposition reduces complexity from O(k^3) per convolution to O(3k) while maintaining expressive power, since features can still reach any neighbor within the receptive field through the composition of axis-aligned passes.

**3. Sparse Feature Pyramid:** To capture multi-scale context, the sparse voxels are organized into a feature pyramid with multiple resolution levels. At coarser levels, sparse voxels are grouped and pooled to provide global scene understanding (e.g., road layout, building outlines). At finer levels, the original sparse voxels retain detailed local geometry. Features from different scales are fused through top-down and lateral connections, all operating in sparse format.

**4. Sparse Transformer Head:** The final prediction head applies self-attention among the sparse voxels. Because attention is restricted to the ~5-15% of voxels that are non-empty, the quadratic cost of self-attention is dramatically reduced compared to attending over the full dense volume. This enables rich contextual reasoning -- e.g., recognizing that a set of sparse voxels forms a vehicle rather than isolated noise -- while remaining computationally feasible.

![Qualitative comparison with dense methods](https://paper-assets.alphaxiv.org/figures/2404.09502/img-3.jpeg)

The sparse processing has two important qualitative effects visible in the results: (1) SparseOcc produces cleaner predictions for continuous structures like roads and buildings because it avoids the hallucination artifacts that dense methods produce in empty regions; and (2) the method scales more gracefully to larger perception ranges because computation grows with the number of occupied voxels rather than the volume of the perception region.

## Results

![Quantitative results](https://paper-assets.alphaxiv.org/figures/2404.09502/img-2.jpeg)

Key results on nuScenes-Occupancy:

| Method | mIoU | FLOPs (relative) | Notes |
|--------|------|-------------------|-------|
| **SparseOcc** | **14.1%** | **25.1%** (74.9% reduction) | Sparse processing throughout |
| Dense baseline | 12.8% | 100% | Full 3D volume processing |
| OccFormer | 12.32% | ~100% | Dual-path transformer (SemanticKITTI) |
| FlashOcc | ~12-13% | ~25-33% | 2D-only with C2H reshape |

The most striking result is that SparseOcc improves accuracy while reducing compute -- a rare combination. Ablation studies validate each component:

- **Sparse Latent Diffuser:** Removing the orthogonal decomposition and using standard sparse 3D convolutions reduces mIoU by ~0.5% while increasing FLOPs
- **Sparse Feature Pyramid:** Single-scale sparse processing (no pyramid) drops mIoU by ~0.8%, confirming the importance of multi-scale context even in sparse settings
- **Sparse Transformer Head:** Replacing self-attention with MLP-only processing on sparse voxels reduces mIoU by ~0.6%, demonstrating the value of inter-voxel contextual reasoning

The qualitative results show that SparseOcc produces notably fewer hallucinations in empty regions and better preserves continuous surface geometry compared to dense baselines.

## Limitations & Open Questions

- **Initial mask quality:** The approach depends on an accurate initial sparsification step -- if occupied voxels are missed by the mask predictor, they cannot be recovered downstream. The quality of the mask predictor is a bottleneck.
- **Irregular sparsity patterns:** COO-format sparse tensors are less hardware-friendly than dense tensors on standard GPUs. While FLOPs are reduced, wall-clock speedup may be less dramatic due to irregular memory access patterns and lack of optimized sparse CUDA kernels for all operations.
- **Temporal integration:** The paper primarily addresses single-frame occupancy. Extending sparse representations to temporal fusion (aligning and merging sparse voxels across frames) is non-trivial because the set of occupied locations changes over time.
- **Scalability to larger ranges:** While sparse processing scales better than dense in principle, the initial view transformer still operates in dense mode. A fully sparse pipeline from images to output remains an open challenge.
- **Benchmark limitations:** The nuScenes-Occupancy benchmark has known limitations in ground truth quality, particularly for distant and thin structures. Performance differences in the 12-15% mIoU range should be interpreted cautiously.

## Connections

Related papers in the wiki:

- [[wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving]] — foundational dense occupancy method; SparseOcc addresses its computational inefficiency by processing only non-empty voxels
- [[wiki/sources/papers/occformer-dual-path-transformer-for-vision-based-3d-semantic-occupancy-prediction]] — dual-path decomposition of 3D processing; SparseOcc takes a more radical approach by eliminating dense processing entirely
- [[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin]] — another efficient occupancy method, but achieves efficiency through 2D-only processing + reshape rather than true sparse 3D processing
- [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]] — alternative sparse representation using 3D Gaussians instead of sparse voxels; both avoid dense grids but with different primitives
- [[wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction]] — probabilistic extension of Gaussian occupancy; shares the motivation of efficient sparse scene representation
- [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]] — addresses the same efficiency problem via linear-complexity Mamba rather than sparsity
- [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] — query-based view transformer that could serve as SparseOcc's initial BEV feature source
- [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] — lift-splat paradigm underlying the initial dense-to-sparse view transformation
- [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] — sparse scene representation for full E2E driving, extending sparsity from perception to planning
