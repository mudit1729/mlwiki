---
title: "Open Questions: BEV Perception & 3D Occupancy"
type: query
status: active
updated: 2026-04-07
tags:
  - questions
  - perception
  - bev
  - occupancy
  - 3d
---

# Open Questions: BEV Perception & 3D Occupancy

Stream-specific open questions for the BEV perception and 3D occupancy pillar. See [[wiki/queries/open-questions]] for the full tree across all streams.

## Representation paradigm

1. **Dense vs. sparse vs. Gaussian:** [[wiki/sources/papers/bevnext-reviving-dense-bev-frameworks-for-3d-object-detection|BEVNeXt]] revived dense BEV to 64.2 NDS SOTA. [[wiki/sources/papers/sparseocc-fully-sparse-3d-occupancy-prediction|SparseOcc]] introduced fully sparse prediction. [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction|GaussianFormer]] represents scenes as sparse 3D Gaussians (5-6x memory reduction). [[wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction|GaussianFormer-2]] reduces overlap by 64% with probabilistic superposition. Which paradigm will win at production scale: the accuracy of dense, the efficiency of sparse, or the flexibility of Gaussians?

2. **Voxels vs. world models:** [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving|OccWorld]] and [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world|Drive-OccWorld]] predict future occupancy states for planning. [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction|GaussianWorld]] models scene evolution. Is occupancy prediction converging toward world models (predict future states) rather than single-frame reconstruction?

3. **Self-supervised occupancy:** [[wiki/sources/papers/selfocc-self-supervised-vision-based-3d-occupancy-prediction|SelfOcc]] eliminated the 3D annotation bottleneck. [[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting|GaussianOcc]] achieves fully self-supervised estimation without even ground-truth poses. [[wiki/sources/papers/gausstr-foundation-model-aligned-gaussian-transformer-for-self-supervised-3d|GaussRender]] uses foundation model alignment for zero-shot semantics. Will self-supervised methods close the gap to supervised, making dense 3D annotation obsolete?

## Efficiency and deployment

4. **Linear-complexity architectures:** [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models|OccMamba]] replaces transformer quadratic attention with linear state-space models (+5.1% IoU, 65% faster). Is Mamba-style linear modeling the path to real-time 3D occupancy, or are efficient transformer variants (FlashAttention, sparse attention) sufficient?

5. **Training-only augmentation:** [[wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising|BEVDiffuser]] uses a diffusion model for BEV denoising that is removed at inference (zero overhead, +12.3% mAP). [[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin|FlashOcc]]'s Channel-to-Height plugin replaces 3D convolutions with 2D processing. How much deployment-free training enrichment can close the gap between efficient and accurate architectures?

6. **Real-time occupancy budget:** For production driving at 10+ Hz, what is the acceptable quality/latency trade-off for 3D occupancy? Is 20 mIoU at 30 FPS more valuable than 40 mIoU at 5 FPS?

## View transformation and depth

7. **Forward vs. backward view transforms:** [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d|LSS]] (forward, geometric) vs. [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers|BEVFormer]] (backward, learned attention) vs. [[wiki/sources/papers/fb-bev-bev-representation-from-forward-backward-view-transformations|FB-BEV]] (both fused). Has FB-BEV settled this debate, or does the optimal approach depend on deployment constraints (compute, latency, accuracy requirements)?

8. **Depth estimation bottleneck:** [[wiki/sources/papers/bevnext-reviving-dense-bev-frameworks-for-3d-object-detection|BEVNeXt]]'s CRF-modulated depth and [[wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting|GaussianLSS]]'s explicit depth uncertainty both improve depth quality. [[wiki/sources/papers/bevformer-v2-adapting-modern-image-backbones-to-birds-eye-view-recognition-via-perspective-supervision|BEVFormer v2]]'s perspective supervision adapts any backbone to 3D. Is monocular depth estimation still the primary bottleneck for camera-only 3D perception?

## Occupancy in E2E systems

9. **Occupancy role in planning:** [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world|Drive-OccWorld]] shows 33% L2 error reduction when planning against predicted occupancy. [[wiki/sources/papers/occgen-generative-multi-modal-3d-occupancy-prediction-for-autonomous-driving|OccGen]] applies diffusion to occupancy (+9.5-13.3% over discriminative). But E2E VLA systems ([[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving|EMMA]], [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving|DriveTransformer]]) bypass explicit occupancy. Is occupancy a necessary intermediate representation, or will it be absorbed into learned E2E representations?

10. **Evaluation metrics:** [[wiki/sources/papers/sparseocc-fully-sparse-3d-occupancy-prediction|SparseOcc]]'s RayIoU became a community standard. But does mIoU or RayIoU actually correlate with downstream driving quality? No paper has rigorously tested this. The perception→planning alignment gap applies to occupancy metrics as much as detection metrics.

## Partially answered

- **Q1 (Dense vs. sparse vs. Gaussian):** GaussianFormer-2's probabilistic superposition and OccMamba's linear SSMs suggest the field is moving away from dense voxels. But BEVNeXt's dense SOTA shows that dense methods aren't dead.
- **Q3 (Self-supervised):** GaussianOcc and GaussRender demonstrate fully self-supervised is viable. The gap to supervised is closing but remains significant for fine-grained semantic classes.
- **Q7 (View transforms):** FB-BEV showed both are complementary. The practical answer is likely deployment-dependent.

## Key papers for this stream

| Paper | Relevance |
|-------|-----------|
| [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] | LSS: foundational BEV paradigm |
| [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] | Learned BEV via deformable attention |
| [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]] | Gaussian scene representation |
| [[wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction]] | Probabilistic Gaussian superposition |
| [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]] | Occupancy world model |
| [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]] | Linear-complexity occupancy |
| [[wiki/sources/papers/bevnext-reviving-dense-bev-frameworks-for-3d-object-detection]] | Dense BEV revival |
| [[wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving]] | Foundational occupancy prediction |
| [[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin]] | Efficient 2D-only occupancy |
| [[wiki/sources/papers/sparseocc-fully-sparse-3d-occupancy-prediction]] | Sparse occupancy + RayIoU metric |

## Related

- [[wiki/concepts/perception]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/queries/open-questions]]
- [[wiki/queries/open-questions-e2e]]
