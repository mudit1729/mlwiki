---
title: Foundation Models
type: concept
status: active
updated: 2026-04-05
tags:
  - llm
  - vlm
  - foundation-models
---

# Foundation Models

Foundation models -- large models pretrained on broad data and adapted to downstream tasks -- are reshaping autonomous driving. This page tracks how LLMs, VLMs, and diffusion models influence autonomy, and examines the emerging "everything as language" paradigm.

## Core foundation model ideas

### The transformer and scaling

[[wiki/sources/papers/attention-is-all-you-need]] (2017) introduced the transformer, which replaced recurrence with self-attention and enabled the scaling that defines modern AI. [[wiki/sources/papers/scaling-laws-for-neural-language-models]] (Kaplan et al., 2020) showed that language model loss follows predictable power laws in compute, data, and parameters. [[wiki/sources/papers/training-compute-optimal-large-language-models]] (Chinchilla, 2022) refined this, demonstrating that most models were undertrained for their size.

These scaling insights drive the foundation-model approach to driving: if enough data and compute produce general-purpose intelligence in language, perhaps the same recipe works for embodied control.

### Large language models

[[wiki/sources/papers/language-models-are-few-shot-learners]] (GPT-3, 2020) demonstrated that sufficiently large language models exhibit emergent capabilities: few-shot learning, instruction following, and reasoning without task-specific fine-tuning. [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] (BERT, 2018) established bidirectional pretraining for representation learning. Together, they defined the pretrain-then-adapt paradigm.

For driving, LLMs serve multiple roles: as reasoning engines (GPT-Driver, DriveGPT4), as planners (EMMA), as explanation generators, and as data augmentation tools. Adapting these large models efficiently is a critical concern: [[wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation]] (2021) introduced continuous prefix optimization as a parameter-efficient alternative to full fine-tuning, training only 0.1% of parameters while matching full fine-tuning performance. This work helped launch the PEFT paradigm that now underpins most foundation model adaptation. [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models]] (LoRA, ICLR 2022) became the dominant method: by injecting trainable low-rank matrices (Delta-W = BA, rank r << d) alongside frozen pretrained weights, LoRA reduces trainable parameters by 10,000x on GPT-3 175B while matching full fine-tuning performance, with zero inference overhead since the low-rank updates merge into the base weights. LoRA is now the default adaptation method for driving VLA systems that fine-tune frozen VLMs for embodied control.

### Vision-language models and self-supervised vision

