---
title: Robotics
type: concept
status: active
updated: 2026-04-05
tags:
  - robotics
  - embodiment
---

# Robotics

Robotics is relevant to this wiki primarily as the origin of vision-language-action (VLA) models that now influence autonomous driving. The robotics community pioneered the idea that large pretrained models can serve as general-purpose controllers for embodied agents, and the driving community has rapidly adopted and adapted these ideas.

## The VLA revolution in robotics

The modern VLA trajectory begins with generalist agents and scales through increasingly capable architectures.

**Gato** ([[wiki/sources/papers/a-generalist-agent]], 2022) demonstrated that a single transformer, trained on a mixture of text, images, and control tokens, could play Atari, caption images, and control a robot arm. The key insight was not state-of-the-art performance on any single task but that a unified token-based architecture could handle heterogeneous modalities including actions. Gato established the "everything as tokens" paradigm that EMMA later brought to driving.

**RT-1** ([[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]], 2022) moved from proof-of-concept to real-world scale. Trained on 130k demonstrations across 700+ tasks, RT-1 showed that transformers could absorb large-scale robotic data and generalize across tasks when conditioned on language instructions. The architecture used a FiLM-conditioned EfficientNet backbone with a transformer trunk, outputting discretized actions.

**PaLM-E** ([[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model]], 2023) asked whether a large language model could serve as the reasoning backbone for an embodied agent. By injecting visual tokens into PaLM's 562B-parameter language model, PaLM-E demonstrated that LLM-scale pretraining transfers to robotic planning and that larger models exhibit positive transfer from language/vision tasks to embodied control.

**RT-2** ([[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]], 2023) completed the loop by fine-tuning a VLM (PaLI-X / PaLM-E) directly on robotic data, representing actions as text tokens. RT-2 showed dramatic generalization: the model could follow instructions involving concepts never seen in robot data, leveraging web-scale visual and linguistic knowledge. This established the VLA blueprint: pretrain large on web data, fine-tune on embodied data, emit actions as tokens.

**RoboCat** ([[wiki/sources/papers/robocat-a-self-improving-generalist-agent-for-robotic-manipulation]], 2023) took a complementary path to RT-2 by focusing on multi-embodiment generalization and self-improvement rather than web-scale pretraining. Building on the Gato architecture, RoboCat trained a single policy across 253 manipulation tasks on three real robot embodiments (Sawyer, Panda, KUKA), demonstrating that heterogeneous multi-robot data produces positive cross-task transfer. Its key innovation was an autonomous self-improvement loop: the trained model generates its own practice data, which is filtered for success and folded back into training, yielding measurable gains each iteration. RoboCat adapted to the unseen KUKA 14-DoF bimanual arm with ~80% success using only 100-1000 demonstrations, establishing that generalist robot policies can rapidly acquire new embodiments.

**OpenVLA** ([[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]], 2024) democratized VLA research by releasing an open-source 7B-parameter model trained on the Open X-Embodiment dataset. OpenVLA showed that the RT-2 paradigm works at smaller scale with open weights, enabling the broader research community to build on VLA foundations.

## Transfer from robotics to driving

Several ideas from the robotics VLA lineage now appear directly in driving systems:

- **Language-conditioned control:** RT-2's language-to-action paradigm maps to driving systems like [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]] and [[wiki/sources/papers/simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment]].
- **Action tokenization:** Gato's and RT-2's approach of discretizing actions as tokens is adopted by [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]].
- **VLM as reasoning backbone:** PaLM-E's architecture pattern appears in [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] and [[wiki/sources/papers/drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states]].
- **Large-scale behavior cloning:** RT-1's data scaling approach influences the push for larger driving datasets.

## Where transfer breaks

- **Safety criticality:** Driving has far less tolerance for exploratory failure than tabletop manipulation. A dropped object is recoverable; a collision at highway speed is not.
- **Multi-agent dynamics:** Robotic manipulation is typically single-agent. Driving involves continuous interaction with dozens of agents whose behavior is partially adversarial and only partially observable.
- **Temporal scale:** Robotic manipulation episodes are seconds to minutes. Driving requires sustained competence over hours with rare but critical events.
- **Evaluation standards:** Robotics evaluation often measures task success rate in controlled settings. Driving demands statistical safety arguments over millions of miles.

