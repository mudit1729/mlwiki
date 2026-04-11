---
title: "DriveAdapter: Breaking the Coupling Barrier of Perception and Planning in End-to-End Autonomous Driving"
tags: [autonomous-driving, end-to-end, planning, imitation-learning, knowledge-distillation, transformer]
status: active
type: paper
year: "2023"
venue: "ICCV 2023"
citations: ~120
arxiv_id: "2308.00398"
paper-faithfullness: audited-solid
---

# DriveAdapter: Breaking the Coupling Barrier of Perception and Planning in End-to-End Autonomous Driving

📄 **[Read on arXiv](https://arxiv.org/abs/2308.00398)**

## Overview

DriveAdapter (Jia et al., ICCV 2023) identifies and addresses a fundamental structural problem in end-to-end autonomous driving: the tight coupling between perception and planning modules. In the standard privileged distillation paradigm (established by [[wiki/sources/papers/learning-by-cheating]]), a teacher agent with access to ground-truth BEV information is first trained, and then a student agent learns to mimic the teacher using only sensor inputs. The student must simultaneously learn both perception (extracting a good BEV representation from cameras) and planning (making driving decisions from that representation). DriveAdapter argues this coupling creates a chicken-and-egg problem: the perception encoder cannot learn good features without a competent planner providing useful gradients, and the planner cannot learn good policies without reliable perception features.

The core insight is to decouple these two learning problems by introducing "adapter" modules between perception and planning that are trained with a **feature alignment objective**: the adapters encourage student perception features to match the privileged features the (reused) teacher planner was trained on, rather than forcing the student to learn planning from scratch. This means the privileged teacher's planning weights are reused directly -- the adapters bridge the distribution gap between predicted privileged inputs and the ground-truth privileged inputs. This decoupling allows perception and planning to be trained and improved independently.

Because the learning-based teacher itself is imperfect and occasionally breaks safety rules, DriveAdapter additionally proposes **action-guided feature learning with a mask**: a mask identifies imperfect teacher features, and hand-crafted rule priors are injected for those masked regions, so the student does not blindly inherit unsafe teacher behaviors. DriveAdapter achieves DS=61.7 on Town05 Long and DS=59.4 on Longest6, competitive with prior methods; with an additional TCP trajectory head (DriveAdapter+TCP), it reaches DS=65.9 on Town05 Long and DS=62.0 on Longest6.

## Key Contributions

- **Decoupled perception-planning training**: Identifies the coupling barrier in privileged distillation and proposes to directly reuse a strong privileged teacher's planning module while the student focuses on perception
- **Feature alignment via adapters**: Adapter modules are inserted between student perception and teacher planning, trained with a feature alignment objective that closes the distribution gap between predicted and ground-truth privileged inputs
- **Action-guided feature learning with a mask**: Because the learning-based teacher is imperfect and sometimes violates safety rules, a mask identifies imperfect teacher features and injects hand-crafted rule priors into the learning process for those regions
- **Strong CARLA performance**: Competitive driving scores on Town05 Long and Longest6 benchmarks; DriveAdapter achieves DS=61.7 on Town05 Long and DS=59.4 on Longest6, with DriveAdapter+TCP reaching DS=65.9 and DS=62.0 respectively

## Architecture / Method

```
┌──────────────────────────────────────────────────────────────┐
│                       DriveAdapter                           │
│                                                              │
│  Camera/LiDAR  ┌─────────────────────────┐                   │
│  Inputs ──────►│  Perception Encoder     │                   │
│                │  (sensor-based student) │  Trainable        │
│                └───────────┬─────────────┘                   │
│                            │ Predicted privileged-like feat. │
│                            ▼                                 │
│               ┌─────────────────────────────┐                │
│               │      Adapter Modules        │                │
│               │  (feature-alignment loss    │  Trainable     │
│               │   to GT privileged features)│                │
│               │                             │                │
│               │  + Action-guided feature    │                │
│               │    learning with a MASK     │                │
│               │    over imperfect teacher   │                │
│               │    features (inject hand-   │                │
│               │    crafted rule priors)     │                │
│               └──────────────┬──────────────┘                │
│                              ▼                               │
│               ┌─────────────────────────────┐                │
│               │    Reused Teacher Planner    │                │
│               │  (pre-trained on privileged │  Reused        │
│               │   ground-truth inputs)      │                │
│               └──────────────┬──────────────┘                │
│                              ▼                               │
│                   Actions / Waypoints                        │
└──────────────────────────────────────────────────────────────┘

Core loss: feature alignment between student-predicted privileged
           features and ground-truth privileged features, plus
           masked action-guided supervision.
```

DriveAdapter's architecture has three elements:

**1. Teacher model (reused at student training time):**
A learning-based privileged teacher (trained with ground-truth states of surrounding agents and map elements) provides both its planning module -- which the student directly reuses rather than retraining from scratch -- and the ground-truth privileged features used as alignment targets.

**2. Sensor-based perception (student):**
A camera/LiDAR perception network is trained to predict the privileged inputs that the teacher's planning module expects. Directly feeding these predicted inputs to the teacher was shown to yield poor driving due to the distribution gap between predicted and ground-truth privileged inputs.

**3. Adapter modules (the key novelty):**
Adapters are inserted between student features and the teacher's planning module and trained with a **feature alignment objective**: student features are aligned with the corresponding ground-truth privileged features so the reused teacher planner receives inputs inside its training distribution.

**Action-guided feature learning with a mask:**
Because the pure learning-based teacher itself is imperfect and occasionally breaks safety rules, DriveAdapter adds a mask that identifies which teacher features are imperfect; for those regions the method injects hand-crafted rule priors via action-guided supervision, so the student is not blindly cloning unsafe teacher behavior.

**Training procedure:**
1. Obtain a privileged teacher trained with ground-truth privileged inputs.
2. Reuse the teacher's planning module directly.
3. Train the student perception network and the adapters end-to-end, minimizing a feature alignment loss between predicted and ground-truth privileged features, combined with the masked action-guided feature learning loss for safety.

## Results

DriveAdapter demonstrates strong improvements on CARLA closed-loop benchmarks:

### Town05 Long Benchmark

| Method | DS ↑ | RC ↑ | IS ↑ |
|--------|------|------|------|
| CILRS | 7.8 | 10.3 | 0.75 |
| LBC | 12.3 | 31.9 | 0.66 |
| Roach | 41.6 | 96.4 | 0.43 |
| LAV | 46.5 | 69.8 | 0.73 |
| TCP | 57.2 | 80.4 | 0.73 |
| ThinkTwice | 65.0 | 95.5 | 0.69 |
| InterFuser* | 68.3 | 95.0 | -- |
| **DriveAdapter** | **61.7** | **92.3** | **0.69** |
| **DriveAdapter + TCP** | **65.9** | **94.4** | **0.72** |

DS = Driving Score, RC = Route Completion, IS = Infraction Score. * = extra training data.

### Longest6 Benchmark

| Method | DS ↑ | RC ↑ | IS ↑ |
|--------|------|------|------|
| WOR | 23.6 | 52.3 | 0.59 |
| LAV | 34.2 | 73.5 | 0.53 |
| Transfuser | 56.7 | 92.3 | 0.62 |
| PlanT with Perception | 57.7 | 88.2 | 0.65 |
| ThinkTwice | 61.3 | 73.0 | 0.81 |
| **DriveAdapter** | **59.4** | **82.0** | **0.68** |
| **DriveAdapter + TCP** | **62.0** | **82.3** | **0.70** |

### Key ablation findings

- **Feature alignment vs. direct teacher reuse**: Directly feeding student-predicted privileged inputs to the reused teacher planner yields poor driving; adding the adapters with feature alignment closes the distribution gap and recovers strong performance, confirming the coupling barrier hypothesis
- **Action-guided masking**: Masking imperfect teacher features and injecting hand-crafted rule priors improves safety-related metrics over using teacher features directly
- **Decoupled training**: Reusing the teacher planning module while training only perception + adapters outperforms training a student planning head from scratch

## Limitations & Open Questions

- **Still relies on privileged training in simulation**: The approach requires access to a simulator with ground-truth privileged information for teacher training, limiting direct applicability to real-world data without sim-to-real transfer
- **CARLA-only evaluation**: All experiments are conducted in CARLA; generalization to real-world driving or other simulators (nuPlan, Waymo) is not demonstrated
- **Imperfect teacher**: Even with masked action-guided feature learning, performance is bottlenecked by the quality of the learning-based teacher whose imperfections the mask is designed to paper over
- **Open question**: Can the adapter / feature-alignment paradigm scale to larger foundation-model-based planners? If the planner is a VLM, does the coupling barrier still exist or does the VLM's generality already bridge the gap?

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
