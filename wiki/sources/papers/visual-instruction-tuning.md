---
title: "Visual Instruction Tuning"
tags: [multimodal, vision-language-model, instruction-tuning, transformer, computer-vision, nlp, foundation-model]
status: active
type: paper
year: "2023"
venue: "NeurIPS 2023"
citations: 13533
arxiv_id: "2304.08485"
---

# Visual Instruction Tuning (LLaVA)

📄 **[Read on arXiv](https://arxiv.org/abs/2304.08485)**

## Overview

Large language models transformed NLP through instruction tuning -- training on diverse instruction-response pairs so models follow human intent across tasks. Visual Instruction Tuning extends this paradigm to the multimodal domain, introducing **LLaVA (Large Language and Vision Assistant)**, the first general-purpose visual and language instruction-following model built by connecting a pretrained CLIP vision encoder with a large language model (Vicuna) through a simple linear projection layer. The paper demonstrates that the instruction-following capabilities of LLMs can be unlocked for visual tasks with surprisingly little architectural complexity, provided the training data captures the right kind of visual reasoning.

The core insight is a novel **GPT-assisted data generation pipeline** that creates 158K multimodal instruction-following samples from existing image caption and bounding box annotations (from COCO). Rather than collecting expensive human-annotated instruction-response pairs for images, the authors feed symbolic visual representations (captions and object locations) to GPT-4 as a "teacher" to generate three types of instruction data: multi-turn conversations (58K), detailed image descriptions (23K), and complex visual reasoning chains (77K). This data, despite being generated without GPT-4 actually seeing the images, is sufficient to teach a vision-language model to follow diverse visual instructions.

LLaVA achieves an 85.1% relative score compared to GPT-4 on a synthetic multimodal benchmark and reaches 92.53% state-of-the-art accuracy on ScienceQA through a GPT-4 judge ensembling strategy. The paper's significance extends far beyond its benchmark numbers: LLaVA established the dominant recipe for open-source multimodal models -- connect a frozen CLIP encoder to an LLM via a lightweight projection, generate instruction-tuning data using a stronger model, and train in two stages. This recipe was adopted and refined by dozens of subsequent models (LLaVA-1.5, LLaVA-NeXT, InternVL, Qwen-VL, and many driving/robotics VLMs).

## Key Contributions

- **GPT-assisted multimodal instruction data generation**: A scalable pipeline that converts existing image annotations (captions + bounding boxes) into 158K diverse instruction-following samples across conversation, detailed description, and complex reasoning categories -- without requiring GPT-4 to see any images
- **Simple yet effective architecture**: Demonstrates that a linear projection layer connecting a frozen CLIP ViT-L/14 vision encoder to a Vicuna LLM is sufficient for strong multimodal instruction-following, establishing the "visual encoder + projection + LLM" blueprint
- **Two-stage training recipe**: Stage 1 aligns vision-language features by training only the projection layer on filtered CC3M caption data (595K image-text pairs); Stage 2 fine-tunes the full LLM end-to-end on 158K instruction-following samples
- **LLaVA-Bench evaluation**: Introduces a GPT-4-based evaluation protocol for open-ended visual instruction-following, measuring relative quality against GPT-4's own responses
- **ScienceQA state-of-the-art**: Achieves 92.53% on ScienceQA through a late-fusion ensembling strategy with GPT-4, demonstrating complementary strengths between visual grounding and textual reasoning

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   LLaVA Architecture                      │
│                                                           │
│  Image                    User Instruction                │
│    │                           │                         │
│    ▼                           │                         │
│  ┌──────────────┐              │                          │
│  │ CLIP ViT-L/14│ (frozen)     │                          │
│  │  224 x 224   │              │                          │
│  └──────┬───────┘              │                          │
│         │ Z_v (patch tokens)   │                          │
│         ▼                      │                          │
│  ┌──────────────┐              │                          │
│  │Linear Project.│  W          │                          │
│  │ H_v = W·Z_v  │              │                          │
│  └──────┬───────┘              │                          │
│         │ Visual tokens        │ Text tokens              │
│         │ (LLM dim)            │                          │
│         └─────────┬────────────┘                          │
│                   │  Interleaved sequence:                 │
│                   │  [sys] [H_v] [instruction] [response] │
│                   ▼                                       │
│  ┌────────────────────────────────┐                       │
│  │    Vicuna (LLaMA fine-tuned)   │                      │
│  │    Autoregressive generation   │                      │
│  │    Loss on response tokens only│                      │
│  └────────────┬───────────────────┘                       │
│               ▼                                          │
│         Generated Response                                │
│                                                           │
│  Training:                                                │
│  Stage 1: Freeze ViT + LLM, train W only (595K CC3M)     │
│  Stage 2: Freeze ViT, fine-tune LLM + W (158K instruct)  │
└──────────────────────────────────────────────────────────┘
```

## Architecture / Method

![Example demonstrating LLaVA's ability to understand complex visual scenes](https://paper-assets.alphaxiv.org/figures/2304.08485v2/car_bbox.jpg)

### Model Architecture

LLaVA's architecture is intentionally minimalist, consisting of three components:

1. **Vision Encoder**: A pretrained CLIP ViT-L/14 operating at 224x224 resolution. The encoder produces a grid of visual patch tokens `Z_v` from the input image. The vision encoder remains frozen throughout training.

2. **Linear Projection Layer**: A single trainable linear layer `W` that maps CLIP visual features into the word embedding space of the language model: `H_v = W · Z_v`, where `H_v` are visual tokens with the same dimensionality as the LLM's text embeddings.

3. **Language Model**: Vicuna (a fine-tuned LLaMA), which processes the interleaved sequence of projected visual tokens and text tokens autoregressively. The LLM is frozen in Stage 1 and fine-tuned in Stage 2.

The input to the LLM is a multimodal sequence: `[system prompt] [visual tokens H_v] [user instruction] [assistant response]`. The model is trained with standard autoregressive next-token prediction, with loss computed only on the assistant's response tokens.

### Data Generation Pipeline

The instruction data generation uses GPT-4 (text-only) as a teacher:

- **Input to GPT-4**: Image captions and bounding box coordinates (symbolic representations, not actual images)
- **Prompt engineering**: Seed examples for each data type guide GPT-4 to produce diverse, contextual responses
- **Three data types**:
  - **Conversation** (58K): Multi-turn Q&A about image content, requiring spatial understanding
  - **Detailed Description** (23K): Rich paragraph-length descriptions of image content
  - **Complex Reasoning** (77K): Multi-step reasoning chains about image content (e.g., inferring cause-effect, counting, spatial relationships)

### Two-Stage Training

- **Stage 1 -- Feature Alignment** (4 hours on 8x A100): Only the projection matrix `W` is trained on 595K filtered CC3M image-caption pairs. Both the vision encoder and LLM are frozen. This aligns the visual feature space with the language embedding space.
- **Stage 2 -- End-to-End Fine-Tuning** (10 hours on 8x A100): The LLM weights are unfrozen and fine-tuned jointly with the projection layer on the 158K GPT-generated instruction-following dataset. The vision encoder remains frozen.

## Results

### LLaVA-Bench Evaluation

LLaVA is evaluated on two custom benchmarks using GPT-4 as a judge, scoring model responses relative to GPT-4's own reference answers:

| Model | LLaVA-Bench (COCO) | LLaVA-Bench (In-the-Wild) |
|-------|--------------------:|---------------------------:|
| LLaVA | **85.1%** | -- |
| BLIP-2 | 65.0% | -- |
| OpenFlamingo | 37.1% | -- |

Instruction tuning improved LLaVA's relative score by over 50 points compared to the base model without instruction tuning. On in-the-wild images, LLaVA outperformed OpenFlamingo by 48% and BLIP-2 by 29%.

### ScienceQA

| Method | Accuracy |
|--------|--------:|
| LLaVA + GPT-4 (ensemble) | **92.53%** |
| GPT-4 (text-only CoT) | 82.69% |
| LLaVA alone | 90.92% |
| Multimodal-CoT (prev. SOTA) | 91.68% |

The ensembling strategy routes questions to either LLaVA or GPT-4 based on answer agreement, achieving complementary gains from visual grounding (LLaVA) and textual reasoning (GPT-4).

### Key Ablation Findings

- **Data type matters**: Complex reasoning data contributes more to performance than conversation or description data alone
- **Projection layer**: Even a simple linear projection is sufficient; the quality of instruction data matters more than projection complexity
- **Scale of instruction data**: Performance improves with more instruction-following samples, with diminishing returns beyond ~150K

## Limitations & Open Questions

- **Resolution bottleneck**: CLIP ViT-L/14 operates at 224x224, severely limiting fine-grained visual understanding (reading text, counting small objects, spatial precision) -- subsequent work (LLaVA-1.5, LLaVA-NeXT) addressed this with higher resolution and dynamic tiling
- **Hallucination**: LLaVA can generate plausible-sounding but visually incorrect descriptions, a known issue with autoregressive VLMs that lack explicit visual grounding mechanisms
- **Single-image limitation**: No support for video or multi-image reasoning in the original formulation
- **Evaluation limitations**: GPT-4-based evaluation, while useful, is noisy and biased toward verbose, well-structured responses -- not necessarily accurate ones
- **Data generation without visual grounding**: GPT-4 generates instruction data from captions and bounding boxes, not actual images, which can introduce systematic biases in the training data

## Connections

Related papers in the wiki:

- [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] -- LLaVA uses CLIP ViT-L/14 as its vision encoder; CLIP's contrastive pretraining provides the visual representations that LLaVA projects into language space
- [[wiki/sources/papers/attention-is-all-you-need]] -- The transformer architecture underlying both the CLIP encoder and the Vicuna LLM
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3 established the foundation for few-shot instruction-following that LLaVA extends to the visual domain
- [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] -- LLaVA's complex reasoning data category explicitly trains multi-step visual reasoning, extending CoT to multimodal settings
- [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] -- BERT's pretrain-then-adapt paradigm informs LLaVA's two-stage approach
- [[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model]] -- PaLM-E (2023) independently explored injecting visual tokens into LLMs for embodied tasks; LLaVA demonstrated a simpler, open-source recipe achieving broad visual instruction-following
- [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]] -- ViT established that pure transformers work for vision; CLIP ViT (used in LLaVA) is a contrastive variant of this architecture
- [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] -- RT-2 applies the VLM-to-action paradigm that LLaVA helped popularize, extending it from visual chat to robotic control
- [[wiki/concepts/foundation-models]] -- LLaVA exemplifies the "connect pretrained modules with minimal glue" philosophy of foundation model adaptation
- [[wiki/concepts/vision-language-action]] -- LLaVA's architecture (vision encoder + projection + LLM) became the standard backbone for VLA models in both robotics and autonomous driving
