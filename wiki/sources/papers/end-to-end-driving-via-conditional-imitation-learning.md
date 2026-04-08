---
title: End-to-end Driving via Conditional Imitation Learning
type: source-summary
status: complete
updated: 2026-04-05
year: 2018
venue: ICRA
tags:
  - paper
  - autonomous-driving
  - imitation-learning
  - e2e
  - vla
citations: 1227
---

# End-to-end Driving via Conditional Imitation Learning

📄 **[Read on arXiv](https://arxiv.org/abs/1710.02410)**

## Overview

This paper introduces conditional imitation learning for end-to-end autonomous driving, where a neural network policy is conditioned on a discrete high-level command (turn left, turn right, go straight, follow lane) to resolve the fundamental multimodal action ambiguity at intersections. The same visual scene at an intersection can correspond to three or more correct actions depending on navigation intent, and without conditioning on intent, a learned policy will average these modes and produce erratic or incorrect behavior.

The key insight is that perception alone is insufficient for determining the correct action at decision points. By adding a high-level command input, the policy becomes controllable and responsive to navigation intent. The paper introduces a branched architecture with separate fully-connected heads per command, gated by command selection, which outperforms the naive approach of concatenating the command with visual features. This conditional policy formulation -- pi(a | o, c) = f_c(g(o)) -- became a foundational design pattern for the field.

This paper is foundational for the entire VLA driving research trajectory. The branched command-conditioned architecture became a durable design pattern that persists in modern VLA models, with the discrete four-word command vocabulary simply replaced by natural language instructions. The progression from CIL's discrete commands to LMDrive's natural language to EMMA's full prompt-driven interface is a direct evolutionary line, making this paper the proto-VLA for autonomous driving.

## Key Contributions

- **Branched command-conditioned architecture:** Separate FC heads per high-level command (left/right/straight/follow), gated by command selection, outperforms naive command-input concatenation
- **Conditional policy formulation:** pi(a | o, c) = f_c(g(o)), where the CNN encoder g produces features and command-specific head f_c produces controls -- the first clean formalization of intent-conditioned driving
- **Data augmentation with noise injection** to handle the distribution shift problem inherent to imitation learning, where the policy encounters states not seen during expert demonstration
- **Dual validation in simulation and real world:** Evaluated in CARLA simulator and on a physical 1/5-scale truck in residential environments
- **Identification of the multimodal output problem:** Clearly demonstrated that identical visual inputs at intersections cause oscillation and wrong turns without intent conditioning

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────────┐
│           Branched Conditional Imitation Learning                 │
│                                                                 │
│  ┌───────────────┐                                              │
│  │ Front Camera  │                                              │
│  │   Image       │                                              │
│  └───────┬───────┘                                              │
│          ▼                                                      │
│  ┌───────────────┐                                              │
│  │   CNN Encoder │                                              │
│  │   g(o)        │                                              │
│  │  (Conv layers │                                              │
│  │   + FC)       │                                              │
│  └───────┬───────┘                                              │
│          │ feature vector                                       │
│          │                                                      │
│          ├───────────────┬───────────────┬───────────────┐      │
│          ▼               ▼               ▼               ▼      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐ │
│  │ f_left      │ │ f_right     │ │ f_straight  │ │ f_follow │ │
│  │ Turn Left   │ │ Turn Right  │ │ Go Straight │ │ Follow   │ │
│  │ FC Head     │ │ FC Head     │ │ FC Head     │ │ Lane     │ │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └────┬─────┘ │
│         │               │               │              │       │
│         └───────┬───────┴───────┬───────┘              │       │
│                 │               │                       │       │
│                 ▼               ▼                              │
│          ┌─────────────────────────────┐                       │
│          │  Command Selector (c)       │                       │
│          │  Activates one branch       │◄── High-level command │
│          └────────────┬────────────────┘    from navigator     │
│                       ▼                                        │
│              ┌─────────────────┐                               │
│              │ Steering, Accel │                               │
│              │    Output       │                               │
│              └─────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

![Conditional imitation learning setup: controller receiving observations and commands to produce actions](https://paper-assets.alphaxiv.org/figures/1710.02410v2/img-1.jpeg)

![Two network architectures: Command Input and Branched architecture for incorporating command information](https://paper-assets.alphaxiv.org/figures/1710.02410v2/img-2.jpeg)

The architecture consists of two main components: a perception module and a set of command-conditional control modules. The perception module is a convolutional neural network (based on a modified ResNet or similar backbone) that takes a single front-facing camera image and produces a feature vector g(o) encoding the visual scene.

The control module uses a branched design. Rather than a single output head, there are separate fully-connected network branches for each high-level command: turn left, turn right, go straight, and follow lane. At inference time, the navigation system provides the current command c, and only the corresponding branch f_c is activated to produce the control output (steering angle and throttle/brake). This branching allows each command-specific head to specialize in the action distribution for that maneuver type, avoiding the averaging problem that occurs when all maneuvers share parameters.

The paper compares this branched architecture against two alternatives: (1) an unconditional model with no command input, which must handle all maneuvers with a single output head, and (2) a command-input model that concatenates a one-hot command encoding with the visual features before a shared output head. The branched design outperforms both.

Training uses standard behavioral cloning on expert demonstrations from CARLA, with two key augmentation strategies. First, viewpoint perturbation: cameras are placed at offset positions during data collection, with labels adjusted to steer back toward the center, creating recovery examples. Second, noise injection: small random perturbations are applied to the expert's controls during data collection, creating slightly off-policy states that the model learns to correct from.

## Results

![CARLA simulator environments: Town 1 (training) and Town 2 (testing)](https://paper-assets.alphaxiv.org/figures/1710.02410v2/img-4.jpeg)

### CARLA Simulator Performance

| Method | Town 1 Success | Town 2 Success |
|---|---|---|
| Branched conditional model | 88% | 64% |
| Command input architecture | 78% | 52% |
| Non-conditional baseline | 20% | 26% |

### Physical Robot Tests

| Configuration | Missed Turns | Human Interventions/Run |
|---|---|---|
| Branched model | 0% | 0.67 |
| Without noise injection | 24.4% | 8.67 |
| Without data augmentation | 73% | 39 |

- Conditional model significantly outperforms unconditional baselines at intersections in CARLA simulation, resolving the oscillation and wrong-turn failure modes that plague unconditional policies
- Branched architecture outperforms command-input architecture: separate heads per command allow each branch to specialize in one maneuver type, yielding cleaner action predictions with higher success rates
- Real-world transfer demonstrated: successfully trained a 1/5-scale truck to drive in residential environments following high-level commands, showing the approach is not limited to simulation
- Noise injection mitigates distribution shift: adding perturbation noise during training substantially improves robustness during autonomous execution, with the model learning to recover from small deviations
- Ablation studies confirm that both the branched architecture and noise injection are independently important, with their combination providing the best performance

## Limitations & Open Questions

- The "language" interface is a predefined 4-word vocabulary, not free-form natural language -- the gap from discrete commands to natural language instructions remained open for years
- Inherits fundamental imitation learning distribution shift and generalization issues despite noise injection -- compounding errors in long-horizon driving remain problematic
- No reasoning or explanation capability -- the policy is a black box that maps (image, command) to controls, providing no interpretability

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/papers/end-to-end-learning-for-self-driving-cars]]
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]]
- [[wiki/sources/papers/simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment]]
- [[wiki/sources/papers/learning-by-cheating]]
