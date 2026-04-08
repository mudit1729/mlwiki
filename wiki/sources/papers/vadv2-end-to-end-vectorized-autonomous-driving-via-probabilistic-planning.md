---
title: "VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning"
tags: [autonomous-driving, end-to-end, planning, vectorized-representation, transformer, probabilistic-planning]
status: active
type: paper
year: "2024"
venue: "arXiv"
citations: 140
arxiv_id: "2402.13243"
---

# VADv2: End-to-End Vectorized Autonomous Driving via Probabilistic Planning

📄 **[Read on arXiv](https://arxiv.org/abs/2402.13243)**

## Overview

VADv2 by Chen et al. (2024) is the successor to [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving|VAD]], addressing a fundamental limitation of deterministic planners in autonomous driving: they output a single trajectory, ignoring that multiple viable driving actions exist in any given scenario. When other agents behave unexpectedly, a deterministic planner has no fallback. VADv2 reframes the planning problem as a probabilistic one, modeling the planning policy as an environment-conditioned stochastic process that outputs a distribution over actions rather than a single trajectory.

The core technical insight draws from large language models: VADv2 discretizes the continuous action space into a finite "planning vocabulary" of representative trajectories derived from clustering human driving demonstrations. A transformer-based architecture then predicts a probability distribution over this vocabulary conditioned on the vectorized scene representation, analogous to how LLMs predict token distributions over a language vocabulary. This enables the planner to express uncertainty across multiple plausible driving modes (e.g., yielding vs. proceeding through an intersection) rather than averaging them into a single unsafe trajectory.

VADv2 achieved state-of-the-art closed-loop performance on the CARLA Town05 benchmark using only camera sensors, demonstrating higher route completion rates and fewer infractions (collisions and traffic rule violations) than prior methods. The probabilistic formulation directly addresses the mode-averaging problem that plagues deterministic planners in multi-modal driving scenarios, making it a significant architectural advance in the vectorized end-to-end driving paradigm.

## Key Contributions

