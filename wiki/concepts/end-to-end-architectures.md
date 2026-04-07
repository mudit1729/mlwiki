---
title: End to End Architectures
type: concept
status: active
updated: 2026-04-05
tags:
  - e2e
  - systems
---

# End-to-End Architectures

"End-to-end" is one of the most overloaded terms in autonomous driving. This page defines a clear taxonomy, traces the evolution of E2E systems, and maps the current landscape.

## Taxonomy

The literature uses "end-to-end" to mean at least four distinct things. This wiki adopts the following classification:

### Type 1: Direct perception-to-control

A single network maps raw sensor input directly to steering and throttle commands. No intermediate representations are exposed. The original NVIDIA self-driving paper [[wiki/sources/papers/end-to-end-learning-for-self-driving-cars]] (2016) is the canonical example: a CNN maps front-camera images to steering angle. Simple and elegant but brittle, uninterpretable, and difficult to debug.

### Type 2: Conditional imitation learning

The network maps sensor input to actions conditioned on a high-level command (turn left, go straight, follow lane). [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]] (CIL, 2018) introduced this approach, showing that simple command conditioning dramatically improves navigation capability over unconditioned direct control. The command provides a minimal interface between route planning and low-level control.

### Type 3: Jointly trained modular systems

The system preserves interpretable intermediate representations (3D detections, agent futures, BEV maps) but trains all modules jointly through a shared loss. [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD, 2023) is the landmark example: it maintains explicit perception, prediction, and planning stages but optimizes them jointly with a planning-centric objective. [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] (VAD) follows the same philosophy with vectorized representations.

### Type 4: VLA / foundation model systems

A large pretrained model (typically a VLM) processes sensor input and produces driving actions, often as tokens. The boundary between perception, prediction, and planning is dissolved into the model's internal representations. [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] (EMMA) is the purest example, treating all outputs including trajectories as language tokens.

## Historical evolution

### The imitation learning era (2016--2020)

[[wiki/sources/papers/end-to-end-learning-for-self-driving-cars]] demonstrated that CNNs can learn to steer from camera images alone. [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]] added command conditioning. [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]] introduced data augmentation for robust imitation. [[wiki/sources/papers/learning-by-cheating]] established the privileged distillation paradigm that became standard on the [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] benchmark.

A key lesson from this era: naive behavior cloning suffers from distributional drift. The agent encounters states not in the training distribution and compounds errors. DAgger-style approaches, data augmentation (ChauffeurNet), and privileged distillation (Learning by Cheating) are all responses to this fundamental problem.

### The joint training era (2022--2024)

[[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] (TransFuser) showed that transformer-based fusion of camera and LiDAR features enables effective end-to-end driving in CARLA. [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) demonstrated that joint training with interpretable intermediate supervision outperforms both fully modular and fully black-box approaches. [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] (VAD) showed the same approach works efficiently with vectorized representations.

### The VLA era (2024--present)

The current wave applies foundation models to driving. Key architectural variants:

- **Unified token models:** [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] encodes everything (perception queries, trajectory waypoints, scene descriptions) as tokens in a single VLM.
- **Decoupled reasoning + planning:** [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] separates VLM reasoning from a lightweight E2E planner, preserving interpretability.
- **Language-instructed action:** [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] uses planning tokens to bridge VLM understanding and continuous action generation.
- **Language as runtime interface:** [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]] accepts natural language navigation instructions at runtime. [[wiki/sources/papers/simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment]] aligns language and action representations for vision-only driving.
- **Adaptive reasoning VLA:** [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]] dynamically switches between fast (direct action) and slow (chain-of-thought) reasoning based on scenario complexity, with RL fine-tuning.
- **Parallel task transformer:** [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]] replaces sequential pipelines with parallel task processing through shared attention, achieving SOTA closed-loop performance with sparse queries.
- **3D-grounded VLA:** [[wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model]] integrates hierarchical 3D scene queries (global, agent, map) into an LLM backbone, achieving SOTA at 0.5B scale.
- **Distilled VLA:** [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] jointly trains a vision planner with an MLLM, then discards the LLM at inference -- achieving 80% collision reduction with zero inference overhead.
- **Explanation-oriented:** [[wiki/sources/papers/drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model]] and [[wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt]] use LLMs primarily for generating interpretable driving explanations and plans.
- **Structured reasoning:** [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] uses graph-structured QA to decompose driving into interpretable reasoning chains. [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]] applies chain-of-thought reasoning to driving decisions.

