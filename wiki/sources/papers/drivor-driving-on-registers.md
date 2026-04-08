---
title: "DrivoR: Driving on Registers"
type: source-summary
status: complete
updated: 2026-04-05
year: 2026
venue: arXiv
tags:
  - paper
  - autonomous-driving
  - e2e
  - perception
  - planning
  - transformer
  - vit
citations: 3
---

📄 **[Read on arXiv](https://arxiv.org/abs/2601.05083)**

# DrivoR: Driving on Registers

## Overview

DrivoR is a full-transformer autonomous driving architecture that uses camera-aware register tokens to compress multi-camera Vision Transformer features into a compact scene representation for trajectory planning. Rather than constructing explicit intermediate representations like Bird's Eye View (BEV) grids, 3D voxels, or vectorized maps, DrivoR relies on a small set of learnable register tokens that attend to all image patches across all cameras and capture planning-relevant information in a compressed form. The approach achieves NAVSIM state-of-the-art (PDMS 94.6) with a 3x throughput improvement over ViT-L baselines.

The core insight is that the intermediate representations between perception and planning can be radically simplified. Register tokens were originally introduced for Vision Transformers to absorb global information and reduce artifact tokens, but DrivoR repurposes them as a bridge between multi-camera perception and trajectory planning. By conditioning register tokens on camera intrinsics and extrinsics, the model learns to aggregate spatial information from all views into a compact set of planning-relevant features without requiring explicit 3D geometric construction.

This aligns with the broader trend toward end-to-end systems that learn their own representations, as seen in UniAD and EMMA, but DrivoR achieves this with much lower computational cost by avoiding large language models entirely. The architecture is purely transformer-based from image patches to trajectory output, demonstrating that strong driving performance does not require the overhead of language model backbones or complex multi-stage pipelines.

## Key Contributions

- **Camera-aware register tokens:** Extends the ViT register token concept (Darcet et al., ICLR 2024) to multi-camera driving -- each register token is conditioned on camera intrinsics/extrinsics, creating a compact, planning-relevant scene representation without explicit 3D construction
- **Full-transformer architecture:** Avoids complex intermediate representations (BEV, occupancy grids, vectorized maps) in favor of pure attention-based reasoning from image tokens to trajectory output
- **Disentangled generation and scoring:** Separate transformer decoders for trajectory generation and scoring with interpretable sub-score components (progress, comfort, collision avoidance), enabling behavior-conditioned driving without retraining
- **LoRA finetuning of DINOv2 backbone:** Efficient adaptation of pretrained ViT-S with minimal trainable parameters, leveraging strong visual features from self-supervised pretraining
- **3x compute reduction:** Over 3x reduction in GFLOPs and peak memory versus ViT-L baselines while maintaining SOTA performance

## Architecture / Method

```
┌──────────────────────────────────────────────────────────────┐
│            DrivoR: Driving on Registers Architecture          │
│                                                               │
│  Multi-Camera Images (4 cameras)                              │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐                    │
│  │Front │  │ FL   │  │ FR   │  │ Back │                    │
│  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘                    │
│     │         │         │         │                          │
│     ▼         ▼         ▼         ▼                          │
│  ┌──────────────────────────────────────────┐               │
│  │  DINOv2 ViT-S + LoRA (per camera)        │               │
│  │  Patch tokens + R register tokens each    │               │
│  │  (camera intrinsics/extrinsics injected)  │               │
│  └──────────────────┬───────────────────────┘               │
│                     │ Discard patch tokens,                  │
│                     │ keep only N x R registers              │
│                     ▼                                        │
│  ┌──────────────────────────────────────────┐               │
│  │  Cross-Camera Self-Attention              │               │
│  │  (registers from all cameras exchange     │               │
│  │   information ──► unified scene tokens)   │               │
│  └──────────────────┬───────────────────────┘               │
│                     ▼                                        │
│     ┌───────────────┴───────────────┐                       │
│     ▼                               ▼                       │
│  ┌───────────────────┐  ┌────────────────────┐              │
│  │ Trajectory Gen    │  │ Disentangled       │              │
│  │ Decoder           │  │ Scoring Decoder    │              │
│  │ (k transformer    │  │ (no gradient flow  │              │
│  │  blocks + ego     │  │  from scorer to    │              │
│  │  state + WTA loss)│  │  generator)        │              │
│  │  ──► |Q| candidate│  │  ──► 6 sub-scores  │              │
│  │     trajectories  │  │  (safety, comfort, │              │
│  └────────┬──────────┘  │   efficiency)      │              │
│           │             └────────┬───────────┘              │
│           └──────────┬───────────┘                          │
│                      ▼                                       │
│           Best-scored trajectory                             │
└──────────────────────────────────────────────────────────────┘
```

DrivoR's architecture has three main stages: multi-camera feature extraction, register-based scene compression, and disentangled trajectory generation and scoring.

In the feature extraction stage, each camera image (typically four cameras: front, front-left, front-right, and back) is processed by a DINOv2 ViT-S backbone fine-tuned with LoRA adapters, reducing trainable parameters and enabling efficient learning of vision-to-register compression. R additional camera-specific register tokens are appended to each camera's ViT input. At the final layer, only the R camera registers are retrieved, forming compact "scene tokens" as planning-relevant scene descriptors. This creates N x R grouped registers (N cameras), dramatically reducing token count while preserving essential information.

In the scene compression stage, the register tokens from all cameras are collected and processed through additional transformer layers. Through self-attention, register tokens from different cameras exchange information, creating a unified scene representation. The total number of register tokens is orders of magnitude smaller than the total number of image patch tokens, achieving aggressive compression while retaining planning-relevant information.

**Trajectory Generation Decoder**: Uses learnable trajectory queries processed through k standard transformer blocks with self-attention, cross-attention to scene tokens, and feed-forward networks. Ego status information (poses, velocities, accelerations, driving commands) is encoded and integrated with trajectory queries. Outputs |Q_traj| candidate trajectories, each a sequence of n_p poses (x, y, theta). Training employs a Winner-Takes-All (WTA) loss: L_traj = min_i (||tau_i - tau_hat||_1 + ||tau_i - tau_hat'||_1), where tau_hat' represents an optional accelerated target to encourage reaching farther waypoints.

**Disentangled Scoring Decoder**: A critical design choice separates trajectory generation and scoring. Each decoded trajectory is transformed into score queries via an MLP, ensuring the scorer only processes decoded trajectories. Gradients from the scoring decoder are prevented from flowing back to the trajectory decoder, maintaining separation during training. The scorer predicts six separate sub-score components aligned with the Predictive Driver Model Score (PDMS), including safety, comfort, and efficiency metrics. Scoring loss uses Binary Cross Entropy: L_score = sum_c lambda_c sum_i BCE(G_theta_c(tau_i), G_c(tau_i)). Total loss: L = L_traj + lambda_s * L_score.

## Results

| Benchmark | Metric | DrivoR | Best Competing | Human |
|-----------|--------|--------|----------------|-------|
| NAVSIM-v1 | PDMS | 94.6 | 93.8 (RAP-DINO) | 94.8 |
| NAVSIM-v2 (navhard) | EPDMS | 54.6 | 53.2 (SimScale) | - |
| HUGSIM (zero-shot) | Road Completion | 49.8 | - | - |
| HUGSIM (zero-shot) | HD-Score | 35.7 | - | - |

| Efficiency Metric | DrivoR | ViT-L Baseline | Reduction |
|-------------------|--------|----------------|-----------|
| Forward Pass Latency | 110ms | 400ms | 3x |
| GFLOPs | ~3x lower | Baseline | 3x |
| Peak Memory | ~3x lower | Baseline | 3x |
| Parameters | ~40M | - | - |

- **NAVSIM-v1 SOTA**: PDMS 94.6 with 134k SimScale data, surpassing all camera-only methods and approaching human driver performance (94.8)
- **NAVSIM-v2 SOTA**: EPDMS 54.6 on the challenging `navhard-two-stage` split, setting a new benchmark
- **Efficiency**: Over 3x throughput improvement (400ms to 110ms per forward pass on single A100 GPU), with 3x reductions in GFLOPS and peak memory; complete model approximately 40M parameters
- **Zero-shot transfer**: Highest reported HUGSIM scores (Road Completion 49.8, HD-Score 35.7) without finetuning, demonstrating strong generalization
- **Register compression superiority**: Register-based compression (90.0 PDMS) outperforms spatial pooling (89.7) and transformer decoder-based compression (89.3), nearly matching models using 250x more tokens with minimal computational overhead
- **Pretraining critical**: DINOv2 pretraining provides over 15 PDMS points improvement versus random initialization; LoRA finetuning demonstrates superior performance and robustness compared to frozen backbones
- **Disentanglement validated**: Separate branches improve over single branch (86.8 vs. 84.7 PDMS); gradient blocking between modules further enhances results (90.0 vs. 86.8 without disentanglement)
- **Interpretable register specialization**: Front camera registers show high de-correlation (specializing for lead vehicles and traffic lights) while rear camera registers exhibit increased correlation, aligning with driving intuition about relative information importance
- Ablation studies confirm that camera-aware conditioning of register tokens is essential -- removing camera embeddings degrades performance significantly

## Limitations & Open Questions

- Evaluated only on NAVSIM benchmarks -- no closed-loop evaluation in CARLA or Bench2Drive, and no real-world deployment evidence
- Camera-only approach does not incorporate LiDAR, raising questions about robustness in adverse weather and lighting conditions
- The register token approach compresses aggressively -- unclear if this loses fine-grained spatial information needed for rare edge cases like small objects or unusual road geometries
- Future directions include incorporating historical frames, additional sensor modalities beyond cameras, and map information into the register-based compression scheme

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/perception]]
- [[wiki/concepts/planning]]
- [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]]
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]]
- [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]]
- [[wiki/sources/papers/deep-residual-learning-for-image-recognition]]
