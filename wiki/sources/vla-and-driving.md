---
title: VLA and Driving
type: source-program
status: active
updated: 2026-04-05
tags:
  - sources
  - vla
  - vlm
  - driving
---

# VLA and Driving

This queue spans general VLA foundations and driving-specific multimodal action papers. The AutoVLA corpus (18 papers, 2018–2025) provides the most comprehensive coverage of how language-vision models have been applied to autonomous driving.

## General VLA / multimodal action foundations

- Gato
- PaLM-E
- RT-1
- RT-2
- RoboCat
- Octo
- OpenVLA
- UniAct
- Dita
- SmolVLA
- **pi0** (Physical Intelligence, 2024) -- flow matching VLA on PaliGemma 3B, 7 platforms, 68 tasks. The reference VLA.
- **pi0.5** (Physical Intelligence, CoRL 2025) -- hierarchical VLA with open-world generalization, 10-15 min tasks in unseen homes
- **pi0.6** (Physical Intelligence, 2025) -- RECAP offline RL for VLA self-improvement, doubled task throughput over imitation
- **FAST** (Physical Intelligence / UC Berkeley, RSS 2025) -- DCT+BPE action tokenizer, 5x faster VLA training
- **OpenVLA-OFT** (Stanford, 2025) -- parallel decoding fine-tuning recipe, 76.5% -> 97.1% on LIBERO, 26x speedup
- **SpatialVLA** (Shanghai AI Lab, 2025) -- Ego3D position encoding for spatial awareness, 1.1M real episodes
- **DexVLA** (Shanghai Jiao Tong, CoRL 2025) -- 1B diffusion expert for dexterous/bimanual manipulation, 0.92 shirt folding
- **Knowledge Insulation** (Physical Intelligence, NeurIPS 2025 Spotlight) -- prevents VLM degradation during VLA training, 7.5x faster convergence
- **VoxPoser** ([[wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models]], CoRL 2023) -- LLM-generated 3D value maps for zero-shot manipulation via code composition + MPC, no robot-specific training

## Driving-specific language and action papers

### Wave 1: Foundations (2018–2019)

- **Conditional Imitation Learning** (Codevilla et al., 2018) — route-conditioned E2E driving, branched architecture
- **Textual Explanations for Self-Driving** (Kim et al., 2018) — BDD-X dataset, attention-aligned explanations
- **Talk2Car** (Deruyttere et al., 2019) — natural language command grounding on nuScenes

### Wave 2: LLM-as-Planner (2023–2024)

- **GPT-Driver** (Mao et al., 2023) — planning as language modeling via GPT-3.5
- **Agent-Driver** (Mao et al., ICLR 2024) — LLM as cognitive agent with tool library, cognitive memory, and chain-of-thought reasoning for driving
- **DriveGPT4** (Xu et al., 2024) — multimodal instruction tuning for joint control + explanation
- **LMDrive** (Shao et al., 2024) — first closed-loop language-conditioned driving
- **VLP** (Pan et al., 2024) — LM semantic priors in BEV planning
- **DriveLM** (Sima et al., 2024) — Graph VQA decomposing perception→prediction→planning
- **Reason2Drive** (Nie et al., 2024) — large-scale video-text reasoning chains
- **DriveMLM** (Wang et al., 2023) — plug-and-play LLM for behavioral planning
- **Drive as You Speak** (Cui et al., 2023) — LLM as bidirectional human-vehicle interaction interface, not planner
- **Talk2Drive** (Cui et al., IEEE ITSC 2024) — LLM-based personalized driving via memory module, real-world deployment, 65.2% takeover reduction
- **Driving with LLMs** (Wayve, 2023) — first concrete LLM-for-driving with vector modality, explainable AD
- **Senna** (Jiang et al., 2024) — decoupled LVLM reasoning + E2E trajectory prediction
- DriveVLM
- VAD
- **VADv2** (Chen et al., 2024) — probabilistic planning via action vocabulary, LLM-inspired next-action prediction, CARLA SOTA
- **GenAD** (2024) — E2E driving as generative trajectory modeling, 0.91m L2, 0.43% collision
- **PARA-Drive** (NVIDIA, 2024) — fully parallel E2E architecture, systematic design space exploration
- **DriveDreamer** (2023) — first real-world-driven world model for driving, diffusion-based video generation
- **Is Ego Status All You Need?** (NVIDIA/Nanjing, 2023) — exposes weakness of open-loop nuScenes evaluation

