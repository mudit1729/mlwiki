---
title: "RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: ICLR
tags:
  - paper
  - robotics
  - diffusion
  - bimanual
  - foundation-model
citations: ~60
arxiv_id: "2410.07864"
---

# RDT-1B: A Diffusion Foundation Model for Bimanual Manipulation

[Read on arXiv](https://arxiv.org/abs/2410.07864)

## Overview

RDT-1B (Tsinghua University, ICLR 2025) presents the largest diffusion transformer for bimanual robot manipulation, scaling to 1.2B parameters. Bimanual manipulation -- using two robot arms simultaneously -- is significantly more challenging than single-arm manipulation due to the high-dimensional action space (14+ DoF), the need for coordination between arms, and the scarcity of bimanual training data. RDT-1B addresses these challenges by adapting the Diffusion Transformer (DiT) architecture from image generation to robot action generation, with specific innovations for bimanual coordination.

The model is pre-trained on a large multi-robot dataset and fine-tuned for bimanual tasks, demonstrating that the diffusion transformer scaling paradigm transfers from image generation to robotic manipulation. RDT-1B achieves state-of-the-art results on bimanual benchmarks, including tasks requiring tight two-arm coordination like folding cloth, pouring between containers, and bimanual pick-and-place.

## Key Contributions

- **Largest diffusion transformer for manipulation**: 1.2B parameters, the first diffusion-based foundation model explicitly designed for bimanual manipulation, demonstrating that scaling improves coordination performance
- **Physically interpretable unified action space**: A 128-dimensional unified action space maps heterogeneous robot actions while preserving physical meaning, enabling cross-robot transfer learning
- **Architectural adaptations for robotics**: QKNorm, RMSNorm, non-linear MLP decoder, and Alternating Condition Injection (ACI) for balanced vision-language conditioning and stable scaling
- **Pre-training + fine-tuning paradigm**: Pre-trained on 46 datasets comprising 1M+ trajectories and 21TB of data, then fine-tuned on 6,000+ bimanual task trajectories across 300+ tasks

## Architecture

```
┌─────────────┐  ┌───────────────┐  ┌──────────────────┐
│ Multi-View  │  │   Language    │  │  Proprioceptive  │
│ Camera Imgs │  │  Instruction  │  │  State (L+R arm) │
│ (3 views)   │  │  (variable)   │  │  MLP + Fourier   │
└──────┬──────┘  └───────┬───────┘  └────────┬─────────┘
       │                 │                   │
       ▼                 ▼                   │
┌──────────────┐ ┌───────────────┐           │
│ Frozen Vision│ │ Frozen T5-XXL │           │
│ Encoder      │ │  Text Encoder │           │
│  (SigLIP)    │ │  + attn mask  │           │
└──────┬───────┘ └───────┬───────┘           │
       │                 │                   │
       │  Alternating Condition Injection    │
       └────────┐ ┌──────┘                   │
                ▼ ▼                          │
┌───────────────────────────────────────┐    │
│     Diffusion Transformer (1.2B)     │    │
│  ┌─────────────────────────────────┐  │    │
│  │ Noised Action Tokens            │◄─┼────┘
│  │ 128-dim unified action space    │  │
│  ├─────────────────────────────────┤  │
│  │ Self-Attention (QKNorm)         │  │
│  │ Cross-Attention (ACI)           │  │
│  │ RMSNorm + MLP decoder           │  │
│  └─────────────────────────────────┘  │
│          × N DiT blocks              │
└───────────────────┬───────────────────┘
                    │
                    ▼  DPM-Solver++ (5 steps)
          ┌─────────────────┐
          │  Action Chunk   │
          │  @ 6 Hz freq    │
          │  Left + Right   │
          └─────────────────┘
```

## Method

RDT-1B adapts the Diffusion Transformer (DiT) architecture for robot action generation with robotics-specific modifications:

1. **Input Representation**: The model takes as input:
   - Three camera views (encoded via a frozen SigLIP vision encoder with multi-dimensional positional embeddings)
   - Language instruction (encoded via a frozen T5-XXL encoder with attention masks for variable-length instructions)
   - Proprioceptive state of both arms (encoded via MLP with Fourier features for high-frequency dynamics)
   - Noised action sequence (the diffusion input)

2. **Diffusion Transformer (DiT) Backbone**: The core architecture is a 1.2B parameter transformer processing noised action tokens over a 128-dimensional unified action space (which maps heterogeneous robot actions while preserving physical meaning):
   - **Action tokenization**: Actions are represented in the 128-dim unified action space, enabling cross-robot pre-training
   - **Conditioning via ACI**: Vision and language features are balanced through Alternating Condition Injection (ACI), which alternates the primary conditioning modality across layers
   - **Normalization**: QKNorm and RMSNorm replace standard LayerNorm for training stability at scale
   - **Non-linear MLP decoder**: A non-linear MLP output head approximates the nonlinearity in robot action distributions, replacing the standard linear projection

3. **Training**: Pre-trained on 46 datasets comprising over 1 million trajectories and 21TB of data for one month on 48 H100 GPUs. Fine-tuned on 6,000+ bimanual task trajectories (300+ tasks, 100+ objects, 15+ scenes) for three days on the same hardware. Data augmentation includes color jittering, image corruption, Gaussian noise, and instruction augmentation.

4. **Inference**: DPM-Solver++ reduces diffusion steps from 100 to 5, achieving 6 Hz action chunk frequency (with 381 Hz average action predictions from those chunks). Action chunking provides temporal consistency and enables coordinated bimanual motions.

**Scaling**: Ablations compare a 166M parameter variant to the full 1.2B model. The larger model substantially outperforms the smaller one, with scale particularly benefiting coordination-heavy tasks.

## Results

RDT-1B achieves a **56% average improvement in success rates** over state-of-the-art baselines (ACT, OpenVLA, and Octo) across diverse bimanual tasks on real ALOHA dual-arm robots. Key findings:

- **Bimanual SOTA**: Highest success rates across all evaluated bimanual task categories vs. ACT, OpenVLA, and Octo
- **Zero-shot generalization**: Maintains high success rates on unseen objects and scenes (e.g., novel cups, unfamiliar rooms) and follows novel language instructions (e.g., "pour water one-third full")
- **Few-shot learning**: Learns complex new skills from 1-5 demonstrations, substantially outperforming baselines on tasks like "Handover" (5-shot) and "Fold Shorts" (1-shot)
- **Diffusion is critical**: Ablating diffusion in favor of regression drops instruction-following success from 100% to 12.5%
- **Scale matters**: The 1.2B model substantially outperforms the 166M variant, with scale particularly benefiting coordination-heavy tasks
- **Pre-training is crucial**: Training from scratch without multi-robot pre-training severely degrades generalization to unseen scenarios

## Limitations & Open Questions

- 1.2B parameters requires substantial GPU memory for inference; real-time deployment on resource-constrained robots is challenging
- Bimanual training data is much scarcer than single-arm data; the model's performance ceiling may be limited by data availability rather than model capacity
- DPM-Solver++ reduces denoising to 5 steps enabling 6 Hz chunk frequency, but this still limits responsiveness for highly dynamic bimanual tasks
- The model does not explicitly reason about contact forces or tactile feedback, which are important for tight-tolerance bimanual assembly tasks
- Evaluation is primarily in simulation and controlled lab settings; robustness to real-world variability is not fully established

## Connections

- [[wiki/concepts/robotics]] -- bimanual manipulation and foundation models
- [[wiki/concepts/foundation-models]] -- scaling diffusion transformers for robotics
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- complementary VLA approach (autoregressive vs. diffusion)
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational DDPM framework
- [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]] -- RT-1 transformer for manipulation
- [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]] -- ViT/DiT architecture lineage
