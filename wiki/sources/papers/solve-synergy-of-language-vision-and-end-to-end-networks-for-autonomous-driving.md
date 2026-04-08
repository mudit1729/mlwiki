---
title: "SOLVE: Synergy of Language-Vision and End-to-End Networks for Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - vla
  - chain-of-thought
  - end-to-end
citations: ~10
arxiv_id: "2501.08975"
---

# SOLVE: Synergy of Language-Vision and End-to-End Networks for Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2501.08975)

## Overview

SOLVE (HUST, CVPR 2025) proposes a synergistic framework that combines a Vision-Language Model (VLM) reasoning branch with an end-to-end (E2E) driving network, connected through a Sequential Q-Former and Trajectory Chain-of-Thought (CoT) mechanism. The key insight is that VLMs provide powerful scene understanding and reasoning but struggle with precise trajectory generation, while E2E networks excel at trajectory prediction but lack interpretable reasoning. SOLVE bridges these complementary strengths.

Rather than using the VLM as a direct planner (which suffers from action space mismatch) or discarding the VLM at inference (losing interpretability), SOLVE establishes a sequential information flow: the VLM first reasons about the scene in natural language (what objects are present, what their intentions are, what the appropriate driving behavior should be), and this reasoning is then injected into the E2E trajectory prediction network via the Sequential Q-Former. The Trajectory CoT mechanism structures the VLM's reasoning to progressively refine from high-level strategy down to trajectory-relevant guidance.

## Key Contributions

- **Sequential Q-Former**: A novel cross-modal bridge that sequentially transfers VLM reasoning features into the E2E planning network, allowing language-grounded reasoning to directly influence trajectory generation
- **Trajectory Chain-of-Thought**: Structures the VLM's reasoning into a progressive chain: scene description -> object analysis -> intention prediction -> driving strategy -> trajectory guidance, producing increasingly trajectory-relevant intermediate outputs
- **VLM + E2E synergy**: Demonstrates that combining VLM reasoning with E2E planning outperforms either approach alone, without requiring the VLM to directly output actions
- **Interpretable driving**: The CoT reasoning provides natural language explanations for driving decisions while maintaining competitive planning performance

## Architecture / Method

```
  ┌──────────────────────────────────────────────────────────────┐
  │  Multi-Camera Images                                         │
  └───────────┬──────────────────────────────────┬───────────────┘
              │                                  │
              ▼                                  ▼
  ┌───────────────────────┐          ┌───────────────────────────┐
  │  VLM Reasoning Branch │          │  E2E Planning Network     │
  │                       │          │                           │
  │  Prompt ──► VLM       │          │  Image Backbone           │
  │             │         │          │       │                   │
  │  Chain-of-Thought:    │          │       ▼                   │
  │  1. Scene Description │          │  BEV Encoder              │
  │  2. Critical Objects  │          │       │                   │
  │  3. Intention Predict │          │       ▼                   │
  │  4. Driving Strategy  │          │  Planning Decoder         │
  │  5. Traj. Guidance    │          │       ▲                   │
  │         │             │          │       │ cross-attention   │
  └─────────┼─────────────┘          └───────┼───────────────────┘
            │                                │
            │    ┌─────────────────────┐      │
            └───►│ Sequential Q-Former │──────┘
                 │  (learnable queries │
                 │   cross-attend to   │
                 │   CoT hidden states)│
                 └─────────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Trajectory Waypoints│
                 └─────────────────────┘
```

SOLVE has three main components:

1. **VLM Reasoning Branch**: A vision-language model (e.g., based on LLaVA or InternVL) takes multi-camera images and a structured prompt as input. The prompt elicits Chain-of-Thought reasoning in a specific sequence:
   - **Scene description**: "Describe the current driving scene"
   - **Critical object analysis**: "Identify objects that affect driving decisions"
   - **Intention prediction**: "What are these objects likely to do?"
   - **Driving strategy**: "What should the ego vehicle do?"
   - **Trajectory guidance**: "Describe the expected trajectory characteristics"

   Each stage produces both text tokens and hidden state features.

2. **Sequential Q-Former**: Inspired by BLIP-2's Q-Former but designed for sequential feature extraction, this module uses a set of learnable query tokens that cross-attend to the VLM's hidden states at each CoT stage. The queries are processed sequentially through the CoT stages, accumulating increasingly trajectory-relevant information. The output is a set of reasoning-enriched feature vectors.

3. **E2E Planning Network**: A standard transformer-based E2E driving model (BEV encoder + planning decoder) that takes multi-camera images and produces trajectory waypoints. The Sequential Q-Former's output features are injected into the planning decoder via cross-attention, allowing the planner to condition on the VLM's reasoning.

**Training**: Multi-task training with: (1) CoT language generation loss (next-token prediction on the reasoning chain), (2) trajectory planning loss (L2 on waypoints), (3) optional perception losses. The VLM and E2E network can be trained jointly or in stages (VLM first, then joint fine-tuning).

## Results

| Method | L2 @ 3s (m) | Collision Rate | Reasoning |
|--------|-------------|----------------|-----------|
| SOLVE | 0.27 | 0.16% | Yes |
| VAD | 0.31 | 0.22% | No |
| Senna | 0.29 | 0.19% | Yes |
| UniAD | 0.33 | 0.25% | No |

- Competitive planning metrics on nuScenes: 0.27m L2 at 3s, surpassing VAD and Senna
- The Sequential Q-Former contributes ~0.03m improvement in L2 over direct feature concatenation, validating the sequential cross-modal transfer design
- Trajectory CoT improves over unstructured VLM reasoning by ~0.02m L2, showing that structured progressive reasoning produces better trajectory guidance
- Ablation: removing VLM branch entirely degrades to pure E2E baseline performance, confirming the VLM's contribution
- Ablation: using VLM text output only (not hidden features) is significantly worse than using hidden features via Q-Former, confirming that continuous feature transfer is superior to discrete text-mediated transfer
- The model generates interpretable reasoning chains that align well with human driving rationale

## Limitations & Open Questions

- The VLM branch adds significant computational overhead at inference time; the paper does not provide latency comparisons
- The quality of CoT reasoning depends heavily on the VLM's pre-training; weaker VLMs may produce misleading guidance
- Evaluation is primarily open-loop on nuScenes; closed-loop evaluation would better test the reasoning-to-action pipeline
- The Sequential Q-Former design has multiple hyperparameters (number of queries, number of stages, attention layers) that require careful tuning

## Connections

- [[wiki/concepts/autonomous-driving]] -- VLM-enhanced E2E driving
- [[wiki/concepts/vision-language-action]] -- synergy between VLM reasoning and action generation
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] -- similar decoupled VLM + E2E approach
- [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] -- related distillation of VLM reasoning into E2E
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] -- structured VQA for driving reasoning
- [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] -- foundational CoT prompting work
- [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] -- related VLA driving approach