[[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] (CLIP, 2021) showed that contrastive pretraining on image-text pairs produces visual representations that generalize across tasks without fine-tuning. CLIP-style encoders now serve as the visual backbone for many driving VLMs. [[wiki/sources/papers/flamingo-a-visual-language-model-for-few-shot-learning]] (Flamingo, 2022) extended in-context few-shot learning from text to the multimodal domain by connecting a frozen contrastive vision encoder and a frozen LM (Chinchilla 70B) through a Perceiver Resampler and gated cross-attention layers. Flamingo established the architectural template -- frozen backbone with lightweight trainable bridges -- that PaLM-E, GPT-4V, and subsequent VLMs adopted, and demonstrated that multimodal few-shot learning is viable without any fine-tuning. Earlier, [[wiki/sources/papers/exploring-simple-siamese-representation-learning]] (SimSiam, 2021) demonstrated that self-supervised visual pretraining requires neither negative pairs nor momentum encoders -- just a Siamese network with stop-gradient -- clarifying the minimal ingredients for representation learning that foundation models build upon. [[wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale]] (ViT, 2020) demonstrated that pure transformer architectures work for vision, enabling unified transformer pipelines from pixels to actions. [[wiki/sources/papers/emerging-properties-in-self-supervised-vision-transformers]] (DINO, 2021) showed that self-supervised training of ViTs via self-distillation produces features with emergent properties -- self-attention maps that perform semantic segmentation without pixel-level supervision, and features that achieve 77.4% ImageNet k-NN accuracy. DINO established self-supervised ViTs as a foundation for visual representation learning, directly inspiring DINOv2 which is now widely adopted in robotics and driving systems. [[wiki/sources/papers/blip-bootstrapping-language-image-pre-training-for-unified-vision-language-understanding-and-generation]] (BLIP, 2022) unified vision-language understanding and generation in a single model via its Multimodal mixture of Encoder-Decoder (MED) architecture, and introduced CapFilt -- a bootstrapping method that uses synthetic caption generation and filtering to clean noisy web data. BLIP bridged the gap between contrastive-only models (CLIP) and generative models, achieving SOTA on retrieval, captioning, and VQA simultaneously, and influenced subsequent systems like BLIP-2 and InstructBLIP.

### Visual instruction tuning

[[wiki/sources/papers/visual-instruction-tuning]] (LLaVA, NeurIPS 2023) demonstrated that connecting a frozen CLIP ViT-L/14 vision encoder to a Vicuna LLM through a simple linear projection layer, then training on GPT-generated multimodal instruction data, produces a powerful general-purpose visual assistant. LLaVA's two-stage recipe (Stage 1: align projection on captions; Stage 2: end-to-end fine-tune on 158K instruction samples) became the dominant blueprint for open-source multimodal models. Its GPT-assisted data generation pipeline -- converting existing image annotations into diverse instruction-following samples without the teacher model seeing images -- showed that synthetic data generation can bootstrap multimodal capabilities cheaply. With ~13,500 citations, LLaVA's architecture directly influenced the design of driving and robotics VLMs that adapt frozen VLM backbones for embodied tasks.

### Vision foundation models for dense prediction

[[wiki/sources/papers/segment-anything]] (SAM, 2023) extended the foundation model paradigm to dense prediction by defining a promptable segmentation task: given any combination of points, boxes, masks, or text, SAM produces valid segmentation masks. Trained on 1.1 billion masks (SA-1B dataset) via a three-stage data engine, SAM demonstrated strong zero-shot transfer across 23 segmentation benchmarks without task-specific fine-tuning. SAM's architecture -- a MAE-pretrained ViT-H image encoder paired with a lightweight transformer mask decoder -- enables real-time interactive use. The model spawned a large ecosystem of derivative work across medical imaging, remote sensing, video segmentation, and 3D scene understanding, and its data engine approach (using the model to generate its own training data) became an influential paradigm for scaling annotation.

### Chain-of-thought reasoning

[[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] (2022) showed that eliciting intermediate reasoning steps dramatically improves LLM performance on complex tasks. This idea is central to driving applications: rather than mapping directly from perception to action, systems decompose the driving decision into explicit reasoning stages.

### Diffusion models

[[wiki/sources/papers/denoising-diffusion-probabilistic-models]] (2020) established diffusion as a powerful generative framework. [[wiki/sources/papers/high-resolution-image-synthesis-with-latent-diffusion-models]] (LDM/Stable Diffusion, 2022) made diffusion practical by moving the denoising process to a compressed latent space, achieving 2.7x faster inference with better FID scores. LDM's cross-attention conditioning mechanism enabled flexible text-to-image, layout-to-image, and inpainting from a single architecture, and its open release as Stable Diffusion democratized high-quality image generation. In autonomy, diffusion models are used for trajectory generation (representing multimodal futures as denoising processes), scene generation (synthetic training data), and world modeling (predicting future scenes for planning).

## Foundation models in driving

### LLM-as-planner

[[wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt]] reformulates motion planning as a language modeling problem, representing trajectories as coordinate tokens that GPT produces autoregressively. [[wiki/sources/papers/drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model]] uses an LLM to generate both driving actions and natural language explanations. These early systems demonstrated feasibility but were evaluated only open-loop.

### VLM-based driving systems

[[wiki/sources/papers/drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states]] aligns multimodal LLMs with behavioral planning states, showing that VLMs can produce structured planning outputs. [[wiki/sources/papers/vlp-vision-language-planning-for-autonomous-driving]] uses vision-language pretraining for planning, leveraging CLIP-style representations for scene understanding.

### The "everything as language" paradigm

[[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] (EMMA) represents the logical extreme: all driving inputs and outputs are language tokens, including camera images (via a vision encoder), route instructions, 3D detection queries, and trajectory waypoints. EMMA treats autonomous driving as a visual question answering problem. This approach leverages the full power of VLM pretraining but raises questions about whether continuous physical quantities (trajectories, velocities) are well-served by discrete tokenization.

### Reasoning-to-action systems

The most recent work bridges foundation model reasoning with continuous control:

- [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]] introduces chain-based reasoning that decomposes driving into perception, prediction, and decision steps before action.
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] structures reasoning as graph-based QA, providing interpretable intermediate states.
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] decouples VLM reasoning from action generation, using the VLM as a "thinking" module whose outputs inform a separate planner.
- [[wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving]] demonstrates that RL can improve reasoning quality beyond what supervised training achieves.

