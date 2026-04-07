---
title: Perception
type: concept
status: active
updated: 2026-04-05
tags:
  - perception
  - scene-understanding
---

# Perception

Perception converts raw sensor data into structured scene representations for downstream prediction and planning. In autonomous driving, perception encompasses detection, tracking, segmentation, occupancy estimation, lane extraction, and the construction of unified scene representations. The last five years have seen a decisive shift toward bird's-eye-view (BEV) representations and transformer-based architectures.

## The BEV revolution

The central challenge of camera-based perception for driving is projecting multiple perspective-view images into a common spatial representation suitable for planning. Two landmark papers define the modern approach.

**Lift-Splat-Shoot** ([[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]], 2020) introduced the lift-splat paradigm: for each pixel, predict a depth distribution, "lift" features into 3D using this distribution, then "splat" them into a BEV grid via pillar pooling. This was the first practical method for generating BEV features from arbitrary multi-camera rigs without explicit depth supervision. The approach remains the backbone of many production perception systems.

**BEVFormer** ([[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]], 2022) replaced the geometric lift-splat projection with learned spatial cross-attention. BEV queries attend to image features through deformable attention at 3D reference points, and temporal self-attention aggregates information across frames. BEVFormer demonstrated strong results on nuScenes detection and segmentation, and its query-based design influenced downstream joint systems like UniAD.

**FB-BEV** ([[wiki/sources/papers/fb-bev-bev-representation-from-forward-backward-view-transformations]], ICCV 2023) unified both paradigms, showing that forward (LSS-style depth projection) and backward (BEVFormer-style query attention) view transformations are complementary. By running both branches and fusing their BEV features with learned gating, FB-BEV achieved +3 NDS over BEVFormer alone on nuScenes. A 3D pre-training strategy using LiDAR depth supervision further bootstraps the forward branch, demonstrating that combining geometric and attention-based view transforms yields the strongest BEV representations.

**BEVNeXt** ([[wiki/sources/papers/bevnext-reviving-dense-bev-frameworks-for-3d-object-detection]], CVPR 2024) demonstrated that dense BEV frameworks can be revived to surpass query-based alternatives through targeted modernization. Three key upgrades -- CRF-modulated depth estimation for object-level depth consistency, long-term recurrent temporal aggregation with large-kernel convolutions, and a two-stage object decoder combining perspective and BEV features -- pushed the dense BEV paradigm to 64.2 NDS on nuScenes test, outperforming both BEVFormer v2 and query-based methods like StreamPETR.

**BEVFormer v2** ([[wiki/sources/papers/bevformer-v2-adapting-modern-image-backbones-to-birds-eye-view-recognition-via-perspective-supervision]], CVPR 2023) solved a critical limitation of the original: modern 2D backbones (InternImage, ConvNeXt) trained on ImageNet performed poorly for BEV tasks due to the domain gap between 2D classification and 3D scene understanding. By adding perspective supervision -- an auxiliary 3D detection head operating directly on backbone features in perspective view -- BEVFormer v2 provides dense gradients that adapt any backbone to 3D perception without depth-specific pre-training. This enabled InternImage-XL to achieve 63.4% NDS on nuScenes, surpassing prior art by 2.4% NDS.

## Camera vs. LiDAR

A persistent debate in driving perception concerns the right sensor suite:

- **LiDAR-centric systems** provide accurate 3D geometry directly but are expensive, mechanically complex, and produce sparse point clouds that require specialized architectures. Early autonomous stacks (Waymo, Cruise) relied heavily on LiDAR.
- **Camera-only systems** are far cheaper and higher resolution but require solving the ill-posed depth estimation problem. The BEV revolution made camera-only competitive on benchmarks. Tesla's production system is camera-only.
- **Fusion approaches** like [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] combine camera and LiDAR features through transformer cross-attention, often achieving the best benchmark numbers. The question is whether LiDAR is worth the cost and complexity at deployment scale.

The [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] dataset has been the standard benchmark for evaluating all three paradigms, providing synchronized camera, LiDAR, and radar data with 3D annotations.

## Map and lane representations

Perception also encompasses extracting road topology and lane structure. [[wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation]] introduced vectorized polyline encoding for HD maps and agent trajectories, replacing rasterized map representations with more efficient and expressive graph structures. This vectorized paradigm was adopted by subsequent systems: [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] extended it to full end-to-end driving, and [[wiki/sources/papers/learning-lane-graph-representations-for-motion-forecasting]] (LaneGCN) built graph convolutions over lane topology for prediction.

