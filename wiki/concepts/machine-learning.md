---
title: Machine Learning
type: concept
status: active
updated: 2026-04-05
tags:
  - ml
  - foundations
---

# Machine Learning

Machine learning provides the technical substrate for every system discussed in this wiki. This page traces the key ideas from the deep learning revolution through to the foundation-model era, with emphasis on the threads that feed into autonomous driving and embodied AI.

## The deep learning revolution

Modern deep learning begins with the demonstration that large convolutional networks trained on GPU hardware can dramatically outperform hand-engineered features. [[wiki/sources/papers/imagenet-classification-with-deep-convolutional-neural-networks]] (AlexNet, 2012) cut ImageNet error nearly in half and launched a decade of architecture scaling. The critical follow-up was [[wiki/sources/papers/deep-residual-learning-for-image-recognition]] (ResNet, 2015), which showed that residual connections allow networks to scale to hundreds of layers without degradation, establishing the blueprint for virtually all modern vision backbones.

Parallel advances in sequence modeling proved equally important. Recurrent networks with attention, pioneered by [[wiki/sources/papers/neural-machine-translation-by-jointly-learning-to-align-and-translate]] (Bahdanau attention, 2014), showed that learned alignment could replace fixed-length bottlenecks. Specialized architectures like [[wiki/sources/papers/pointer-networks]] demonstrated that output spaces could be variable and input-dependent, foreshadowing the flexible decoding strategies used in modern planners. [[wiki/sources/papers/neural-turing-machines]] explored external memory for neural networks, an idea that resurfaces in world-model and map-memory designs for driving.

## The transformer era

[[wiki/sources/papers/attention-is-all-you-need]] (2017) unified these threads by replacing recurrence entirely with self-attention, enabling massive parallelism and scaling. The transformer architecture now dominates language ([[wiki/sources/papers/language-models-are-few-shot-learners]]), vision ([[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]]), speech ([[wiki/sources/papers/deep-speech-2]]), and multimodal settings. For driving, transformers underpin BEV encoders (BEVFormer), trajectory decoders (VAD), and the VLA systems that treat perception, prediction, and planning as a single sequence modeling problem.

## Scaling laws and compute-optimal training

A defining insight of the 2020s is that model performance is predictable from scale. [[wiki/sources/papers/scaling-laws-for-neural-language-models]] (Kaplan et al., 2020) established power-law relationships between compute, data, parameters, and loss. [[wiki/sources/papers/training-compute-optimal-large-language-models]] (Chinchilla, 2022) refined this to show that most large models were undertrained relative to their size. These findings directly shape how foundation models for driving are designed: the push toward larger VLMs and longer training schedules in systems like EMMA and DriveVLM follows from scaling-law reasoning.

## Self-supervised and multimodal pretraining

Self-supervised pretraining allows models to learn general representations before task-specific fine-tuning. [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] introduced masked language modeling; [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] (CLIP) extended contrastive pretraining to vision-language pairs. [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] opened the generative modeling frontier, with diffusion now used for scene generation, data augmentation, and world modeling in driving contexts.

## Reasoning and chain-of-thought

[[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] showed that prompting LLMs to produce intermediate reasoning steps dramatically improves performance on complex tasks. This idea is central to driving VLAs: systems like DriveLM and Reason2Drive use chain-of-thought structures to decompose driving decisions into perception, prediction, and planning stages before emitting actions.

## Present state and open problems

- **Scaling vs. efficiency:** Scaling laws favor larger models, but driving demands real-time inference. How to reconcile these pressures remains open.
- **Distribution shift:** ML models are brittle under distribution shift, and driving presents severe train/deploy mismatch (weather, geography, adversarial agents).
- **Uncertainty quantification:** Most neural networks produce poorly calibrated confidence estimates, a critical gap for safety-critical deployment.
- **Data-centric ML:** The field is shifting from architecture innovation to data curation, augmentation, and synthesis, but best practices for driving data remain unsettled.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/imagenet-classification-with-deep-convolutional-neural-networks]] | Launched deep learning era with GPU-trained CNNs |
| [[wiki/sources/papers/deep-residual-learning-for-image-recognition]] | Residual connections enabling very deep networks |
| [[wiki/sources/papers/attention-is-all-you-need]] | Transformer architecture replacing recurrence with self-attention |
| [[wiki/sources/papers/scaling-laws-for-neural-language-models]] | Power-law scaling relationships for neural LMs |
| [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] | CLIP: contrastive vision-language pretraining |
| [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] | Intermediate reasoning steps improve LLM performance |
| [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] | Diffusion models for high-quality generation |
| [[wiki/sources/papers/neural-machine-translation-by-jointly-learning-to-align-and-translate]] | Attention mechanism for sequence-to-sequence models |

## Related

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/robotics]]
- [[wiki/concepts/end-to-end-architectures]]
