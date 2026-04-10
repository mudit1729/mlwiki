---
title: "LanguageMPC: Large Language Models as Decision Makers for Autonomous Driving"
tags:
  - autonomous-driving
  - llm
  - planning
  - nlp
  - model-predictive-control
  - multimodal
  - chain-of-thought
type: source-summary
status: active
year: "2023"
venue: "arXiv"
citations: 100
arxiv_id: "2310.03026"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2310.03026)**

## Overview

LanguageMPC addresses a fundamental limitation in autonomous driving: traditional planners (MPC, RL) struggle with complex scenarios that require high-level reasoning about scene context, intent, and strategy. The paper proposes a novel integration of large language models with Model Predictive Control, where the LLM serves not as a direct controller but as a high-level decision maker that modulates MPC parameters. This dual-frequency architecture lets the LLM reason at a slower cadence while MPC maintains real-time responsiveness -- an elegant solution to the LLM inference latency problem that plagues other LLM-for-driving approaches.

The core method operates through a structured three-stage LLM reasoning pipeline: (1) **scenario encoding**, where the LLM processes trajectory predictions and allocates attention to relevant vehicles via dynamic observation matrices; (2) **action guidance**, where the LLM discretizes potential actions into intervals to bias the MPC action space; and (3) **weight adjustment**, where the LLM dynamically selects cost function weights for the MPC optimization. Rather than generating trajectories or control commands directly, the LLM modifies the MPC objective through soft constraints -- a key design decision that preserves the safety guarantees and stability of classical control while injecting semantic reasoning.

Evaluated across five scenarios in the SUMO traffic simulator, LanguageMPC achieves zero collisions in four out of five scenarios (signalized intersections, unsignalized intersections, roundabouts, and lane-changing), reduces overall costs by 18.1% vs. traditional MPC in signalized intersections and 16.4% in unsignalized intersections, and consistently outperforms classical MPC and RL baselines (DQN, PPO, SAC, ADP). In the fifth scenario (emergency obstacle avoidance), LanguageMPC records only 3 collisions versus 7–11 for baseline methods — still best-in-class but not zero. The paper also demonstrates text-modulated driving style adjustment via natural language commands and multi-vehicle coordination through a hybrid centralized-distributed LLM architecture. GPT-3.5 is used as the LLM, operating at ~0.4 Hz with MPC executing at 10 Hz.

## Key Contributions

- **LLM-MPC integration via soft constraints:** The LLM modifies MPC cost function parameters (weights, action biases, attention masks) rather than generating direct control commands, preserving MPC's optimization-based safety guarantees
- **Three-stage structured LLM reasoning:** Scenario encoding (attention allocation) -> action guidance (action discretization) -> weight adjustment (cost function tuning), providing a principled decomposition of the decision-making problem
- **Dual-frequency architecture:** LLM operates at low frequency for high-level decisions while MPC runs at control frequency, addressing the inference latency bottleneck that limits real-time LLM deployment in driving
- **Dynamic observation matrix with LLM attention masks:** The LLM selectively attends to relevant vehicles and filters distractions, focusing MPC optimization on the most important agents in the scene
- **Text-modulated driving and multi-vehicle coordination:** Demonstrates that natural language can adjust driving style at runtime and that a hybrid centralized-distributed LLM architecture can coordinate multiple vehicles

## Architecture / Method