### Wave 3: Reasoning-to-Action (2025)

- **SimLingo** (Renz et al., 2025) — vision-only closed-loop VLA with Action Dreaming
- **ORION** (Fu et al., 2025) — holistic reasoning→planning via QT-Former + planning token
- **EMMA** (Hwang et al., 2025) — Waymo industry-scale "everything as language" model
- **Alpamayo-R1** (Wang et al., 2025) — NVIDIA production VLA, 99ms latency, real road testing
- **WoTE** (Li et al., 2025) — BEV world model for online trajectory evaluation
- **AlphaDrive** (Jiang et al., 2025) — GRPO-based RL for driving VLMs (DeepSeek R1-style)
- **DriveMoE** (Yang et al., 2025) — Mixture-of-Experts for scene/skill specialization
- **AutoVLA** (UCLA, 2025) — dual-process adaptive reasoning VLA with RL fine-tuning
- **DriveTransformer** (2025, ICLR) — unified parallel-task transformer, sparse queries, SOTA Bench2Drive
- **OpenDriveVLA** (2025) — open-source VLA with 3D spatial-aware hierarchical scene queries (0.5B-7B)
- **DiMA** (2025) — distill MLLM reasoning into efficient vision planner, discard LLM at inference
- **MomAD** (2025) — momentum-aware planning for temporal consistency in E2E driving
- **HERMES** (2025) — unified world model for simultaneous 3D scene understanding and generation
- **GaussianWorld** (2024) — Gaussian world model for streaming 3D occupancy prediction
- **DiffusionDrive** (HUST/Horizon, 2025) — truncated diffusion for E2E planning, 88.1 PDMS, 2 steps, 45 FPS
- **DriveGPT** (Waymo, 2025) — first scaling laws for driving, 1.1B autoregressive behavior model
- **GoalFlow** (Horizon/HKU, 2025) — goal-driven flow matching, 90.3 PDMS, single-step inference
- **LAW** (CASIA, 2025) — self-supervised latent world model for E2E driving, SOTA nuScenes+NAVSIM+CARLA
- **CarPlanner** (ZJU, 2025) — first RL planner to beat IL+rules on nuPlan, consistency-regularized AR
- **SOLVE** (HUST, 2025) — Sequential Q-Former + Trajectory CoT, VLM-E2E synergy

## Key design axes (from AutoVLA analysis)

| Axis | Options seen in corpus |
|------|----------------------|
| Language role | supervision / runtime control / explanation / all three |
| Action space | waypoints / controls / planner tokens / language tokens |
| Evaluation | open-loop only / closed-loop sim / real-world |
| Architecture | VLM + planner hook / true VLA / decoupled reasoning + E2E |
| Training | IL only / IL + RL / GRPO / multi-stage |

## Questions to answer while ingesting

- Is language used for supervision, runtime control, explanation, or all three?
- What is the action space?
- Does the paper improve actual planning, or mainly interpretation and interface quality?
- Is the system a VLM with planner hooks, or a true VLA model?
- Open-loop or closed-loop evaluation?
- Does it handle long-tail / adversarial scenarios?

## Warning

This area is recent and terminology is unstable. The wiki should be stricter than the papers are about the difference between vision-language reasoning and action generation.

## Ingested papers

### Batch 01 (general VLA + early driving)

- [[wiki/sources/papers/a-generalist-agent]]
- [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]]
- [[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model]]
- [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]]
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]]
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]]
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]]
- [[wiki/sources/papers/drivevlm-the-convergence-of-autonomous-driving-and-large-vision-language-models]]

### Batch 02 (AutoVLA corpus)

- [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]]
- [[wiki/sources/papers/textual-explanations-for-self-driving]]
- [[wiki/sources/papers/talk2car]]
- [[wiki/sources/papers/gpt-driver]]
- [[wiki/sources/papers/drivegpt4]]
- [[wiki/sources/papers/vlp-vision-language-planning]]
- [[wiki/sources/papers/reason2drive]]
- [[wiki/sources/papers/simlingo]]
- [[wiki/sources/papers/orion]]
- [[wiki/sources/papers/emma]]
- [[wiki/sources/papers/drivemlm]]
- [[wiki/sources/papers/alpamayo-r1]]
- [[wiki/sources/papers/senna]]
- [[wiki/sources/papers/wote-bev-world-model]]
- [[wiki/sources/papers/alphadrive]]
- [[wiki/sources/papers/drivemoe]]
- [[wiki/sources/papers/drivor-driving-on-registers]]

