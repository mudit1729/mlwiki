---
title: "DriveAdapter: Breaking the Coupling Barrier of Perception and Planning in End-to-End Autonomous Driving"
tags: [autonomous-driving, end-to-end, planning, imitation-learning, knowledge-distillation, transformer]
status: active
type: paper
year: "2023"
venue: "ICCV 2023"
citations: ~120
arxiv_id: "2308.00398"
---

# DriveAdapter: Breaking the Coupling Barrier of Perception and Planning in End-to-End Autonomous Driving

📄 **[Read on arXiv](https://arxiv.org/abs/2308.00398)**

## Overview

DriveAdapter (Jia et al., ICCV 2023) identifies and addresses a fundamental structural problem in end-to-end autonomous driving: the tight coupling between perception and planning modules. In the standard privileged distillation paradigm (established by [[wiki/sources/papers/learning-by-cheating]]), a teacher agent with access to ground-truth BEV information is first trained, and then a student agent learns to mimic the teacher using only sensor inputs. The student must simultaneously learn both perception (extracting a good BEV representation from cameras) and planning (making driving decisions from that representation). DriveAdapter argues this coupling creates a chicken-and-egg problem: the perception encoder cannot learn good features without a competent planner providing useful gradients, and the planner cannot learn good policies without reliable perception features.

The core insight is to decouple these two learning problems by introducing an "adapter" module between perception and planning. The adapter is a small transformer-based network that translates the imperfect intermediate representations produced by a sensor-based perception encoder into a format compatible with a pre-trained, frozen privileged planner. This means the privileged teacher's planning weights are reused directly -- the adapter learns to bridge the domain gap between ground-truth BEV features and sensor-derived features, rather than requiring the student to learn planning from scratch. This decoupling allows perception and planning to be trained and improved independently.

DriveAdapter achieves state-of-the-art results on the CARLA closed-loop benchmarks (Town05 Long and Longest6), significantly outperforming prior methods including TCP, InterFuser, and TransFuser. A key practical benefit is modularity: any perception encoder (TransFuser, BEVFormer, etc.) can be plugged in with any privileged planner, and each can be upgraded independently. The paper also demonstrates that the adapter can incorporate action-conditioned features to handle multi-modal driving behaviors (e.g., turning left vs. right at an intersection).

## Key Contributions

- **Decoupled perception-planning training**: Identifies the coupling barrier in privileged distillation and proposes a principled decomposition where the perception encoder and planning policy are trained separately, connected by a lightweight adapter
- **Adapter module**: A transformer-based network that translates sensor-derived features into the feature space of a pre-trained privileged planner, enabling direct reuse of privileged planning weights without retraining
- **Action-conditioned multi-modal planning**: Introduces action conditioning into the adapter to handle multi-modal driving behaviors at decision points (intersections, lane changes), addressing the mode averaging problem in imitation learning
- **Plug-and-play modularity**: Any perception backbone and any privileged planner can be combined through the adapter, enabling independent upgrades to either component
- **State-of-the-art CARLA performance**: Achieves top driving scores on Town05 Long and Longest6 benchmarks, surpassing TCP, InterFuser, and TransFuser by significant margins

## Architecture / Method

```
┌──────────────────────────────────────────────────────────────┐
│                       DriveAdapter                           │
│                                                              │
│  Camera/LiDAR  ┌─────────────────────────┐                   │
│  Inputs ──────►│  Perception Encoder     │                   │
│                │  (TransFuser / ResNet / │                   │
│                │   BEVFormer -- any)     │  Trainable        │
│                └───────────┬─────────────┘                   │
│                            │ Sensor features z_s             │
│                            ▼                                 │
│  Nav Command  ┌─────────────────────────────┐                │
│  (left/right/ │      Adapter Module         │                │
│   straight)   │  ┌───────────────────────┐  │                │
│  ────────────►│  │  Cross-Attention      │  │  Trainable     │
│    (FiLM)     │  │  Learnable queries    │  │                │
│               │  │  attend to z_s        │  │                │
│               │  │  + action conditioning│  │                │
│               │  └───────────┬───────────┘  │                │
│               │              │ Adapted feat. │                │
│               └──────────────┼──────────────┘                │
│                              │ (matches privileged           │
│                              │  feature space)               │
│                              ▼                               │
│               ┌─────────────────────────────┐                │
│               │    Frozen Privileged Planner │                │
│               │  (pre-trained on GT BEV)    │  Frozen        │
│               │  Roach / TCP-teacher        │                │
│               └──────────────┬──────────────┘                │
│                              ▼                               │
│                      Waypoint Trajectory                     │
└──────────────────────────────────────────────────────────────┘

Training: L2(predicted waypoints, expert waypoints) + aux perception losses
```

DriveAdapter's architecture consists of three components:

**1. Privileged Teacher (frozen at student training time):**
A standard privileged agent (e.g., Roach, TCP-teacher) is trained with access to ground-truth BEV information from the CARLA simulator. This teacher learns a strong planning policy parameterized as a neural network that maps privileged BEV features to waypoint trajectories. Once trained, the teacher's planning weights are frozen.

**2. Sensor-based Perception Encoder:**
Any camera-based perception backbone (e.g., TransFuser's ResNet+Transformer, BEVFormer, or a simple ResNet) processes raw sensor inputs (multi-view cameras, optionally LiDAR) and produces intermediate feature representations. This encoder is trained to produce features that, after adaptation, can drive the frozen planner effectively.

**3. Adapter Module (the key novelty):**
A small transformer network sits between the perception encoder and the frozen planner. It takes the sensor-derived features as input and outputs features in the same space as the privileged BEV features the planner was trained on. The adapter uses cross-attention: learnable query tokens attend to the perception features, and the output is projected to match the privileged feature dimensionality.

The adapter also supports **action conditioning**: a high-level navigation command (from the route planner) is encoded and used to modulate the adapter's queries via FiLM conditioning or concatenation. This allows the adapter to produce different feature translations depending on the intended maneuver, addressing the multi-modality problem where the same scene could require different actions depending on the driver's intent.

**Training procedure:**
1. Train the privileged teacher agent with ground-truth BEV inputs (standard privileged training)
2. Freeze the teacher's planning network
3. Train the perception encoder + adapter jointly, where the loss is computed on the final waypoint outputs from the frozen planner. The adapter bridges the gap between sensor features and privileged features.

The key equation is straightforward: given sensor features `z_s = Encoder(images)` and the adapter `A`, the final output is `waypoints = FrozenPlanner(A(z_s, command))`. The loss is L2 between predicted and expert waypoints, plus any auxiliary perception losses.

## Results

DriveAdapter demonstrates strong improvements on CARLA closed-loop benchmarks:

### Town05 Long Benchmark

| Method | DS ↑ | RC ↑ | IS ↑ |
|--------|------|------|------|
| CILRS | 7.47 | 13.40 | 0.56 |
| LBC | 30.97 | 55.01 | 0.56 |
| TransFuser | 54.52 | 78.41 | 0.70 |
| TCP | 55.14 | 78.20 | 0.71 |
| InterFuser | 68.31 | 95.03 | 0.72 |
| **DriveAdapter** | **75.18** | **93.56** | **0.80** |

DS = Driving Score, RC = Route Completion, IS = Infraction Score.

### Longest6 Benchmark

| Method | DS ↑ | RC ↑ | IS ↑ |
|--------|------|------|------|
| TransFuser | 49.01 | 68.24 | 0.72 |
| TCP | 50.35 | 69.12 | 0.73 |
| InterFuser | 57.74 | 81.78 | 0.71 |
| **DriveAdapter** | **63.89** | **83.25** | **0.77** |

### Key ablation findings

- **Adapter vs. direct distillation**: Adding the adapter module improves driving score by ~10-15 points over standard feature-level distillation, confirming the coupling barrier hypothesis
- **Action conditioning**: Action-conditioned adapter improves performance at intersections by 8-12% compared to unconditional adapter, particularly reducing wrong-turn infractions
- **Perception backbone flexibility**: DriveAdapter works with multiple perception encoders (TransFuser, ResNet-34, BEVFormer), consistently improving each, demonstrating true plug-and-play modularity
- **Frozen vs. fine-tuned planner**: Keeping the planner frozen performs comparably to or better than fine-tuning it jointly, validating the decoupling hypothesis

## Limitations & Open Questions

- **Still relies on privileged training in simulation**: The approach requires access to a simulator with ground-truth BEV information for teacher training, limiting direct applicability to real-world data without sim-to-real transfer
- **CARLA-only evaluation**: All experiments are conducted in CARLA; generalization to real-world driving or other simulators (nuPlan, Waymo) is not demonstrated
- **Adapter adds a module but not much compute**: The adapter is lightweight, but the overall system still requires the full perception encoder and full planner at inference time
- **Multi-modal planning is limited**: The action conditioning handles discrete mode selection (turn left/right/straight) but does not address continuous multi-modality in trajectory space (cf. diffusion-based planners like [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]])
- **Open question**: Can the adapter paradigm scale to larger foundation-model-based planners? If the planner is a VLM, does the coupling barrier still exist or does the VLM's generality already bridge the gap?

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/learning-by-cheating]] — establishes the privileged distillation paradigm that DriveAdapter improves upon
- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] — one of the perception encoders used with DriveAdapter; DriveAdapter outperforms it significantly
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] — UniAD represents the jointly-trained paradigm; DriveAdapter offers an alternative via decoupled training
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] — another jointly-trained E2E approach that DriveAdapter's decoupling philosophy contrasts with
- [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]] — foundational conditional imitation learning that DriveAdapter builds upon
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] — primary evaluation environment
- [[wiki/sources/papers/para-drive-parallelized-architecture-for-real-time-autonomous-driving]] — PARA-Drive similarly explores modular E2E design choices, complementary to DriveAdapter's adapter approach
- [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] — DiMA also uses distillation to decouple components, but distills the LLM rather than adapting the planner
- [[wiki/concepts/planning]] — DriveAdapter's core contribution is to planning methodology
- [[wiki/concepts/end-to-end-architectures]] — DriveAdapter is a Type 3 E2E system with explicit decoupling
- [[wiki/concepts/autonomous-driving]] — broader context for CARLA-based E2E driving research
