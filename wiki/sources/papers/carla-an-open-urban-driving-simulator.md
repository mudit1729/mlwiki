---
title: CARLA: An Open Urban Driving Simulator
type: source-summary
status: seed
updated: 2026-04-05
year: 2017
venue: CoRL
tags:
  - paper
  - autonomous-driving
  - benchmark
  - simulator
citations: 6490
---

# CARLA: An Open Urban Driving Simulator

## Citation

Dosovitskiy, Ros, Codevilla, Lopez, Koltun (Intel Labs / CVC Barcelona), CoRL, 2017.

📄 **[Read on arXiv](https://arxiv.org/abs/1711.03938)**

## Overview

CARLA (Car Learning to Act) is an open-source simulator for autonomous driving research, built on Unreal Engine 4, that provides realistic urban environments with dynamic weather, traffic, and pedestrians. The simulator was designed specifically to support development, training, and benchmarking of autonomous driving systems, including sensor-based perception, imitation learning, and reinforcement learning approaches. CARLA provides flexible sensor suites (RGB cameras, depth, semantic segmentation, LiDAR, GPS, IMU), controllable NPCs, and a Python API for programmatic interaction.

The paper introduced CARLA along with a systematic benchmark comparing three approaches to autonomous driving: a modular pipeline (perception + planning), an imitation learning approach (conditional imitation learning), and a reinforcement learning approach (A3C). The benchmark evaluated these methods on goal-directed navigation tasks in both training and novel environments under varying weather conditions. This standardized evaluation framework became critically important for the field, as it provided the first reproducible, controlled comparison of fundamentally different autonomous driving paradigms.

CARLA's impact on the autonomous driving research community has been extraordinary. With over 6,000 citations, it became the default evaluation platform for end-to-end driving research. The CARLA Leaderboard established standardized benchmarks that enabled direct comparison between methods, accelerating progress in the field. Nearly every major end-to-end driving paper published between 2018 and 2024 (including ChauffeurNet, LMDrive, and many VLA driving systems) either evaluates on CARLA or uses CARLA-generated training data.

## Key Contributions

- **Open-source, high-fidelity driving simulator**: Built on Unreal Engine 4 with physically-based rendering, dynamic weather (rain, fog, sun angle), day/night cycles, and realistic urban layouts with traffic lights, signs, pedestrians, and vehicles
- **Flexible sensor configuration**: Supports RGB cameras (arbitrary placement and intrinsics), depth maps, semantic segmentation ground truth, LiDAR point clouds, GPS, IMU, and vehicle telemetry -- all accessible via Python API
- **Standardized benchmark for driving approaches**: First controlled comparison of modular pipeline vs. imitation learning vs. reinforcement learning on identical tasks and environments, establishing a reproducible evaluation framework
- **Goal-directed navigation tasks**: Benchmark tasks include straight driving, single turn, navigation (follow GPS route), and navigation with dynamic obstacles, with separate training and test weather conditions to measure generalization
- **Controllable traffic and scenarios**: Programmable NPC vehicles and pedestrians, traffic light control, and scenario injection enable systematic testing of edge cases and safety-critical situations

## Architecture / Method

![CARLA simulator showcasing diverse weather conditions in the same urban environment](https://paper-assets.alphaxiv.org/figures/1711.03938v1/img-0.jpeg)

```
┌────────────────────────────────────────────────────────────┐
│                CARLA Server-Client Architecture             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────┐                      │
│  │         CARLA Server             │                      │
│  │      (Unreal Engine 4)           │                      │
│  │                                  │                      │
│  │  ┌────────────┐ ┌────────────┐   │                      │
│  │  │  Physics   │ │ Rendering  │   │                      │
│  │  │  Engine    │ │ (PBR)      │   │                      │
│  │  └────────────┘ └────────────┘   │                      │
│  │  ┌────────────┐ ┌────────────┐   │                      │
│  │  │  NPC AI    │ │  Weather   │   │                      │
│  │  │ (vehicles, │ │ (rain,fog, │   │                      │
│  │  │  peds)     │ │  sun,night)│   │                      │
│  │  └────────────┘ └────────────┘   │                      │
│  └──────────────┬───────────────────┘                      │
│                 │  TCP/IP                                   │
│                 ▼                                          │
│  ┌──────────────────────────────────┐                      │
│  │       Python / C++ Client        │                      │
│  │                                  │                      │
│  │  ┌──────────┐   ┌────────────┐   │                      │
│  │  │ Sensors: │   │ Control:   │   │                      │
│  │  │ RGB, Depth│   │ Steer,     │   │                      │
│  │  │ Seg, LiDAR│   │ Throttle,  │   │                      │
│  │  │ GPS, IMU  │   │ Brake      │   │                      │
│  │  └──────────┘   └────────────┘   │                      │
│  └──────────────────────────────────┘                      │
│                                                            │
│  Benchmark Tasks: Straight │ One-Turn │ Nav │ Nav-Dynamic  │
└────────────────────────────────────────────────────────────┘
```

CARLA is built as a server-client architecture. The server runs the Unreal Engine 4 simulation (physics, rendering, NPC AI) and the client connects via a Python/C++ API to control the ego vehicle, configure sensors, and retrieve observations. The simulation runs at a configurable timestep (typically 10-20 FPS for training, up to 60 FPS for evaluation).

The simulator provides several urban maps with varying complexity. Each map includes buildings, roads with lane markings, traffic lights, stop signs, and spawn points for vehicles and pedestrians. Weather is parameterized by cloud coverage, precipitation, sun altitude/azimuth, and fog density. NPC vehicles follow predefined autopilot routes with basic collision avoidance.

The benchmark defines four task conditions of increasing difficulty: (1) straight -- drive straight to a goal; (2) one turn -- navigate one intersection; (3) navigation -- follow a multi-waypoint route; (4) navigation dynamic -- same as navigation but with other vehicles and pedestrians. Success is measured by percentage of goal-reaching episodes within a time limit. The three baseline approaches evaluated are: a modular pipeline using semantic segmentation + rule-based planning, conditional imitation learning (CIL) trained on expert demonstrations with high-level commands, and A3C reinforcement learning trained from raw pixels.

## Results

- **Modular pipeline** achieves the highest success rate in training conditions (86-92%) but degrades significantly in novel weather (68-82%), showing overfitting to visual conditions
- **Imitation learning (CIL)** achieves moderate success (82-89% training, 68-80% new weather) with the simplest training procedure and fastest inference
- **Reinforcement learning (A3C)** achieves lowest overall success (52-68%) but shows the most consistent behavior across weather conditions, suggesting better generalization from reward-based learning
- **Dynamic obstacles** dramatically reduce success for all methods, with the RL agent particularly struggling (14% success on navigation dynamic in new weather)
- **Generalization gap**: All methods show significant performance drops when tested in unseen weather conditions, quantifying the sim-to-real-style domain gap even within the simulator

## Limitations & Open Questions

- The visual and physical realism, while high for 2017, falls short of real-world complexity -- the domain gap between CARLA and real driving remains substantial, and good CARLA performance does not guarantee real-world transfer
- NPC behavior uses simple rule-based autopilot rather than learned or naturalistic driving models, limiting the realism of interactive scenarios
- The benchmark tasks are relatively simple (point-to-point navigation); CARLA later added the Leaderboard with more complex scenarios, but the original benchmark does not cover highway driving, parking, or complex multi-agent interactions

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/sources/autonomous-driving-seminal-papers]]
- [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]]
- [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]]
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]]