## The next frontier: humanoid robots and industry-scale VLA (2025)

**GR00T N1** ([[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]], 2025) extends the VLA paradigm to full humanoid robots through a dual-system architecture: a vision-language module (System 2) at 10Hz for reasoning and a diffusion transformer (System 1) at 120Hz for motor control. Its "data pyramid" integrates web video, synthetic data, and real demonstrations, achieving 76.8% success on GR-1 humanoid tasks. GR00T N1 is released as an open foundation model.

**Gemini Robotics** ([[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]], 2025) brings Google's Gemini 2.0 into physical robotics with a two-tier model family. Gemini Robotics-ER handles spatial reasoning while the full Gemini Robotics model operates as a VLA at 50Hz via a cloud-local hybrid architecture. It demonstrates over 80% success on diverse manipulation tasks and 79% on long-horizon tasks including origami folding, with cross-embodiment transfer to novel platforms.

**Cosmos** ([[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai]], 2025) provides the world model infrastructure that complements direct VLA approaches. By generating high-fidelity synthetic training data through diffusion and autoregressive world models, Cosmos addresses the data scarcity problem that limits embodied AI training.

## Self-improvement beyond imitation

**Self-Improving Embodied Foundation Models** ([[wiki/sources/papers/self-improving-embodied-foundation-models]], 2025) from Google DeepMind completes the LLM training pipeline analogy for robotics by adding an autonomous RL stage after supervised fine-tuning. The model learns a "steps-to-go" prediction that serves as a self-generated reward function, enabling robots to practice autonomously without manual reward engineering. Policies trained with just 10% imitation data plus 1% autonomous practice outperform 80% imitation-only baselines. Most notably, robots achieve true behavioral generalization, learning to manipulate novel objects (bananas) never seen in training by discovering effective strategies through self-play. This establishes that the pretrain-SFT-RL pipeline from language models transfers to embodied AI.

## Cross-embodiment and efficient VLA (2025)

**UniAct** ([[wiki/sources/papers/uniact-universal-actions-for-enhanced-embodied-foundation-models]], CVPR 2025) proposes a Universal Action Space via VQ codebooks (256 codes, 128-dim) that captures generic atomic behaviors shared across 28 robot embodiments. The 0.5B model outperforms 14x larger models (OpenVLA-7B) by solving the action heterogeneity problem at the representation level rather than scaling model size. 40% of codebook entries produce consistent, interpretable behaviors across platforms.