### Batch 03 (robotics VLA + world models + driving)

- [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]]
- [[wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world]]
- [[wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai]]
- [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]]
- [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]]

### Batch 04 (self-supervised driving, temporal E2E, BEV perception, world models, embodied RL)

- [[wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation]]
- [[wiki/sources/papers/bridgead-bridging-past-and-future-end-to-end-autonomous-driving-with-historical-prediction]]
- [[wiki/sources/papers/self-improving-embodied-foundation-models]]
- [[wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting]]
- [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]]

### Batch 05 (VLA, world models, momentum planning, distillation)

- [[wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model]]
- [[wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation]]
- [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]]
- [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]]
- [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]]

### Batch 06 (cross-embodiment robotics VLA + 3D occupancy perception)

- [[wiki/sources/papers/uniact-universal-actions-for-enhanced-embodied-foundation-models]]
- [[wiki/sources/papers/dita-scaling-diffusion-transformer-for-generalist-vla-policy]]
- [[wiki/sources/papers/embodiment-scaling-laws-in-robot-locomotion]]
- [[wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics]]
- [[wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction]]
- [[wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models]]
- [[wiki/sources/papers/gausstr-foundation-model-aligned-gaussian-transformer-for-self-supervised-3d]]
- [[wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising]]

### Batch 06 (diffusion/flow planning, scaling laws, RL planning, VLM-E2E synergy, robotics VLA/diffusion)

- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]]
- [[wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving]]
- [[wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation]]
- [[wiki/sources/papers/law-enhancing-end-to-end-autonomous-driving-with-latent-world-model]]
- [[wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving]]
- [[wiki/sources/papers/solve-synergy-of-language-vision-and-end-to-end-networks-for-autonomous-driving]]
- [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models]]
- [[wiki/sources/papers/rdt-1b-a-diffusion-foundation-model-for-bimanual-manipulation]]

### Batch 07 (Physical Intelligence VLA family + robotics VLA advances)

- [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control]]
- [[wiki/sources/papers/pi05-a-vision-language-action-model-with-open-world-generalization]]
- [[wiki/sources/papers/pi06-a-vla-that-learns-from-experience]]
- [[wiki/sources/papers/fast-efficient-action-tokenization-for-vision-language-action-models]]
- [[wiki/sources/papers/openvla-oft-optimizing-speed-and-success-for-vla-fine-tuning]]
- [[wiki/sources/papers/spatialvla-exploring-spatial-representations-for-vla-models]]
- [[wiki/sources/papers/dexvla-vision-language-model-with-plug-in-diffusion-expert]]
- [[wiki/sources/papers/knowledge-insulating-vision-language-action-models]]

### Batch 08 (world models, parallel E2E, generative driving, evaluation, LLM-for-driving)

- [[wiki/sources/papers/drivedreamer-towards-real-world-driven-world-models]]
- [[wiki/sources/papers/para-drive-parallelized-architecture-for-real-time-autonomous-driving]]
- [[wiki/sources/papers/genad-generative-end-to-end-autonomous-driving]]
- [[wiki/sources/papers/is-ego-status-all-you-need-for-open-loop-end-to-end-autonomous-driving]]
- [[wiki/sources/papers/driving-with-llms-fusing-object-level-vector-modality-for-explainable-autonomous-driving]]
- [[wiki/sources/papers/drive-as-you-speak-enabling-human-like-interaction-with-large-language-models-in-autonomous-vehicles]]

### Batch 09 (orchestration, cross-embodiment, async planning, Gaussian representations, occupancy world models)

- [[wiki/sources/papers/autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents]]
- [[wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers]]
- [[wiki/sources/papers/asyncdriver-asynchronous-large-language-model-enhanced-planner-for-autonomous-driving]]
- [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]]
- [[wiki/sources/papers/driving-gaussian-composite-gaussian-splatting-for-surrounding-dynamic-driving-scenes]]
- [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]]
