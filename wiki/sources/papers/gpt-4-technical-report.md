---
title: "GPT-4 Technical Report"
tags: [nlp, language-modeling, transformer, foundation-model, multimodal, scaling, rlhf]
status: active
type: paper
year: "2023"
venue: "arXiv"
citations: 26297
arxiv_id: "2303.08774"
---

# GPT-4 Technical Report

📄 **[Read on arXiv](https://arxiv.org/abs/2303.08774)**

## Overview

GPT-4 is a large-scale multimodal Transformer model developed by OpenAI that accepts both image and text inputs and produces text outputs. It represents a major step in the trajectory from GPT-3 to general-purpose AI systems, achieving human-level performance on a wide range of professional and academic benchmarks -- most notably passing a simulated bar exam with a score in the top 10% of test takers. The model demonstrated strong capabilities across language understanding, reasoning, code generation, and visual comprehension, establishing it as the most capable publicly-documented LLM at the time of release.

A central technical contribution of the report is the development of infrastructure for **predictable scaling**: OpenAI built methods to accurately forecast GPT-4's final performance using models trained with as little as 1/1,000th of GPT-4's compute budget. This validated power-law relationships in a production setting, extending the theoretical scaling laws of Kaplan et al. and Chinchilla to a practical system-level prediction framework. The ability to predict large-model behavior from small-scale experiments fundamentally changes how compute-intensive model training can be planned and de-risked.

GPT-4 also introduced significant safety improvements through reinforcement learning from human feedback (RLHF) with a novel addition: **Rule-Based Reward Models (RBRMs)**. These combine human preference modeling with explicit policy rules, achieving an 82% reduction in disallowed content responses compared to GPT-3.5 and reducing toxic generations to 0.73% on the RealToxicityPrompts benchmark. The report is notably opaque about architectural details, training data, and compute -- a deliberate choice citing competitive and safety concerns that marked a shift in disclosure norms for frontier AI systems.

## Key Contributions

- **Multimodal capability**: First GPT-family model to process both image and text inputs, handling documents, charts, photographs, and technical diagrams alongside text
- **Predictable scaling infrastructure**: Demonstrated that final model performance can be reliably predicted from 1/1,000x compute experiments using power-law extrapolation, enabling principled planning of large-scale training runs
- **Human-level benchmark performance**: Achieved top-10% bar exam scores, strong performance on AP exams, GRE, LSAT, and medical licensing exams (USMLE), and competitive results on 25+ professional/academic benchmarks
- **Safety via RLHF + RBRMs**: Introduced Rule-Based Reward Models as a complement to human preference-trained reward models, enabling more precise control over safety-relevant behaviors
- **Calibration analysis**: Documented that pre-training produces well-calibrated models but post-training (RLHF) degrades calibration -- an important finding for safety-critical deployments

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                GPT-4 Training Pipeline                       │
│                                                             │
│  Stage 1: Pre-training                                      │
│  ┌────────────────┐     ┌──────────────────────────┐        │
│  │ Massive Text   │────►│  Transformer (decoder)   │        │
│  │ Corpus         │     │  Next-token prediction   │        │
│  └────────────────┘     └────────────┬─────────────┘        │
│                                      │                      │
│  Stage 2: Supervised Fine-Tuning     ▼                      │
│  ┌────────────────┐     ┌──────────────────────────┐        │
│  │ Instruction-   │────►│  SFT Model              │        │
│  │ Response Pairs │     │  (improved instruction   │        │
│  └────────────────┘     │   following)             │        │
│                         └────────────┬─────────────┘        │
│                                      │                      │
│  Stage 3: RLHF + RBRMs              ▼                      │
│  ┌────────────────┐     ┌──────────────────────────┐        │
│  │ Human Prefs +  │────►│  Reward Model            │        │
│  │ Rule-Based     │     │  (learned + explicit     │        │
│  │ Reward Models  │     │   policy rules)          │        │
│  └────────────────┘     └────────────┬─────────────┘        │
│                                      │ RL optimization      │
│                                      ▼                      │
│                         ┌──────────────────────────┐        │
│  Multimodal Input:      │  GPT-4 (aligned)        │        │
│  Text ──┐               │  - 82% reduction in     │        │
│  Image ─┴──► Vision ───►│    disallowed content   │        │
│              Encoder     └──────────────────────────┘        │
│                                                             │
│  Predictable Scaling: 1/1000x compute ──► predict final perf│
└─────────────────────────────────────────────────────────────┘
```

![Predictable scaling from small models to GPT-4](https://paper-assets.alphaxiv.org/figures/2303.08774v6/bigger-layers.jpeg)

GPT-4 is built on the Transformer architecture and trained in three stages:

1. **Pre-training**: Large-scale next-token prediction on a vast text corpus (details undisclosed). The model learns general language understanding and world knowledge from this unsupervised stage.

2. **Supervised fine-tuning (SFT)**: The pre-trained model is fine-tuned on curated instruction-response pairs to improve helpfulness and instruction following.

3. **RLHF alignment**: Reinforcement learning from human feedback using a reward model trained on human preference comparisons. GPT-4 introduces Rule-Based Reward Models that augment learned reward signals with explicit policy constraints (e.g., refusing to generate harmful content), providing more granular safety control.

For visual inputs, images are processed alongside text through a vision encoder integrated into the Transformer pipeline. The specific architecture of the vision component is not disclosed, but it handles diverse visual content including natural images, screenshots, documents with mixed text and diagrams, and mathematical notation.

The predictable scaling methodology works by training a series of smaller models at various compute scales, fitting power-law curves to their performance, and extrapolating to predict the final large model's results. This was validated on both the pre-training loss and downstream task metrics (e.g., HumanEval coding benchmark), with predictions matching actual GPT-4 performance closely.

## Results

GPT-4 was evaluated across a broad set of professional, academic, and ML benchmarks:

| Benchmark | GPT-4 | GPT-3.5 | Notes |
|-----------|-------|---------|-------|
| Bar Exam (simulated) | ~90th percentile | ~10th percentile | Uniform Bar Exam |
| LSAT | ~88th percentile | ~40th percentile | |
| GRE Quantitative | ~80th percentile | ~25th percentile | |
| AP Calculus BC | 4/5 | 1/5 | |
| USMLE (Medical) | Passing | Near-passing | Self-assessment step exams |
| HumanEval (code) | 67.0% | 48.1% | Zero-shot |
| MMLU (5-shot) | 86.4% | 70.0% | Massive multitask benchmark |
| HellaSwag (10-shot) | 95.3% | 85.5% | |

On multilingual benchmarks, GPT-4 outperformed existing English-language LLMs in 24 of 26 languages tested, including low-resource languages, despite being predominantly English-trained.

Safety metrics showed substantial improvement: 82% reduction in disallowed content generation vs. GPT-3.5, and 0.73% toxicity rate on RealToxicityPrompts. However, the model retains limitations including knowledge cutoff (pre-September 2021 training data), hallucination of facts, vulnerability to adversarial prompts, and degraded confidence calibration after RLHF.

## Limitations & Open Questions

- **Opacity**: The report deliberately withholds architecture size, training data composition, compute budget, and hardware details -- making independent verification and scientific reproduction impossible
- **Hallucination**: GPT-4 still generates plausible but incorrect statements, particularly for obscure or recent facts, and can be confidently wrong
- **Calibration degradation**: RLHF improves helpfulness but damages the model's ability to express appropriate uncertainty -- a critical concern for safety-critical downstream applications including autonomous driving
- **Knowledge cutoff**: Static training data creates a hard boundary on temporal knowledge, requiring external retrieval or fine-tuning for current information
- **Adversarial robustness**: Remains vulnerable to jailbreaks and adversarial prompts despite safety training, suggesting fundamental limitations of RLHF-based alignment
- **Evaluation saturation**: Performance on many existing benchmarks is near ceiling, raising questions about whether current evaluation suites can meaningfully differentiate future models

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3, the direct predecessor; GPT-4 extends in-context learning with multimodal inputs and substantially improved reasoning
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- Kaplan et al. scaling laws that GPT-4's predictable scaling infrastructure validates and operationalizes at production scale
- [[wiki/sources/papers/training-compute-optimal-large-language-models]] -- Chinchilla compute-optimal training; GPT-4 likely incorporates these insights in its data-to-parameter ratio
- [[wiki/sources/papers/attention-is-all-you-need]] -- The Transformer architecture underlying GPT-4
- [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] -- Chain-of-thought reasoning that GPT-4 exhibits as an emergent capability, later formalized in downstream driving systems
- [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] -- BERT established pre-training paradigm; GPT-4 represents the autoregressive branch scaled to its extreme
- [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] -- CLIP pioneered vision-language alignment; GPT-4's multimodal capability builds on this lineage
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] -- EMMA applies GPT-4-class multimodal models directly to autonomous driving as "everything-as-language"
- [[wiki/concepts/foundation-models]] -- GPT-4 as the defining example of the foundation model paradigm
- [[wiki/concepts/machine-learning]] -- Scaling laws and the transformer era
