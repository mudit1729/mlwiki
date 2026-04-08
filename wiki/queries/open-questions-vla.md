---
title: "Open Questions: Vision-Language-Action Models"
type: query
status: active
updated: 2026-04-07
tags:
  - questions
  - vla
  - robotics
  - driving
---

# Open Questions: Vision-Language-Action Models

Stream-specific open questions for the VLA pillar. See [[wiki/queries/open-questions]] for the full tree across all streams.

## Architecture and scaling

1. **Dual-system generality:** The dual-system pattern (slow VLM at 7-10 Hz + fast motor policy at 120-200 Hz) independently emerged at Physical Intelligence ([[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control|pi0]]), Google DeepMind ([[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world|Gemini Robotics]]), NVIDIA ([[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots|GR00T N1]]), and Figure AI ([[wiki/sources/papers/helix-a-vla-for-generalist-humanoid-control|Helix]]). Is this the converged architecture, or will single-rate systems eventually dominate?

2. **Cross-embodiment scaling limits:** [[wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation|CrossFormer]] trains one policy across 20+ embodiments. [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers|HPT]] shows scaling laws for heterogeneous robot pretraining. But do these scaling laws hold across dramatically different action spaces (manipulation vs. driving vs. locomotion), or do they plateau?

3. **Action tokenization:** [[wiki/sources/papers/fast-efficient-action-tokenization-for-vision-language-action-models|FAST]]'s DCT+BPE achieves 5x faster VLA training. [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control|pi0]] uses flow matching for continuous actions. [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving|EMMA]] tokenizes trajectories as language. What is the right action representation — continuous, discrete vocabulary, or hybrid?

4. **VLM knowledge preservation:** [[wiki/sources/papers/knowledge-insulating-vision-language-action-models|Knowledge Insulation]] shows VLA training degrades VLM capabilities. How much VLM knowledge is actually needed for embodied control, and what is the optimal trade-off between language understanding and motor competence?

## Training and improvement

5. **RL for VLAs:** [[wiki/sources/papers/pi06-a-vla-that-learns-from-experience|pi0.6]] doubled task throughput via offline RL self-improvement. [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning|DeepSeek-R1]] showed RL with rule-based rewards produces emergent reasoning. Can driving VLAs benefit from GRPO-style RL, or does the lack of clean reward functions (unlike math/code) make this fundamentally harder?

6. **Embodied chain-of-thought:** [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models|ECoT]] increased VLA success by 28% through embodied reasoning. Does chain-of-thought reasoning scale to 50+ Hz control, or is it inherently a slow-system capability?

7. **Open-world generalization:** [[wiki/sources/papers/pi05-a-vision-language-action-model-with-open-world-generalization|pi0.5]] generalizes to unseen homes for 10-15 minute tasks. What is the failure mode — perception (novel objects), reasoning (novel situations), or motor control (novel physical interactions)?

## Robotics → driving transfer

8. **VLA transfer to driving:** [[wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models|VoxPoser]] demonstrates LLMs can compose spatial objectives for manipulation without robot-specific training. The "LLM writes code to define value maps" paradigm works for tabletop manipulation — does it transfer to high-speed multi-agent driving?

9. **Action abstraction gap:** Robotics VLAs operate on joint angles/end-effector poses. Driving VLAs operate on trajectories/waypoints/controls. How much of VLA progress transfers when the action abstraction is fundamentally different?

10. **Speed regime mismatch:** Robotics VLAs can recover from errors at low speed. Driving at 60+ mph leaves no recovery margin. Does this fundamentally change the architecture requirements, or is it just a latency constraint?

## Partially answered

- **Q1 (Dual-system):** Four independent convergences strongly suggest this is the right architecture for now. But single-rate 50 Hz models (pi0 flow matching) show the boundary is soft.
- **Q5 (RL for VLAs):** pi0.6 proves offline RL works for manipulation. AlphaDrive applies GRPO to driving VLMs. But reward design for driving safety/comfort remains the bottleneck.
- **Q8 (VoxPoser transfer):** 3D value map composition is an alternative to E2E VLAs, avoiding task-specific training entirely. Whether it scales to driving's complexity and speed is untested.

## Key papers for this stream

| Paper | Relevance |
|-------|-----------|
| [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control]] | Reference VLA: flow matching, 7 robots, 68 tasks |
| [[wiki/sources/papers/pi06-a-vla-that-learns-from-experience]] | RL self-improvement for VLAs |
| [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] | Open-source VLA baseline |
| [[wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation]] | Cross-embodiment scaling |
| [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]] | Heterogeneous pretraining scaling laws |
| [[wiki/sources/papers/octo-an-open-source-generalist-robot-policy]] | First open generalist robot policy |
| [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models]] | Embodied chain-of-thought |
| [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]] | Humanoid foundation model |
| [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]] | Gemini for physical robotics |
| [[wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models]] | LLM-composed spatial objectives |

## Related

- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/vla-and-driving]]
- [[wiki/queries/open-questions]]
- [[wiki/queries/open-questions-e2e]]
