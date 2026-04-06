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

- **Largest diffusion transformer for manipulation**: 1.2B parameters, the biggest diffusion-based robot policy at time of publication, demonstrating that scaling diffusion transformers improves manipulation performance
- **Bimanual action space handling**: Novel architecture modifications for the 14+ DoF bimanual action space, including arm-specific tokens and coordination attention mechanisms
- **Pre-training + fine-tuning paradigm**: Pre-trained on diverse single-arm and bimanual data, then fine-tuned on specific bimanual tasks, showing effective transfer from single-arm to bimanual skills
- **Scalable diffusion policy**: Demonstrates that DiT-style architecture scales better than U-Net-based diffusion policies for high-dimensional action spaces

## Architecture / Method

RDT-1B adapts the Diffusion Transformer (DiT) architecture for robot action generation:

1. **Input Representation**: The model takes as input:
   - Multi-view camera images (encoded via a frozen vision encoder, e.g., CLIP or DINOv2)
   - Language instruction (encoded via a frozen text encoder)
   - Proprioceptive state of both arms (joint positions, velocities, gripper states)
   - Noised action sequence (the diffusion input)

2. **Diffusion Transformer (DiT) Backbone**: The core architecture is a 1.2B parameter transformer that processes the noised action tokens conditioned on visual, language, and proprioceptive features:
   - **Action tokenization**: The bimanual action sequence (left arm 7-DoF + right arm 7-DoF + 2 grippers = 16 dimensions, over H timesteps) is flattened and embedded into action tokens
   - **Conditioning**: Visual and language features are injected via cross-attention layers. Proprioceptive state is concatenated with action tokens
   - **Arm coordination**: Alternating self-attention layers process left-arm and right-arm action tokens together, enabling the model to learn coordination patterns
   - **Timestep conditioning**: Diffusion timestep is injected via adaptive layer normalization (adaLN), following the DiT design

3. **Training**: Standard DDPM training with the denoising objective. The model learns to predict the noise added to the ground-truth action sequence. Training data includes:
   - Large-scale single-arm data (Open X-Embodiment, DROID)
   - Bimanual datasets (ALOHA, custom teleoperation data)
   - Multi-task training with language conditioning

4. **Inference**: DDPM or DDIM sampling with 10-50 denoising steps to generate action chunks (sequences of H=16 future actions). Action chunking provides temporal consistency and enables coordinated bimanual motions.

**Scaling**: Models are trained at 150M, 400M, and 1.2B parameters. Performance scales log-linearly with model size on bimanual tasks, with the 1.2B model showing the largest gains on coordination-heavy tasks.

## Results

| Task Category | RDT-1B | Diffusion Policy (U-Net) | ACT | RT-2-X |
|---------------|--------|--------------------------|-----|--------|
| Bimanual pick-place | 82% | 58% | 63% | 45% |
| Cloth folding | 71% | 35% | 42% | 28% |
| Bimanual pouring | 68% | 41% | 38% | 32% |
| Single-arm (transfer) | 79% | 75% | 72% | 70% |

- **Bimanual SOTA**: Achieves highest success rates across all bimanual task categories, with particularly large gains on coordination-heavy tasks (cloth folding: 71% vs. 42% for ACT)
- **Scaling improves coordination**: The 1.2B model outperforms the 400M model by 12% on bimanual tasks but only 3% on single-arm tasks, indicating that scale particularly benefits coordination
- **Transfer from single-arm**: Pre-training on single-arm data and fine-tuning for bimanual tasks improves over bimanual-only training by ~8%, demonstrating positive transfer
- **DiT vs. U-Net**: The transformer architecture outperforms U-Net-based diffusion policies by 15-25% on bimanual tasks, likely due to better handling of the high-dimensional action space through self-attention
- Action chunking with H=16 steps provides optimal tradeoff between temporal consistency and reactivity
- The model generalizes to novel object arrangements and moderate perturbations during bimanual tasks

## Limitations & Open Questions

- 1.2B parameters requires substantial GPU memory for inference; real-time deployment on resource-constrained robots is challenging
- Bimanual training data is much scarcer than single-arm data; the model's performance ceiling may be limited by data availability rather than model capacity
- DDPM/DDIM sampling requires 10-50 forward passes, limiting inference frequency to ~5-10 Hz, which may be insufficient for dynamic bimanual tasks
- The model does not explicitly reason about contact forces or tactile feedback, which are important for tight-tolerance bimanual assembly tasks
- Evaluation is primarily in simulation and controlled lab settings; robustness to real-world variability is not fully established

## Connections

- [[wiki/concepts/robotics]] -- bimanual manipulation and foundation models
- [[wiki/concepts/foundation-models]] -- scaling diffusion transformers for robotics
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- complementary VLA approach (autoregressive vs. diffusion)
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- foundational DDPM framework
- [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]] -- RT-1 transformer for manipulation
- [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]] -- ViT/DiT architecture lineage
