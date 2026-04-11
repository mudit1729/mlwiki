---
title: "SOLVE: Synergy of Language-Vision and End-to-End Networks for Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-11
year: 2025
venue: CVPR 2025
tags:
  - paper
  - autonomous-driving
  - vla
  - chain-of-thought
  - end-to-end
citations: ~10
arxiv_id: "2505.16805"
paper-faithfullness: audited-fixed
---

# SOLVE: Synergy of Language-Vision and End-to-End Networks for Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2505.16805)

## Overview

SOLVE proposes a synergistic framework that combines a Vision-Language Model (VLM) reasoning branch (SOLVE-VLM) with an end-to-end (E2E) driving network (SOLVE-E2E), connected through a shared visual encoder and a Trajectory Chain-of-Thought (T-CoT) mechanism. The key insight is that VLMs provide powerful scene understanding and reasoning but are too slow for real-time planning, while E2E networks excel at trajectory prediction but lack interpretable reasoning. SOLVE bridges these complementary strengths via feature-level integration rather than text-mediated information transfer.

The central architectural innovation is a shared visual encoder used by both components, enabling mutual enhancement. The VLM generates high-quality trajectory proposals asynchronously (temporal decoupling strategy), which are stored in a memory system and used by the E2E model as initialization priors. The Trajectory Chain-of-Thought (T-CoT) paradigm enables the VLM to select from a pre-computed trajectory bank and then refine individual waypoints, rather than auto-regressively generating trajectories from scratch — addressing the VLM's well-known difficulty with precise spatial generation.

## Key Contributions

- **Shared visual encoder**: Feature-level integration where both SOLVE-VLM and SOLVE-E2E share the same compressed visual representations, enabling mutual enhancement and consistent scene understanding
- **Sequential Q-Former (SQ-Former)**: Compresses multi-view camera images into a fixed set of visual tokens through three sequential stages — foreground object detection, scene understanding, and navigation context — serving both VLM and E2E components
- **Trajectory Chain-of-Thought (T-CoT)**: The VLM selects from a pre-computed trajectory bank rather than generating from scratch, then refines individual waypoints; this two-stage (select + refine) approach avoids the fragility of auto-regressive spatial generation
- **Temporal decoupling**: VLM operates asynchronously at lower frequency, storing trajectory proposals in a memory system that the real-time E2E model uses as initialization priors — resolving the speed vs. reasoning trade-off

## Architecture / Method

```
  ┌──────────────────────────────────────────────────────────────┐
  │  Multi-Camera Images                                         │
  └───────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │  Sequential Q-Former   │  (shared visual encoder)
              │  Stage 1: Foreground   │
              │  Stage 2: Scene        │
              │  Stage 3: Navigation   │
              └────────┬───────────────┘
                       │ visual tokens
              ┌────────┴─────────────────────────────┐
              │                                      │
              ▼                                      ▼
  ┌───────────────────────┐          ┌───────────────────────────┐
  │  SOLVE-VLM            │          │  SOLVE-E2E                │
  │  (asynchronous)       │          │  (real-time)              │
  │                       │          │                           │
  │  T-CoT:               │          │  Planning Decoder         │
  │  1. Select trajectory │          │       ▲                   │
  │     from bank         │  memory  │       │ init prior        │
  │  2. Refine waypoints  │─────────►│  trajectory memory        │
  └───────────────────────┘          └───────────────────────────┘
                                               │
                                               ▼
                                   ┌─────────────────────┐
                                   │  Trajectory Waypoints│
                                   └─────────────────────┘
```

SOLVE has three main components:

1. **Sequential Q-Former (SQ-Former)**: A shared visual encoder that compresses multi-view camera images into a fixed set of visual tokens. It operates sequentially through three stages:
   - **Stage 1 — Foreground object detection**: Encodes dynamic objects (vehicles, pedestrians, cyclists)
   - **Stage 2 — Scene understanding**: Captures static elements (road layout, traffic signs, environment)
   - **Stage 3 — Navigation context**: Integrates temporal and spatial relationships for path planning

   The SQ-Former is trained jointly with both SOLVE-VLM and SOLVE-E2E, ensuring its visual representations are optimized for both reasoning and real-time planning.

2. **SOLVE-VLM (asynchronous reasoning)**: Takes shared visual tokens as input and applies the Trajectory Chain-of-Thought (T-CoT) paradigm in two stages:
   - **Stage 1 — Trajectory selection**: The VLM selects the most appropriate trajectory from a pre-computed trajectory bank using its reasoning about traffic rules, safety, and driving context
   - **Stage 2 — Trajectory refinement**: The VLM adjusts individual waypoints of the selected trajectory to match the specific scenario

   The VLM operates asynchronously at lower frequency and stores its refined trajectory proposals in a trajectory memory system.

3. **SOLVE-E2E (real-time planning)**: A real-time E2E driving network that accesses VLM-generated trajectories from the memory system as initialization priors, guiding its own trajectory generation while maintaining real-time performance. The shared visual encoder provides consistent scene representations to both components.

**Training**: Multi-task training with trajectory planning loss and VLM trajectory selection/refinement objectives. The shared visual encoder is trained jointly with both components, receiving gradients from both the VLM reasoning tasks and the E2E planning loss.

## Results

Evaluated on the nuScenes open-loop planning benchmark, SOLVE achieves state-of-the-art performance across displacement error (L2) and collision rate metrics, outperforming prior VLM-E2E integration methods such as VAD. (Specific numeric results should be verified against the published paper; figures in the original wiki were not verified against ground truth.)

- **State-of-the-art on nuScenes**: Consistent improvements across L2 displacement error and collision rate metrics at multiple prediction horizons
- **Ablation — shared visual encoder**: Removing the shared encoder and reverting to independent visual processing degrades performance, confirming that feature-level synergy is a genuine contribution
- **Ablation — T-CoT paradigm**: The trajectory selection+refinement approach significantly outperforms direct VLM trajectory generation, validating the design choice of using a trajectory bank
- **Ablation — temporal decoupling**: The asynchronous VLM strategy maintains real-time E2E performance while incorporating high-quality reasoning guidance
- Qualitative analysis shows SOLVE-generated trajectories exhibit improved adherence to traffic rules and more natural driving behavior compared to pure E2E baselines

## Limitations & Open Questions

- Evaluation is open-loop on nuScenes; closed-loop evaluation would better test whether the VLM reasoning truly improves real-world driving behavior
- The temporal decoupling strategy relies on a trajectory memory system that may contain stale VLM proposals in rapidly changing environments
- The quality of trajectory selection and refinement depends on the trajectory bank quality; poor candidate generation could bottleneck the T-CoT process
- The SQ-Former's three-stage sequential design introduces hyperparameters (number of queries per stage, attention layers) that require tuning

## Connections

- [[wiki/concepts/autonomous-driving]] -- VLM-enhanced E2E driving
- [[wiki/concepts/vision-language-action]] -- synergy between VLM reasoning and action generation
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] -- similar decoupled VLM + E2E approach
- [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] -- related distillation of VLM reasoning into E2E
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] -- structured VQA for driving reasoning
- [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] -- foundational CoT prompting work
- [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] -- related VLA driving approach
