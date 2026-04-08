---
title: "DriveGPT: Scaling Autoregressive Behavior Models for Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: ICML
tags:
  - paper
  - autonomous-driving
  - scaling-laws
  - autoregressive
  - foundation-model
citations: ~30
arxiv_id: "2412.14415"
---

# DriveGPT: Scaling Autoregressive Behavior Models for Driving

[Read on arXiv](https://arxiv.org/abs/2412.14415)

## Overview

DriveGPT (Waymo, ICML 2025) is the first work to systematically study scaling laws for autoregressive behavior models in autonomous driving. Drawing inspiration from the scaling laws discovered for large language models (Kaplan et al., Chinchilla), DriveGPT demonstrates that similar power-law relationships hold when scaling model size, dataset size, and compute for driving behavior prediction. The model is trained autoregressively to predict future trajectories of all agents in a driving scene, scaling up to 1.1B parameters and training on over 100M real-world driving demonstrations from the Waymo dataset.

The central finding is that driving behavior models follow predictable scaling laws: test loss decreases as a power law with increasing model parameters, data tokens, and training compute, mirroring the scaling behavior observed in LLMs. This provides the autonomous driving community with a principled framework for allocating resources and predicting performance improvements from scaling.

## Key Contributions

- **First scaling laws for driving**: Demonstrates that autoregressive driving models follow power-law scaling relationships analogous to those in LLMs, with predictable loss reduction as a function of model size, dataset size, and compute
- **1B+ parameter driving model**: Scales an autoregressive behavior model to 1.1B parameters, the largest driving-specific model at time of publication
- **100M+ demonstrations**: Trained on the largest real-world driving dataset used for a single behavior model, spanning diverse scenarios from Waymo's fleet
- **Compute-optimal allocation**: Derives compute-optimal ratios for model size vs. data size in the driving domain, analogous to Chinchilla scaling
- **Transfer to downstream tasks**: Shows that scale improves zero-shot transfer to motion prediction and planning benchmarks

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                    DriveGPT Architecture                     │
│                                                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │              Scene Tokenizer                      │       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐  │       │
│  │  │ Road     │ │ Traffic  │ │ Agent States     │  │       │
│  │  │ Geometry │ │ Signals  │ │ (pos,vel,heading)│  │       │
│  │  └────┬─────┘ └────┬─────┘ └────────┬─────────┘  │       │
│  │       └─────────────┼────────────────┘            │       │
│  │                     ▼                             │       │
│  │         Discretized Token Sequence                │       │
│  │    [road₁ road₂ ... sig₁ ... agent₁_t₁ ...]     │       │
│  └─────────────────────┬────────────────────────────┘       │
│                        ▼                                     │
│  ┌──────────────────────────────────────────────────┐       │
│  │     Decoder-Only Transformer (15M ─► 1.1B)       │       │
│  │     ┌─────────────────────────────────┐           │       │
│  │     │   Causal Self-Attention Layers  │           │       │
│  │     │   (depth/width scale with size) │           │       │
│  │     └─────────────┬───────────────────┘           │       │
│  │                   ▼                               │       │
│  │   Next-Token Prediction (Cross-Entropy Loss)      │       │
│  └─────────────────────┬────────────────────────────┘       │
│                        ▼                                     │
│         Autoregressive Future Trajectory Tokens               │
│    [agent₁_t₂ agent₂_t₂ ... agent₁_t₃ agent₂_t₃ ...]      │
└─────────────────────────────────────────────────────────────┘

Scaling Law:  L(N,D) = A/N^α + B/D^β + L_∞
              N = parameters, D = dataset size, L_∞ = irreducible loss
```

DriveGPT formulates driving as next-token prediction over discretized scene representations. The architecture consists of:

1. **Scene Tokenizer**: Road geometry, traffic signals, and agent states (position, velocity, heading) are tokenized into a structured sequence. Each agent's trajectory is discretized into spatial tokens at each timestep. The tokenization preserves the relational structure between agents and map elements.

2. **Autoregressive Transformer**: A decoder-only transformer (GPT-style) processes the tokenized scene history and autoregressively predicts future tokens for all agents. The model uses causal attention and predicts one timestep at a time for all agents, then conditions on those predictions for subsequent timesteps.

3. **Scaling Configurations**: Models range from 15M to 1.1B parameters, with corresponding increases in transformer depth, width, and attention heads. The dataset is scaled from 1M to 100M+ demonstrations.

**Training**: Standard next-token prediction with cross-entropy loss over discretized trajectory tokens. Training uses standard LLM infrastructure (distributed data parallel, gradient checkpointing, mixed precision). The authors perform systematic experiments varying model size and data size to fit scaling law curves.

**Scaling Law Formulation**: Test loss L follows L(N,D) = A/N^alpha + B/D^beta + L_inf, where N is model parameters, D is dataset size, and L_inf is the irreducible loss. The fitted exponents alpha and beta characterize how efficiently each resource reduces loss.

## Results

| Model Size | Parameters | Test Loss | WOMD (mAP) |
|-----------|------------|-----------|-------------|
| Small | 15M | 2.84 | 0.31 |
| Medium | 120M | 2.51 | 0.38 |
| Large | 450M | 2.32 | 0.43 |
| XL | 1.1B | 2.18 | 0.47 |

- **Scaling laws confirmed**: Test loss follows a power law with model size (exponent ~0.07) and data size (exponent ~0.05), consistent across 3 orders of magnitude
- Compute-optimal frontier shows that for a fixed compute budget, balanced scaling of model and data outperforms scaling either alone
- **Downstream transfer**: Larger models achieve better zero-shot performance on Waymo Open Motion Dataset (WOMD) motion prediction benchmark without task-specific fine-tuning
- The irreducible loss L_inf is substantial, reflecting the inherent stochasticity of human driving behavior -- even a perfect model cannot predict exactly which maneuver a driver will choose
- Emergent capabilities at scale: the 1.1B model exhibits qualitatively better handling of rare events (U-turns, multi-agent interactions) compared to smaller models
- Training on 100M+ demonstrations shows no signs of data saturation for the 1.1B model, suggesting further scaling would continue to improve

## Limitations & Open Questions

- Scaling laws are fit to the Waymo dataset distribution; generalization to other geographies and driving cultures is unvalidated
- The autoregressive formulation requires sequential generation at inference time, creating latency challenges for real-time planning at 1B+ scale
- The relationship between behavior prediction loss and actual driving safety/performance is not directly established -- lower loss does not guarantee fewer collisions
- Tokenization of continuous trajectories introduces discretization artifacts; the optimal vocabulary size and spatial resolution remain open questions
- The study focuses on behavior prediction, not closed-loop driving; the scaling laws may not transfer directly to closed-loop performance

## Connections

- [[wiki/concepts/autonomous-driving]] -- behavior prediction and planning
- [[wiki/concepts/foundation-models]] -- scaling laws for domain-specific foundation models
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- original LLM scaling laws (Kaplan et al.)
- [[wiki/sources/papers/training-compute-optimal-large-language-models]] -- Chinchilla scaling laws
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3 and the scaling paradigm
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, contrasting modular E2E approach
