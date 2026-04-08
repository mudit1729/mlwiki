---
title: "Open Questions: LLM Reasoning for Autonomy"
type: query
status: active
updated: 2026-04-07
tags:
  - questions
  - llm
  - reasoning
  - planning
  - driving
---

# Open Questions: LLM Reasoning for Autonomy

Stream-specific open questions for LLM reasoning applied to driving and robotics. See [[wiki/queries/open-questions]] for the full tree across all streams.

## Language role in autonomy

1. **Language at maturity:** As driving VLAs improve, does language remain as intermediate reasoning ([[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving|Senna]], [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation|ORION]]), get absorbed into dense embeddings, or evolve into something else? [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving|DiMA]]'s strategy of distilling then discarding the LLM suggests language may be a training-time tool, not a runtime necessity.

2. **Reasoning vs. planning:** [[wiki/sources/papers/llms-cant-plan-but-can-help-planning-in-llm-modulo-frameworks|"LLMs Can't Plan"]] (ICML 2024, 200+ citations) argues LLMs should reason, not plan — they need external model-based verifiers. Is this distinction fundamental, or will larger models with better training overcome planning limitations?

3. **Chain-of-thought overhead:** [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models|ECoT]] gets +28% success from embodied CoT, but at inference cost. [[wiki/sources/papers/tree-of-thoughts-deliberate-problem-solving-with-large-language-models|Tree of Thoughts]] showed that deliberate multi-path exploration dramatically improves complex problem solving. Is CoT essential for safety-critical decisions, or can its benefits be distilled into faster models (as [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning|DeepSeek-R1]] distills to 1.5B)?

4. **Structured vs. free-form reasoning:** [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering|DriveLM]]'s Graph VQA imposes structure (perception→prediction→planning). [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving|Reason2Drive]] uses chain-based decomposition. Free-form CoT is more flexible. Which level of structure optimizes the reasoning-accuracy trade-off for driving?

## RL and reasoning emergence

5. **RL-emergent reasoning for driving:** [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning|DeepSeek-R1]] showed CoT emerges from RL with rule-based rewards in math/code. [[wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving|Alpamayo-R1]] applies RL to driving reasoning. Can driving produce sufficiently clean reward signals for RL-emergent reasoning, or is the reward specification problem fundamentally harder than math verification?

6. **Reward function design:** Math and code have verifiable correctness signals. Driving has safety (no collision), comfort (smooth ride), progress (reach goal), and efficiency (minimize time). Are these sufficient for GRPO-style RL, or does driving need learned reward models?

## Cognitive architecture

7. **Dual-process reasoning:** [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving|AutoVLA]] dynamically switches between fast (direct action) and slow (CoT) reasoning. How should the system decide when to think deeply? Is complexity estimation itself a learnable skill?

8. **LLM as interface vs. core:** [[wiki/sources/papers/drive-as-you-speak-enabling-human-like-interaction-with-large-language-models-in-autonomous-vehicles|Drive as You Speak]] uses LLMs as passenger interfaces. Should production AV stacks separate the "interaction LLM" from the "planning LLM/VLA," or can a single model serve both roles safely?

9. **Agent frameworks at scale:** [[wiki/sources/papers/a-language-agent-for-autonomous-driving|Agent-Driver]] established the LLM-as-agent framework with tool use and memory. [[wiki/sources/papers/asyncdriver-asynchronous-large-language-model-enhanced-planner-for-autonomous-driving|AsyncDriver]] decouples LLM reasoning from real-time planning via async updates. Is the agent framework (tools + memory + reasoning) the right paradigm for autonomous driving, or is it too slow for safety-critical real-time control?

## Partially answered

- **Q2 (Reasoning vs. planning):** Evidence from "LLMs Can't Plan" and the success of VLA + world-model-verifier architectures ([[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model|WoTE]]) supports the distinction. But [[wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving|DriveGPT]]'s scaling laws suggest that with enough data, autoregressive prediction may subsume explicit planning.
- **Q3 (CoT overhead):** DeepSeek-R1's distillation to 1.5B models shows reasoning can be compressed. DiMA's distill-and-discard approach is the driving analog.
- **Q7 (Dual-process):** AutoVLA's dual-process approach is promising. [[wiki/sources/papers/qwen3-technical-report|Qwen3]]'s unified thinking mode (same model dynamically chooses deep vs. quick thinking) may be the foundation model analog.

## Key papers for this stream

| Paper | Relevance |
|-------|-----------|
| [[wiki/sources/papers/llms-cant-plan-but-can-help-planning-in-llm-modulo-frameworks]] | LLMs should reason, not plan |
| [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] | Original CoT for reasoning |
| [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning]] | RL-emergent reasoning |
| [[wiki/sources/papers/tree-of-thoughts-deliberate-problem-solving-with-large-language-models]] | Multi-path deliberate reasoning |
| [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models]] | Embodied CoT for VLAs |
| [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] | Structured graph reasoning |
| [[wiki/sources/papers/a-language-agent-for-autonomous-driving]] | LLM-as-agent for driving |
| [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] | Language as intermediate reasoning |
| [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] | Distill and discard LLM |
| [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]] | Dual-process adaptive reasoning |

## Related

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/planning]]
- [[wiki/queries/open-questions]]
- [[wiki/queries/open-questions-e2e]]
