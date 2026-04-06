---
title: Planning
type: concept
status: active
updated: 2026-04-05
tags:
  - planning
  - control
---

# Planning

Planning converts scene understanding and future predictions into driving actions. It is the module closest to the physical world and the one where errors are most consequential. The field has evolved from rule-based state machines through learned imitation planners to VLA systems that fold planning into a single multimodal model.

## Planning hierarchy

Driving planning traditionally operates at multiple levels:

- **Route planning:** High-level navigation graph search (A* on road network). Largely solved.
- **Behavior planning:** Discrete decisions (lane change, yield, merge, stop). Traditionally rule-based or finite state machines.
- **Trajectory planning:** Continuous path generation satisfying kinematic constraints, comfort, and safety. The focus of most learned planning research.
- **Control:** Low-level actuation (steering, throttle, brake). Often a PID or MPC controller tracking the planned trajectory.

The end-to-end trend collapses these levels. Modern systems often output trajectories or waypoints directly, bypassing explicit behavior planning entirely.

## Evolution of learned planning

### ChauffeurNet and robust imitation (2019)

[[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]] introduced key ideas for making imitation learning robust for planning: synthesizing perturbations during training, adding trajectory perturbation loss, and using a mid-level bird's-eye-view representation. ChauffeurNet demonstrated that naive behavior cloning fails due to distributional drift and that data augmentation is essential.

### Privileged distillation (2020)

[[wiki/sources/papers/learning-by-cheating]] formalized the two-stage approach: first train a privileged expert with access to ground-truth state, then distill into a sensorimotor student that operates from raw sensors. This paradigm dominates CARLA benchmarks and provides a principled way to separate the "what to do" problem from the "how to perceive" problem.

### Joint planning in end-to-end systems (2023)

[[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) demonstrated that jointly training perception, prediction, and planning with a planning-centric objective yields significantly better planning than modular pipelines. The planner receives features from upstream modules and optimizes a trajectory that is both safe and comfortable. [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] extended this with vectorized representations, making the joint system more efficient.

### VLA planners (2024--2025)

The current frontier applies vision-language models directly to planning:

- [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] integrates language understanding with action generation, using planning tokens that bridge VLM reasoning and continuous trajectory output. Evaluated in closed-loop.
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] decouples VLM reasoning from the planner: the VLM produces human-readable scene descriptions and driving rationale, which a separate lightweight planner converts to trajectories. This preserves interpretability while leveraging VLM knowledge.
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] takes the maximalist approach, representing trajectories as language tokens and training a single VLM to produce them directly.
- [[wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving]] achieves real-time VLA planning (99ms latency) with RL-enhanced reasoning, demonstrating that VLA planners can meet deployment constraints.
- [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] complements VLA planning with a BEV world model that evaluates candidate trajectories for physical plausibility and safety.

### RL for planning beyond imitation

A key 2025 development is the application of reinforcement learning to push planning beyond the imitation ceiling. [[wiki/sources/papers/alphadrive-unleashing-the-power-of-vlms-in-autonomous-driving]] applies GRPO (Group Relative Policy Optimization) to driving VLMs, showing that RL fine-tuning improves planning in scenarios where the demonstration data contains suboptimal behavior. [[wiki/sources/papers/drivemoe-mixture-of-experts-for-vision-language-action-in-autonomous-driving]] uses mixture-of-experts to handle the multimodal nature of planning decisions, where averaging across modes produces dangerous trajectories.

## The open-loop vs. closed-loop debate

This is the field's most important evaluation question. Open-loop planning evaluation replays logged scenarios and measures trajectory displacement error against the human driver's actual trajectory. Closed-loop evaluation places the planner in simulation where its actions affect the scene.

The problem with open-loop evaluation: a planner that outputs the average trajectory (safe but passive) scores well on displacement metrics but drives terribly in closed-loop, where it must make decisive lane changes and assertive merges. Conversely, a planner that makes one aggressive-but-correct maneuver may score poorly on open-loop metrics because it deviates from the logged trajectory.

