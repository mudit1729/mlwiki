---
title: "Hydra-MDP: End-to-End Multimodal Planning with Multi-Target Hydra-Distillation"
tags: [autonomous-driving, end-to-end, planning, knowledge-distillation, imitation-learning, multimodal]
status: active
type: paper
year: "2024"
venue: "NeurIPS 2024 (NAVSIM Challenge Winner)"
citations: 50
arxiv_id: "2406.06978"
---

# Hydra-MDP: End-to-End Multimodal Planning with Multi-Target Hydra-Distillation

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2406.06978)**

## Overview

Hydra-MDP addresses a fundamental limitation of imitation learning for autonomous driving: standard behavior cloning learns only to mimic human demonstrations, with no explicit optimization for safety-critical metrics like collision avoidance, drivable area compliance, or time-to-collision. The paper proposes a multi-target knowledge distillation framework where multiple "teacher" signals -- both human demonstrations and rule-based safety evaluators -- are distilled into a single student network through specialized prediction heads (the "Hydra" heads).

The core insight is that autonomous driving evaluation is inherently multi-dimensional (safety, compliance, comfort, progress), and collapsing these into a single scalar score before distillation loses critical information. Instead, Hydra-MDP trains the student to predict each metric independently via separate Hydra Prediction Heads, then selects the trajectory that optimizes a composite score at inference time. This preserves the multi-objective structure of the problem through the entire pipeline.

Hydra-MDP won first place in the NAVSIM challenge, achieving 86.5 PDM Score with the best single model and up to 91.0 with larger vision backbones. The results demonstrate strong scalability -- unlike prior work suggesting diminishing returns, performance consistently improves with larger backbones and richer planning vocabularies.

## Key Contributions

- **Multi-target Hydra distillation:** Separate prediction heads for each closed-loop metric (NC, DAC, TTC, Comfort, EP), avoiding information loss from score aggregation
- **Planning vocabulary via K-means clustering:** Discretizes continuous trajectory space into ~700K expert trajectory clusters, converting planning into a scoring/selection problem
- **Offline simulation for teacher labels:** Runs ground-truth-perception simulation for every trajectory candidate in the vocabulary, generating per-metric supervision without online simulation
- **Elimination of non-differentiable post-processing:** The neural network directly learns the relationship between sensor observations and safety metrics, enabling end-to-end gradient flow
- **Scaling behavior:** Demonstrates consistent improvements with larger vision backbones and planning vocabularies, contradicting prior claims of diminishing returns

## Architecture / Method