## Design trade-offs

| Trade-off | Type 1-2 (Direct/CIL) | Type 3 (Joint modular) | Type 4 (VLA) |
|-----------|----------------------|----------------------|--------------|
| Interpretability | None / minimal | High (explicit intermediates) | Variable (depends on architecture) |
| Debugging | Difficult | Module-level | Difficult |
| Data efficiency | Low | Moderate | High (pretrained backbone) |
| Benchmark performance | Moderate | Strong | State-of-the-art |
| Real-time capable | Yes | Yes | Challenging (large models) |
| Safety certification | Very difficult | Tractable | Very difficult |

## Present state and open problems

- **Unified vs. decoupled:** Whether fully unified systems (EMMA) or decoupled reasoning + planning (Senna) will dominate is the field's central architectural question. Unified is simpler; decoupled is more interpretable and potentially safer.
- **Intermediate supervision:** Type 3 systems use explicit intermediate supervision; Type 4 systems largely do not. Whether intermediate supervision is a necessary scaffold or an unnecessary constraint is debated.
- **Closed-loop competence:** Many E2E systems are evaluated only open-loop. The gap between open-loop metrics and closed-loop driving competence remains large and poorly understood.
- **Latency:** VLA models with billions of parameters struggle to meet real-time requirements. [[wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving]] demonstrates 99ms inference but required significant engineering. [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] offers an alternative: distill and discard the LLM entirely.
- **Temporal consistency:** [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] shows that E2E planners suffer from temporal inconsistency, producing jittery trajectories. Momentum-aware planning addresses this with trajectory and perception momentum.
- **Safety verification:** E2E systems resist formal verification. Combining learned E2E planners with verifiable safety layers is an active area. [[wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model]] offers one approach through world-model-based trajectory checking.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/end-to-end-learning-for-self-driving-cars]] | Direct perception-to-steering CNN |
| [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]] | Command-conditioned imitation learning |
| [[wiki/sources/papers/learning-by-cheating]] | Privileged distillation paradigm |
| [[wiki/sources/papers/planning-oriented-autonomous-driving]] | UniAD: jointly trained modular E2E |
| [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] | Vectorized joint E2E |
| [[wiki/sources/papers/vadv2-end-to-end-vectorized-autonomous-driving-via-probabilistic-planning]] | Probabilistic vectorized E2E with action vocabulary |
| [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] | Transformer sensor fusion for E2E |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Everything-as-tokens VLA |
| [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] | Decoupled VLM reasoning + E2E planning |
| [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] | Vision-language-instructed action generation |
| [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]] | Adaptive dual-process VLA with RL |
| [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]] | Parallel-task sparse transformer E2E |
| [[wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation]] | Self-supervised MLLM E2E without annotations |
| [[wiki/sources/papers/bridgead-bridging-past-and-future-end-to-end-autonomous-driving-with-historical-prediction]] | History-enhanced jointly trained E2E (Type 3) |
| [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] | World-model-augmented E2E with occupancy planning |
| [[wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model]] | 3D-grounded open-source VLA |
| [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] | MLLM distillation for efficient E2E |
| [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] | Momentum-aware temporal consistency |
| [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] | Fully sparse E2E with parallel prediction-planning |
| [[wiki/sources/papers/sparsedriveV2-end-to-end-autonomous-driving-via-sparse-scene-representation]] | Factorized trajectory vocabulary scoring, 92.0 PDMS |
| [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] | Pseudo-simulation evaluation benchmark (CoRL 2025) |
| [[wiki/sources/papers/think-twice-before-driving-towards-scalable-decoders-for-end-to-end-autonomous-driving]] | Scalable cascaded decoder for E2E, decoder depth as scaling axis |
| [[wiki/sources/papers/driveadapter-breaking-the-coupling-barrier-of-perception-and-planning-in-end-to-end-autonomous-driving]] | Decoupled perception-planning via adapter, plug-and-play modularity |
| [[wiki/sources/papers/hydra-mdp-end-to-end-multimodal-planning-with-multi-target-hydra-distillation]] | Multi-target distillation with vocabulary-based planning, NAVSIM winner |

## Related

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/planning]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/concepts/foundation-models]]
- [[wiki/comparisons/modular-vs-end-to-end]]
