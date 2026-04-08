---
title: "Open Questions: End-to-End Driving"
type: query
status: active
updated: 2026-04-07
tags:
  - questions
  - e2e
  - driving
  - planning
---

# Open Questions: End-to-End Driving

Stream-specific open questions for the end-to-end autonomous driving pillar. See [[wiki/queries/open-questions]] for the full tree across all streams.

## Architectural design

1. **Unified vs. decoupled VLA:** Will [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving|EMMA]]'s "everything as language tokens" or [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving|Senna]]'s decoupled reasoning + planning prove more scalable and deployable? EMMA is simpler; Senna is more interpretable. Neither has been tested at full production scale with safety guarantees.

2. **Parallel vs. sequential task processing:** [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving|DriveTransformer]] parallelizes perception-prediction-planning via shared attention, while [[wiki/sources/papers/planning-oriented-autonomous-driving|UniAD]] processes them sequentially with joint training. Does parallel processing lose important causal structure, or is the efficiency gain worth it?

3. **Intermediate supervision necessity:** Type 3 systems ([[wiki/sources/papers/planning-oriented-autonomous-driving|UniAD]], [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving|VAD]]) use explicit 3D detection/prediction supervision. Type 4 systems ([[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving|EMMA]]) largely do not. Is intermediate supervision a necessary scaffold for safety-certifiable systems, or an unnecessary constraint that limits scaling?

## Planning paradigm

4. **Generative vs. discriminative planning:** [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving|DiffusionDrive]] (diffusion, 45 FPS) and [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation|GoalFlow]] (flow matching) represent multimodal futures natively. [[wiki/sources/papers/vadv2-end-to-end-vectorized-autonomous-driving-via-probabilistic-planning|VADv2]] uses a discrete action vocabulary. [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation|SparseDrive]] uses sparse factorized scoring. Which paradigm best handles the multimodality of real driving?

5. **RL vs. imitation ceiling:** [[wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving|CarPlanner]] is the first RL planner to beat IL+rules on nuPlan. Does this signal a fundamental ceiling in imitation learning for driving, paralleling the LLM trajectory (pretraining → SFT → RLHF)?

6. **Scaling laws for driving:** [[wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving|DriveGPT]] (Waymo) demonstrated LLM-style scaling laws hold for driving behavior models. Do these laws continue to hold, and what is the compute-optimal data-to-parameter ratio for driving?

## Evaluation and deployment

7. **Benchmark adequacy:** Are [[wiki/sources/papers/navsim-data-driven-non-reactive-autonomous-vehicle-simulation|NAVSIM]] and Bench2Drive sufficient for evaluating 2025-era E2E systems? [[wiki/sources/papers/is-ego-status-all-you-need-for-open-loop-end-to-end-autonomous-driving|"Is Ego Status All You Need?"]] exposed fatal flaws in open-loop nuScenes evaluation. Do current closed-loop benchmarks have similar blind spots?

8. **Temporal consistency:** [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving|MomAD]] shows E2E planners produce jittery trajectories. Is momentum-aware planning a sufficient fix, or is temporal inconsistency a deeper architectural problem?

9. **Real-time inference:** Most VLA-based E2E systems exceed real-time latency budgets. [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving|DiMA]]'s approach (discard LLM at inference) and [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving|DiffusionDrive]]'s truncation (20→2 steps) are workarounds. Is there a principled architecture that is both powerful and real-time?

## Partially answered

- **Q4 (Generative planning):** Evidence increasingly favors generative. DiffusionDrive, GoalFlow, and [[wiki/sources/papers/genad-generative-end-to-end-autonomous-driving|GenAD]] all show strong results. VADv2's vocabulary-based approach bridges generative and discriminative.
- **Q5 (RL ceiling):** CarPlanner and the LLM analogy (InstructGPT → DPO → R1) suggest SFT has a ceiling. But driving RL reward design remains much harder than language reward design.
- **Q7 (Benchmarks):** NAVSIM v2 addresses some limitations with pseudo-simulation, but reactive multi-agent evaluation at scale remains unsolved.

## Key papers for this stream

| Paper | Relevance |
|-------|-----------|
| [[wiki/sources/papers/planning-oriented-autonomous-driving]] | UniAD: joint modular E2E reference |
| [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]] | Parallel-task E2E SOTA |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Everything-as-tokens at industry scale |
| [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] | Decoupled reasoning + planning |
| [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] | Real-time diffusion planning |
| [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation]] | Flow matching for trajectories |
| [[wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving]] | First RL planner beating IL+rules |
| [[wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving]] | Scaling laws for driving |
| [[wiki/sources/papers/navsim-data-driven-non-reactive-autonomous-vehicle-simulation]] | Evaluation benchmark |

## Related

- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/planning]]
- [[wiki/queries/open-questions]]
- [[wiki/queries/open-questions-vla]]