![Architecture overview](https://paper-assets.alphaxiv.org/figures/2406.06978v4/x1.png)

### Perception Network

Hydra-MDP builds on the TransFuser architecture for sensor fusion. The perception network processes front-view camera images and LiDAR point clouds through separate backbones (e.g., ResNet or larger vision models), fusing them via transformer layers to produce environmental tokens encoding rich semantic information about the driving scene.

### Planning Vocabulary

Rather than predicting continuous trajectories directly, Hydra-MDP discretizes the action space using a **planning vocabulary** created by K-means clustering of ~700,000 expert trajectories from the training dataset. Each trajectory in the vocabulary consists of 40 timesteps of (x, y, heading) coordinates over a 4-second planning horizon. At inference, the model scores every trajectory in the vocabulary and selects the highest-scoring one.

### Multi-Target Hydra Heads

The trajectory decoder uses a set of specialized prediction heads -- one per evaluation metric:

| Head | Metric | Description |
|------|--------|-------------|
| NC Head | No at-fault Collisions | Predicts collision-free probability |
| DAC Head | Drivable Area Compliance | Predicts road boundary compliance |
| TTC Head | Time to Collision | Predicts time-to-collision safety margin |
| C Head | Comfort | Predicts jerk/acceleration comfort score |
| EP Head | Ego Progress | Predicts forward progress along route |

Each head is trained with supervision from offline simulation: for every trajectory in the planning vocabulary, a rule-based simulator with ground-truth perception evaluates the trajectory against each metric, producing per-metric labels. The student model learns to predict these scores from raw sensor inputs.

### Teacher-Student Paradigm

- **Human teacher:** Provides expert trajectory demonstrations from log-replay data
- **Rule-based teachers:** Offline simulation models that evaluate trajectory candidates against closed-loop metrics using ground truth perception

The key advantage of this paradigm is that teachers operate with perfect perception (ground truth), while the student must learn from noisy real sensor observations. This separation forces the student to develop robust perception-to-planning mappings that generalize to real-world conditions.

## Results

![Results](https://paper-assets.alphaxiv.org/figures/2406.06978v4/x2.png)

Hydra-MDP achieved first place in the NAVSIM challenge with state-of-the-art performance across all metrics:

| Method | PDM Score | NC (%) | DAC (%) | TTC | Comfort | EP |
|--------|-----------|--------|---------|-----|---------|-----|
| **Hydra-MDP (best single)** | **86.5** | **97.9** | **96.1** | -- | -- | -- |
| **Hydra-MDP (large backbone)** | **91.0** | -- | -- | -- | -- | -- |
| TransFuser baseline | -- | -- | -- | -- | -- | -- |
| Single aggregated score distillation | degraded | -- | -- | -- | -- | -- |

Key findings from ablations:

- **Multi-target vs. single-score distillation:** Distilling a single aggregated score instead of per-metric scores causes significant performance degradation, confirming the multi-target approach is essential
- **Planning vocabulary size:** Larger vocabularies consistently improve all metrics, highlighting the benefit of richer trajectory candidate sets
- **Backbone scaling:** Performance scales strongly with larger vision backbones (up to 91.0 PDM), contradicting prior claims of diminishing returns in E2E driving

## Limitations & Open Questions

- **Dependence on planning vocabulary:** The discrete trajectory set is fixed at training time; novel maneuvers outside the vocabulary cannot be generated
- **Offline simulation fidelity:** Teacher labels come from rule-based simulation with GT perception -- the quality of distillation depends on simulator fidelity
- **LiDAR dependency:** The TransFuser backbone requires LiDAR input, limiting deployment to LiDAR-equipped vehicles
- **Closed-loop validation:** While winning NAVSIM (a pseudo-simulation benchmark), full closed-loop and real-world deployment results are not reported
- **Vocabulary scalability:** As vocabulary size grows, inference cost increases linearly; efficient retrieval or hierarchical scoring could improve scalability

## Connections

Related papers in the wiki:

- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] -- Hydra-MDP builds on the TransFuser architecture for its perception backbone
- [[wiki/sources/papers/learning-by-cheating]] -- The privileged distillation paradigm (teacher with GT, student with sensors) that Hydra-MDP extends to multi-target distillation
- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] -- Alternative approach to multimodal trajectory generation using truncated diffusion (88.1 PDMS on NAVSIM)
- [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation]] -- Flow matching approach achieving 90.3 PDMS on NAVSIM, competing paradigm to vocabulary-based scoring
- [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] -- The evaluation benchmark (NAVSIM) where Hydra-MDP won first place
- [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] -- SparseDriveV2 also uses factorized trajectory vocabulary scoring, achieving 92.0 PDMS
- [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] -- Another distillation approach for E2E driving, distilling MLLM reasoning rather than metric scores
- [[wiki/sources/papers/driveadapter-breaking-the-coupling-barrier-of-perception-and-planning-in-end-to-end-autonomous-driving]] -- Related teacher-student paradigm for decoupling perception and planning
- [[wiki/concepts/planning]] -- Broader context on planning paradigms in autonomous driving
- [[wiki/concepts/end-to-end-architectures]] -- Taxonomy of E2E approaches; Hydra-MDP is a Type 3 jointly trained system with vocabulary-based planning