```
┌─────────────────────────────────────────────────────────┐
│                LanguageMPC Framework                      │
│                                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │  High-Level Loop (LLM, low frequency)       │        │
│  │                                             │        │
│  │  ┌──────────────┐                           │        │
│  │  │ Traffic Scene │  (ego state, trajectories,│        │
│  │  │ Text Encoding │   road topology, signals) │        │
│  │  └──────┬───────┘                           │        │
│  │         ▼                                   │        │
│  │  ┌──────────────────┐                       │        │
│  │  │ Stage 1: Scenario │──► Observation Matrix │        │
│  │  │ Encoding (Attn)   │   (which agents to    │        │
│  │  └──────┬───────────┘    attend to)          │        │
│  │         ▼                                   │        │
│  │  ┌──────────────────┐                       │        │
│  │  │ Stage 2: Action   │──► Action Intervals   │        │
│  │  │ Guidance          │   (soft bias terms)   │        │
│  │  └──────┬───────────┘                       │        │
│  │         ▼                                   │        │
│  │  ┌──────────────────┐                       │        │
│  │  │ Stage 3: Weight   │──► Cost Weights       │        │
│  │  │ Adjustment        │   (rebalance MPC obj) │        │
│  │  └──────┬───────────┘                       │        │
│  └─────────┼───────────────────────────────────┘        │
│            ▼                                            │
│  ┌─────────────────────────────────────────────┐        │
│  │  Low-Level Loop (MPC, real-time frequency)  │        │
│  │                                             │        │
│  │  min  w_track * ||x - x_ref||²             │        │
│  │   u   + w_action * ||u - u_bias||²         │        │
│  │       + w_safety * safety_cost(obs_matrix)  │        │
│  │  s.t. vehicle dynamics, constraints         │        │
│  │                    │                        │        │
│  │                    ▼                        │        │
│  │           ┌──────────────┐                  │        │
│  │           │ Control Cmds │                  │        │
│  │           │ (steer, acc) │                  │        │
│  │           └──────────────┘                  │        │
│  └─────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

![LanguageMPC Framework](https://paper-assets.alphaxiv.org/figures/2310.03026v4/img-0.jpeg)

The LanguageMPC system operates as a hierarchical controller with two loops:

**High-level loop (LLM):** At each decision step, the LLM receives a structured text encoding of the current traffic scene including ego vehicle state, surrounding vehicle trajectories, road topology, and traffic signals. It processes this through three stages:

1. **Scenario Encoding:** The LLM analyzes predicted trajectories of surrounding vehicles and assigns attention weights, producing a dynamic observation matrix that tells MPC which agents to prioritize. This acts as an attention mask filtering the MPC's constraint space.

2. **Action Guidance:** The LLM reasons about appropriate driving actions (e.g., accelerate, decelerate, lane change) and discretizes them into action intervals that bias the MPC's action search space. These serve as soft constraints rather than hard commands.

3. **Weight Adjustment:** Based on the scenario analysis, the LLM selects appropriate weights for the MPC cost function components (tracking deviation, action penalty, safety margin), effectively rebalancing the optimization objective for the current situation.

The LLM used in experiments is **GPT-3.5**, operating at approximately **0.4 Hz** (updates every ~2.5 seconds, or ~1.5 seconds with emergency pre-evaluation). The MPC runs at **10 Hz** for real-time control.

**Low-level loop (MPC):** The MPC controller operates at real-time frequency, optimizing trajectories subject to:
- Tracking cost (deviation from reference trajectory)
- Action penalty with LLM-provided bias terms
- Safety constraints shaped by the LLM's dynamic observation matrix
- Vehicle dynamics constraints

The MPC cost function incorporates LLM outputs as soft constraints, allowing the optimization to deviate from LLM suggestions when physical constraints or safety requirements demand it.

![Scenario Results](https://paper-assets.alphaxiv.org/figures/2310.03026v4/img-1.jpeg)

## Results

LanguageMPC was evaluated across five driving scenarios in the SUMO simulator against traditional MPC and four RL baselines (DQN, PPO, SAC, ADP):

| Method | Signalized Intersection | Unsignalized Intersection | Roundabout | Lane-Changing | Emergency Obstacle Avoidance |
|--------|------------------------|--------------------------|------------|---------------|------------------------------|
| LanguageMPC | **0 collisions, -18.1% cost** | **0 collisions, -16.4%** | **0 collisions** | **0 collisions** | **3 collisions** (best) |
| Traditional MPC | Higher cost baseline | Collisions observed | Collisions observed | Collisions observed | 7–11 collisions |
| DQN | Suboptimal | Suboptimal | Suboptimal | Suboptimal | 7–11 collisions |
| PPO | Suboptimal | Suboptimal | Suboptimal | Suboptimal | 7–11 collisions |
| SAC | Suboptimal | Suboptimal | Suboptimal | Suboptimal | 7–11 collisions |
| ADP | Suboptimal | Suboptimal | Suboptimal | Suboptimal | 7–11 collisions |

Key findings:
- **Zero collisions** in 4 out of 5 scenarios; in the fifth (emergency obstacle avoidance) LanguageMPC records **3 collisions vs. 7–11** for baselines — still best but not zero
- **18.1% cost reduction** vs traditional MPC in signalized intersections; **16.4% improvement** in unsignalized intersections
- **Text-modulated driving:** Successfully adjusted driving style (aggressive vs. conservative) via natural language commands at runtime
- **Novel scenario handling:** The system correctly interpreted and responded to text guidance about road construction avoidance and other uncommon situations
- **Multi-vehicle coordination:** A hybrid centralized-distributed LLM architecture coordinated multiple autonomous vehicles, with a central LLM providing global strategy and local LLMs handling individual vehicle control

## Limitations & Open Questions

- **SUMO simulator only:** All experiments use the SUMO traffic simulator, which has simpler dynamics than CARLA or real-world driving. Transfer to more realistic environments is unvalidated.
- **LLM inference latency:** GPT-3.5 takes ~2.5 seconds per standard call (~1.5 seconds with emergency pre-evaluation), yielding ~0.4 Hz update rate. While the dual-frequency design mitigates this, sub-second critical decisions cannot rely on LLM reasoning. The paper acknowledges LLMs have "limited sensitivity to precise numerical values," which is why actions and weights are discretized into predefined pools rather than generated as raw numbers.
- **Structured text input assumption:** The system requires structured scene descriptions as LLM input, which depends on upstream perception quality. How perception errors propagate through LLM reasoning to MPC parameters is not studied.
- **Limited scenario complexity:** Five SUMO scenarios, while diverse, do not cover the full tail of real-world driving complexity (pedestrians, cyclists, adverse weather, construction zones beyond text guidance).
- **No comparison with later LLM-for-driving methods:** As a 2023 paper, it predates Agent-Driver, AsyncDriver, and other LLM-planner integration approaches that might offer different trade-offs.
- **Open question:** Is parameter modulation (LanguageMPC) or asynchronous feature injection (AsyncDriver) the more scalable paradigm for LLM-MPC integration?

## Connections

Related papers in the wiki:

- [[wiki/sources/papers/a-language-agent-for-autonomous-driving]] -- Agent-Driver (ICLR 2024) takes a different approach: LLM as cognitive agent with tool library and memory, rather than MPC parameter modulation. Both address LLM-for-planning but with fundamentally different integration paradigms.
- [[wiki/sources/papers/asyncdriver-asynchronous-large-language-model-enhanced-planner-for-autonomous-driving]] -- AsyncDriver (ECCV 2024) shares the dual-frequency insight (LLM at low frequency, planner at high frequency) but uses feature injection via cross-attention rather than cost function modulation. Direct successor in the asynchronous LLM-planner design space.
- [[wiki/sources/papers/driving-with-llms-fusing-object-level-vector-modality-for-explainable-autonomous-driving]] -- Driving with LLMs (Wayve, ICRA 2024) is a contemporary paper also exploring LLM integration for driving, but focuses on explainability via QA rather than MPC parameter modulation.
- [[wiki/sources/papers/drive-as-you-speak-enabling-human-like-interaction-with-large-language-models-in-autonomous-vehicles]] -- Drive as You Speak explores LLM as human-vehicle interaction interface; LanguageMPC's text-modulated driving capability is a related but more control-oriented use of natural language.
- [[wiki/sources/papers/drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states]] -- DriveMLM aligns LLMs with behavioral planning states; LanguageMPC takes a more classical control approach by keeping MPC as the planner and using LLM for parameter tuning.
- [[wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models]] -- VoxPoser similarly uses LLMs to shape an optimization landscape (3D value maps for MPC) rather than generating actions directly. LanguageMPC applies an analogous principle to driving: LLM defines the objective, classical optimizer executes.
- [[wiki/concepts/planning]] -- Broader context on the evolution from classical to learned to LLM-augmented planning
- [[wiki/concepts/autonomous-driving]] -- Application domain context
