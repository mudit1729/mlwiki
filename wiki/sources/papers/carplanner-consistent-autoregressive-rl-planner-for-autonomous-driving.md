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
---

# CarPlanner: Consistent Auto-regressive RL Planner for Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2502.19908)

## Overview

CarPlanner (Zhejiang University, CVPR 2025) introduces a consistent autoregressive reinforcement learning planner that is the first RL-based planner to surpass imitation learning (IL) + rule-based methods on the nuPlan benchmark. While IL-based planners suffer from distribution shift (the model encounters states at test time that differ from training demonstrations) and rule-based post-processing adds fragile hand-crafted heuristics, CarPlanner uses RL to learn a planner that is robust to its own generated states.

The key technical contribution is a consistency-regularized autoregressive architecture that generates trajectory waypoints sequentially while maintaining temporal consistency across waypoints. Standard autoregressive generation suffers from compounding errors (each waypoint conditions on potentially erroneous previous waypoints), which is especially problematic in safety-critical driving. CarPlanner addresses this with a consistency loss that penalizes kinematic violations and ensures smooth, physically plausible trajectories.

## Key Contributions

- **First RL planner to beat IL+rules on nuPlan**: Demonstrates that RL-based planning can surpass the dominant paradigm of imitation learning with rule-based refinement on a large-scale real-world planning benchmark
- **Consistency-regularized autoregressive generation**: Novel architecture that generates waypoints autoregressively while enforcing temporal consistency through kinematic constraints, preventing the compounding error problem
- **RL training for driving planners**: Develops a practical RL training pipeline for trajectory planning, addressing reward design, exploration, and sample efficiency challenges specific to the driving domain
- **Closed-loop superior performance**: Strong results in closed-loop simulation, where the planner must react to its own actions' consequences

## Architecture / Method

CarPlanner consists of:

1. **Scene Representation**: The driving scene is represented using vectorized inputs: HD map elements (lane boundaries, crosswalks, traffic lights), surrounding agent trajectories (position, velocity, heading over time), and ego vehicle state. These are encoded using a PointNet-style encoder and fused via cross-attention.

2. **Autoregressive Trajectory Generator**: A transformer decoder generates trajectory waypoints one at a time. At each step, the model attends to the scene features and all previously generated waypoints to produce the next waypoint. This autoregressive structure naturally captures the sequential, causal nature of trajectory planning.

3. **Consistency Regularization**: To prevent compounding errors, CarPlanner enforces:
   - **Kinematic consistency**: Predicted waypoints must satisfy bicycle model constraints (curvature limits, acceleration bounds)
   - **Temporal smoothness**: L2 penalty on jerk (third derivative of position) to prevent jerky trajectories
   - **Self-consistency**: The trajectory generated from any intermediate waypoint should match the remaining suffix of the full trajectory, implemented via a self-consistency loss

4. **RL Training**: The model is first pre-trained with imitation learning (behavioral cloning on expert demonstrations), then fine-tuned with RL. The RL reward combines:
   - Progress reward (distance traveled toward goal)
   - Safety reward (penalty for collisions, near-misses)
   - Comfort reward (penalty for high jerk, lateral acceleration)
   - Rule compliance (traffic light violations, lane departures)

   Training uses PPO with the IL-pretrained policy as initialization, which provides stable exploration from a reasonable starting point.

## Results

| Method | Type | nuPlan Score | Collision Rate |
|--------|------|-------------|----------------|
| CarPlanner | RL | 87.2 | 1.8% |
| PDM-Closed (IL+rules) | IL+rules | 85.4 | 2.3% |
| PlanTF (IL) | IL | 82.1 | 3.1% |
| GameFormer (IL) | IL | 80.5 | 3.7% |

- **nuPlan SOTA**: 87.2 overall score, surpassing PDM-Closed (85.4), the previous best IL+rule-based method
- **Lower collision rate**: 1.8% vs. 2.3% for PDM-Closed, demonstrating that RL improves safety
- **No rule-based post-processing needed**: Eliminates the need for hand-crafted safety rules and trajectory smoothing that prior methods require
- **Consistency regularization is critical**: Removing consistency losses degrades performance by ~4 points and increases collision rate to 3.5%, confirming that naive autoregressive RL suffers from compounding errors
- **RL vs. IL ablation**: RL fine-tuning improves over IL pretraining by ~5 points on nuPlan score, with the largest gains in interactive scenarios (merging, unprotected turns)
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
