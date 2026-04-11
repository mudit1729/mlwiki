---
title: CARLA: An Open Urban Driving Simulator
type: source-summary
status: seed
updated: 2026-04-11
year: 2017
venue: CoRL
tags:
  - paper
  - autonomous-driving
  - benchmark
  - simulator
citations: 6490
paper-faithfullness: audited-solid
---

# CARLA: An Open Urban Driving Simulator

## Citation

Dosovitskiy, Ros, Codevilla, Lopez, Koltun (Intel Labs / Toyota Research Institute / CVC Barcelona), CoRL, 2017.

📄 **[Read on arXiv](https://arxiv.org/abs/1711.03938)**

## Overview

CARLA (Car Learning to Act) is an open-source simulator for autonomous driving research, built on Unreal Engine 4, that provides realistic urban environments with dynamic weather, traffic, and pedestrians. The simulator was designed specifically to support development, training, and benchmarking of autonomous driving systems, including sensor-based perception, imitation learning, and reinforcement learning approaches. CARLA provides flexible sensor suites (RGB cameras, depth maps, semantic segmentation across 12 classes) along with vehicle state data (GPS coordinates, orientation, speed, acceleration), controllable NPCs, and a Python API for programmatic interaction. LiDAR, IMU, and radar were not part of the original 2017 paper and were added in later versions.

The paper introduced CARLA along with a systematic benchmark comparing three approaches to autonomous driving: a modular pipeline (perception + planning), an imitation learning approach (conditional imitation learning), and a reinforcement learning approach (A3C). The benchmark evaluated these methods on goal-directed navigation tasks in both training and novel environments under varying weather conditions. This standardized evaluation framework became critically important for the field, as it provided the first reproducible, controlled comparison of fundamentally different autonomous driving paradigms.

CARLA's impact on the autonomous driving research community has been extraordinary. With over 6,000 citations, it became one of the most widely used evaluation platforms for simulation-based driving research. Later CARLA releases and the CARLA Leaderboard further standardized comparisons between methods, accelerating progress in the field.

## Key Contributions

- **Open-source, high-fidelity driving simulator**: Built on Unreal Engine 4 with physically-based rendering, dynamic weather, two lighting conditions (midday and sunset), and realistic urban layouts with traffic lights, signs, pedestrians, and vehicles
- **Flexible sensor configuration**: Supports RGB cameras (arbitrary placement and intrinsics), depth maps, and semantic segmentation ground truth (12 classes: road, lane markings, traffic signs, sidewalks, vehicles, pedestrians, and others), plus vehicle state data (GPS coordinates, orientation, speed, acceleration) -- all accessible via Python API. LiDAR, IMU, and radar are not part of the original paper.
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
│  │  │  peds)     │ │  sun,set)  │   │                      │
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
│  │  │ Seg, GPS  │   │ Throttle,  │   │                      │
│  │  │ State Data│   │ Brake      │   │                      │
│  │  └──────────┘   └────────────┘   │                      │
│  └──────────────────────────────────┘                      │
│                                                            │
│  Benchmark Tasks: Straight │ One-Turn │ Nav │ Nav-Dynamic  │
└────────────────────────────────────────────────────────────┘
```

CARLA is built as a server-client architecture. The server runs the Unreal Engine 4 simulation (physics, rendering, NPC AI) and the client connects via a Python/C++ API to control the ego vehicle, configure sensors, and retrieve observations.

The simulator provides two towns with varying complexity: Town 1 for training and Town 2 for testing. Each town includes buildings, roads with lane markings, traffic lights, stop signs, and spawn points for vehicles and pedestrians. Weather is parameterized by cloud coverage, precipitation, sun altitude/azimuth, and fog density. NPC vehicles follow predefined autopilot routes with basic collision avoidance.

The benchmark defines four task conditions of increasing difficulty: (1) straight -- drive straight to a goal; (2) one turn -- navigate one intersection; (3) navigation -- follow a multi-waypoint route; (4) navigation dynamic -- same as navigation but with other vehicles and pedestrians. Success is measured by percentage of goal-reaching episodes within a time limit. The three baseline approaches evaluated are: a modular pipeline using semantic segmentation + rule-based planning, conditional imitation learning (CIL) trained on expert demonstrations with high-level commands, and A3C reinforcement learning trained from raw pixels.

## Results

- **Modular pipeline** achieves competitive success rates, similar to imitation learning (often within 10%), using semantic segmentation + rule-based planning. Exhibits brittle failure modes where perception failures cause complete breakdown; performs best at avoiding collisions with cars and static objects.
- **Imitation learning (CIL)** trained on approximately 14 hours of data (80% automated agent, 20% human) achieves comparable performance to the modular pipeline with more graceful degradation under challenging conditions; best at avoiding traffic infractions.
- **Reinforcement learning (A3C)** achieves substantially lower success rates across all tasks compared to both other approaches, trained over approximately 12 days of simulated driving (~10 million steps). Underperformance attributed to algorithm brittleness and task complexity.
- **Weather generalization**: Surprisingly, all three approaches generalize well to unseen weather -- performance in new weather conditions was comparable to or better than performance in training weather.
- **Town/spatial generalization gap**: The critical failure mode is spatial generalization -- success rates dropped by at least 50% on complex navigation tasks when tested in the unseen Town 2 environment, revealing spatial generalization as a fundamental open challenge.

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