- **Probabilistic planning via action vocabulary:** Discretizes continuous trajectory space into a finite set of representative trajectories (planning vocabulary) derived by clustering human demonstrations, enabling the planner to output a categorical distribution over actions rather than regressing a single trajectory
- **LLM-inspired planning formulation:** Frames autonomous driving planning as next-token prediction over an action vocabulary, drawing a direct parallel to language modeling and enabling the use of cross-entropy-based training objectives
- **Scene-conditioned action distribution:** Uses a transformer decoder that attends to vectorized scene tokens (map polylines, agent trajectories, ego state) to produce action probabilities, preserving the efficiency of vectorized representations from VAD
- **Conflict-aware action selection:** Introduces a conflict resolution mechanism that evaluates candidate trajectories from the predicted distribution for safety violations (collision checking against predicted agent futures), selecting the highest-probability collision-free trajectory at inference time
- **State-of-the-art closed-loop performance:** Achieves best results on CARLA Town05 Long benchmark among camera-only methods, validating that probabilistic planning substantially improves closed-loop driving over deterministic alternatives

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     VADv2 Pipeline                        │
│                                                           │
│  Multi-camera Images                                      │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────┐                                         │
│  │ BEV Encoder  │ (backbone + BEV lifting)                │
│  └──────┬───────┘                                         │
│         │                                                │
│    ┌────┴──────────────┐                                  │
│    ▼                   ▼                                  │
│  ┌──────────┐   ┌──────────┐                              │
│  │ Map Det  │   │ Agent    │                              │
│  │(polylines)│   │ Pred     │                             │
│  └────┬─────┘   └────┬─────┘                              │
│       │  Vectorized   │                                   │
│       │  Scene Tokens  │                                  │
│       └───────┬───────┘                                   │
│               ▼                                           │
│  ┌────────────────────────────┐   ┌───────────────────┐   │
│  │ Probabilistic Planning     │   │Planning Vocabulary│   │
│  │ Transformer Decoder        │◄──│K trajectories     │   │
│  │ (ego queries + cross-attn) │   │(K-means clusters) │   │
│  └────────────┬───────────────┘   └───────────────────┘   │
│               │                                           │
│               ▼                                           │
│  ┌────────────────────────────┐                           │
│  │ P(action | scene)          │  Categorical distribution  │
│  │ [p1, p2, ..., pK]         │  over K vocabulary entries  │
│  └────────────┬───────────────┘                           │
│               │                                           │
│               ▼                                           │
│  ┌────────────────────────────┐                           │
│  │ Conflict-Aware Selection   │  Check top trajectories    │
│  │ (collision filtering)      │  against predicted agents  │
│  └────────────┬───────────────┘                           │
│               ▼                                           │
│         Best safe trajectory                              │
└──────────────────────────────────────────────────────────┘
```

## Architecture / Method

![VADv2 architecture overview](https://paper-assets.alphaxiv.org/figures/2402.13243/x1.png)

VADv2 builds on the VAD architecture but replaces the deterministic planning head with a probabilistic planning framework. The architecture has four main stages:

**Stage 1 -- Scene Encoding:** Multi-camera images are processed by an image backbone (ResNet-50 or similar) and lifted to BEV space. The BEV features are then used to extract vectorized scene representations: map polylines (lane boundaries, crosswalks, road edges) and agent trajectories (predicted futures of surrounding vehicles and pedestrians), following the same approach as VAD.

**Stage 2 -- Planning Vocabulary Construction (offline):** Before training, the continuous trajectory space is discretized by clustering a large set of human driving trajectories from the training dataset. K-means or a similar clustering algorithm is applied to produce K representative trajectories (the "planning vocabulary"). Each vocabulary entry is a fixed-length sequence of 2D waypoints representing a canonical driving maneuver (straight, slight left, hard right, decelerate, etc.). This vocabulary is fixed during training and inference.

**Stage 3 -- Probabilistic Planning Transformer:** A transformer decoder takes learnable ego planning queries and attends to the vectorized scene tokens (map vectors, agent vectors, and ego state embeddings) via cross-attention. Instead of regressing waypoints, the decoder produces logits over the K vocabulary entries. A softmax produces a probability distribution over the planning vocabulary. The model is trained with three losses:
- **Distribution loss:** Cross-entropy between the predicted action distribution and the ground-truth action (the vocabulary entry closest to the human driver's actual trajectory)
- **Scene token loss:** Auxiliary losses on the scene encoding (map detection, agent prediction) inherited from VAD
- **Conflict loss:** A penalty term that discourages high probability on vocabulary entries that would cause collisions with predicted agent trajectories

**Stage 4 -- Conflict-Aware Inference:** At test time, the model predicts the full action distribution. Rather than simply taking the argmax, VADv2 performs conflict checking: each high-probability trajectory candidate is evaluated against predicted agent futures for collision. The highest-probability collision-free trajectory is selected. This two-stage process (predict distribution, then filter) provides an additional safety layer without requiring a separate safety module.

![Additional method details](https://paper-assets.alphaxiv.org/figures/2402.13243/x2.png)

## Results

### CARLA Town05 Long Benchmark (Closed-Loop)

| Method | Driving Score | Route Completion | Infraction Score |
|--------|--------------|-----------------|-----------------|
| VADv2 (camera-only) | **44.5** | **83.2%** | **0.53** |
| VAD (camera-only) | 30.3 | 75.2% | 0.40 |
| UniAD | 33.4 | 72.4% | 0.46 |
| TransFuser (camera+LiDAR) | 31.0 | 47.5% | 0.65 |

- **47% improvement in Driving Score over VAD:** The probabilistic formulation yields a large closed-loop gain (44.5 vs. 30.3), validating that expressing uncertainty over actions matters significantly for real driving performance
- **Superior route completion:** 83.2% route completion represents a substantial improvement over VAD (75.2%) and UniAD (72.4%), indicating the probabilistic planner is better at handling complex intersections and lane changes where deterministic planners stall or collide
- **Reduced infractions:** The conflict-aware selection mechanism reduces collision rates by filtering out trajectories that would intersect with predicted agent positions
- **Camera-only advantage:** VADv2 outperforms TransFuser which uses both camera and LiDAR, demonstrating that a strong planning formulation can compensate for sensor limitations
- **Ablation on vocabulary size K:** Performance improves as K increases up to a point (diminishing returns beyond K~512), confirming that finer action discretization captures more driving modes but with bounded benefit
- **Conflict checking matters:** Removing the conflict-aware selection at inference time degrades performance significantly, showing that the probabilistic distribution alone is not sufficient -- the safety filtering is essential

## Limitations & Open Questions

- **Vocabulary discretization:** The fixed planning vocabulary cannot represent arbitrary trajectories -- only combinations of the K cluster centers. Unusual maneuvers not well-represented in the training data (e.g., rare swerves, U-turns) may be poorly covered
- **Open-loop gap:** While VADv2 demonstrates strong closed-loop results on CARLA, it inherits VAD's reliance on nuScenes-style training data which is primarily straight driving. The vocabulary reflects the training distribution
- **Vocabulary construction is offline:** The planning vocabulary is fixed before training and not adapted during learning. An end-to-end learnable vocabulary (analogous to learned tokenizers in NLP) could improve coverage
- **Single-step planning:** VADv2 selects one trajectory per timestep without explicit temporal consistency between consecutive selections, which could cause jittery driving in practice (cf. [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving|MomAD]]'s momentum-aware approach)
- **Conflict checking assumes accurate prediction:** The safety filtering is only as good as the agent prediction quality. If predicted agent futures are wrong, the conflict check may filter good trajectories or pass unsafe ones

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- direct predecessor; VADv2 builds on VAD's vectorized scene representation and replaces the deterministic planner
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, the jointly trained modular E2E system that VAD and VADv2 improve upon
- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] -- alternative approach to multimodal planning using truncated diffusion instead of discrete vocabulary
- [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation]] -- flow matching approach to multimodal trajectory generation, another solution to the mode-averaging problem
- [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] -- addresses temporal consistency in E2E planning, complementary to VADv2's probabilistic formulation
- [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] -- SparseDrive/V2 also uses trajectory vocabulary scoring but with a factorized vocabulary
- [[wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving]] -- RL-based planner that also addresses multimodal planning but through autoregressive generation
- [[wiki/concepts/planning]] -- broader context on planning evolution
- [[wiki/concepts/end-to-end-architectures]] -- taxonomy of E2E approaches (VADv2 is Type 3: jointly trained modular)
