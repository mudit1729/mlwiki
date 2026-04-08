---
title: "Open Questions: Foundation Models & Cross-Embodiment"
type: query
status: active
updated: 2026-04-07
tags:
  - questions
  - foundation-models
  - scaling
  - cross-embodiment
---

# Open Questions: Foundation Models & Cross-Embodiment

Stream-specific open questions for foundation models, scaling, and cross-embodiment transfer. See [[wiki/queries/open-questions]] for the full tree across all streams.

## Scaling and efficiency

1. **Compute-optimal scaling for embodied AI:** [[wiki/sources/papers/scaling-laws-for-neural-language-models|Kaplan scaling laws]] and [[wiki/sources/papers/training-compute-optimal-large-language-models|Chinchilla]] established compute-optimal ratios for language. [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers|HPT]] shows scaling laws for robot pretraining. But do these laws hold for multimodal embodied data (images + proprioception + actions), or does the data mixture change the optimal ratio?

2. **Open vs. closed model trajectory:** [[wiki/sources/papers/llama-2-open-foundation-and-fine-tuned-chat-models|Llama 2]], [[wiki/sources/papers/mistral-7b|Mistral 7B]], [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model|OpenVLA]], and [[wiki/sources/papers/octo-an-open-source-generalist-robot-policy|Octo]] catalyzed more downstream work than closed counterparts. [[wiki/sources/papers/qwen3-technical-report|Qwen3]] and [[wiki/sources/papers/gemma-3-technical-report|Gemma 3]] now match frontier closed models. Will open-source maintain this acceleration, or will proprietary data advantages (Waymo driving logs, Tesla fleet data) create an insurmountable moat for driving?

3. **Adaptation efficiency:** [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models|LoRA]] (29K citations) and [[wiki/sources/papers/qlora-efficient-finetuning-of-quantized-language-models|QLoRA]] made efficient adaptation standard. [[wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation|Prefix-Tuning]] pioneered continuous prompt optimization. Is parameter-efficient fine-tuning sufficient for embodied domains, or do physical tasks require more extensive adaptation than language tasks?

4. **Distillation as deployment strategy:** [[wiki/sources/papers/gemma-3-technical-report|Gemma 3]]'s 4B matches prior-generation 27B via distillation. [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning|DeepSeek-R1]] distills reasoning to 1.5B. [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving|DiMA]] distills LLM reasoning into a vision planner. Is train-large-distill-small the universal deployment pattern for safety-critical systems?

## Cross-embodiment transfer

5. **Embodiment scaling laws:** [[wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation|CrossFormer]] (20+ embodiments) and [[wiki/sources/papers/embodiment-scaling-laws-in-robot-locomotion|embodiment scaling laws]] show returns from embodiment diversity. Is there an optimal diversity-depth trade-off — how many embodiments vs. how much data per embodiment?

6. **Action space universality:** [[wiki/sources/papers/uniact-universal-actions-for-enhanced-embodied-foundation-models|UniAct]] proposes universal action representations. [[wiki/sources/papers/fast-efficient-action-tokenization-for-vision-language-action-models|FAST]] introduces DCT+BPE tokenization. Can a single action representation truly span manipulation, navigation, locomotion, and driving, or are domain-specific action spaces necessary?

7. **World model as universal simulator:** [[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai|Cosmos]] and [[wiki/sources/papers/unisim-learning-interactive-real-world-simulators|UniSim]] train world models on internet-scale video for physical AI simulation. Can learned world models replace engineered simulators for training embodied agents, or do they introduce systematic biases?

## Multimodal reasoning

8. **Vision-language alignment quality:** [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision|CLIP]] (58K citations) established contrastive vision-language alignment. [[wiki/sources/papers/visual-instruction-tuning|LLaVA]] (13K+ citations) added instruction tuning. [[wiki/sources/papers/blip-bootstrapping-language-image-pre-training-for-unified-vision-language-understanding-and-generation|BLIP]] unified understanding + generation. Is current VL alignment sufficient for safety-critical spatial reasoning, or is there a fundamental "grounding gap" between CLIP-style alignment and true 3D spatial understanding?

9. **Emergent capabilities and risks:** [[wiki/sources/papers/on-the-opportunities-and-risks-of-foundation-models|The Foundation Models report]] warned about emergence and homogenization risks. [[wiki/sources/papers/gpt-4-technical-report|GPT-4]] demonstrated surprising emergent capabilities. As driving models scale, will we see emergent driving capabilities (handling novel scenarios) or emergent failures (systematic blind spots)?

10. **Alignment for physical systems:** [[wiki/sources/papers/training-language-models-to-follow-instructions-with-human-feedback|InstructGPT]] and [[wiki/sources/papers/direct-preference-optimization-your-language-model-is-secretly-a-reward-model|DPO]] align LLMs to human preferences. Driving alignment requires physical safety guarantees. Can RLHF/DPO techniques transfer to physical AI, or do we need fundamentally new alignment methods?

## Partially answered

- **Q2 (Open vs. closed):** The open-source acceleration is clear empirically. Qwen3 and Gemma 3 matching frontier models in 2025 suggests convergence is accelerating. But driving-specific data remains a differentiator.
- **Q4 (Distillation):** Strong evidence from Gemma 3, R1, and DiMA that distillation works across domains. The pattern is converging toward train-large-distill-small as standard practice.
- **Q8 (VL alignment):** CLIP → LLaVA → SAM trajectory shows alignment is improving. But [[wiki/sources/papers/segment-anything|SAM]]'s promptable segmentation and DINO's emergent properties suggest 2D alignment may not be enough for 3D spatial reasoning needed in driving.

## Key papers for this stream

| Paper | Relevance |
|-------|-----------|
| [[wiki/sources/papers/on-the-opportunities-and-risks-of-foundation-models]] | Foundational framework: emergence + homogenization |
| [[wiki/sources/papers/scaling-laws-for-neural-language-models]] | Scaling laws for language |
| [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]] | Scaling laws for heterogeneous robots |
| [[wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation]] | One policy for 20+ embodiments |
| [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models]] | Dominant adaptation method |
| [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] | CLIP: vision-language alignment |
| [[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai]] | World foundation model platform |
| [[wiki/sources/papers/unisim-learning-interactive-real-world-simulators]] | Interactive real-world simulators |
| [[wiki/sources/papers/qwen3-technical-report]] | Open-weight reasoning models |
| [[wiki/sources/papers/gemma-3-technical-report]] | Distillation-driven efficiency |

## Related

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/machine-learning]]
- [[wiki/queries/open-questions]]
- [[wiki/queries/open-questions-vla]]
