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
citations: ~0
arxiv_id: "2412.14415"
---

# DriveGPT: Scaling Autoregressive Behavior Models for Driving

[Read on arXiv](https://arxiv.org/abs/2412.14415)

## Overview

DriveGPT (Cruise, ICML 2025) is the first work to systematically study scaling laws for autoregressive behavior models in autonomous driving. Drawing inspiration from the scaling laws discovered for large language models (Kaplan et al., Chinchilla), DriveGPT demonstrates that similar power-law relationships hold when scaling model size, dataset size, and compute for driving behavior prediction. The model is trained autoregressively to predict future trajectories of all agents in a driving scene, scaling up to 1.4B parameters and training on 120M real-world driving demonstrations from Cruise's internal fleet dataset.

The central finding is that driving behavior models follow predictable scaling laws: test loss decreases as a power law with increasing model parameters, data tokens, and training compute, mirroring the scaling behavior observed in LLMs. This provides the autonomous driving community with a principled framework for allocating resources and predicting performance improvements from scaling.

## Key Contributions

- **First scaling laws for driving**: Demonstrates that autoregressive driving models follow power-law scaling relationships analogous to those in LLMs, with predictable loss reduction as a function of model size, dataset size, and compute
- **1B+ parameter driving model**: Scales an autoregressive behavior model to 1.4B parameters, the largest driving-specific model at time of publication
- **120M demonstrations**: Trained on the largest real-world driving dataset used for a single behavior model, spanning diverse scenarios from Cruise's fleet
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
│  │  │ Road/Map │ │ Nearby   │ │ Target Agent     │  │       │
│  │  │(PointNet)│ │ Agents   │ │ History          │  │       │
│  │  └────┬─────┘ └────┬─────┘ └────────┬─────────┘  │       │
│  │       └─────────────┼────────────────┘            │       │
│  └─────────────────────┼────────────────────────────┘       │
│                        ▼                                     │
│  ┌──────────────────────────────────────────────────┐       │
│  │     Transformer Encoder                           │       │
│  │     (fuses agent history + map context)           │       │
│  └─────────────────────┬────────────────────────────┘       │
│                        ▼                                     │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Autoregressive Decoder (1.5M ─► 1.4B params)    │       │
│  │  Verlet Actions: s_{t+1} = s_t + Δs_t + a_t      │       │
│  │  (discrete action space, cross-entropy loss)      │       │
│  └─────────────────────┬────────────────────────────┘       │
│                        ▼                                     │
│         Autoregressive Future Trajectory Tokens               │
│    [agent_t₁ agent_t₂ ... agent_tT]  (step-by-step)         │
└─────────────────────────────────────────────────────────────┘

Scaling Law:  L(N,D) = A/N^α + B/D^β + L_∞
              N = parameters, D = dataset size, L_∞ = irreducible loss
```

DriveGPT formulates driving as next-token prediction over discretized scene representations. The architecture consists of:

1. **Scene Tokenizer**: Road geometry, traffic signals, and agent states (position, velocity, heading) are tokenized into a structured sequence. Each agent's trajectory is discretized into spatial tokens at each timestep using a **PointNet-like tokenization** for map elements. The tokenization preserves the relational structure between agents and map elements.

2. **Encoder-Decoder Transformer**: An encoder fuses target agent history, nearby agent trajectories, and map information. An autoregressive decoder then generates future trajectories step-by-step. The model predicts agent movements using **Verlet Actions** — representing displacements as second derivatives (s_{t+1} = s_t + (s_t - s_{t-1}) + a_t) to maintain kinematic consistency while using a discrete action space.

3. **Scaling Configurations**: Models range from 1.5M to 1.4B parameters (evaluated at 1.5M, 4M, 8M, 12M, 26M, 94M, 163M, 358M, 629M, 1.4B), with the dataset scaled from ~2.2M to 120M demonstrations.

**Training**: Cross-entropy loss over the discrete action space. Training uses a single epoch over 120M segments, batch size 2048, Adam optimizer with cosine decay, on 16 NVIDIA H100 GPUs.

**Scaling Law Formulation**: Test loss L follows L(N,D) = A/N^alpha + B/D^beta + L_inf, where N is model parameters, D is dataset size, and L_inf is the irreducible loss. The fitted exponents characterize how efficiently each resource reduces loss. The authors perform systematic experiments varying model size and data size across the 1.5M–1.4B parameter range and 2.2M–120M data range to fit these curves.

## Results

**WOMD Benchmark (test set, non-ensemble):**

| Model | minADE | minFDE | Miss Rate | Soft mAP |
|-------|--------|--------|-----------|----------|
| DriveGPT-WOMD | 0.5279 | 1.0609 | 0.1236 | 0.3795 |
| DriveGPT-Finetune | 0.5240 | 1.0538 | 0.1202 | 0.3857 |

- **Scaling laws confirmed**: Validation loss decreases consistently as model size scales from 1.5M to 1.4B parameters and data scales from 2.2M to 120M segments; the autoregressive decoder outperforms one-shot decoders beyond 8M parameters
- **Data is the primary bottleneck**: With the full 120M dataset, validation loss improves up to ~94M parameters before plateauing; smaller datasets (≤21M) show minimal benefit from model scaling
- **Downstream transfer**: Pretraining on 120M internal segments then fine-tuning on WOMD yields up to 3% additional performance gains in geometric metrics; the model outperforms prior non-ensemble methods on minADE/minFDE
- The soft mAP is lower than geometric metrics due to compounded probability estimation errors in long autoregressive sequences — an acknowledged limitation
- Closed-loop deployment on Cruise's fleet achieves <50ms inference latency in challenging urban scenarios
- Training on 120M demonstrations shows no signs of data saturation for the 1.4B model, suggesting further scaling would continue to improve

## Limitations & Open Questions

- Scaling laws are fit to Cruise's internal dataset distribution; generalization to other geographies and driving cultures is unvalidated
- The autoregressive formulation requires sequential generation at inference time, creating latency challenges for real-time planning at 1B+ scale
- The relationship between behavior prediction loss and actual driving safety/performance is not directly established -- lower loss does not guarantee fewer collisions
- Tokenization of continuous trajectories introduces discretization artifacts; the optimal vocabulary size and spatial resolution remain open questions
- The scaling analysis is primarily demonstrated on validation loss and WOMD benchmarks; longer-horizon closed-loop scaling behavior remains less characterized

## Connections

- [[wiki/concepts/autonomous-driving]] -- behavior prediction and planning
- [[wiki/concepts/foundation-models]] -- scaling laws for domain-specific foundation models
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- original LLM scaling laws (Kaplan et al.)
- [[wiki/sources/papers/training-compute-optimal-large-language-models]] -- Chinchilla scaling laws
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3 and the scaling paradigm
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, contrasting modular E2E approach