[[wiki/sources/papers/carla-an-open-urban-driving-simulator]] provides the primary closed-loop benchmark. Papers evaluated only on open-loop nuScenes metrics should be interpreted with significant caution. The field is converging on the position that closed-loop evaluation is a minimum requirement for planning claims.

## Present state and open problems

- **Imitation ceiling:** Behavior cloning cannot exceed the quality of demonstration data. RL offers a path beyond this ceiling but introduces instability and reward design challenges.
- **Safety guarantees:** No learned planner provides formal safety guarantees. Combining learned planning with rule-based safety layers (responsibility-sensitive safety, control barrier functions) is an active area.
- **Comfort and naturalness:** Planning metrics focus on safety and progress but rarely measure comfort, smoothness, or human-likeness, which matter for passenger acceptance.
- **Rare scenarios:** Planners trained on normal driving fail on edge cases (emergency braking, construction zones, adversarial agents). How to ensure coverage of the long tail is unresolved.
- **Interpretability:** Regulators increasingly demand that planning decisions be explainable. The decoupled approach (Senna) offers one path; whether it sacrifices performance is debated.
- **Multi-agent game theory:** Planning in dense traffic is a multi-agent game. Most planners treat other agents as independent obstacles rather than strategic actors.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]] | Robust imitation learning with data augmentation |
| [[wiki/sources/papers/learning-by-cheating]] | Privileged expert distillation for planning |
| [[wiki/sources/papers/planning-oriented-autonomous-driving]] | UniAD: planning-centric joint training |
| [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] | Efficient vectorized planning |
| [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] | Vision-language-instructed action generation |
| [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] | Decoupled VLM reasoning + lightweight planner |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Trajectories as language tokens |
| [[wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving]] | Real-time VLA planning with RL |
| [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] | World-model trajectory verification |
| [[wiki/sources/papers/alphadrive-unleashing-the-power-of-vlms-in-autonomous-driving]] | GRPO-based RL for driving VLMs |
| [[wiki/sources/papers/drivemoe-mixture-of-experts-for-vision-language-action-in-autonomous-driving]] | MoE for multimodal planning |
| [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] | Momentum-aware temporal consistency for E2E planning |
| [[wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model]] | Open-source VLA with hierarchical 3D scene queries |
| [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] | MLLM-to-planner distillation for efficient planning |
| [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]] | Adaptive reasoning VLA with RL fine-tuning |
| [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]] | Parallel-task planning with GMM multi-mode |
| [[wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation]] | Self-supervised MLLM planning without annotations |
| [[wiki/sources/papers/bridgead-bridging-past-and-future-end-to-end-autonomous-driving-with-historical-prediction]] | Multi-step temporal queries for history-enhanced planning |
| [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] | Occupancy world model for planning trajectory evaluation |
| [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] | Primary closed-loop evaluation benchmark |
| [[wiki/sources/papers/a-language-agent-for-autonomous-driving]] | LLM cognitive agent with tool use, memory, and chain-of-thought for planning |
| [[wiki/sources/papers/asyncdriver-asynchronous-large-language-model-enhanced-planner-for-autonomous-driving]] | Asynchronous LLM-planner decoupling for real-time driving |
| [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]] | Original occupancy world model for joint scene-ego prediction |
| [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] | Sparse parallel prediction-planning with safety-aware selection |
| [[wiki/sources/papers/sparsedriveV2-end-to-end-autonomous-driving-via-sparse-scene-representation]] | Factorized trajectory vocabulary scoring, 92.0 PDMS SOTA |
| [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] | Pseudo-simulation benchmark, R^2=0.8 with closed-loop |
| [[wiki/sources/papers/think-twice-before-driving-towards-scalable-decoders-for-end-to-end-autonomous-driving]] | Cascaded decoder with iterative trajectory refinement, scalable decoder depth |
| [[wiki/sources/papers/driveadapter-breaking-the-coupling-barrier-of-perception-and-planning-in-end-to-end-autonomous-driving]] | Decoupled perception-planning via adapter, reuses frozen privileged planner |

## Related

- [[wiki/concepts/prediction]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/comparisons/modular-vs-end-to-end]]
