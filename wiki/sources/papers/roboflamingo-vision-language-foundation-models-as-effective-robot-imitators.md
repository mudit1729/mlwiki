---
title: "RoboFlamingo: Vision-Language Foundation Models as Effective Robot Imitators"
tags: [robotics, vla, imitation-learning, multimodal, foundation-model, transformer]
status: active
type: paper
year: "2024"
venue: "ICLR 2024"
citations: 100
arxiv_id: "2311.01378"
paper-faithfullness: audited-clean
---

# RoboFlamingo: Vision-Language Foundation Models as Effective Robot Imitators

📄 **[Read on arXiv](https://arxiv.org/abs/2311.01378)**

## Overview

RoboFlamingo addresses the question of whether publicly available vision-language models (VLMs) can serve as effective backbones for robot imitation learning, without requiring the massive compute budgets of proprietary systems like RT-2 or PaLM-E. The paper demonstrates that by fine-tuning the open-source OpenFlamingo model on robot manipulation demonstrations, a relatively lightweight framework can achieve state-of-the-art performance on the CALVIN language-conditioned manipulation benchmark.

The core insight is a **decoupled architecture** that separates vision-language comprehension from sequential decision-making. Rather than forcing the VLM to directly output actions (as RT-2 does), RoboFlamingo uses the frozen or lightly fine-tuned Flamingo backbone for single-step multimodal understanding, then feeds these representations into a dedicated policy head (an LSTM) that handles the temporal aspects of robot control. This decoupling allows the system to leverage the VLM's rich visual-linguistic representations while using an architecture better suited for sequential action prediction.

RoboFlamingo achieves an average task sequence length of 4.09 on CALVIN (completing ~4 out of 5 chained tasks), substantially outperforming prior methods including HULC (3.06) and RT-1 (2.45). Critically, this is achieved with a single consumer-grade GPU for fine-tuning, making VLA research accessible to the broader community -- a theme later amplified by OpenVLA and SmolVLA.

## Key Contributions

- **First demonstration** that open-source VLMs (OpenFlamingo) can be effectively adapted for robot manipulation through efficient fine-tuning, achieving SOTA on CALVIN without proprietary models or massive compute.
- **Decoupled architecture design** separating VLM-based perception/language understanding from temporal policy learning, showing this is more effective than end-to-end VLA approaches for sequential manipulation tasks.
- **Systematic ablation** of VLM components for robotics: the paper isolates the contributions of visual pre-training, language grounding, and the policy head architecture, finding that explicit temporal modeling via LSTM is crucial and cannot be replaced by simple MLP heads.
- **Accessibility milestone** -- demonstrating that competitive robot learning can be done on a single GPU, democratizing VLA research months before OpenVLA made this a community priority.

## Architecture

```
  Language Instruction          Multi-View RGB Images (per timestep)
        │                              │
        ▼                              ▼
┌───────────────┐             ┌─────────────────┐
│  LLM Backbone │             │  Frozen ViT-L   │
│  (Flamingo)   │             │  (CLIP)         │
└───────┬───────┘             └────────┬────────┘
        │                              │
        │                     ┌────────┴────────┐
        │                     │    Perceiver    │
        │                     │    Resampler    │
        │                     │ (→ fixed tokens)│
        │                     └────────┬────────┘
        │                              │
        └──────────┐  ┌────────────────┘
                   ▼  ▼
        ┌──────────────────────┐
        │  Gated Cross-Attn    │
        │  (fuse vision+lang)  │
        │  interleaved in LLM  │
        └──────────┬───────────┘
                   │
                   │  (per-timestep features)
                   ▼
        ┌──────────────────────┐
        │   LSTM Policy Head   │
        │  (temporal modeling  │
        │   over obs history)  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │  Linear → 7-DoF      │
        │  Action (pos,rot,grip)│
        └──────────────────────┘
```

## Method

![RoboFlamingo architecture overview](https://paper-assets.alphaxiv.org/figures/2311.01378v3/img-0.jpeg)

RoboFlamingo builds on the OpenFlamingo architecture, which itself extends Flamingo with open weights. The system processes multi-view observations and language instructions through three main stages:

**1. Vision Encoder (ViT).** Each image observation is encoded by a frozen Vision Transformer (ViT-L/14 from CLIP). The ViT produces patch-level visual features that capture rich semantic information from pre-training on web-scale image-text data.

**2. Perceiver Resampler.** The variable-length ViT features are compressed into a fixed number of visual tokens via Flamingo's Perceiver Resampler -- a cross-attention module that attends over the visual features using a small set of learned latent queries. This produces a compact visual representation regardless of image resolution.

**3. Feature Fusion Decoder (Gated Cross-Attention).** The language instruction is processed by the LLM backbone, and visual tokens from the Perceiver Resampler are fused in via gated cross-attention layers interleaved with the LLM's self-attention layers. This produces a joint vision-language representation for the current observation.

**4. Policy Head (LSTM).** The fused vision-language features from each timestep are fed sequentially into an LSTM-based policy head that models temporal dependencies across the observation history. The LSTM outputs are mapped through a linear layer to predict 7-DoF robot actions (3D position, 3D rotation, 1D gripper).

![Ablation and method details](https://paper-assets.alphaxiv.org/figures/2311.01378v3/img-1.jpeg)

During fine-tuning, the ViT backbone is typically frozen while the Perceiver Resampler, gated cross-attention layers, and the policy head are trained. The LLM backbone can be either frozen or fine-tuned depending on the variant. The paper explores multiple fine-tuning strategies: full fine-tuning of the fusion layers, freezing various components, and co-training with language modeling objectives to preserve VLM capabilities.

### Training

- **Loss:** MSE loss on continuous end-effector pose prediction, combined with BCE loss on discrete gripper open/close status (weighted by λ_gripper)
- **Data:** CALVIN benchmark demonstrations -- 24 hours of play data across 34 tasks in 4 environments, with language annotations
- **Fine-tuning:** The VLM backbone (OpenFlamingo 3B or 9B) is adapted with relatively few gradient steps; the policy head is trained from scratch
- **Observation history:** The LSTM policy head processes a window of recent observations (typically 10-20 steps) to capture temporal context

## Results

![Results on CALVIN benchmark](https://paper-assets.alphaxiv.org/figures/2311.01378v3/img-3.jpeg)

RoboFlamingo sets a new state-of-the-art on the CALVIN benchmark for language-conditioned manipulation:

| Method | Avg. Len. | 1 Task | 2 Tasks | 3 Tasks | 4 Tasks | 5 Tasks |
|--------|-----------|--------|---------|---------|---------|---------|
| **RoboFlamingo** | **4.09** | **96.4%** | **89.6%** | **82.4%** | **74.0%** | **66.8%** |
| HULC | 3.06 | 82.7% | 66.6% | 52.5% | 40.0% | 30.7% |
| RT-1 (adapted) | 2.45 | 72.2% | 52.1% | 37.1% | 25.2% | 16.8% |
| MCIL | 1.08 | 37.3% | 14.7% | 5.4% | 1.7% | 0.5% |

### Key ablation findings

- **Policy head matters most:** Replacing the LSTM head with an MLP drops average length from 4.09 to ~2.5, confirming that explicit temporal modeling is essential for sequential manipulation.
- **VLM pre-training is critical:** Training the same architecture from scratch (no VLM pre-training) yields significantly worse results, demonstrating that web-scale vision-language knowledge transfers to robotic control.
- **Fine-tuning strategy:** Fine-tuning the cross-attention layers while keeping the ViT frozen gives the best trade-off between performance and compute. Full fine-tuning provides marginal gains at much higher cost.
- **Language grounding helps:** The language-conditioned variant outperforms vision-only baselines, showing that Flamingo's language understanding transfers to task specification in robotics.

## Limitations & Open Questions

- **Single benchmark:** Results are demonstrated only on CALVIN, which features a single robot arm in a tabletop setting. Generalization to diverse embodiments and environments is not tested.
- **No real-world validation:** All experiments are in simulation. The sim-to-real transfer properties of the fine-tuned VLM representations are unknown.
- **Closed-source training data for VLM:** While OpenFlamingo is open-source, the VLM's pre-training data (LAION) has quality and licensing concerns that may affect downstream use.
- **Action space limitations:** The 7-DoF action space is relatively simple. Whether the approach scales to higher-DoF manipulation (bimanual, dexterous hands) is untested.
- **Temporal modeling ceiling:** The LSTM policy head, while effective, may limit scalability compared to transformer-based temporal architectures used in later work (e.g., diffusion policy heads in pi0, DexVLA).

## Connections

Related papers in the wiki:

- [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] -- RT-2 is the primary comparison point; RoboFlamingo achieves competitive results with open-source models and far less compute
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- OpenVLA continues the democratization theme RoboFlamingo started, scaling to 7B parameters with Open X-Embodiment data
- [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]] -- RT-1 serves as a baseline on CALVIN; RoboFlamingo significantly outperforms it
- [[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model]] -- PaLM-E represents the "scale up" approach to embodied VLMs; RoboFlamingo shows smaller open models can be competitive
- [[wiki/sources/papers/robocat-a-self-improving-generalist-agent-for-robotic-manipulation]] -- RoboCat takes a multi-embodiment approach; RoboFlamingo focuses on efficient single-embodiment adaptation
- [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models]] -- ECoT later adds chain-of-thought reasoning to VLA fine-tuning, building on the VLM-for-robotics paradigm RoboFlamingo helped establish
- [[wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics]] -- SmolVLA (2025) pushes the accessibility theme further with a 450M model on single GPU
- [[wiki/concepts/vision-language-action]] -- RoboFlamingo sits at the transition between Wave 1 VLAs (RT-1/RT-2) and the open-source VLA movement
- [[wiki/concepts/robotics]] -- broader context on the VLA revolution in robotics
- [[wiki/concepts/foundation-models]] -- RoboFlamingo demonstrates foundation model transfer to embodied control