**Dita** ([[wiki/sources/papers/dita-scaling-diffusion-transformer-for-generalist-vla-policy]], ICCV 2025) scales diffusion transformers for cross-embodiment VLA with in-context conditioning: language, visual, and action tokens are processed in a unified causal Transformer sequence. At 334M parameters, Dita achieves 83.7% on SimplerEnv (vs OpenVLA's 16.3%) and adapts to real-world Franka tasks with just 10-shot fine-tuning.

**SmolVLA** ([[wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics]], 2025) from Hugging Face demonstrates that a 450M-parameter VLA with Flow Matching, layer skipping, and asynchronous inference can match 3.3B models (78.3% vs 61.7% on real-world tasks) while training on a single GPU. This makes practical VLA research accessible without large compute budgets.

**Embodiment Scaling Laws** ([[wiki/sources/papers/embodiment-scaling-laws-in-robot-locomotion]], CoRL 2025) provides the first empirical evidence that training on diverse morphologies follows power-law scaling for generalization to unseen robots. Using ~1,000 procedurally generated embodiments (GENBOT-1K), the work achieves zero-shot sim-to-real transfer to Unitree Go2 and H1 hardware.

## Data collection and orchestration at scale

**AutoRT** ([[wiki/sources/papers/autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents]], 2024) from Google DeepMind addresses the data scarcity bottleneck from a different angle: instead of using foundation models as controllers, it uses VLMs and LLMs as intelligent orchestrators of large-scale robot data collection. Over 7 months, AutoRT deployed 53 robots across 4 buildings, collecting 77,000 episodes with 6,650+ unique tasks. A "Robot Constitution" (inspired by constitutional AI) ensures safe task generation, improving safety from 26% to 87% under adversarial testing. One human can supervise 3-5 robots simultaneously.

**HPT** ([[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]], NeurIPS 2024) provides the architecture for consuming such heterogeneous data. Its modular stem-trunk-head design processes diverse proprioceptive and visual inputs through embodiment-specific stems into a shared transformer trunk (up to 1B+ parameters). HPT demonstrates clear scaling laws for robotics: performance improves predictably with data size, diversity, model size, and compute. This is among the first evidence that the language model scaling paradigm transfers to robotic control, with 10-30% gains in simulation and 20%+ gains on real robot tasks.

## Present state and open problems

- **Scale gap:** Robotics VLA datasets (Open X-Embodiment: ~1M episodes) are orders of magnitude smaller than language pretraining corpora. Whether VLA scaling laws mirror language scaling laws is unknown, though embodiment scaling laws are now emerging.
- **Sim-to-real:** Both robotics and driving face sim-to-real transfer challenges, but the domains have developed largely separate simulation ecosystems. Embodiment scaling work shows promising zero-shot transfer.
- **Action space design:** The optimal action representation (continuous vs. discretized tokens vs. VQ codebooks vs. diffusion) remains contested. UniAct's universal actions and Dita's continuous diffusion offer competing paradigms.
- **Real-time inference:** Large VLA models (7B+ parameters) struggle with real-time control. SmolVLA demonstrates that compact models with async inference can match larger ones, suggesting architecture design matters more than scale.
- **Cross-embodiment transfer:** Whether a single VLA can control both a robot arm and a vehicle remains speculative but increasingly plausible, with UniAct covering 28 embodiments and scaling laws showing positive transfer across morphology classes.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/a-generalist-agent]] | Gato: single transformer for heterogeneous tasks including control |
| [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]] | Large-scale real-world robotic control via transformers |
| [[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model]] | LLM-scale model as embodied reasoning backbone |
| [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] | VLM fine-tuned for robotic action, web knowledge transfer |
| [[wiki/sources/papers/robocat-a-self-improving-generalist-agent-for-robotic-manipulation]] | Multi-embodiment generalist with self-improvement loop, 253 tasks |
| [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] | Open-source 7B VLA model |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Driving system adopting robotics-style action tokenization |
| [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]] | Language-conditioned closed-loop driving |
| [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] | VLM reasoning backbone for driving |
| [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]] | Open dual-system VLA for humanoid robots |
| [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]] | Industry-scale VLA from Gemini 2.0 |
| [[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai]] | World foundation model platform for physical AI |
| [[wiki/sources/papers/self-improving-embodied-foundation-models]] | Self-improving EFMs via steps-to-go RL, behavioral generalization |
| [[wiki/sources/papers/uniact-universal-actions-for-enhanced-embodied-foundation-models]] | Universal action space via VQ codebooks for cross-embodiment VLA |
| [[wiki/sources/papers/dita-scaling-diffusion-transformer-for-generalist-vla-policy]] | DiT-based VLA with in-context conditioning, 10-shot adaptation |
| [[wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics]] | 450M VLA competitive with 10x larger models, async inference |
| [[wiki/sources/papers/embodiment-scaling-laws-in-robot-locomotion]] | First embodiment scaling laws across ~1000 robot morphologies |
| [[wiki/sources/papers/autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents]] | Foundation model orchestration for large-scale robot data collection |
| [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]] | Cross-embodiment scaling laws via stem-trunk-head architecture |
| [[wiki/sources/papers/video-prediction-policy-a-generalist-robot-policy-with-predictive-visual-representations]] | Video diffusion as predictive encoder for robot policies (ICML 2025 Spotlight) |
| [[wiki/sources/papers/helix-a-vla-for-generalist-humanoid-control]] | Dual-system VLA for 35-DoF humanoid control at 200Hz (Figure AI) |
| [[wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models]] | Zero-shot manipulation via LLM-composed 3D value maps + MPC (CoRL 2023) |

## Related

- [[wiki/concepts/vision-language-action]]
- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/end-to-end-architectures]]
