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

[[wiki/sources/papers/attention-is-all-you-need]] (2017) unified these threads by replacing recurrence entirely with self-attention, enabling massive parallelism and scaling. The transformer architecture now dominates language ([[wiki/sources/papers/language-models-are-few-shot-learners]]), vision ([[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]]), speech ([[wiki/sources/papers/deep-speech-2]]), and multimodal settings. [[wiki/sources/papers/swin-transformer-hierarchical-vision-transformer-using-shifted-windows]] (Swin Transformer, 2021) made transformers practical as general-purpose vision backbones by introducing hierarchical multi-scale features and shifted window attention with linear complexity, replacing ResNet across detection, segmentation, and BEV perception pipelines. For driving, transformers underpin BEV encoders (BEVFormer), trajectory decoders (VAD), and the VLA systems that treat perception, prediction, and planning as a single sequence modeling problem.

## Scaling laws and compute-optimal training

A defining insight of the 2020s is that model performance is predictable from scale. [[wiki/sources/papers/scaling-laws-for-neural-language-models]] (Kaplan et al., 2020) established power-law relationships between compute, data, parameters, and loss. [[wiki/sources/papers/training-compute-optimal-large-language-models]] (Chinchilla, 2022) refined this to show that most large models were undertrained relative to their size. These findings directly shape how foundation models for driving are designed: the push toward larger VLMs and longer training schedules in systems like EMMA and DriveVLM follows from scaling-law reasoning.

## Self-supervised and multimodal pretraining

Self-supervised pretraining allows models to learn general representations before task-specific fine-tuning. [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] introduced masked language modeling; [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] (CLIP) extended contrastive pretraining to vision-language pairs. [[wiki/sources/papers/exploring-simple-siamese-representation-learning]] (SimSiam, 2021) showed that self-supervised visual learning can be dramatically simplified: a Siamese network with stop-gradient and a prediction MLP achieves competitive results without negative pairs, momentum encoders, or large batches, clarifying which components of prior methods were truly essential. [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] opened the generative modeling frontier, and [[wiki/sources/papers/diffusion-models-beat-gans-on-image-synthesis]] proved that diffusion models with classifier guidance could surpass GANs on image quality, catalyzing the shift toward diffusion-based generation across images, video, audio, 3D, and planning in driving contexts.

## Reasoning and chain-of-thought

[[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] showed that prompting LLMs to produce intermediate reasoning steps dramatically improves performance on complex tasks. This idea is central to driving VLAs: systems like DriveLM and Reason2Drive use chain-of-thought structures to decompose driving decisions into perception, prediction, and planning stages before emitting actions.

[[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning]] (DeepSeek-R1, 2025) demonstrated that chain-of-thought reasoning can emerge from pure reinforcement learning without human-annotated reasoning demonstrations. Using Group Relative Policy Optimization (GRPO) with simple rule-based rewards on a 671B MoE base model, R1-Zero discovers self-verification, reflection, and adaptive compute allocation. The full R1 model uses a multi-stage pipeline (cold-start SFT → reasoning RL → rejection sampling SFT → alignment RL) to reach performance competitive with OpenAI-o1 on math, code, and science benchmarks. Crucially, reasoning capabilities distill effectively to models as small as 1.5B parameters, democratizing access to strong reasoning. This represents a paradigm shift: the training objective (RL with outcome rewards), not just scale, is a key axis for capability emergence.

## Parameter-efficient adaptation

As models scale to billions of parameters, full fine-tuning becomes impractical for multi-task deployment. [[wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation]] (2021) demonstrated that prepending learned continuous vectors to transformer key-value pairs at every layer enables task adaptation with only 0.1% of parameters, matching full fine-tuning on generation tasks. [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models]] (LoRA, ICLR 2022) became the dominant PEFT method: by freezing pretrained weights and injecting trainable low-rank decomposition matrices (Delta-W = BA, rank r << d), LoRA reduces trainable parameters by 10,000x on GPT-3 175B while matching full fine-tuning, with zero inference overhead after merging. Together, prefix-tuning, LoRA, adapters, and prompt tuning form the PEFT paradigm now standard for adapting foundation models to downstream tasks, including driving VLA systems that fine-tune large VLMs for action prediction.

## The foundation model paradigm

[[wiki/sources/papers/on-the-opportunities-and-risks-of-foundation-models]] (Bommasani et al., 2021) formalized the concept of foundation models -- large models pretrained on broad data via self-supervision, then adapted to downstream tasks. The report identified two defining phenomena: **emergence** (unanticipated capabilities arising from scale) and **homogenization** (convergence around a few base models). Both have been validated by subsequent developments: GPT-4's emergent capabilities, the dominance of LoRA/RLHF adaptation pipelines, and the concentration of frontier model development among a handful of labs.

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
| [[wiki/sources/papers/exploring-simple-siamese-representation-learning]] | SimSiam: minimal self-supervised learning without negatives or momentum |
| [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] | Intermediate reasoning steps improve LLM performance |
| [[wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning]] | Emergent reasoning from RL; GRPO; distillation to small models |
| [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] | Diffusion models for high-quality generation |
| [[wiki/sources/papers/diffusion-models-beat-gans-on-image-synthesis]] | Classifier guidance enabling diffusion to surpass GANs |
| [[wiki/sources/papers/neural-machine-translation-by-jointly-learning-to-align-and-translate]] | Attention mechanism for sequence-to-sequence models |
| [[wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation]] | Parameter-efficient fine-tuning via continuous prefix optimization (0.1% params) |
| [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models]] | LoRA: low-rank adaptation reducing trainable params by 10,000x with zero inference overhead |
| [[wiki/sources/papers/on-the-opportunities-and-risks-of-foundation-models]] | Coined "foundation model"; emergence + homogenization framework |
| [[wiki/sources/papers/swin-transformer-hierarchical-vision-transformer-using-shifted-windows]] | Hierarchical vision transformer; general-purpose backbone replacing CNNs |

## Related

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/robotics]]
- [[wiki/concepts/end-to-end-architectures]]
