---
title: "CarPlanner: Consistent Auto-regressive RL Planner for Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - reinforcement-learning
  - planning
  - autoregressive
citations: ~15
arxiv_id: "2502.19908"
paper-faithfullness: audited-solid
---

# CarPlanner: Consistent Auto-regressive RL Planner for Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2502.19908)

## Overview

CarPlanner (Zhejiang University + Cainiao Network, CVPR 2025) introduces a consistent autoregressive reinforcement learning planner that is the first RL-based planner to surpass both imitation learning (IL) and rule-based methods on the nuPlan benchmark. While IL-based planners suffer from distribution shift (the model encounters states at test time that differ from training demonstrations) and rule-based post-processing adds fragile hand-crafted heuristics, CarPlanner uses RL to learn a planner that is robust to its own generated states.

The key technical contribution is a consistent autoregressive architecture that generates trajectory waypoints sequentially while maintaining temporal consistency. Standard autoregressive generation suffers from compounding errors (each waypoint conditions on potentially erroneous previous waypoints), which is especially problematic in safety-critical driving. CarPlanner addresses this through a generation-selection framework: a mode selector first identifies a stable driving mode representation that remains constant across all time steps, and the trajectory generator conditions on this fixed mode, preventing drift and ensuring coherent trajectories.

## Key Contributions

- **First RL planner to beat IL+rules on nuPlan**: Demonstrates that RL-based planning can surpass the dominant paradigm of imitation learning with rule-based refinement on a large-scale real-world planning benchmark
- **Consistent autoregressive generation**: Novel generation-selection architecture where a mode selector provides a stable mode representation that anchors the autoregressive trajectory generator, preventing compounding error drift
- **RL training for driving planners**: Develops a practical RL training pipeline for trajectory planning, addressing reward design, exploration, and sample efficiency challenges specific to the driving domain
- **Closed-loop superior performance**: Strong results in closed-loop simulation, where the planner must react to its own actions' consequences

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                     Scene Encoder                           │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ HD Map   │  │ Agent    │  │ Ego      │                  │
│  │ Elements │  │ Trajs    │  │ State    │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
│       │              │             │                         │
│       ▼              ▼             ▼                         │
│  ┌──────────────────────────────────────┐                   │
│  │  PointNet Encoder + Cross-Attention  │                   │
│  └──────────────────┬───────────────────┘                   │
│                     │ Scene Features                        │
└─────────────────────┼───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌──────────────────┐   ┌──────────────────────────────────────┐
│  Mode Selector   │   │   Autoregressive Trajectory Generator│
│                  │   │                                      │
│  Scene ──► P(m)  │   │  Scene + mode c ──► Transformer     │
│  (cross-entropy  │   │  w_{t-1} ────────► (causal attn)    │
│   + L1 side task)│   │                          │           │
│       │          │   │                          ▼           │
│       ▼          │   │                    w_t (waypoint)    │
│  mode c (stable, │   │                                      │
│  fixed across    │──►│  mode c remains constant             │
│  all time steps) │   │  across all autoregressive steps     │
└──────────────────┘   └──────────────────────────────────────┘

Training Pipeline:
  ┌──────────┐    ┌───────────────┐    ┌──────────────────┐
  │ Expert   │    │  IL Pretrain   │    │   RL Fine-tune   │
  │ Demos    │──►│  (L1 loss)     │──►│  (PPO)           │
  └──────────┘    └───────────────┘    └──────────────────┘
                                              │
                                  R = -DE + R_collision
                                       + R_drivable
