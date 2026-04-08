---
title: Open Questions
type: query
status: active
updated: 2026-04-07
tags:
  - questions
  - agenda
  - map
---

# Open Questions

This page is the root of the open-questions tree. Each research pillar has its own dedicated page with stream-specific questions grounded in the papers we've ingested. See [[wiki/queries/research-tree]] for an interactive visual map.

## Question tree

```
Overview
├── 1. End-to-End Driving (9 questions)
│   ├── Unified vs. decoupled VLA architecture
│   ├── Generative vs. discriminative planning
│   ├── RL vs. imitation ceiling
│   ├── Scaling laws for driving
│   └── ... → open-questions-e2e
│
├── 2. Vision-Language-Action Models (10 questions)
│   ├── Dual-system generality
│   ├── Cross-embodiment scaling limits
│   ├── RL for VLAs
│   ├── Robotics → driving transfer gap
│   └── ... → open-questions-vla
│
├── 3. LLM Reasoning for Autonomy (9 questions)
│   ├── Language role at maturity
│   ├── Reasoning vs. planning distinction
│   ├── RL-emergent reasoning for driving
│   ├── Dual-process cognitive architecture
│   └── ... → open-questions-llm-reasoning
│
├── 4. Foundation Models & Cross-Embodiment (10 questions)
│   ├── Compute-optimal scaling for embodied AI
│   ├── Open vs. closed model trajectory
│   ├── Cross-embodiment action universality
│   ├── Alignment for physical systems
│   └── ... → open-questions-foundation-models
│
└── 5. BEV Perception & 3D Occupancy (10 questions)
    ├── Dense vs. sparse vs. Gaussian
    ├── Occupancy world models
    ├── Self-supervised methods
    ├── Occupancy role in E2E planning
    └── ... → open-questions-bev-perception
```

## Stream pages

| Stream | Questions | Key tension | Top papers |
|--------|-----------|-------------|------------|
| [[wiki/queries/open-questions-e2e\|End-to-End Driving]] | 9 | Unified vs. decoupled, generative vs. discriminative | UniAD, DriveTransformer, EMMA, DiffusionDrive |
| [[wiki/queries/open-questions-vla\|VLA Models]] | 10 | Dual-system convergence, cross-embodiment limits | pi0, CrossFormer, OpenVLA, GR00T N1 |
| [[wiki/queries/open-questions-llm-reasoning\|LLM Reasoning]] | 9 | Language as scaffold vs. core, reasoning vs. planning | LLMs Can't Plan, DeepSeek-R1, ECoT, DriveLM |
| [[wiki/queries/open-questions-foundation-models\|Foundation Models]] | 10 | Open vs. closed, scaling laws for embodied AI | Scaling Laws, HPT, CLIP, LoRA, Cosmos |
| [[wiki/queries/open-questions-bev-perception\|BEV & 3D Occupancy]] | 10 | Dense vs. Gaussian, occupancy in E2E | GaussianFormer, OccWorld, BEVNeXt, OccMamba |

**Total: 48 open questions** across 5 research pillars, grounded in 198 papers spanning 1993-2026.

## Cross-cutting themes

These questions recur across multiple streams and may represent the deepest open problems:

### 1. The RL frontier
Every stream is hitting an imitation learning ceiling. CarPlanner (E2E), pi0.6 (VLA), DeepSeek-R1 (reasoning), AlphaDrive (driving VLM) all show RL pushes beyond SFT. But reward design for physical systems remains the bottleneck.
- E2E: [[wiki/queries/open-questions-e2e]] Q5
- VLA: [[wiki/queries/open-questions-vla]] Q5
- Reasoning: [[wiki/queries/open-questions-llm-reasoning]] Q5-Q6

### 2. Scaling laws for embodied AI
Language scaling laws are well-established. Do they transfer to multimodal embodied data?
- E2E: [[wiki/queries/open-questions-e2e]] Q6 (DriveGPT scaling)
- Foundation: [[wiki/queries/open-questions-foundation-models]] Q1 (compute-optimal embodied)
- VLA: [[wiki/queries/open-questions-vla]] Q2 (cross-embodiment scaling)

### 3. Distillation as deployment pattern
Train large, distill small appears universal: Gemma 3, DeepSeek-R1, DiMA all use it. Is this the deployment path for safety-critical systems?
- Foundation: [[wiki/queries/open-questions-foundation-models]] Q4
- Reasoning: [[wiki/queries/open-questions-llm-reasoning]] Q1, Q3
- E2E: [[wiki/queries/open-questions-e2e]] Q9

### 4. Evaluation adequacy
Every stream questions whether current benchmarks measure what matters.
- E2E: [[wiki/queries/open-questions-e2e]] Q7 (NAVSIM/Bench2Drive)
- BEV: [[wiki/queries/open-questions-bev-perception]] Q10 (mIoU vs. planning quality)
- VLA: [[wiki/queries/open-questions-vla]] Q7 (open-world failure modes)

### 5. Explicit structure vs. learned representations
The central tension of the entire wiki: when does hand-designed structure help?
- E2E: [[wiki/queries/open-questions-e2e]] Q1-Q3
- BEV: [[wiki/queries/open-questions-bev-perception]] Q9
- Reasoning: [[wiki/queries/open-questions-llm-reasoning]] Q4

## Navigation

- [[wiki/overview]] — Wiki overview and five research pillars
- [[wiki/syntheses/research-thesis]] — Current thesis synthesizing these questions
- [[wiki/queries/research-tree]] — Interactive visual tree of the wiki structure
- [[wiki/concepts/vision-language-action]] — VLA concept page
- [[wiki/concepts/end-to-end-architectures]] — E2E concept page
- [[wiki/concepts/perception]] — BEV/perception concept page
- [[wiki/concepts/foundation-models]] — Foundation models concept page
