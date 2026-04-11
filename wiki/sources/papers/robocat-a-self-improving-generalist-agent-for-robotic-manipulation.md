---
title: "RoboCat: A Self-Improving Generalist Agent for Robotic Manipulation"
tags: [robotics, transformer, imitation-learning, multimodal, foundation-model, multi-embodiment]
status: active
type: paper
year: "2023"
venue: "TMLR 2023"
citations: ~200
arxiv_id: "2306.11706"
paper-faithfullness: audited-fixed
---

📄 **[Read on arXiv](https://arxiv.org/abs/2306.11706)**

## Overview

RoboCat, developed by Google DeepMind, is a multi-embodiment, multi-task generalist agent for robotic manipulation built on a transformer-based architecture. The paper addresses a fundamental challenge in robotics: how to build a single agent that can leverage heterogeneous robotic experience from different robots and tasks to rapidly master novel skills and embodiments. Unlike prior specialist systems trained for individual tasks or embodiments, RoboCat consumes action-labelled visual experience across a diverse repertoire of motor control skills spanning simulated and real robotic arms with varying observation and action spaces.

The core insight is that a large, diverse training mixture enables both zero-shot generalization to new tasks and efficient few-shot adaptation using only 100-1000 demonstrations. RoboCat builds on the Gato architecture (a visual goal-conditioned decision transformer) but scales it to 253 manipulation tasks across three real robot embodiments (Sawyer, Panda, KUKA) and simulation. Critically, the trained model can generate its own training data for subsequent iterations, creating an autonomous self-improvement loop where each generation of RoboCat produces better data that trains a stronger next generation.

Large-scale evaluations demonstrate that scaling and diversifying training data produces cross-task transfer benefits and enhanced adaptation efficiency. Experiments span 36 real robots across three embodiment types (Sawyer 5-DoF, Panda 7-DoF, KUKA 14-DoF bimanual) and two simulated arms (Sawyer 7-DoF, Panda 7-DoF). The single RoboCat agent adapts to previously unseen embodiments like the KUKA 14-DoF bimanual arm with nearly 80% success rates, and self-generated data integration significantly boosts generalist capabilities across the board.

## Key Contributions

- **Multi-embodiment generalist agent:** A single transformer policy that controls Sawyer, Panda, and KUKA robots across 253 diverse manipulation tasks with shared weights
- **Self-improvement loop:** The trained model generates its own practice data, which is filtered and added to the training set for the next iteration, creating an autonomous capability expansion cycle
- **Few-shot adaptation:** Demonstrates that 100-1000 demonstrations suffice to adapt the generalist to entirely new tasks or embodiments, dramatically reducing data requirements compared to training from scratch
- **Cross-task transfer:** Empirically validates that heterogeneous multi-task, multi-embodiment data produces positive transfer, with the generalist outperforming single-task specialists on many tasks
- **Scaling analysis:** Studies the effect of data diversity and scale on generalization, showing consistent improvement as the training mixture grows

## Architecture

```
┌──────────────────────────────────────────────────┐
│              Self-Improvement Loop                │
│                                                  │
│  ┌──────────┐    ┌───────────┐   ┌───────────┐  │
│  │ Train     │──►│ Deploy on │──►│ Filter by │  │
│  │ RoboCat_i │   │ robots    │   │ success   │  │
│  └──────────┘    └───────────┘   └─────┬─────┘  │
│       ▲                                │         │
│       └────── Add to training data ◄───┘         │
└──────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│        RoboCat Architecture (Gato-based)       │
│                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Goal Img │  │ Multi-Cam│  │ Propriocept. │ │
│  │ or Lang  │  │ RGB Imgs │  │ (joints,grip)│ │
│  └────┬─────┘  └────┬─────┘  └──────┬───────┘ │
│       │              │               │         │
│       ▼              ▼               ▼         │
│  ┌──────────────────────────────────────────┐  │
│  │  Tokenize (VQ-GAN + discretize states)   │  │
│  │  → unified flat token sequence           │  │
│  └─────────────────┬────────────────────────┘  │
│                    │                            │
│                    ▼                            │
│  ┌──────────────────────────────────────────┐  │
│  │  Decoder-Only Transformer                │  │
│  │  (autoregressive next-token prediction)  │  │
│  └─────────────────┬────────────────────────┘  │
│                    │                            │
│                    ▼                            │
│  ┌──────────────────────────────────────────┐  │
│  │  Discretized Action Tokens               │  │
│  │  (per-dim bins, embodiment-specific)      │  │
│  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
```

## Method

![RoboCat overview](https://paper-assets.alphaxiv.org/figures/2306.11706v2/x1.png)

RoboCat extends the Gato architecture — a decoder-only transformer that treats observations, actions, and goals as a unified token sequence. The architecture processes multi-camera RGB images through a frozen VQ-GAN encoder that produces visual tokens, which are interleaved with proprioceptive state tokens and discretized action tokens in a causal sequence. A key architectural innovation is the prediction of future image tokens (5 time steps ahead) alongside action tokens, which improves visual dynamics understanding and generalization.

**Tokenization:** Images are encoded into discrete visual tokens via a frozen VQ-GAN encoder. Proprioceptive states (joint angles, gripper state) and actions are discretized into integer bins within per-dimension ranges. All modalities share a single vocabulary and are packed into a flat sequence for autoregressive prediction.

**Conditioning:** The model is conditioned on task identity through goal images or language tokens prepended to the context. At inference time, the model autoregressively predicts the next action tokens given the observation history and goal specification.

**Self-improvement procedure:**
1. Train an initial RoboCat model on the full heterogeneous dataset
2. Use the trained model to autonomously collect practice episodes on target tasks
3. Filter the collected data by success (using hindsight goal relabeling and vision-based reward models as success detectors)
4. Add successful episodes to the training set
5. Retrain the model on the expanded dataset
6. Repeat — each iteration produces a stronger model that generates better practice data

**Training details:** The model is trained with a standard cross-entropy loss on next-token prediction over the action tokens. The training mixture is carefully balanced across embodiments and tasks to prevent any single data source from dominating. Data from all embodiments is pooled into a single training run with embodiment-specific tokenization handled at the input/output level.

## Results

RoboCat demonstrates strong performance across several evaluation axes:

| Evaluation | Metric | Result |
|------------|--------|--------|
| Total tasks mastered | Task count | 253 task variations across 16 task families |
| Novel embodiment (KUKA 14-DoF) | Success rate | ~80% after few-shot adaptation |
| Few-shot data requirement | Episodes needed | 100-1000 demonstrations |
| Self-improvement gain | Avg success delta | Significant improvement over base model across tasks |
| Cross-task transfer | Specialist vs generalist | Generalist matches or exceeds specialists on many tasks |
| Model sizes evaluated | Parameters | 1.18B vs 364M (larger model essential for complex tasks) |

**Key experimental findings:**

- **Data diversity helps:** Adding data from unrelated tasks and embodiments improves performance on target tasks, even when the additional data comes from a different robot. This is strong evidence for positive cross-embodiment transfer.
- **Self-improvement works:** Each iteration of the self-improvement loop produces measurable gains. The model trained on its own generated data (filtered for success) outperforms the model trained only on human demonstrations.
- **Few-shot adaptation is efficient:** The generalist model adapts to new tasks with 1-2 orders of magnitude less data than training a specialist from scratch, confirming that the diverse pretraining provides a strong initialization.
- **Novel embodiment transfer:** RoboCat successfully adapts to the KUKA 14-DoF bimanual arm, an embodiment not seen during initial training, demonstrating that the learned representations capture manipulation knowledge that transfers across robot morphologies.

## Limitations & Open Questions

- **Success detection dependency:** The self-improvement loop relies on being able to automatically detect whether a practice episode was successful. Scaling this to open-ended tasks without scripted success detectors remains challenging.
- **Simulation-to-real gap:** While RoboCat uses both simulated and real data, the paper does not fully characterize how sim-to-real transfer quality varies across the self-improvement iterations.
- **Compute cost:** Training a single generalist model on 253 tasks across multiple embodiments requires substantial compute. The paper does not provide detailed scaling law analysis relating compute budget to capability.
- **Action space limitations:** The discretized action representation may limit precision for tasks requiring fine-grained continuous control. Whether continuous action spaces (as in later diffusion-based approaches) would improve performance is unexplored.
- **Open question:** Can the self-improvement loop continue indefinitely, or does it plateau? What determines the ceiling of autonomous improvement without human intervention?

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/a-generalist-agent]] — RoboCat directly builds on the Gato architecture, extending it to multi-embodiment robotic manipulation with self-improvement
- [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]] — RT-1 established large-scale real-world robotic control via transformers; RoboCat scales this to multiple embodiments
- [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] — RT-2 demonstrated VLM-to-robot transfer; RoboCat takes a complementary approach via self-generated data rather than web pretraining
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] — OpenVLA later democratized VLA research; RoboCat preceded it as evidence that generalist robot policies are viable
- [[wiki/sources/papers/self-improving-embodied-foundation-models]] — Extends the self-improvement idea with RL-based autonomous practice and steps-to-go rewards, building on RoboCat's data-generation loop concept
- [[wiki/sources/papers/autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents]] — AutoRT addresses the same data collection challenge from an orchestration angle rather than self-play
- [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]] — HPT's stem-trunk-head design provides an alternative architecture for cross-embodiment learning
- [[wiki/concepts/robotics]] — Broader context on the VLA revolution in robotics
- [[wiki/concepts/vision-language-action]] — VLA paradigm that RoboCat contributes to