```

CarPlanner consists of four main components:

1. **Non-reactive Transition Model**: Predicts future trajectories of surrounding traffic agents in a single forward pass (non-reactive to the ego vehicle), given the initial state. This single-shot prediction significantly improves training efficiency vs. step-by-step simulation. It uses PointNet-style encoders for map and agent data fused via self-attention Transformers.

2. **Scene Representation**: The driving scene is represented using vectorized inputs: HD map elements (lane boundaries, crosswalks, traffic lights), surrounding agent trajectories (position, velocity, heading over time), and ego vehicle state. These are encoded using a PointNet-style encoder and fused via cross-attention.

3. **Autoregressive Trajectory Generator (RL Policy)**: A transformer decoder generates trajectory waypoints one at a time. At each step, the model attends to the scene features and all previously generated waypoints to produce the next waypoint. This autoregressive structure naturally captures the sequential, causal nature of trajectory planning.

4. **Consistent Autoregressive Generation**: Rather than penalty-based regularization, CarPlanner achieves consistency through its generation-selection architecture:
   - A **mode selector** assigns probabilities to decomposed driving modes: **longitudinal modes** (scalar average speeds) and **lateral modes** (possible routes from map topology via graph search), selecting a stable combined mode representation `c`
   - The trajectory generator conditions on this mode `c`, which **remains constant across all time steps**, ensuring coherent temporal consistency
   - This avoids compounding errors because each waypoint is anchored to the same stable mode rather than drifting
   - An **Invariant-View Module (IVM)** preprocesses policy inputs by transforming map, agent, and route information into the ego vehicle's current coordinate frame and applying KNN selection, ensuring time-agnostic and spatially consistent state representations

5. **RL Training**: The model is first pre-trained with imitation learning (L1 loss on trajectory error), then fine-tuned with RL using PPO. The RL reward is:
   - `R_t = -DE_t + R_collision + R_drivable`
   - **DE** (Displacement Error): distance from the ground-truth expert trajectory at each step; penalizing DE guides the policy toward expert-like behavior
   - **R_collision**: -1 for collisions, 0 otherwise
   - **R_drivable**: -1 for out-of-drivable-area violations, 0 otherwise

   The mode selector is trained with cross-entropy loss on the positive mode plus an L1 regression side task. The IL-pretrained policy provides stable initialization for RL exploration.

## Results

Performance is measured using the nuPlan Closed-Loop Score (CLS-NR, non-reactive setting) on the Test14-Random split.

| Method | Type | CLS-NR |
|--------|------|--------|
| **CarPlanner** | **RL** | **94.07** |
| PLUTO | IL | 91.92 |
| PDM-Closed | Rule-based | 90.05 |

- **nuPlan SOTA**: CLS-NR of 94.07, surpassing the best IL method PLUTO (91.92) and the best rule-based method PDM-Closed (90.05)
- **First RL planner to beat IL and rule-based SOTAs** on this challenging large-scale benchmark
- **Reactive setting**: CarPlanner scores 91.10 CLS-R, slightly below PDM-Closed (91.64), attributed to training exclusively in non-reactive settings
- **Consistency is critical**: The consistent auto-regressive framework significantly outperforms vanilla auto-regressive RL in closed-loop performance, confirming that mode conditioning prevents temporal drift
- **Invariant-View Module impact**: Coordinate transformation alone boosts CLS from 90.78 to 94.07 and progress (S-PR) from 91.37 to 95.06
- **Reward design**: Using displacement error alone leads to near-static trajectories; combining with collision and drivable-area rewards raises S-CR from 97.49 to 99.22 and S-Area from 96.91 to 99.22
- **Training efficiency**: Model-based approach achieves two orders of magnitude higher samples/second than model-free RL baselines (e.g., ScenarioNet)
- The model handles long-tail scenarios (aggressive cut-ins, jaywalkers) better than IL methods, likely because RL explores and learns from failure states

## Limitations & Open Questions

- RL training requires a differentiable simulator or reward model, which may not capture all real-world driving complexities
- The reward function is hand-designed and may not fully capture human driving preferences; reward misspecification remains a risk
- Training stability of RL for driving planners is still challenging; the method requires careful hyperparameter tuning
- Evaluation is on nuPlan simulation only; real-world deployment gap remains

## Connections

- [[wiki/concepts/autonomous-driving]] -- RL-based planning
- [[wiki/concepts/planning]] -- autoregressive trajectory planning with RL
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, modular E2E approach
- [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]] -- IL + data augmentation for driving
- [[wiki/sources/papers/alphadrive-unleashing-the-power-of-vlms-in-autonomous-driving]] -- GRPO-based RL for driving VLMs
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] -- vectorized representation baseline
