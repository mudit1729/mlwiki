---
title: "Pseudo-Simulation for Autonomous Driving (NAVSIM v2)"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: CoRL 2025
tags:
  - paper
  - autonomous-driving
  - benchmark
  - simulation
  - evaluation
citations: 62
arxiv_id: "2506.04218"
---

# Pseudo-Simulation for Autonomous Driving (NAVSIM v2)

:page_facing_up: **[Read on arXiv](https://arxiv.org/abs/2506.04218)**

## Overview

Pseudo-Simulation by Cao, Hallgarten et al. (Tubingen / Shanghai AI Lab / NVIDIA / Stanford, CoRL 2025) introduces a novel evaluation paradigm for autonomous driving that bridges the gap between open-loop evaluation (fast but unreliable) and closed-loop simulation (accurate but expensive). The key insight is that you can pre-generate diverse synthetic observations from real driving data using 3D Gaussian Splatting, creating a bank of plausible future states that approximate what the ego vehicle would observe under different actions -- without requiring a full online simulator.

NAVSIM v2 implements this pseudo-simulation framework as the de facto standard benchmark for end-to-end autonomous driving evaluation. The benchmark reveals that pseudo-simulation correlates much better with closed-loop simulation (R^2=0.8) than the best existing open-loop metric (R^2=0.7), while being orders of magnitude cheaper than full simulation. It also uncovers previously unknown failure modes in popular AV algorithms that open-loop metrics miss entirely.

## Key Contributions

- **Pseudo-simulation paradigm**: A new evaluation approach that operates on real datasets but augments them with pre-generated synthetic observations via 3D Gaussian Splatting, combining the realism of open-loop data with the feedback sensitivity of closed-loop evaluation
- **3D Gaussian Splatting for driving scenes**: Specializes Gaussian Splatting for outdoor driving by pre-generating diverse observations varying in position, heading, and speed from initial real-world observations
- **Proximity-based importance weighting**: Assigns higher importance to synthetic observations that best match the AV's likely future behavior, approximating the closed-loop compounding error effect
- **NAVSIM v2 benchmark**: Public leaderboard with challenging driving scenarios from nuPlan (navhard subset: 450 Stage 1 + 5462 Stage 2 observations), establishing a community standard for E2E driving evaluation
- **Failure mode discovery**: Reveals previously unknown failure modes in popular methods that open-loop evaluation misses

## Architecture / Method

The pseudo-simulation pipeline operates in two phases:

**Phase 1 -- Observation Generation (Offline):** From each real-world driving observation (multi-camera images + ego state), the system generates a bank of synthetic observations using 3D Gaussian Splatting. The Gaussians are fit to the real driving scene and then re-rendered from novel viewpoints corresponding to different ego positions, headings, and speeds. This produces a set of plausible future observations the ego might encounter under different actions. This phase is done once and cached.

**Phase 2 -- Evaluation (Online):** The AV model is evaluated in a loop:
1. Given an observation, the AV predicts an action (trajectory)
2. The system selects the pre-generated synthetic observation that best matches where the AV's action would take it, using proximity-based weighting
3. This synthetic observation becomes the input for the next step
4. The process repeats, capturing compounding errors that open-loop evaluation misses

The proximity-based weighting scheme is critical: rather than requiring exact trajectory matching (which would need infinite pre-generated observations), the system weights nearby observations inversely by distance and heading difference, creating a soft approximation of the true closed-loop dynamics.

**NAVSIM v2 Benchmark Design:** The benchmark uses a curated subset of nuPlan called "navhard" -- challenging scenarios including dense traffic, construction zones, and complex intersections. The PDMS (Planning-Driven Metric Score) evaluates trajectories on safety, progress, comfort, and rule compliance.

## Results

### Correlation with Closed-Loop Simulation

| Evaluation Method | R^2 with Closed-Loop |
|---|---|
| Standard open-loop (L2 distance) | 0.3-0.5 |
| Best open-loop metric (PDM-Open) | 0.7 |
| **Pseudo-simulation (NAVSIM v2)** | **0.8** |

### NAVSIM v2 Leaderboard (Selected Methods)

| Method | PDMS (v2) |
|---|---|
| Constant velocity baseline | ~60 |
| TransFuser | ~70 |
| UniAD | ~75 |
| SparseDriveV2 | ~92 (on v1) |

Pseudo-simulation reveals that several methods that score well on open-loop metrics fail in pseudo-simulation due to compounding errors in dynamic scenarios.

## Limitations

- Pre-generated observations cannot capture all possible future states; rare or extreme deviations from the observation bank may not be well represented
- 3D Gaussian Splatting rendering quality degrades at large viewpoint changes from the original observation
- Does not model reactive agents (other vehicles, pedestrians do not respond to the ego vehicle's actions)
- Requires high-quality 3D reconstruction of driving scenes, which depends on sensor quality and scene complexity
- R^2=0.8 correlation with closed-loop is strong but not perfect; safety-critical edge cases may still be missed

## Connections

- Supersedes the original NAVSIM (2406.15349, NeurIPS 2024) as the standard E2E driving benchmark
- [[wiki/sources/papers/sparsedriveV2-end-to-end-autonomous-driving-via-sparse-scene-representation]] reports 92.0 PDMS on NAVSIM v1
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] provides full closed-loop simulation that NAVSIM v2 approximates more cheaply
- Builds on the nuPlan dataset which extends [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]]
- Evaluates methods like [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) and [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] (TransFuser)
- Gaussian Splatting rendering connects to the perception methods in [[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting]] and [[wiki/sources/papers/gaussrender-learning-3d-occupancy-with-gaussian-rendering]]
