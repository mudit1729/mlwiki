---
title: "Helix: A Vision-Language-Action Model for Generalist Humanoid Control"
type: source-summary
status: complete
updated: 2026-04-05
year: 2025
venue: Figure AI Technical Report
tags:
  - paper
  - robotics
  - vla
  - humanoid
  - high-frequency-control
citations: 0
arxiv_id: null
paper-faithfullness: audited-solid
---

# Helix: A Vision-Language-Action Model for Generalist Humanoid Control

:page_facing_up: **[Read at Figure AI](https://www.figure.ai/news/helix)**

## Overview

Helix (Figure AI, Technical Report February 2025) is the first vision-language-action model to achieve high-rate continuous control of an entire humanoid upper body, including wrists, torso, head, and individual fingers across 35 degrees of freedom. The core innovation is a dual-system "System 1, System 2" architecture that separates high-level semantic reasoning (slow, expressive VLM) from low-level motor control (fast, lightweight visuomotor policy).

System 2 is a 7-billion-parameter Vision-Language Model (VLM) that runs at 7-9 Hz, handling scene understanding, language comprehension, and task-level planning. System 1 is an 80-million-parameter visuomotor policy that translates System 2's latent semantic representations into precise continuous actions at 200 Hz. This separation allows Helix to combine the broad generalization and language understanding of VLMs with the fast reactive control needed for dexterous manipulation.

Helix is the first VLA to simultaneously operate two humanoid robots for shared long-horizon manipulation tasks with novel objects, and runs entirely onboard embedded low-power GPUs, making it deployment-ready.

## Key Contributions

- **Dual-system VLA architecture (System 1 + System 2)**: Separates slow semantic reasoning (7B VLM at 7-9 Hz) from fast motor control (80M policy at 200 Hz), achieving both broad generalization and precise dexterous control
- **First whole-body humanoid VLA**: Controls 35 DoF including individual fingers, wrists, torso, and head -- far beyond prior VLAs that controlled only 6-7 DoF robot arms
- **Dual-robot coordination**: First VLA to simultaneously control two humanoid robots solving a shared manipulation task
- **Auto-labeled training data**: Collects ~500 hours of multi-robot multi-operator teleoperated data, using a VLM to generate hindsight language instruction labels automatically
- **Onboard deployment**: Runs entirely on embedded low-power GPUs, enabling commercial deployment

## Architecture / Method

```
┌──────────────────────────────────────────────────────────────┐
│                  HELIX DUAL-SYSTEM VLA                        │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐           │
│  │ Camera 1  │  │ Camera 2 │  │ Language          │           │
│  │ (head)    │  │ (wrist)  │  │ Instruction       │           │
│  └────┬──────┘  └────┬─────┘  └───────┬──────────┘           │
│       │              │                │                       │
│       ▼              ▼                ▼                       │
│  ┌──────────────────────────────────────────────┐            │
│  │        System 2 — Slow Brain (7-9 Hz)        │            │
│  │        7B Vision-Language Model               │            │
│  │  ┌──────────────────────────────────────┐    │            │
│  │  │ Scene Understanding + Language Ground.│    │            │
│  │  │ Task Planning + Subtask Sequencing    │    │            │
│  │  └──────────────────────────────────────┘    │            │
│  └─────────────────────┬────────────────────────┘            │
│                        │ Latent Semantic                      │
│                        │ Representations                      │
│                        ▼                                      │
│  ┌──────────────────────────────────────────────┐            │
│  │        System 1 — Fast Brain (200 Hz)        │            │
│  │        80M Visuomotor Policy                  │            │
│  │  ┌──────────────────────────────────────┐    │            │
│  │  │ Continuous Joint Actions (35 DoF)     │    │            │
│  │  │ Fingers + Wrists + Torso + Head       │    │            │
│  │  └──────────────────────────────────────┘    │            │
│  └─────────────────────┬────────────────────────┘            │
│                        │                                      │
│                        ▼                                      │
│              ┌──────────────────┐                             │
│              │  Joint Commands   │                             │
│              │  (5ms per action) │                             │
│              └──────────────────┘                             │
└──────────────────────────────────────────────────────────────┘
```

The architecture is organized around two interacting systems:

**System 2 (Slow Brain):** A 7-billion-parameter VLM pre-trained on internet-scale vision-language data. Takes multi-camera images and natural language instructions as input. Produces rich latent semantic representations that encode the current scene state, object identities, spatial relationships, and task progress. Operates at 7-9 Hz due to computational cost.

System 2 provides:
- Scene understanding (what objects are present, their properties)
- Language grounding (mapping instructions to visual referents)
- Task-level planning (what subtask to execute next)
- Contextual embeddings passed to System 1

**System 1 (Fast Brain):** An 80-million-parameter visuomotor policy that takes System 2's latent representations plus raw visual input and produces continuous joint-level actions at 200 Hz. This high control frequency is essential for dexterous manipulation -- grasping, reorienting, and placing objects requires sub-10ms reactive control.

System 1 provides:
- Fast reactive motor control (200 Hz, 5ms per action)
- Continuous action output across all 35 DoF
- Fine-grained force modulation for dexterous tasks
- Compliance and safety through high-rate feedback

**Training Data Pipeline:** A high-quality dataset of ~500 hours of diverse teleoperated behaviors is collected using multiple robots and multiple human operators. An auto-labeling VLM generates hindsight natural language instructions for each demonstration, creating language-conditioned training pairs without manual annotation.

**Dual-Robot Operation:** For multi-robot tasks, each robot has its own System 1 + System 2 stack, but they share task-level context through language instructions describing the joint task. The robots do not directly communicate actions but coordinate through shared semantic understanding.

## Results

Helix demonstrates several qualitative capabilities that represent firsts for VLA models:

- **Dexterous manipulation**: Picks up, reorients, and places diverse objects using individual finger control
- **Novel object generalization**: Manipulates objects never seen during training, leveraging VLM pre-training for zero-shot recognition
- **Long-horizon tasks**: Completes multi-step manipulation sequences requiring task switching and error recovery
- **Dual-robot coordination**: Two Figure 02 robots collaboratively solve tasks (e.g., handoff objects) guided by shared language instructions
- **Real-time onboard**: All computation runs on the robot's embedded GPUs, with no cloud dependence

No standardized benchmark results are reported in the technical report; evaluation is primarily through real-world task demonstrations.

## Limitations

- No standardized benchmark evaluation (e.g., CALVIN, MetaWorld), making quantitative comparison with other VLAs difficult
- System 2 VLM operates at only 7-9 Hz, creating potential latency in responding to novel situations
- The ~500-hour training dataset is proprietary and specific to Figure's robots, limiting reproducibility
- Dual-robot coordination relies on shared language context rather than explicit communication, which may not scale to more complex multi-agent scenarios
- Lower-body locomotion is not addressed; Helix controls only the upper body

## Connections

- Directly extends the VLA paradigm from [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] to humanoid scale
- The System 1/System 2 architecture echoes the dual-system design in [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]] (GR00T N1), which also separates high-level reasoning from fast motor control
- Shares the VLM backbone approach of [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]] (Gemini Robotics) but targets humanoid rather than general manipulation
- Auto-labeled training data connects to the approach of [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] which trains on diverse robot data
- The video-diffusion approach of [[wiki/sources/papers/video-prediction-policy-a-generalist-robot-policy-with-predictive-visual-representations]] (VPP) offers an alternative to Helix's VLM-based backbone
- High-frequency control requirements connect to the adaptive reasoning in driving VLAs like [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]]
