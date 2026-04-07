---
title: Overview
type: overview
status: active
updated: 2026-04-06
tags:
  - map
  - autonomy
  - ml
---

# Overview

This wiki maps the convergence of machine learning, robotics, and foundation models into real autonomy systems — **190 papers from 2012 to 2026**, spanning foundational architectures ([[wiki/sources/papers/attention-is-all-you-need|Transformer]], [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale|ViT]], [[wiki/sources/papers/deep-residual-learning-for-image-recognition|ResNet]]), the LLM revolution ([[wiki/sources/papers/gpt-4-technical-report|GPT-4]], [[wiki/sources/papers/llama-2-open-foundation-and-fine-tuned-chat-models|Llama 2]], [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models|LoRA]], [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models|Chain-of-Thought]]), vision-language breakthroughs ([[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision|CLIP]], [[wiki/sources/papers/visual-instruction-tuning|LLaVA]], [[wiki/sources/papers/segment-anything|SAM]]), and the cutting edge of embodied AI and autonomous driving.

The field has undergone three major shifts:

1. **Modular → End-to-End**: From perception-prediction-planning pipelines ([[wiki/sources/papers/planning-oriented-autonomous-driving|UniAD]] CVPR 2023 Best Paper, [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving|VAD]]) to unified architectures where [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving|DriveTransformer]] parallelizes all tasks in a single transformer and [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving|DiffusionDrive]] achieves real-time diffusion planning at 45 FPS.

2. **Imitation → RL**: From pure behavioral cloning to RL-enhanced planning where [[wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving|CarPlanner]] is the first RL planner to beat IL+rules on nuPlan, and [[wiki/sources/papers/pi06-a-vla-that-learns-from-experience|π₀.₆]] doubles robot task throughput via offline RL self-improvement.

3. **Task-specific → Generalist VLA**: From narrow models to Vision-Language-Action agents that generalize across embodiments — [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control|π₀]] (flow matching across 7 robots, 68 tasks), [[wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation|CrossFormer]] (one policy for 20+ embodiments including quadcopters), [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots|GR00T N1]], and [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world|Gemini Robotics]].

## Five research pillars

### 1. End-to-end autonomous driving

The perception→prediction→planning decomposition ([[wiki/concepts/perception]], [[wiki/concepts/prediction]], [[wiki/concepts/planning]]) is being collapsed. [[wiki/sources/papers/planning-oriented-autonomous-driving|UniAD]] unified it into one framework; [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving|DriveTransformer]] (ICLR 2025) parallelized all tasks; [[wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving|DriveGPT]] (Waymo, ICML 2025) proved LLM-style scaling laws hold for driving. Diffusion and flow-matching planners ([[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving|DiffusionDrive]], [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation|GoalFlow]]) displaced autoregressive methods, while [[wiki/sources/papers/navsim-data-driven-non-reactive-autonomous-vehicle-simulation|NAVSIM]] became the definitive evaluation benchmark with 143 teams. See [[wiki/concepts/end-to-end-architectures]].

### 2. Vision-language-action models

[[wiki/concepts/vision-language-action|VLA models]] matured from proof-of-concept to open-source infrastructure in 2024. [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model|OpenVLA]] (7B, 970K demos) outperforms the closed RT-2-X (55B) by 16.5%. [[wiki/sources/papers/octo-an-open-source-generalist-robot-policy|Octo]] was the first open generalist robot policy. [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control|π₀]] introduced flow matching for continuous 50 Hz control. The dual-system pattern (slow VLM reasoning at 7–10 Hz + fast motor control at 120–200 Hz) independently emerged at Google DeepMind, Physical Intelligence, NVIDIA, and Figure AI.

### 3. LLM reasoning for driving and robotics

LLMs transitioned from curiosity to structured cognitive agents. [[wiki/sources/papers/a-language-agent-for-autonomous-driving|Agent-Driver]] established the LLM-as-agent framework with tool use and chain-of-thought reasoning. [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering|DriveLM]] introduced graph-structured VQA reasoning. [[wiki/sources/papers/llms-cant-plan-but-can-help-planning-in-llm-modulo-frameworks|LLMs Can't Plan]] (ICML 2024) provided theoretical grounding for why LLMs should reason, not plan — pairing with external verifiers. [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models|ECoT]] increased VLA success by 28% through embodied reasoning.

### 4. Foundation models and cross-embodiment transfer

[[wiki/concepts/foundation-models|Foundation models]] proved cross-embodiment scaling works. [[wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation|CrossFormer]] (900K trajectories, 20+ embodiments) is the first single policy for manipulators, navigators, quadrupeds, and aerial vehicles. [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers|HPT]] demonstrated scaling laws for heterogeneous robot pretraining across 52 datasets. [[wiki/sources/papers/unisim-learning-interactive-real-world-simulators|UniSim]] enables zero-shot real-world transfer from learned simulators. The foundational stack — [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision|CLIP]], [[wiki/sources/papers/high-resolution-image-synthesis-with-latent-diffusion-models|Latent Diffusion]], [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models|LoRA]], [[wiki/sources/papers/mamba-linear-time-sequence-modeling-with-selective-state-spaces|Mamba]] — underpins all of it.