## Perception in end-to-end systems

In the end-to-end era, perception is no longer a standalone module but part of a jointly trained system. [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) showed that training perception with a planning-centric loss improves both perception quality and downstream planning. The trend is toward implicit perception: systems like [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] process raw images through a VLM and directly output driving decisions, with no explicit intermediate 3D representation.

However, interpretability concerns push back against fully implicit perception. [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] uses explicit BEV world models for trajectory evaluation, arguing that spatial grounding improves safety verification. The tension between implicit and explicit perception representations remains unresolved.

## Occupancy and scene representation

Beyond object detection, occupancy prediction has emerged as an alternative perception paradigm. Rather than detecting and classifying individual objects, occupancy methods predict which 3D voxels are occupied and by what semantic class. This handles irregular objects (construction debris, fallen trees) that detection-based systems struggle with. The [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] ecosystem now includes occupancy benchmarks alongside detection.

**SurroundOcc** ([[wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving]], ICCV 2023) was one of the foundational papers establishing camera-based 3D occupancy prediction. It uses spatial cross-attention to lift multi-view 2D features into a 3D volume, then applies a coarse-to-fine 3D U-Net decoder with multi-scale supervision (scene-class affinity loss + lovasz-softmax) to produce dense voxel predictions. Critically, SurroundOcc introduced an automated dense ground truth generation pipeline -- aggregating multi-frame LiDAR, applying Poisson surface reconstruction, and propagating labels via nearest-neighbor -- that solved the annotation bottleneck and enabled subsequent occupancy research. It achieved 20.30 mIoU on nuScenes, nearly tripling prior camera-only methods.

**OccFormer** ([[wiki/sources/papers/occformer-dual-path-transformer-for-vision-based-3d-semantic-occupancy-prediction]], ICCV 2023) introduced an efficient dual-path transformer for dense 3D occupancy prediction from cameras. Rather than applying full 3D attention, OccFormer decomposes processing into local (per-height-slice 2D attention) and global (height-averaged BEV attention) pathways, then uses a Mask2Former-based decoder with preserve-pooling and class-guided sampling to handle sparse structures and class imbalance. It achieved 12.32% mIoU on SemanticKITTI (camera-only SOTA at the time) and became an influential baseline that subsequent methods like GaussianFormer explicitly compare against.

