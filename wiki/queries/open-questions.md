---
title: Open Questions
type: query
status: active
updated: 2026-04-05
tags:
  - questions
  - agenda
---

# Open Questions

## Priority research questions (original)

1. What is the most defensible taxonomy for "end-to-end" in autonomous driving?
2. Which perception benchmarks correlate best with closed-loop gains?
3. Which prediction architectures materially improve downstream planning instead of just forecasting metrics?
4. How much of robotics VLA progress transfers to road driving without changing the action abstraction?
5. Which LLM/VLM techniques are genuinely architecture-relevant for autonomy, versus useful only for tooling and labeling?
6. Can world-model-style training produce better planners, or does it mostly improve simulation and offline evaluation?

## New questions from AutoVLA corpus

7. **Decoupled vs unified VLA:** Will Senna's approach (separate LVLM reasoning + E2E planning with human-readable bridge) or EMMA's approach (everything as language tokens) prove more scalable and deployable?
8. **RL for driving VLAs:** Can GRPO-style RL (AlphaDrive) scale to production driving the way RLHF scaled for LLMs? What reward functions are sufficient?
9. **Mode averaging in driving:** Is DriveMoE's expert specialization approach the right solution, or will larger models with better training overcome mode averaging without explicit MoE?
10. **World model role:** Is WoTE's pattern (VLA generates candidates, world model verifies safety) the right decomposition, or should world models be integrated into the planning loop?
11. **Language role at maturity:** As driving VLAs improve, does language remain as intermediate reasoning (Senna, ORION), get absorbed into dense embeddings, or evolve into something else?
12. **Benchmark adequacy:** Are Bench2Drive and NAVSIM sufficient for evaluating 2025-era VLAs, or do we need new evaluation paradigms for RL-trained and world-model-augmented systems?
13. **Production gap:** Alpamayo-R1 is the only paper claiming real-world deployment — what are the missing pieces for other architectures?
14. **Geographic generalization:** DriveMLM/LLaDA raises whether LLM-based rule adaptation can handle traffic law differences across regions — is this a solved problem or a fundamental challenge?
15. **Human-vehicle interaction:** Drive as You Speak highlights that LLMs can serve as passenger interfaces, not just planners — should production AV stacks separate the "interaction LLM" from the "planning LLM/VLA," or can a single model serve both roles safely?

## Partially answered by AutoVLA evidence

- **Q4 (Robotics VLA transfer to driving):** VoxPoser ([[wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models]]) demonstrates that LLMs can compose spatial objectives for manipulation without any robot-specific training. The "LLM writes code to define value maps" paradigm is an alternative to end-to-end VLAs, but whether 3D value map composition transfers to the higher-speed, multi-agent driving domain is untested.
- **Q5 (LLM/VLM architecture relevance):** Evidence is mixed. Language as intermediate reasoning (Senna, ORION, DriveLM) appears genuinely architecture-relevant. Language as action output (EMMA) works at Waymo scale. Language for explanation only (DriveGPT4) appears less architecturally important. VoxPoser adds a new mode: language as code generation for spatial objective composition, which avoids task-specific training entirely.
- **Q6 (World models):** WoTE suggests world models are most valuable as safety verification layers, complementing VLA planners rather than replacing them. Not yet clear if world-model training improves the VLA planner itself.
- **Q9 (Mode averaging in driving):** VADv2 ([[wiki/sources/papers/vadv2-end-to-end-vectorized-autonomous-driving-via-probabilistic-planning]]) provides strong evidence that explicit multimodal planning (via a discrete action vocabulary) significantly outperforms deterministic single-trajectory planners in closed-loop. This complements DriveMoE's MoE approach with a simpler vocabulary-based alternative and suggests mode averaging is a real problem requiring architectural solutions, not just larger models.
