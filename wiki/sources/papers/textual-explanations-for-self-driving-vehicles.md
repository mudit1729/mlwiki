---
title: "Textual Explanations for Self-Driving Vehicles (BDD-X)"
type: source-summary
status: complete
updated: 2026-04-05
year: 2018
venue: ECCV
tags:
  - paper
  - autonomous-driving
  - vla
  - explainability
  - attention
  - benchmark
citations: 427
paper-faithfullness: audited-fixed
---

📄 **[Read on arXiv](https://arxiv.org/abs/1807.11546)**

# Textual Explanations for Self-Driving Vehicles

## Overview

End-to-end driving models produce control signals without any rationale, making them opaque and untrustworthy for safety-critical deployment. This paper by Kim et al. (ECCV 2018) addresses this by creating BDD-X -- the first large-scale benchmark for explainable autonomous driving -- and proposing an attention-alignment mechanism that grounds natural-language driving explanations in the same visual regions that influenced the control decision.

The key philosophical contribution is the distinction between introspective explanations and post-hoc rationalizations. An introspective explanation is causally related to the decision process (the model explains what it actually attended to), while a rationalization merely generates plausible text about the scene that may have no connection to what drove the decision. The attention alignment loss explicitly encourages the former: the explanation generator's attention map is regularized to match the controller's spatial attention map, creating a causal link between what the model looks at for control and what it talks about in its explanation.

BDD-X became the standard benchmark for explainable driving research, directly reused by DriveGPT4, DriveLM, and many subsequent works. The attention-alignment paradigm established here remains influential, though modern VLA systems have shifted from separate controller+explainer architectures toward unified models where language and action share the same representation, making the faithfulness question even more central.

## Key Contributions

- **BDD-X dataset**: Built on BDD100K with 6,984 video clips (over 77 hours, 26,228 annotations) paired with human-written action descriptions ("car is slowing down") and justifications ("because a pedestrian is crossing"), establishing the standard testbed for explainable driving
- **Dual-model architecture**: Visual attention-based controller (images to steering/acceleration with spatial attention maps) coupled with a video-to-text explanation generator (encoder-decoder with temporal and spatial attention)
- **Two attention alignment strategies**: Strongly Aligned Attention (SAA) directly reuses the controller's attention map in the explanation generator; Weakly Aligned Attention (WAA) trains a separate attention mechanism in the explainer but constrains it via a KL-divergence loss toward the controller's attention map. WAA achieves the best explanation quality in both automatic metrics and human evaluations.
- **Introspective vs rationalization distinction**: Formally separates causally-grounded explanations from post-hoc plausible-but-not-causal text generation, a distinction that remains philosophically important in 2025 VLA research
- **First language-output driving system with explicit visual grounding**: Prior work generated explanations without any mechanism to ensure they were related to the decision process

## Architecture / Method

```
         BDD-X: Attention-Aligned Controller + Explainer

  Video Frames [f1, f2, ..., fT]
        │
        ├──────────────────────────────────────┐
        ▼                                      ▼
  ┌───────────────────┐              ┌───────────────────┐
  │  Vehicle Controller│              │ Explanation Generator│
  │                   │              │                     │
  │  CNN (5-layer)    │              │  CNN Encoder         │
  │       │           │              │       │             │
  │       ▼           │              │       ▼             │
  │  Spatial Attention │              │  LSTM Decoder       │
  │   A_ctrl          │              │  + Attention A_expl │
  │       │           │              │       │             │
  │       ▼           │              │       ▼             │
  │  LSTM ──► Control │              │  Word-by-word text  │
  │  (steer, speed)   │              │  "stopping because  │
  └────────┬──────────┘              │   of pedestrian"    │
           │                         └──────────┬──────────┘
           │                                    │
           │         ┌────────────────────────┐ │
           └────────►│  Alignment (two modes): │◄┘
                     │  SAA: A_expl = A_ctrl   │
                     │  WAA: L_align =         │
                     │   KL(A_ctrl || A_expl)  │
                     └────────────────────────┘

  Total Loss: L = L_control + λ_text * L_text + λ_align * L_align
```

The system has two components trained jointly. The **vehicle controller** takes a sequence of frames and produces steering angle and speed predictions. It uses a five-layer CNN (without max-pooling, similar to Bojarski et al.) with spatial attention to produce attention-weighted visual features, which are processed by an LSTM to generate control signals. The spatial attention map A_ctrl indicates which image regions the controller relies on for its decisions.

The **explanation generator** is an encoder-decoder model. The encoder processes the same video frames through a CNN, and the decoder generates natural-language explanations word by word using an LSTM with attention over the visual features. The decoder's attention map A_expl indicates which image regions the explanation references.

The paper introduces two attention alignment strategies. In **Strongly Aligned Attention (SAA)**, the explanation generator directly reuses the controller's attention map, guaranteeing the two components look at identical regions. In **Weakly Aligned Attention (WAA)**, the explanation generator has its own separate attention network but is guided by a KL-divergence loss L_align = KL(A_ctrl || A_expl), which encourages alignment while preserving flexibility. WAA outperforms SAA in both automatic NLG metrics and human evaluations. The total loss is L = L_control + lambda_text * L_text + lambda_align * L_align, where L_control is the driving loss (MSE on steering/speed), L_text is the language generation loss (cross-entropy), and L_align is the attention alignment regularizer (KL divergence in the WAA variant).

This architecture ensures that when the explanation says "stopping because of pedestrian on right," the explanation generator is actually attending to the pedestrian on the right, and that region is also what the controller used for its braking decision.

## Results

- **WAA achieves best explanation quality**: in human evaluation, the Weakly Aligned Attention model achieved 66.0% correctness for explanations and 93.5% for descriptions, outperforming both SAA and the rationalization baseline
- **BDD-X provides a reusable benchmark** that became the de facto testbed for explainable driving research, directly used by DriveGPT4, Reason2Drive, and others
- **Explanations are grounded in controller attention regions**, providing evidence that the language output is connected to the actual decision process rather than arbitrary scene narration
- **Standard NLG metrics (BLEU, METEOR, CIDEr)** show improvements with attention alignment, though the human evaluation results are more meaningful for assessing faithfulness
- **Qualitative examples** demonstrate that aligned explanations correctly identify the causal factors (pedestrians, traffic lights, lead vehicles) while unaligned explanations sometimes reference irrelevant scene elements

## Limitations & Open Questions

- Aligned attention does not definitively prove causal correctness -- the faithfulness problem means aligned language can still be plausible yet not truly decision-causing, since the alignment is a soft regularizer rather than a hard guarantee
- Offline evaluation only with no closed-loop safety validation of the driving component; the control model is simple and not competitive with modern driving systems
- Language quality is limited by template-like descriptions in BDD-X, which constrains the diversity and naturalness of generated explanations
- Language is output only, not input -- no instruction following capability, limiting the system to explanation rather than interaction

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/papers/drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model]]
- [[wiki/sources/papers/simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment]]
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]]
- [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]]
- [[wiki/sources/papers/talk2car-taking-control-of-your-self-driving-car]]
