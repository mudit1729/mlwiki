---
title: "NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking"
tags: [autonomous-driving, benchmark, simulation, evaluation, planning, end-to-end]
status: active
type: paper
year: "2024"
venue: "NeurIPS 2024"
citations: 100
arxiv_id: "2406.15349"
paper-faithfullness: audited-solid
---

# NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2406.15349)**

## Overview

Autonomous vehicle evaluation has long been split between two unsatisfying extremes: open-loop metrics that replay logged trajectories and compare predicted paths against human reference (fast but unreliable), and closed-loop simulation that renders full sensor observations at each step (accurate but computationally prohibitive and plagued by sim-to-real domain gaps). NAVSIM, by Dauner, Li, Yang et al. (University of Tubingen, Shanghai AI Lab, NVIDIA Research, Robert Bosch, University of Toronto, Stanford), introduces a **non-reactive simulation** paradigm that bridges this gap. The driving policy is queried once at scene initialization to generate a 4-second planned trajectory, and a kinematic bicycle model propagates the vehicle forward at 10Hz to evaluate consequences in a bird's-eye-view abstraction -- without expensive sensor re-rendering.

The paper's central empirical finding is that its proposed evaluation metric, **PDM Score (PDMS)**, achieves 0.7--0.8 correlation with closed-loop simulation scores, while traditional open-loop metrics (e.g., Average Displacement Error) achieve only 0.2--0.5 correlation. This validates the non-reactive assumption for short-horizon evaluation and provides a computationally tractable yet meaningful benchmark. NAVSIM also introduces a principled data curation strategy that filters out trivially easy and unsolvable scenarios from nuPlan, yielding a challenging subset where high performance requires genuine perception and planning. The CVPR 2024 NAVSIM Challenge attracted 143 teams and 463 submissions, rapidly establishing the benchmark as a community standard for end-to-end driving evaluation.

A key insight from the benchmark results is that complex multi-module architectures (UniAD at 83.4% PDMS trained for ~240 GPU-days, PARA-Drive at 84.0% PDMS trained for ~240 GPU-days) achieve only marginal gains over simpler architectures like TransFuser (84.0% PDMS trained in 1 GPU-day), suggesting potential over-engineering in the field. Even the best models trail human expert performance (94.8% PDMS) by roughly 10 percentage points, highlighting substantial remaining challenges.

## Key Contributions

- **Non-reactive simulation paradigm**: Bridges open-loop and closed-loop evaluation by querying the policy once, then simulating consequences via an LQR controller and kinematic bicycle model in BEV -- no sensor rendering required
- **PDM Score (PDMS)**: A hierarchical evaluation metric combining multiplicative safety penalties (collision, drivable area compliance) with weighted performance metrics (ego progress, time-to-collision, comfort), achieving 0.7--0.8 correlation with closed-loop simulation
- **Principled data curation**: Filters nuPlan scenarios to remove trivially easy cases (constant velocity PDMS > 0.8) and annotation errors (human reference PDMS < 0.8), ensuring benchmarked scenarios are challenging yet solvable
- **Large-scale benchmarking**: Evaluates a suite of driving planners (from ego-status MLPs to UniAD-class multi-module systems) on a standardized benchmark, revealing that architectural complexity does not reliably translate to performance gains
- **Community adoption**: The CVPR 2024 challenge demonstrated real-world impact, with the winning entry (Hydra-MDP) reviving classical trajectory-sampling approaches

## Architecture / Method