### 5. BEV perception and 3D occupancy

BEV-based 3D perception pivoted to Gaussians, sparsity, and world models. [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction|GaussianFormer]] replaced dense voxels with semantic Gaussians (75–82% memory reduction). [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving|OccWorld]] pioneered occupancy-based world models with GPT-like generation. [[wiki/sources/papers/sparseocc-fully-sparse-3d-occupancy-prediction|SparseOcc]] introduced the RayIoU metric that became the community standard. [[wiki/sources/papers/selfocc-self-supervised-vision-based-3d-occupancy-prediction|SelfOcc]] eliminated the annotation bottleneck with self-supervised training. See [[wiki/concepts/perception]].

## The foundational ML stack

The wiki also covers the papers that made all of the above possible:

| Era | Key papers |
|-----|-----------|
| **Architecture** | [[wiki/sources/papers/attention-is-all-you-need\|Transformer]] (91K+ cit.), [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale\|ViT]] (91K+), [[wiki/sources/papers/swin-transformer-hierarchical-vision-transformer-using-shifted-windows\|Swin]] (44K+), [[wiki/sources/papers/deep-residual-learning-for-image-recognition\|ResNet]] |
| **Language models** | [[wiki/sources/papers/gpt-4-technical-report\|GPT-4]] (26K+), [[wiki/sources/papers/llama-2-open-foundation-and-fine-tuned-chat-models\|Llama 2]] (22K+), [[wiki/sources/papers/mistral-7b\|Mistral 7B]], [[wiki/sources/papers/mixtral-of-experts\|Mixtral]] |
| **Vision-language** | [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision\|CLIP]] (58K+), [[wiki/sources/papers/visual-instruction-tuning\|LLaVA]] (13K+), [[wiki/sources/papers/segment-anything\|SAM]] (19K+), [[wiki/sources/papers/flamingo-a-visual-language-model-for-few-shot-learning\|Flamingo]] |
| **Generative** | [[wiki/sources/papers/high-resolution-image-synthesis-with-latent-diffusion-models\|Latent Diffusion]] (32K+), [[wiki/sources/papers/denoising-diffusion-probabilistic-models\|DDPM]], [[wiki/sources/papers/diffusion-models-beat-gans-on-image-synthesis\|Diffusion Beats GANs]] |
| **Efficiency** | [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models\|LoRA]] (29K+), [[wiki/sources/papers/qlora-efficient-finetuning-of-quantized-language-models\|QLoRA]], [[wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation\|Prefix-Tuning]] |
| **Alignment** | [[wiki/sources/papers/training-language-models-to-follow-instructions-with-human-feedback\|InstructGPT]] (24K+), [[wiki/sources/papers/direct-preference-optimization-your-language-model-is-secretly-a-reward-model\|DPO]], [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models\|Chain-of-Thought]] (27K+) |
| **Agents** | [[wiki/sources/papers/react-synergizing-reasoning-and-acting-in-language-models\|ReAct]] (8K+), [[wiki/sources/papers/toolformer-language-models-can-teach-themselves-to-use-tools\|Toolformer]] |

## What the wiki answers

- Which papers are actually foundational, and why?
- Which benchmarks are over-indexed relative to real deployment value?
- Where do modular systems still dominate?
- What does "end-to-end" mean in each paper, exactly?
- How should VLM/VLA progress in robotics be interpreted for autonomous driving?
- Which open problems are bottlenecked by data, simulation, evaluation, or architecture?

## Navigation

| Section | Description |
|---------|-------------|
| [[wiki/taxonomies/research-map]] | Field breakdown across research directions |
| [[wiki/concepts/vision-language-action]] | VLA evolution from CIL to π₀ — the core action paradigm |
| [[wiki/sources/ilya-top-30]] | Ilya's curated 30-paper curriculum on deep learning foundations |
| [[wiki/sources/vla-and-driving]] | 90+ driving and robotics VLA papers organized by wave |
| [[wiki/syntheses/research-thesis]] | Current high-level thesis with evidence for and against |
| [[wiki/queries/open-questions]] | 15 active research questions with partial answers |
| [[wiki/comparisons/modular-vs-end-to-end]] | The core systems architecture debate |

