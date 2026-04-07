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

## Core architecture and scaling

- Attention Is All You Need
- Language Models are Unsupervised Multitask Learners
- BERT
- Scaling Laws for Neural Language Models
- Training Compute-Optimal Large Language Models
- GPT-3
- Mixtral of Experts (Sparse MoE)
- LLaMA

## Parameter-efficient fine-tuning

- Prefix-Tuning: Optimizing Continuous Prompts for Generation
- LoRA: Low-Rank Adaptation of Large Language Models
- Adapter methods

## Instruction tuning and alignment

- InstructGPT
- [[wiki/sources/papers/direct-preference-optimization-your-language-model-is-secretly-a-reward-model]] -- DPO: eliminates RL from preference alignment via closed-form reward reparameterization
- RLHF preference-optimization papers
- Constitutional AI

## Tool use and retrieval

- ReAct
- Toolformer
- Retrieval-Augmented Generation papers when directly useful

## Multimodal bridge

- CLIP
- DINO (self-supervised ViT features)
- BLIP
- Flamingo
- **LLaVA (Visual Instruction Tuning)** -- established the dominant open-source recipe for multimodal instruction-following: CLIP encoder + linear projection + LLM, with GPT-assisted instruction data generation
- Kosmos-style multimodal models
- GPT-4V era papers and technical reports

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