[[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] (Drive-OccWorld, 2024) takes occupancy prediction further by building a 4D occupancy forecasting world model that predicts future occupancy states conditioned on ego actions. The system uses semantic-conditional and motion-conditional normalization to address BEV artifacts, achieving 9.4% improvement in occupancy forecasting and 33% reduction in planning L2 error at 1s horizon compared to UniAD. Its occupancy-based planner evaluates candidate trajectories against predicted future occupancy, handling irregular objects that detection-based systems miss.

**GaussianLSS** ([[wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting]], 2025) addresses the efficiency-accuracy trade-off in BEV perception by extending LSS with explicit depth uncertainty modeling and Gaussian Splatting. By predicting depth distributions per pixel and transforming uncertainty into 3D Gaussians that are splatted onto the BEV plane, GaussianLSS achieves 38.3% IoU (within 0.4% of SOTA PointBEV) at 2.5x the speed and 3.8x less memory, making it practical for deployment.

**GaussianFormer** ([[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]], ECCV 2024) takes a fundamentally different approach to occupancy prediction, representing scenes as sparse sets of 3D semantic Gaussians rather than dense voxel grids. Each Gaussian adaptively models position, shape, and semantics, with a transformer decoder refining properties through self-encoding and cross-attention to multi-view images. The result is 5-6x memory reduction vs. SurroundOcc/OccFormer with only ~2% mIoU trade-off. **OccWorld** ([[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]], ECCV 2024) introduced the original occupancy world model, using VQ-VAE tokenization and a GPT-like spatial-temporal transformer for autoregressive 4D occupancy forecasting and joint ego planning, achieving competitive performance with UniAD despite requiring no HD maps or instance annotations.

[[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]] reformulates occupancy prediction as a world modeling problem, using 3D Gaussians to model scene evolution over time. By decomposing changes into ego motion alignment, dynamic object movement, and new area completion, GaussianWorld achieves over 2% mIoU improvement without additional inference overhead. [[wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation]] takes a complementary approach, unifying 3D scene understanding and future scene generation within a single LLM framework using BEV tokenization and differentiable volume rendering.

**FlashOcc** ([[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin]], 2023) takes a radically simple approach to efficient occupancy: replace all 3D convolutions with 2D BEV processing and a zero-cost Channel-to-Height reshape that splits the channel dimension into height bins. The plug-and-play C2H module integrates with existing BEV frameworks (BEVDet, FB-OCC) to achieve 3-4x faster inference and 2-3x memory reduction with only modest accuracy trade-offs on Occ3D-nuScenes; its temporal variant (FlashOcc-T) closes the gap entirely.

**GaussianFormer-2** ([[wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction]], CVPR 2025) introduces a probabilistic Gaussian superposition model where each Gaussian represents an occupancy probability and Gaussians combine via multiplication rather than addition. This reduces overlap by 64% and achieves superior performance with only 8.9% of the Gaussians (25,600 vs 144,000) and 51% memory reduction compared to GaussianFormer.

**OccMamba** ([[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]], CVPR 2025) is the first Mamba-based network for occupancy prediction, replacing transformer quadratic complexity with linear state-space modeling. Its height-prioritized 2D Hilbert expansion preserves spatial locality when flattening 3D voxels to 1D sequences, achieving +5.1% IoU over prior SOTA with 65% inference time reduction.

**GaussianOcc** ([[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting]], ICCV 2025) achieves *fully self-supervised* occupancy estimation (no ground-truth poses, no 3D annotations) by using Gaussian splatting for both pose learning (GSP) and fast voxel rendering (GSV), delivering 2.7x faster training and 5x faster rendering. **GaussianFlowOcc** ([[wiki/sources/papers/gaussianflowocc-sparse-occupancy-with-gaussian-splatting-and-temporal-flow]], ICCV 2025) replaces dense voxel grids with sparse 3D Gaussian distributions plus temporal flow, achieving 51%+ mIoU improvement and 50x faster inference with only 2D pseudo-label supervision. **GaussRender** ([[wiki/sources/papers/gaussrender-learning-3d-occupancy-with-gaussian-rendering]], ICCV 2025) adds a plug-and-play Gaussian rendering loss for projective 3D-2D consistency during training, improving TPVFormer by +3.75 mIoU with zero inference overhead.

## Radar-camera fusion

Radar offers a cost-effective alternative to LiDAR, providing direct distance and velocity measurements in all weather. **RaCFormer** ([[wiki/sources/papers/racformer-query-based-radar-camera-fusion-for-3d-object-detection]], CVPR 2025) addresses depth misalignment in radar-camera fusion through query-based dual-view attention, radar-aware depth prediction, and an implicit dynamic catcher using the Doppler effect. It achieves 64.9% mAP and 70.2% NDS on nuScenes -- surpassing LiDAR-only baselines at a fraction of the sensor cost.

**GaussTR** ([[wiki/sources/papers/gausstr-foundation-model-aligned-gaussian-transformer-for-self-supervised-3d]], CVPR 2025) achieves zero-shot semantic occupancy prediction without 3D annotations by aligning sparse 3D Gaussians with 2D Vision Foundation Models (CLIP, DINO) through differentiable splatting. It reaches 12.27 mIoU on Occ3D-nuScenes using only 3% of scene representation parameters, demonstrating that self-supervised approaches can bypass expensive 3D labeling.

**BEVDiffuser** ([[wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising]], CVPR 2025) tackles BEV feature noise via a training-only diffusion model conditioned on ground-truth object layouts. Removed at inference (zero overhead), it yields 12.3% mAP and 10.1% NDS improvement on nuScenes, with 20-29% mAP gains in night scenarios -- demonstrating that BEV feature quality is a bottleneck worth addressing directly.

## Present state and open problems

- **Perception-planning alignment:** Optimizing perception for perception metrics (mAP, NDS) does not guarantee improved planning. The field needs perception metrics that correlate with downstream driving quality.
- **Long-range perception:** Current BEV methods degrade significantly beyond 50-70m. Highway driving demands reliable perception at 150m+.
- **Adverse conditions:** Rain, fog, glare, and night driving remain unsolved for camera-only systems.
- **Temporal reasoning:** Single-frame perception misses velocity, acceleration, and intent cues. Temporal BEV models (BEVFormer) help but are not sufficient for complex multi-agent reasoning.
- **Online mapping:** The push toward map-light and map-free driving requires perception systems to construct road topology on the fly, without HD map priors.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d]] | Lift-Splat paradigm for multi-camera BEV |
| [[wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers]] | Query-based spatiotemporal BEV with deformable attention |
| [[wiki/sources/papers/fb-bev-bev-representation-from-forward-backward-view-transformations]] | Unified forward-backward view transformation combining LSS and BEVFormer paradigms |
| [[wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving]] | Foundational multi-camera 3D occupancy prediction with dense GT pipeline |
| [[wiki/sources/papers/bevformer-v2-adapting-modern-image-backbones-to-birds-eye-view-recognition-via-perspective-supervision]] | Perspective supervision for backbone-agnostic BEV perception |
| [[wiki/sources/papers/bevnext-reviving-dense-bev-frameworks-for-3d-object-detection]] | CRF-modulated depth + long-term temporal aggregation revives dense BEV to 64.2 NDS SOTA |
| [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] | Standard multimodal driving dataset |
| [[wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation]] | Vectorized map and agent encoding |
| [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] | Camera-LiDAR fusion via transformers |
| [[wiki/sources/papers/planning-oriented-autonomous-driving]] | Joint perception-prediction-planning training |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Implicit perception via VLM |
| [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] | Explicit BEV world model for trajectory verification |
| [[wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting]] | Uncertainty-aware LSS with Gaussian Splatting for efficient BEV |
| [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] | 4D occupancy forecasting world model for planning |
| [[wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation]] | Self-supervised 3D spatio-temporal MLLM for driving |
| [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]] | 3D Gaussian world model for streaming occupancy |
| [[wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation]] | Unified 3D understanding + generation world model |
| [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]] | ViT: transformers for vision, backbone for many BEV systems |
| [[wiki/sources/papers/swin-transformer-hierarchical-vision-transformer-using-shifted-windows]] | Hierarchical vision transformer with shifted windows; standard backbone for BEV and detection systems |
| [[wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction]] | Probabilistic Gaussian superposition for efficient 3D occupancy |
| [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]] | First Mamba-based occupancy network with linear complexity |
| [[wiki/sources/papers/gausstr-foundation-model-aligned-gaussian-transformer-for-self-supervised-3d]] | Self-supervised 3D occupancy via foundation model alignment |
| [[wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising]] | Training-only diffusion for BEV denoising, zero inference overhead |
| [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]] | Sparse 3D Gaussian occupancy with 5-6x memory reduction |
| [[wiki/sources/papers/driving-gaussian-composite-gaussian-splatting-for-surrounding-dynamic-driving-scenes]] | Gaussian splatting for dynamic driving scene reconstruction |
| [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]] | Original 3D occupancy world model with VQ-VAE tokenization |
| [[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting]] | Fully self-supervised occupancy via Gaussian splatting (no GT pose) |
| [[wiki/sources/papers/gaussianflowocc-sparse-occupancy-with-gaussian-splatting-and-temporal-flow]] | Sparse Gaussian occupancy + temporal flow, 50x faster inference |
| [[wiki/sources/papers/gaussrender-learning-3d-occupancy-with-gaussian-rendering]] | Plug-and-play Gaussian rendering loss for 3D-2D consistency |
| [[wiki/sources/papers/racformer-query-based-radar-camera-fusion-for-3d-object-detection]] | Radar-camera fusion via query-based dual-view attention |
| [[wiki/sources/papers/occformer-dual-path-transformer-for-vision-based-3d-semantic-occupancy-prediction]] | Dual-path transformer for efficient dense 3D semantic occupancy |
| [[wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin]] | Channel-to-Height plugin for 2D-only occupancy, 3-4x faster inference |
| [[wiki/sources/papers/yolov10-real-time-end-to-end-object-detection]] | NMS-free real-time detection via consistent dual assignments; holistic efficiency-accuracy optimization |

## Related

- [[wiki/concepts/prediction]]
- [[wiki/concepts/planning]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/sources/autonomous-driving-seminal-papers]]
