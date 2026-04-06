---
title: Vision Language Action
type: concept
status: active
updated: 2026-04-05
tags:
  - vla
  - vlm
  - multimodal
---

# Vision Language Action

This page tracks the bridge from multimodal understanding to action generation, informed by the AutoVLA corpus of 18 papers spanning 2018–2025.

## Working definition

A VLA system consumes visual context and language-conditioned intent, then emits actions or action-relevant latent state. In robotics, actions may be motor commands or low-level policies. In driving, actions may be trajectories, waypoints, controls, or planner tokens.

## Important distinctions

- **VLM vs VLA:** understanding-only systems are not action models. A VLM that describes a driving scene is not the same as a VLA that outputs a trajectory.
- **Language as supervision vs language as runtime interface:** CIL uses discrete commands at runtime; BDD-X uses language only during training; LMDrive uses language at runtime; DriveLM uses it for structured reasoning.
- **Action tokens vs continuous controls:** EMMA tokenizes everything including trajectories; Senna decouples language reasoning from continuous E2E planning.
- **Offline imitation vs interactive control:** Open-loop evaluation (GPT-Driver, DriveGPT4) vs closed-loop (LMDrive, SimLingo, ORION).

## Three waves of driving VLA (from AutoVLA analysis)

### Wave 1: Foundations (2018–2019)
- **Conditional Imitation Learning** established intent-conditioned driving with a 4-word vocabulary
- **BDD-X** introduced language-action alignment through attention-based explanations
- **Talk2Car** grounded free-form language to objects in driving scenes

### Wave 2: LLM-as-Planner (2023–2024)
- Explosion of LLM/VLM applications to driving
- Key tension: language for planning (GPT-Driver) vs language for explanation (DriveGPT4) vs language for structured reasoning (DriveLM)
- Critical finding: **open-loop evaluation is insufficient** — LMDrive demonstrated closed-loop is essential

### Wave 3: Reasoning-to-Action (2025)
- Focus shifts to bridging the reasoning-action gap
- **RL enters the picture:** AlphaDrive applies GRPO-based RL (DeepSeek R1-style) to driving VLMs
- **World models complement VLAs:** WoTE uses BEV world models for trajectory safety verification
- **MoE architectures:** DriveMoE addresses mode averaging through expert specialization
- **Production deployment:** Alpamayo-R1 achieves 99ms latency with real road testing
- **Adaptive reasoning:** AutoVLA introduces dual-process thinking (fast/slow) for driving VLAs with RL fine-tuning
- **3D-grounded VLA:** OpenDriveVLA integrates hierarchical 3D queries into LLM, achieves SOTA at 0.5B scale
- **Distillation as deployment strategy:** DiMA jointly trains MLLM + vision planner, discards MLLM at inference (80% collision reduction, zero overhead)

## Key design axes

| Axis | Options | Key papers |
|------|---------|------------|
| Language role | Supervision / runtime control / explanation | BDD-X / LMDrive / DriveGPT4 |
| Action space | Controls / waypoints / planner tokens / language tokens | CIL / VAD / ORION / EMMA |
| Architecture | VLM + planner / true VLA / decoupled | DriveGPT4 / SimLingo / Senna |
| Evaluation | Open-loop / closed-loop sim / real-world | GPT-Driver / LMDrive / Alpamayo-R1 |
| Training | IL / IL+RL / GRPO / multi-stage | CIL / Alpamayo-R1 / AlphaDrive / ORION |

## Emerging consensus (as of 2025)

1. **Closed-loop evaluation is non-negotiable** for driving VLAs — open-loop metrics don't predict driving competence
2. **Language is most valuable as intermediate reasoning**, not as the action output itself (Senna's human-readable bridge, ORION's planning token)
3. **RL is the next frontier** — SFT ceiling appears real; AlphaDrive and Alpamayo-R1 both use RL to push beyond imitation
4. **World models and VLAs are complementary**, not competing — WoTE shows physics-based verification can catch VLA failures
5. **MoE architectures** address the fundamental mode-averaging problem in diverse driving scenarios

## Robotics VLA frontier (2025)

The VLA paradigm continues to push boundaries in robotics:

- **Video Prediction Policy** ([[wiki/sources/papers/video-prediction-policy-a-generalist-robot-policy-with-predictive-visual-representations]], ICML 2025 Spotlight) reinterprets video diffusion models as predictive visual encoders rather than generators, achieving 18.6% improvement on CALVIN by extracting future-encoding representations from a single VDM forward pass.
- **Helix** ([[wiki/sources/papers/helix-a-vla-for-generalist-humanoid-control]], Figure AI 2025) is the first VLA to control an entire humanoid upper body (35 DoF) at 200 Hz via a dual-system architecture: a 7B VLM (System 2, 7-9 Hz) feeds latent representations to an 80M visuomotor policy (System 1, 200 Hz). It demonstrates dual-robot coordination on shared long-horizon tasks.

## Driving-specific open questions

- Does language add supervision, controllability, interpretability, or only presentation value?
- Can VLA-style pretraining reduce the amount of task-specific driving data needed?
- What is the right action abstraction for driving: controls, trajectories, anchors, or planner state?
- Will the decoupled approach (Senna: separate reasoning + planning) or unified approach (EMMA: everything as tokens) win?
- Can GRPO-style RL scale to production driving the way it scaled for LLM reasoning?

## Related

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/planning]]
- [[wiki/sources/vla-and-driving]]
- [[wiki/comparisons/modular-vs-end-to-end]]