![Comparison of evaluation approaches](https://paper-assets.alphaxiv.org/figures/2406.15349v2/x1.png)

```
┌───────────────────────────────────────────────────────────┐
│                   Scene Initialization                     │
│  Multi-camera images + Ego state + HD Map                 │
└─────────────────────────┬─────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│              Driving Agent (queried once)                  │
│         Outputs: 4-second planned trajectory               │
└─────────────────────────┬─────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│              LQR Controller                                │
│     Converts waypoints ──► steering + acceleration         │
└─────────────────────────┬─────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│         Kinematic Bicycle Model (10 Hz)                    │
│    Propagates ego vehicle ──► simulated trajectory         │
└─────────────────────────┬─────────────────────────────────┘
                          │
                          ▼
┌───────────────────────────────────────────────────────────┐
│                   PDM Score                                │
│  ┌─────────────────────┐  ┌─────────────────────────────┐ │
│  │ Safety (multiply)   │  │ Performance (weighted avg)   │ │
│  │  - No Collision     │  │  - Ego Progress             │ │
│  │  - Drivable Area    │  │  - Time-to-Collision        │ │
│  └─────────┬───────────┘  │  - Comfort                  │ │
│            │              └──────────────┬──────────────┘ │
│            └──────── PDMS = NC*DAC * w_avg(EP,TTC,C) ────┘ │
└───────────────────────────────────────────────────────────┘
```

### Non-Reactive Simulation Pipeline

NAVSIM operates on the **OpenScene** dataset (a public redistribution of nuPlan). At evaluation time:

1. The driving agent receives sensor observations (multi-camera images + ego state) at scene initialization
2. The agent outputs a planned trajectory of 4 seconds
3. An **LQR controller** converts the planned waypoints into steering and acceleration commands
4. A **kinematic bicycle model** propagates the ego vehicle at 10Hz, producing a simulated trajectory
5. The simulated trajectory is scored against the recorded scene using the PDM Score

The "non-reactive" assumption means other agents follow their recorded trajectories regardless of the ego vehicle's actions. While this cannot capture multi-agent interaction effects, the paper shows it provides strong correlation with reactive closed-loop evaluation for the 4-second horizon.

### PDM Score

The PDMS combines sub-metrics hierarchically:

**Safety penalties (multiplicative):**
- **No Collisions (NC):** Full penalty for dynamic agent collisions; partial penalty (0.5) for static objects
- **Drivable Area Compliance (DAC):** Full penalty for driving outside designated road areas

**Performance metrics (weighted average):**
- **Ego Progress (EP):** Route advancement normalized by a safe upper bound
- **Time-to-Collision (TTC):** Safe margins to surrounding vehicles
- **Comfort (C):** Trajectory smoothness evaluated via acceleration and jerk thresholds

The combined formula: `PDMS = NC * DAC * weighted_average(EP, TTC, C)`

### Data Curation

![Data filtering analysis](https://paper-assets.alphaxiv.org/figures/2406.15349v2/x2.png)

The benchmark addresses the problem of trivial scenarios through two-sided filtering:
- **Remove too-easy scenarios:** If a constant-velocity baseline achieves PDMS > 0.8, the scenario does not require intelligent perception or planning
- **Remove unsolvable scenarios:** If the human reference trajectory scores PDMS < 0.8, the scenario likely has annotation errors or is inherently ambiguous

This produces the **navtrain** (103,000 samples) and **navtest** (12,000 samples) splits.

## Results

![Correlation analysis](https://paper-assets.alphaxiv.org/figures/2406.15349v2/x3.png)

### PDMS Correlation with Closed-Loop Simulation

PDMS achieves 0.7--0.8 correlation with closed-loop simulation scores across various planning durations and query frequencies, validating the non-reactive assumption. Traditional open-loop metrics (ADE, FDE) achieve only 0.2--0.5 correlation.

### Benchmark Results

| Model | PDMS | Training Compute |
|-------|------|-----------------|
| Human Expert | 94.8% | -- |
| TransFuser | 84.0% | 1 GPU-day |
| PARA-Drive | 84.0% | 240 GPU-days |
| Latent TransFuser | 83.8% | -- |
| UniAD | 83.4% | 240 GPU-days |
| Ego Status MLP | 65.6% | -- |
| Constant Velocity | 20.6% | -- |

Key observations:
- Complex architectures (UniAD, PARA-Drive) do not outperform simpler models (TransFuser) despite orders-of-magnitude more compute
- Even the best models trail human experts by ~10 percentage points
- The ego-status MLP baseline (65.6%) reveals how much can be achieved without any visual perception, echoing the findings of [[wiki/sources/papers/is-ego-status-all-you-need-for-open-loop-end-to-end-autonomous-driving]]

### CVPR 2024 Challenge Results

![Challenge results](https://paper-assets.alphaxiv.org/figures/2406.15349v2/x5.png)

- **143 teams**, 463 submissions
- **Winner: Hydra-MDP** -- extended TransFuser with trajectory sampling and scoring, reviving classical planning approaches
- **Runner-up:** Vision Language Model (VLM) approach, reflecting growing interest in foundation models for driving

## Limitations & Open Questions

- **Non-reactive assumption:** Cannot capture compounding errors or the ego vehicle's influence on other agents over longer horizons. The 4-second evaluation window limits assessment of long-horizon planning
- **Traffic rule coverage:** The current metric does not evaluate all traffic rules (e.g., stop signs, traffic lights, fuel efficiency)
- **Dataset bias:** Built exclusively on nuPlan data, which may not represent all driving conditions and geographies
- **Complexity vs. performance paradox:** The finding that simple models match complex ones may reflect benchmark limitations rather than genuine architectural parity -- longer horizons or more complex scenarios might differentiate architectures
- **Future direction:** NAVSIM v2 ([[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]]) addresses several of these limitations through pseudo-simulation with 3D Gaussian Splatting, enabling multi-step evaluation with compounding error capture

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] -- direct successor that extends NAVSIM with pseudo-simulation via 3D Gaussian Splatting for multi-step closed-loop-like evaluation
- [[wiki/sources/papers/is-ego-status-all-you-need-for-open-loop-end-to-end-autonomous-driving]] -- exposed weaknesses of open-loop nuScenes evaluation, motivating NAVSIM's non-reactive simulation approach
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] -- the primary closed-loop simulation benchmark that NAVSIM aims to complement with cheaper evaluation
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- standard open-loop benchmark whose limitations NAVSIM addresses
- [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] -- key baseline that achieves competitive performance on NAVSIM despite simplicity
- [[wiki/sources/papers/planning-oriented-autonomous-driving]] -- UniAD, complex multi-module system benchmarked on NAVSIM
- [[wiki/sources/papers/para-drive-parallelized-architecture-for-real-time-autonomous-driving]] -- parallel E2E architecture benchmarked on NAVSIM
- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] -- reports 88.1 PDMS on NAVSIM
- [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation]] -- reports 90.3 PDMS on NAVSIM
- [[wiki/concepts/planning]] -- broader context on planning evaluation challenges
