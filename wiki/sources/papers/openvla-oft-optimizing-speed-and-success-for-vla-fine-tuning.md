---
title: "OpenVLA-OFT: Optimizing Speed and Success for VLA Fine-Tuning"
type: source-summary
status: active
updated: 2026-04-05
year: 2025
venue: arXiv
tags:
  - paper
  - robotics
  - vla
  - fine-tuning
  - deployment
citations: 364
arxiv_id: "2502.19645"
paper-faithfullness: audited-fixed
---

# OpenVLA-OFT: Optimizing Speed and Success for VLA Fine-Tuning

[Read on arXiv](https://arxiv.org/abs/2502.19645)

## Overview

OpenVLA-OFT presents a systematic empirical study of fine-tuning strategies for Vision-Language-Action models, identifying a recipe that boosts the original OpenVLA from 76.5% to 97.1% success rate on the LIBERO benchmark while achieving a 26x inference speedup. The paper addresses a critical deployment bottleneck: OpenVLA's autoregressive action generation runs at only 3-5 Hz, far below the 25-50+ Hz required for real-world high-frequency control. Through careful evaluation of three axes -- action generation strategy, action representation, and learning objectives -- the authors arrive at an optimized fine-tuning configuration that makes VLA deployment practical.

The core architectural change replaces autoregressive (sequential) action token generation with parallel decoding using bidirectional attention, enabling all action tokens to be predicted simultaneously. The base OFT recipe combines parallel decoding, action chunking, a continuous action representation, and an L1 regression objective. An extended variant, OpenVLA-OFT+, additionally incorporates FiLM (Feature-wise Linear Modulation) for enhanced language grounding in scenarios requiring disambiguation across language-conditioned tasks.

## Key Contributions

- **97.1% success on LIBERO**: Up from 76.5% for vanilla OpenVLA, establishing a new state-of-the-art for VLA fine-tuning on this benchmark
- **26x inference speedup**: Parallel action decoding replaces sequential autoregressive generation, reaching deployment-viable control frequencies
- **Systematic fine-tuning analysis**: Evaluates action generation strategy (autoregressive vs. parallel), action representation (discrete bins vs. continuous), and learning objectives across multiple benchmarks
- **Real-world validation on ALOHA**: Demonstrates strong bimanual manipulation performance despite OpenVLA being pre-trained only on single-arm data, showing generalization through fine-tuning

## Architecture / Method

```
              OpenVLA-OFT vs Original OpenVLA
              ────────────────────────────────

  Original OpenVLA (Slow):        OpenVLA-OFT (Fast):
  ┌─────────────────────┐         ┌─────────────────────────┐
  │ Image + Language     │         │ Image + Language          │
  └──────────┬──────────┘         └──────────┬──────────────┘
             ▼                               ▼
  ┌─────────────────────┐         ┌─────────────────────────┐
  │   VLM Backbone       │         │   VLM Backbone           │
  └──────────┬──────────┘         └──────────┬──────────────┘
             │                               │
             ▼                               ▼
  Sequential (causal attn):      Parallel (bidirectional attn):
  a₁ ──► a₂ ──► ... ──► a₇      ┌───┬───┬───┬───┬───┬───┬───┐
  (7 forward passes)             │a₁ │a₂ │a₃ │a₄ │a₅ │a₆ │a₇ │
                                 └───┴───┴───┴───┴───┴───┴───┘
                                 (1 forward pass ──► 26x faster)
                                 + continuous actions + L1 loss

  OpenVLA-OFT+ also adds FiLM conditioning for language grounding:
  Language ──► FiLM ──► modulate visual patch embeddings

  + LoRA fine-tuning + Proprioception + Multi-camera
```

![OpenVLA-OFT architecture with parallel decoding and FiLM](https://paper-assets.alphaxiv.org/figures/2502.19645v2/figure_1_openvla_aloha.001.jpeg)

The key modifications to OpenVLA are:

**Base OFT recipe** (four components together yield 97.1% on LIBERO):

1. **Parallel action decoding**: Replaces causal (autoregressive) attention over action tokens with bidirectional attention, allowing all action dimensions to attend to each other and be predicted in a single forward pass rather than sequentially. This is the primary source of the 26x speedup.

2. **Action chunking**: Predicts K future actions per forward pass (K=8 for LIBERO simulation, K=25 for real ALOHA), further increasing throughput and smoothing execution.

3. **Continuous action representation**: A separate MLP action head maps final hidden states directly to continuous action values, replacing the original 256-bin discretization.

4. **L1 regression objective**: Minimizes mean L1 distance between predicted and ground-truth actions, simpler and faster than diffusion while achieving equivalent performance.

**OpenVLA-OFT+ extensions** (add-ons for real-world deployment):

5. **FiLM conditioning**: Feature-wise Linear Modulation layers modulate visual patch embeddings using averaged language instruction embeddings, providing robust language grounding. Without FiLM, language-conditioned task performance drops to chance level (33.3%) on ALOHA.

6. **Multi-modal input processing**: Enhanced handling of proprioceptive state and multi-camera views alongside standard image + language inputs.

7. **LoRA fine-tuning**: Parameter-efficient adaptation preserving pre-trained knowledge while adapting to new tasks and embodiments.

![FiLM integration for language modulation](https://paper-assets.alphaxiv.org/figures/2502.19645v2/film_figure.001.jpeg)

## Results

![LIBERO benchmark results](https://paper-assets.alphaxiv.org/figures/2502.19645v2/libero_tasks.001.jpeg)

![ALOHA bimanual task performance](https://paper-assets.alphaxiv.org/figures/2502.19645v2/aloha_task_performance_results_v3.001.jpeg)

| Configuration | LIBERO Success | Inference Speed | Notes |
|--------------|---------------|-----------------|-------|
| OpenVLA (original) | 76.5% | 3-5 Hz | Autoregressive, slow |
| OpenVLA-OFT | 97.1% | 109.7 Hz | Parallel decoding + chunking (K=8 sim / K=25 real), 26x faster |
| Baselines (ACT, DP) | Variable | 10-50 Hz | Task-specific methods |

- **LIBERO benchmark**: 97.1% success rate, a 20.6 percentage point improvement over vanilla OpenVLA
- **ALOHA bimanual tasks**: OpenVLA-OFT+ achieves 87.8% average success across four dexterous tasks, outperforming π0 (77.1%), RDT-1B (78.4%), ACT (72.3%), and Diffusion Policy (77.5%)
- **Language grounding**: FiLM conditioning achieves 79.2% on language-conditioned "put X into pot" tasks vs. 33.3% (chance level) without FiLM
- **Parallel decoding + action chunking** is the single largest contributor to both speed and accuracy improvements, yielding ~14% absolute gain on LIBERO; continuous action representations add another ~5%
- Fine-tuning generalizes well: single-arm pre-training transfers effectively to bimanual setups through OFT recipe

![Language grounding evaluation](https://paper-assets.alphaxiv.org/figures/2502.19645v2/aloha_language_grounding_results.001.jpeg)

## Limitations

- The systematic study is empirical rather than theoretical; the optimal recipe may not transfer to very different VLA architectures or action spaces
- Evaluation primarily on LIBERO (simulation) and ALOHA (specific hardware); broader real-world validation across diverse platforms is needed
- Parallel decoding sacrifices the ability to condition later action dimensions on earlier ones, which may matter for highly coordinated multi-joint actions
- The 26x speedup is measured at the action generation level; end-to-end system latency includes vision encoding which is not optimized here

## Connections

- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- direct predecessor; OFT provides the optimized fine-tuning recipe for OpenVLA
- [[wiki/sources/papers/fast-efficient-action-tokenization-for-vision-language-action-models]] -- complementary approach: FAST compresses tokens, OFT parallelizes decoding
- [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control]] -- pi0 uses flow matching for continuous actions; OFT stays within the discrete token paradigm but parallelizes it
- [[wiki/concepts/vision-language-action]] -- addresses the deployment speed bottleneck of VLA models
- [[wiki/concepts/robotics]] -- practical fine-tuning for real-world robot deployment
