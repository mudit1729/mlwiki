---
title: "On the Opportunities and Risks of Foundation Models"
tags: [foundation-model, nlp, computer-vision, robotics, multimodal, transformer, survey]
status: active
type: paper
year: "2021"
venue: "arXiv (Stanford HAI)"
citations: 6057
arxiv_id: "2108.07258"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2108.07258)**

## Overview

"On the Opportunities and Risks of Foundation Models" is a comprehensive 200+ page report from over 100 researchers at Stanford's Center for Research on Foundation Models (CRFM). It introduces and formalizes the term **foundation model** -- a model trained on broad data at scale using self-supervision that can be adapted to a wide range of downstream tasks. The report argues that AI has undergone a series of paradigm shifts: from hand-engineered features to machine learning (1990s), to deep learning (2010s), and now to foundation models, where a single pretrained model serves as the base for numerous applications.

Two phenomena define this paradigm: **emergence** (the spontaneous development of unanticipated capabilities, such as GPT-3's in-context learning) and **homogenization** (the concentration of the field around a few powerful base models that serve as foundations for many applications). While homogenization creates powerful leverage -- improvements to the foundation model propagate to all downstream systems -- it also introduces systemic risk, since defects in the foundation model (bias, toxicity, factual errors) propagate equally broadly.

The report spans four major domains: capabilities (language, vision, robotics), applications (healthcare, law, education), technology (modeling, training, evaluation, systems, data, security), and society (bias, misuse, environmental impact, economics, ethics). It emphasizes that foundation models remain "poorly understood" regarding their internal mechanisms, failure modes, and full capabilities, and calls for "deep interdisciplinary collaboration" among AI researchers, domain experts, and social impact scholars.

## Key Contributions

- **Coined and formalized the term "foundation model"**, providing a shared vocabulary for the paradigm of large pretrained models adapted to downstream tasks
- **Identified emergence and homogenization** as the two defining phenomena of the foundation model paradigm, with distinct opportunity and risk profiles for each
- **Comprehensive multi-domain analysis** spanning technical capabilities, social impact, legal implications, healthcare applications, education, economics, and environmental costs
- **Articulated systemic risks** of homogenization: bias amplification, single points of failure, power concentration among large technology companies, and environmental costs of training at scale
- **Called for interdisciplinary research norms**, including consideration of "when not to build" certain systems, responsible development practices, and professional standards

## Architecture / Method

![Foundation model paradigm overview](https://paper-assets.alphaxiv.org/figures/2108.07258v3/img-0.jpeg)

This is a survey and position paper rather than a methods paper, so there is no novel architecture. Instead, the report provides a conceptual framework for understanding foundation models:

**The Foundation Model Pipeline:**
1. **Pretraining**: Train on broad, diverse data using self-supervised objectives (e.g., masked language modeling, contrastive learning, autoregressive generation)
2. **Adaptation**: Fine-tune or prompt the pretrained model for specific downstream tasks
3. **Deployment**: Use the adapted model in applications across domains

**Key Technical Themes Analyzed:**
- **Data**: The role of internet-scale training data, data quality, curation, and the legal/ethical implications of training on scraped data
- **Modeling**: Transformer architectures, scaling laws, multimodal learning, and the trade-offs between model size and efficiency
- **Training**: Self-supervised learning objectives, compute requirements, and the environmental cost of large-scale training
- **Evaluation**: The inadequacy of existing benchmarks for measuring emergent capabilities and the need for holistic evaluation frameworks
- **Security and privacy**: Adversarial robustness, data extraction attacks, and the privacy implications of models memorizing training data

![Capabilities and applications mapping](https://paper-assets.alphaxiv.org/figures/2108.07258v3/img-1.jpeg)

## Results

This paper does not present experimental results in the traditional sense. Instead, it synthesizes the state of the field as of mid-2021 and makes forward-looking predictions. Key observations include:

| Dimension | Opportunity | Risk |
|-----------|------------|------|
| **Homogenization** | Improvements propagate to all downstream tasks | Defects propagate equally; single points of failure |
| **Emergence** | Unexpected capabilities (few-shot learning, reasoning) | Unpredictable failure modes; difficult to test exhaustively |
| **Healthcare** | Enhanced diagnostic efficiency, drug discovery | Bias in medical data, liability for AI errors |
| **Law** | Improved access to justice, legal research automation | Perpetuation of existing legal biases |
| **Education** | Personalized tutoring, accessibility | Cheating, deskilling, digital divide |
| **Environment** | Efficiency gains from shared models | Massive training compute costs (carbon footprint) |
| **Economics** | Productivity gains, new industries | Power concentration, labor displacement |

The report's predictions have been largely validated by subsequent developments: the emergence of GPT-4, the dominance of foundation model adaptation (LoRA, RLHF), the proliferation of multimodal models (Flamingo, LLaVA, GPT-4V), and ongoing societal debates about AI safety, copyright, and regulation.

## Limitations & Open Questions

- **Theoretical understanding**: The report acknowledges that foundation models are "poorly understood" -- why emergence occurs, what capabilities scale predictably, and what failure modes exist remain open
- **Evaluation gap**: Existing benchmarks are insufficient for measuring the full range of foundation model capabilities and risks
- **Governance**: How to govern foundation models that cross domain boundaries and national jurisdictions is unresolved
- **Environmental cost**: The carbon footprint of training foundation models at scale is a growing concern with no clear mitigation path
- **Equity and access**: The concentration of foundation model development among well-resourced labs raises questions about equitable access and benefit distribution

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3 is the paradigmatic example of emergent capabilities in foundation models discussed throughout this report
- [[wiki/sources/papers/attention-is-all-you-need]] -- the transformer architecture that underpins virtually all foundation models
- [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] -- CLIP exemplifies the multimodal foundation model paradigm analyzed here
- [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] -- BERT as an early foundation model for NLP
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- scaling laws that explain why foundation models improve predictably with compute
- [[wiki/sources/papers/training-compute-optimal-large-language-models]] -- Chinchilla scaling laws refining the compute-optimal training insights discussed in this report
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- diffusion models as a generative foundation model paradigm
- [[wiki/sources/papers/palm-scaling-language-modeling-with-pathways]] -- PaLM as a subsequent large-scale foundation model validating this report's predictions
- [[wiki/concepts/foundation-models]] -- the wiki concept page directly organized around the ideas formalized in this report
- [[wiki/concepts/machine-learning]] -- broader ML context for the paradigm shifts described
