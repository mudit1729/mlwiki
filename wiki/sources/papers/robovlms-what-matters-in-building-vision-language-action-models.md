---
title: "RoboVLMs: What Matters in Building Vision-Language-Action Models"
tags: [robotics, vla, transformer, multimodal, foundation-model, imitation-learning]
status: active
type: paper
year: "2024"
venue: "arXiv"
citations: 50
arxiv_id: "2412.14058"
paper-faithfullness: audited-fixed
---

# RoboVLMs: What Matters in Building Vision-Language-Action Models

📄 **[Read on arXiv](https://arxiv.org/abs/2412.14058)**

## Overview

RoboVLMs is a large-scale empirical study from Tsinghua University, ByteDance Research, and collaborators that systematically investigates the design principles for building effective Vision-Language-Action (VLA) models. While VLA models have emerged as a compelling paradigm for generalist robot control -- leveraging powerful vision-language representations from pretrained VLMs -- the field has lacked systematic understanding of which design choices actually matter. RoboVLMs addresses this gap through over 600 experiments spanning VLM backbone selection, VLA architectural formulations, action space design, and cross-embodiment data strategies.

The study introduces the RoboVLMs framework, a flexible codebase supporting systematic comparison across eight VLM backbones (3B to 9B parameters, including Flamingo, LLaVA, Qwen-VL, MoonDream, UForm, KosMos, and PaliGemma) and four VLA formulations (one-step continuous, one-step discrete, interleaved-continuous history, and policy-head-continuous history). Evaluation covers both simulation benchmarks (CALVIN, SimplerEnv) and real-world experiments on a 7-DoF Kinova Gen3 robot with 100 tasks and 74K trajectories.

The key findings provide concrete, actionable guidance: KosMos and PaliGemma backbones significantly outperform alternatives due to comprehensive vision-language pretraining; continuous action spaces consistently beat discrete autoregressive tokenization, especially on longer-horizon tasks; policy-head architectures for history integration outperform interleaved approaches; and a post-training strategy (pretrain on cross-embodiment data, fine-tune on target domain) is the most effective way to leverage heterogeneous robot datasets. The best-performing RoboVLM configuration achieves state-of-the-art results with a 12.6% absolute gain on single tasks and 30.3% improvement on 5 consecutive tasks on the CALVIN unseen split, with emergent self-correction behavior in real-world settings.

## Key Contributions

- **Systematic VLM backbone comparison**: Evaluated 8 VLM backbones (3B-9B) across all VLA formulations, finding KosMos and PaliGemma are consistently best due to rich vision-language pretraining -- settling a previously unclear design choice
- **Action space analysis**: Demonstrated that continuous actions consistently outperform discrete autoregressive tokenization, particularly for long-horizon tasks where discretization errors compound
- **History integration architecture**: Found that policy-head structures (external temporal aggregation modules) outperform interleaved token approaches, preserving the original VLM's vision-language fusion while adding temporal reasoning
- **Cross-embodiment data strategy**: Established that post-training (cross-embodiment pretrain then target fine-tune) is the optimal strategy, vs. co-training or target-only training
- **Open-source framework**: Released the RoboVLMs codebase enabling reproducible VLA research across backbone and architecture combinations

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│               RoboVLMs Framework: 4 Formulations           │
│                                                            │
│  Images + Language ──► VLM Backbone (8 options tested)     │
│                        │                                   │
│         ┌──────────────┼──────────────┐                    │
│         │              │              │                     │
│    One-Step        One-Step      History Models             │
│    Continuous      Discrete      ┌─────────┴──────────┐    │
│         │              │         │                     │    │
│         ▼              ▼         ▼                     ▼    │
│    ┌─────────┐   ┌─────────┐  ┌───────────┐   ┌──────────┐│
│    │MLP Head │   │LM Head  │  │Interleaved│   │Policy    ││
│    │→ cont.  │   │→ action │  │tokens in  │   │Head      ││
│    │7-DoF    │   │tokens   │  │VLM context│   │(separate ││
│    │action   │   │(RT-2    │  │+ cont.    │   │temporal  ││
│    │         │   │ style)  │  │action head│   │module)   ││
│    └─────────┘   └─────────┘  └───────────┘   └──────────┘│
│                                                            │
│  Best config: PaliGemma/KosMos + Policy-Head + Continuous  │
│  Data strategy: Pretrain cross-embodiment → fine-tune      │
└────────────────────────────────────────────────────────────┘
```

## Method

The RoboVLMs framework supports four VLA formulations built on a common VLM backbone:

**One-step models** process only the current observation:
- *Continuous-Action*: VLM features are passed through an MLP action head that directly regresses continuous 7-DoF actions (6-DoF pose + gripper)
- *Discrete-Action*: Actions are discretized into tokens and predicted autoregressively by the VLM's language head, following the RT-2 paradigm

**History models** incorporate temporal context from past observations:
- *Interleaved-Continuous*: Multiple timesteps of images and proprioception are interleaved as tokens in the VLM's context window, with a continuous action head
- *Policy-Head-Continuous*: Current observation is processed by the VLM, but a separate policy head (e.g., a small transformer or MLP) aggregates VLM features with historical embeddings to produce actions

The system processes multi-camera RGB images and proprioceptive state, outputting 7-dimensional action vectors. Eight VLM backbones are tested: variants from the Flamingo family, LLaVA, Qwen-VL, MoonDream, UForm, KosMos, and PaliGemma.

### Key findings on architecture

| Design Choice | Best Option | Why |
|--------------|-------------|-----|
| VLM backbone | KosMos, PaliGemma | Comprehensive V-L pretraining on large-scale datasets |
| Action space | Continuous | Avoids discretization error accumulation over long horizons |
| History integration | Policy-Head | Preserves VLM fusion; adds temporal context externally |
| Cross-embodiment data | Post-training | Pre-train cross-embodiment, fine-tune on target domain |

## Results

The best RoboVLM configuration achieves state-of-the-art performance on CALVIN:

| Method | 1 Task | 2 Tasks | 3 Tasks | 4 Tasks | 5 Tasks |
|--------|--------|---------|---------|---------|---------|
| **RoboVLM (best)** | **+12.6% abs** | — | — | — | **+30.3% abs** |
| Prior SOTA | baseline | — | — | — | baseline |

*(Relative improvements reported over prior SOTA on CALVIN ABC->D unseen split)*

### Key ablation insights

1. **Backbone matters most**: Switching from the weakest to strongest VLM backbone yields larger gains than any architectural change, underscoring that the quality of pretrained visual-linguistic representations is the dominant factor
2. **Continuous vs. discrete**: The gap widens on longer-horizon tasks (5 consecutive tasks), where discrete tokenization accumulates quantization error across sequential action predictions
3. **Post-training > co-training**: Simply mixing cross-embodiment data during training hurts performance on the target domain due to distribution mismatch; the two-stage post-training approach resolves this

### Real-world results

Real-world experiments on a 7-DoF Kinova Gen3 demonstrate:
- Generalization to unseen distractors, backgrounds, and target objects
- Robustness to novel natural-language skill descriptions
- Emergent self-correction: the model recovers from intermediate failures without explicit recovery training

## Limitations & Open Questions

- **Scale ceiling**: All tested backbones are 3B-9B parameters; whether the findings (e.g., backbone ranking) hold at larger scales (30B+) is unknown
- **Action representation**: The study compares continuous vs. discrete actions and includes flow matching as an evaluated training objective (finding no significant gain over MSE+BCE for short-horizon tasks), but does not evaluate structured alternatives like VQ codebooks (UniAct)
- **Single-arm focus**: Experiments use a single 7-DoF manipulator; generalization to bimanual, mobile, or humanoid embodiments is untested
- **Real-time deployment**: Inference speed and latency are not systematically benchmarked across configurations
- **Does backbone ranking transfer across tasks?** KosMos and PaliGemma excel on manipulation -- unclear if this holds for navigation, locomotion, or driving

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] — RT-2 established the VLA paradigm that RoboVLMs systematically ablates; the discrete action tokenization approach tested here directly follows RT-2's design
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] — OpenVLA is one of the key baselines; RoboVLMs demonstrates that backbone and architecture choices can significantly outperform OpenVLA's fixed design
- [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control]] — pi0 uses PaliGemma (one of RoboVLMs' top backbones) with flow matching actions, validating the backbone finding while exploring a different action space
- [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models]] — ECoT adds chain-of-thought reasoning to VLAs; RoboVLMs' history integration findings are complementary
- [[wiki/sources/papers/uniact-universal-actions-for-enhanced-embodied-foundation-models]] — UniAct's VQ codebook action space is an alternative to the continuous/discrete dichotomy studied here
- [[wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics]] — SmolVLA shows a 450M model can compete with 3B+ models, raising questions about whether RoboVLMs' backbone rankings hold at smaller scales
- [[wiki/sources/papers/fast-efficient-action-tokenization-for-vision-language-action-models]] — FAST proposes DCT+BPE action tokenization as a third alternative to the continuous/discrete options evaluated here
- [[wiki/concepts/vision-language-action]] — broader VLA paradigm context
- [[wiki/concepts/robotics]] — robotics VLA landscape