### World foundation models

[[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai]] (Cosmos, 2025) extends the foundation model paradigm to world simulation. Rather than understanding or generating language, Cosmos generates high-fidelity video predictions of physical environments. Trained on 10K H100 GPUs with 100M curated video clips, the platform provides both diffusion-based and autoregressive world models that can be fine-tuned for autonomous driving scene generation, robotic manipulation prediction, and camera view synthesis. This addresses a critical bottleneck: the scarcity of safe, high-quality training data for physical AI.

### Robotics foundation models

[[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]] (GR00T N1, 2025) and [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]] (Gemini Robotics, 2025) extend foundation models to direct physical control. Both leverage web-scale multimodal pretraining and fine-tune for robotic action generation, demonstrating that the pretrain-then-adapt recipe transfers from language to embodied domains.

## What foundation models add to driving

1. **World knowledge:** VLMs pretrained on internet-scale data understand traffic signs, road markings, weather conditions, and cultural driving norms without explicit annotation.
2. **Reasoning capability:** Chain-of-thought and instruction-following abilities enable structured decision decomposition.
3. **Language interface:** Natural language provides an interpretable intermediate representation between perception and action, aiding debugging and regulatory compliance.
4. **Data efficiency:** Pretrained representations reduce the amount of driving-specific data needed for competent performance.
5. **Generalization:** Foundation models generalize to novel scenarios (unusual road configurations, unfamiliar objects) better than task-specific models.

## Present state and open problems

- **Latency:** Foundation models with billions of parameters are difficult to run in real-time. Distillation, quantization, and early-exit strategies are active areas.
- **Hallucination:** LLMs/VLMs can generate confident but incorrect scene descriptions or trajectory predictions. In driving, hallucination can be fatal.
- **Grounding:** Foundation models may produce linguistically fluent reasoning that is not actually grounded in the visual scene. Ensuring perceptual grounding is critical.
- **Safety alignment:** RLHF and constitutional AI techniques from language models do not directly transfer to safety-critical physical systems. Driving-specific alignment is needed.
- **Tokenization of physical quantities:** Whether discretizing continuous trajectories into tokens loses essential information (smoothness, curvature continuity) is contested.
- **Scaling laws for driving:** Whether the compute-optimal scaling relationships from language transfer to driving data and driving performance is unknown and important.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/attention-is-all-you-need]] | Transformer architecture |
| [[wiki/sources/papers/scaling-laws-for-neural-language-models]] | Scaling laws for neural LMs |
| [[wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision]] | CLIP: contrastive vision-language pretraining |
| [[wiki/sources/papers/segment-anything]] | SAM: promptable segmentation foundation model, SA-1B dataset |
| [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]] | Chain-of-thought reasoning |
| [[wiki/sources/papers/language-models-are-few-shot-learners]] | GPT-3: emergent few-shot capabilities |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Everything-as-language driving |
| [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] | Decoupled VLM reasoning for driving |
| [[wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt]] | LLM-as-planner for driving |
| [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] | Diffusion models for generation |
| [[wiki/sources/papers/high-resolution-image-synthesis-with-latent-diffusion-models]] | Latent diffusion: efficient high-resolution generation via compressed latent space |
| [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]] | Chain-based reasoning for driving |
| [[wiki/sources/papers/drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states]] | VLM aligned with behavioral planning |
| [[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai]] | World foundation model platform |
| [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]] | Open foundation model for humanoid robots |
| [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]] | Gemini 2.0 for physical robotics |
| [[wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation]] | Self-supervised MLLM scaling for driving without annotations |
| [[wiki/sources/papers/self-improving-embodied-foundation-models]] | Self-improving EFMs via autonomous RL practice |
| [[wiki/sources/papers/autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents]] | Foundation model orchestration for robot data collection at scale |
| [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]] | Cross-embodiment scaling laws via heterogeneous pre-trained transformers |

## Related

- [[wiki/concepts/machine-learning]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/sources/vla-and-driving]]
