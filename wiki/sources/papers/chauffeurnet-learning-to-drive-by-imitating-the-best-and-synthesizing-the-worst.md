---
title: ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst
type: source-summary
status: seed
updated: 2026-04-11
year: 2019
venue: RSS 2019
tags:
  - paper
  - autonomous-driving
  - imitation-learning
  - planning
citations: 844
paper-faithfullness: audited-fixed
---

# ChauffeurNet: Learning to Drive by Imitating the Best and Synthesizing the Worst

📄 **[Read on arXiv](https://arxiv.org/abs/1812.03079)**

## Citation

Bansal, Krizhevsky, Ogale (Waymo Research), RSS, 2019.

## Canonical link

- [Paper](https://arxiv.org/abs/1812.03079)

## Overview

ChauffeurNet is Waymo's mid-level imitation learning system that learns to drive by combining expert demonstration cloning with synthesized worst-case perturbations. The key insight is that naive behavioral cloning fails because the training distribution only contains good driving -- the model never sees recovery from mistakes, near-collisions, or off-route situations. ChauffeurNet addresses this by augmenting expert logs with synthetically generated perturbations (adding noise to the ego vehicle's position and heading) and training with explicit environment-aware losses (collision loss, on-road loss, geometry loss) in addition to the standard imitation loss.

The system operates on a mid-level representation: rather than consuming raw sensor data, it takes rendered top-down images showing the road map, traffic lights, speed limits, route plan, dynamic objects (from an upstream perception system), and past ego poses. The model outputs a future trajectory as a sequence of waypoints, which a low-level controller then executes. This mid-level approach makes the system robust to perception changes and enables data augmentation that would be impossible with raw sensor inputs.

ChauffeurNet was significant for several reasons. It was one of the first papers from a major autonomous driving company (Waymo) to publish detailed machine learning methodology for real-world driving. The synthesized perturbation approach became widely adopted in subsequent imitation learning work. The paper also clearly articulated the distributional shift problem in behavioral cloning for driving and provided a practical, scalable solution that worked on real vehicles. Its influence extends to later end-to-end systems that adopted similar auxiliary loss designs.

## Key Contributions

- **Synthesized perturbation training**: Augments expert demonstrations by perturbing the ego vehicle's position and heading, then training the model to recover back to the expert trajectory -- directly addressing the distribution shift problem of behavioral cloning
- **Environment-aware auxiliary losses**: Beyond trajectory imitation loss, adds collision loss (penalizing trajectories overlapping with other agents), on-road loss (penalizing off-road predictions), and geometry loss (penalizing trajectories that violate road geometry), making the model environment-aware rather than purely imitative
- **Mid-level input representation**: Uses rendered top-down images combining road map, traffic signals, dynamic agents, route, and ego history rather than raw sensor data, enabling clean data augmentation and decoupling from perception stack changes
- **Past motion dropout**: Randomly drops the ego vehicle's motion history during training, preventing the model from learning a trivial "keep going straight" prior and forcing genuine route-conditioned planning
- **Real-vehicle deployment**: Demonstrated on Waymo's self-driving vehicles in real traffic, validating the approach beyond simulation

## Architecture / Method

```
Input: Top-Down Rendered Images (80m x 80m, ~0.2m/pixel)
┌──────────────────────────────────────────────────────┐
│  Channels: Road Map │ Traffic Lights │ Speed Limits  │
│           Route Plan│ Dynamic Agents │ Ego History   │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   FeatureNet    │
              │   (CNN encoder) │
              └────────┬────────┘
                       │ Spatial Feature Map
                       ▼
              ┌─────────────────────────────────────────┐
              │              AgentRNN                    │
              │                                         │
              │  Step 1: Attend features ──► (x,y,θ)₁   │
              │           │                             │
              │           ▼ Render predicted box         │
              │  Step 2: Attend updated map ──► (x,y,θ)₂│
              │           │                             │
              │           ▼ Render predicted box         │
              │  Step N: Attend updated map ──► (x,y,θ)ₙ│
              └────────────────────┬────────────────────┘
                                   │ Trajectory
                                   ▼
                          ┌─────────────────┐
                          │  Low-Level      │
                          │  Controller     │
                          └─────────────────┘

Training Losses:
┌──────────┐  ┌───────────┐  ┌──────────┐  ┌─────────┐
│ Imitation│  │ Collision │  │ On-Road  │  │Geometry │
│ Loss (L2)│  │ Loss      │  │ Loss     │  │ Loss    │
└─────┬────┘  └─────┬─────┘  └────┬─────┘  └────┬────┘
      └─────────────┼─────────────┼──────────────┘
                    ▼
        Synthesized Perturbations:
        (random shift/rotation of ego)
        ──► Train to recover to expert traj
```

ChauffeurNet takes as input a stack of top-down rendered images at the current and past timesteps. Each image is a multi-channel representation encoding: road map and lanes, traffic light state, speed limit, route plan, bounding boxes of dynamic agents, and ego vehicle's past trajectory. The images cover a region around the ego vehicle (e.g., 80m x 80m) at a resolution of roughly 0.2m/pixel.

The model architecture is a convolutional neural network (FeatureNet) that processes the top-down image stack into spatial features, followed by an AgentRNN that autoregressively predicts future waypoints. At each step, the RNN attends to the spatial features, outputs a waypoint (x, y, heading), renders the predicted agent box onto the feature map, and feeds this updated representation to the next step. This autoregressive rendering allows the model to reason about its own future occupancy when planning subsequent steps.

The training loss is a weighted combination of: (1) imitation loss (L2 distance to expert waypoints), (2) environment losses (collision, on-road, geometry), and (3) a heading loss. Synthesized perturbations are applied during training by randomly shifting and rotating the ego vehicle from its logged position, then training the model to plan a trajectory that recovers to the expert trajectory within a few timesteps. The perturbation magnitude is annealed during training.

## Results

- **Scenario-based closed-loop gains**: The perturbation-trained models substantially outperform imitation-only baselines on the paper's three closed-loop scenario suites: nudging around a parked car, recovering from trajectory perturbations, and slowing for a slower lead vehicle
- **Parked-car avoidance**: In the parked-car scenario, all models except M4 collided roughly half the time, while M4 reduced collisions to 10% and successfully passed the obstacle in 90% of cases
- **Recovery from perturbations**: Models trained with perturbation data recover from lane-offset and heading-error scenarios much more reliably than the no-perturbation baseline, with the stronger variants handling all evaluated deviations in this setup
- **Real-world deployment**: Waymo reports deploying the final model on a self-driving car and replicating the stop-sign handling, turning, and long-duration closed-loop behavior observed in simulation
- **Component ablations matter**: The paper's M0-M4 ablations show that perturbation training, environment losses, and imitation-dropout/reweighting each contribute to the closed-loop improvements

## Limitations & Open Questions

- The mid-level representation depends entirely on upstream perception quality -- perception errors (missed detections, wrong classifications) propagate directly to the planner with no opportunity for the learning system to compensate
- The synthesized perturbations are heuristic (Gaussian noise on position/heading); they may not cover the full space of real failure modes, and more sophisticated adversarial perturbation strategies could be more effective
- The system is purely reactive (no explicit prediction of other agents' future behavior); later work on joint prediction-planning suggests that modeling other agents' responses leads to better interactive driving

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/planning]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]]
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]]
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]]
