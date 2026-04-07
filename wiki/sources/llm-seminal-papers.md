---
title: LLM Seminal Papers
type: source-program
status: active
updated: 2026-04-05
tags:
  - sources
  - llm
  - foundational
---

# LLM Seminal Papers

This page tracks the canonical LLM and adjacent foundation-model papers that matter for the autonomy side of the wiki.

## Foundational surveys and frameworks

- [[wiki/sources/papers/on-the-opportunities-and-risks-of-foundation-models]] -- Stanford HAI report (2021) that coined "foundation model" and formalized emergence + homogenization as the defining phenomena of the paradigm

## Core architecture and scaling

- Attention Is All You Need
- Language Models are Unsupervised Multitask Learners
- BERT
- Scaling Laws for Neural Language Models
- Training Compute-Optimal Large Language Models
- GPT-3
- Mixtral of Experts (Sparse MoE)
- LLaMA
- Qwen3 (dense + MoE family with thinking mode, 36T tokens, 119 languages)

## Parameter-efficient fine-tuning

- Prefix-Tuning: Optimizing Continuous Prompts for Generation
- LoRA: Low-Rank Adaptation of Large Language Models
- Adapter methods

## Instruction tuning and alignment

- [[wiki/sources/papers/scaling-instruction-finetuned-language-models]] -- Flan-PaLM/Flan-T5: scaled instruction finetuning to 1,836 tasks + CoT data across T5 and PaLM architectures, 0.2% of pre-training compute for +9.4% held-out improvement, established instruction tuning as standard post-training recipe
- InstructGPT
- [[wiki/sources/papers/direct-preference-optimization-your-language-model-is-secretly-a-reward-model]] -- DPO: eliminates RL from preference alignment via closed-form reward reparameterization
- RLHF preference-optimization papers
- Constitutional AI

## Reasoning and search

- Chain-of-Thought Prompting
- [[wiki/sources/papers/tree-of-thoughts-deliberate-problem-solving-with-large-language-models]] -- ToT: generalizes CoT into tree-structured search with LM-based state evaluation, 74% on Game of 24 vs. 4% for CoT, NeurIPS 2023
- [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning]] -- DeepSeek-R1: emergent reasoning from pure RL with rule-based rewards (GRPO), multi-stage pipeline, effective distillation to 1.5B-70B models

## Tool use and retrieval

- ReAct
- Toolformer
- Retrieval-Augmented Generation papers when directly useful

## Open-weight multimodal model families

- **Gemma 3** (Google DeepMind, 2025) -- 1B-27B open-weight family with native vision via SigLIP, 128K context via 5:1 local/global attention, knowledge distillation enabling 4B to match prior 27B. [[wiki/sources/papers/gemma-3-technical-report]]

## Multimodal bridge

- CLIP
- DINO (self-supervised ViT features)
- BLIP
- Flamingo
- **LLaVA (Visual Instruction Tuning)** -- established the dominant open-source recipe for multimodal instruction-following: CLIP encoder + linear projection + LLM, with GPT-assisted instruction data generation
- Kosmos-style multimodal models
- GPT-4V era papers and technical reports
- Gemini 2.5 (sparse MoE multimodal with inference-time reasoning)

## What to extract during ingest

- architectural contribution,
- scaling insight,
- training recipe,
- alignment method,
- relevance to autonomy or VLA systems.

## Already seeded in batch 01

- [[wiki/sources/papers/attention-is-all-you-need]]
- [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]]
- [[wiki/sources/papers/language-models-are-few-shot-learners]]
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]]
- [[wiki/sources/papers/training-compute-optimal-large-language-models]]
- [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]]
- [[wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation]]
- [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models]]

## Ingested individually

- [[wiki/sources/papers/training-language-models-to-follow-instructions-with-human-feedback]] -- InstructGPT: RLHF alignment pipeline (SFT -> RM -> PPO), foundational for instruction-tuned LLMs
- [[wiki/sources/papers/flamingo-a-visual-language-model-for-few-shot-learning]] -- Flamingo: few-shot multimodal learning via frozen LM + Perceiver Resampler + gated cross-attention, template for VLM architecture
- [[wiki/sources/papers/blip-bootstrapping-language-image-pre-training-for-unified-vision-language-understanding-and-generation]] -- BLIP: unified encoder-decoder for vision-language understanding + generation, CapFilt data bootstrapping, ICML 2022
- [[wiki/sources/papers/llama-2-open-foundation-and-fine-tuned-chat-models]] -- Llama 2: open-source RLHF-aligned LLM family (7B-70B), detailed alignment pipeline with dual reward models, backbone for driving VLA systems (e.g., AsyncDriver)
- [[wiki/sources/papers/visual-instruction-tuning]] -- LLaVA: visual instruction tuning via CLIP + linear projection + Vicuna, GPT-assisted data generation, blueprint for open-source multimodal models
- [[wiki/sources/papers/mixtral-of-experts]] -- Mixtral 8x7B: sparse MoE LLM, top-2 of 8 experts per token, 13B active of 47B total, matches Llama 2 70B quality
- [[wiki/sources/papers/palm-scaling-language-modeling-with-pathways]] -- PaLM: 540B dense Transformer trained via Pathways, SOTA few-shot on 28/29 benchmarks, emergent discontinuous scaling on BIG-bench
- [[wiki/sources/papers/scaling-instruction-finetuned-language-models]] -- Flan-PaLM/Flan-T5: instruction finetuning at scale (1,836 tasks + CoT), 75.2% MMLU, +9.4% on held-out tasks, architecture-agnostic across T5 and PaLM
- [[wiki/sources/papers/gemini-25-pushing-the-frontier-with-advanced-reasoning-multimodality-long-context-and-next-generation-agentic-capabilities]] -- Gemini 2.5: sparse MoE multimodal Transformer with "Thinking" inference-time reasoning, 1M+ token context, AIME 2025 88.0%, agentic capabilities
- [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning]] -- DeepSeek-R1: reasoning via RL (GRPO) with rule-based rewards, competitive with o1 on math/code, distillation to small models
- [[wiki/sources/papers/qwen3-technical-report]] -- Qwen3: dense (0.6B-32B) + MoE (30B-A3B, 235B-A22B) family with unified thinking mode, 36T tokens across 119 languages, four-stage post-training with reasoning RL, Apache 2.0
- [[wiki/sources/papers/tree-of-thoughts-deliberate-problem-solving-with-large-language-models]] -- ToT: tree-structured search over LM-generated thoughts with LM-based evaluation, generalizes CoT, NeurIPS 2023
- [[wiki/sources/papers/gemma-3-technical-report]] -- Gemma 3: 1B-27B open-weight multimodal family, 5:1 local/global attention for 128K context, SigLIP vision encoder, knowledge distillation enabling 4B to match prior 27B
