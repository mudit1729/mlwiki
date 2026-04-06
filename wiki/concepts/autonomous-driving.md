---
title: Autonomous Driving
type: concept
status: active
updated: 2026-04-05
tags:
  - autonomy
  - driving
---

# Autonomous Driving

Autonomous driving is the central application domain of this wiki. The field has undergone three distinct eras of architectural philosophy, each reflecting broader shifts in how ML is applied to safety-critical control.

## The traditional stack

The canonical decomposition splits driving into [[wiki/concepts/perception]], [[wiki/concepts/prediction]], and [[wiki/concepts/planning]], with mapping, localization, control, and safety monitoring as overlays. Each module is developed and evaluated independently, with hand-designed interfaces between them. This modularity aids debugging and certification but creates information bottlenecks and error propagation.

## Era 1: Modular pipelines (pre-2020)

Early learning-based driving focused on individual modules. [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] provided the benchmark that drove perception research. Systems used separate detection, tracking, prediction, and planning components. The key limitation: optimizing each module independently does not optimize the full driving task. Errors in perception propagate through prediction into planning with no mechanism for recovery.

## Era 2: Hybrid and end-to-end learning (2020--2023)

The second era introduced joint training across modules while preserving interpretable intermediate representations. [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] fused camera and LiDAR features through transformers for direct waypoint prediction. [[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) demonstrated that jointly training perception, prediction, and planning with a planning-centric loss yields large gains. [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] showed that vectorized scene representations enable efficient end-to-end driving without dense rasterized maps.

Imitation learning matured through this era. [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]] introduced data augmentation for imitation robustness. [[wiki/sources/papers/learning-by-cheating]] established the privileged-agent distillation paradigm: train an expert with ground-truth access, then distill into a sensorimotor student. Simulation benchmarks like [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] became the standard testbed.

## Era 3: Foundation models and VLA systems (2023+)

The current era applies large vision-language models directly to driving. [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] (EMMA) treats all driving outputs as language tokens, including trajectories. [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]] decouples VLM reasoning from continuous planning. [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] integrates vision-language understanding with action generation in closed-loop. [[wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving]] achieves real-time deployment with RL-enhanced reasoning.

This era is also marked by the introduction of RL beyond imitation: [[wiki/sources/papers/alphadrive-unleashing-the-power-of-vlms-in-autonomous-driving]] applies GRPO-style RL to driving VLMs, while [[wiki/sources/papers/drivemoe-mixture-of-experts-for-vision-language-action-in-autonomous-driving]] uses mixture-of-experts to handle the multimodal nature of driving decisions.

**AutoVLA** ([[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]], 2025) introduces dual-process adaptive reasoning -- dynamically switching between fast direct action and slow chain-of-thought reasoning based on scenario complexity -- with RL fine-tuning on a compact Qwen2.5-VL-3B backbone.

**DriveTransformer** ([[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]], 2025) rethinks the E2E architecture itself: parallel task processing with sparse queries replaces the sequential dense-BEV pipeline, achieving SOTA on Bench2Drive with favorable scaling laws showing decoder scaling matters more than backbone scaling.

[[wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model]] demonstrates that open-source VLAs with hierarchical 3D queries can match larger models at 0.5B scale. [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] shows MLLM reasoning can be distilled into efficient vision planners, resolving the efficiency-vs-reasoning tradeoff with 80% collision reduction and zero inference overhead.

World models have also emerged as a key paradigm. [[wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation]] unifies 3D scene understanding and future generation in a single LLM framework. [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]] reformulates occupancy prediction as world modeling using 3D Gaussians. [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] addresses temporal inconsistency in E2E planning through momentum-aware trajectory selection.

## Benchmarks and evaluation

- **nuScenes** ([[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]]): de facto standard for perception and open-loop planning evaluation.
- **CARLA** ([[wiki/sources/papers/carla-an-open-urban-driving-simulator]]): primary closed-loop simulation benchmark. Leaderboard versions (Town05, Longest6, Bench2Drive) test increasingly difficult scenarios.
- **Open-loop vs closed-loop:** A recurring tension. Open-loop metrics (L2 displacement, collision rate on replayed logs) often fail to predict closed-loop competence. The field is converging on closed-loop evaluation as the minimum standard.

## What makes driving distinct

- Safety-critical operation at high speed with no tolerance for exploration failures
- Severe long-tail distribution: rare events dominate real-world risk
- Multi-agent interaction with partially observable, adversarial participants
- Large train/deploy distribution gap across geographies, weather, and infrastructure

## Present state and open problems

- **Closed-loop gap:** Many state-of-the-art systems still rely primarily on open-loop evaluation. Bridging the open-loop/closed-loop performance gap is the field's most urgent methodological problem.
- **Sim-to-real transfer:** CARLA results do not reliably predict real-world performance. Better simulators and domain adaptation remain critical.
- **Safety certification:** No consensus framework exists for certifying learned driving systems.
- **Data scaling:** Whether scaling driving data follows the same power laws as language modeling is unresolved.
- **Interpretability:** Regulators and users demand explanations for driving decisions, but most end-to-end systems operate as black boxes.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/planning-oriented-autonomous-driving]] | UniAD: joint training with planning-centric objective |
| [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] | Vectorized E2E driving without rasterized maps |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Everything-as-tokens multimodal driving |
| [[wiki/sources/papers/learning-by-cheating]] | Privileged-agent distillation paradigm |
| [[wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving]] | Transformer-based sensor fusion for driving |
| [[wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst]] | Robust imitation via data augmentation |
| [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] | Multimodal driving dataset and benchmarks |
| [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] | Open urban driving simulator |
| [[wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving]] | Adaptive dual-process VLA with RL |
| [[wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving]] | Parallel-task sparse transformer for E2E driving |
| [[wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation]] | Self-supervised MLLM for scalable annotation-free driving |
| [[wiki/sources/papers/bridgead-bridging-past-and-future-end-to-end-autonomous-driving-with-historical-prediction]] | History-enhanced E2E driving with multi-step temporal queries |
| [[wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting]] | Efficient uncertainty-aware BEV via Gaussian Splatting |
| [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] | 4D occupancy world model for planning |
| [[wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model]] | Open-source VLA with hierarchical 3D scene queries |
| [[wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation]] | Unified world model for 3D understanding + generation |
| [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] | Momentum-aware temporal consistency for planning |
| [[wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction]] | Gaussian world model for streaming occupancy |
| [[wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving]] | MLLM-to-planner distillation |
| [[wiki/sources/papers/asyncdriver-asynchronous-large-language-model-enhanced-planner-for-autonomous-driving]] | Asynchronous LLM-planner decoupling, ~40% cost reduction |
| [[wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction]] | Sparse Gaussian occupancy with 5-6x memory reduction |
| [[wiki/sources/papers/driving-gaussian-composite-gaussian-splatting-for-surrounding-dynamic-driving-scenes]] | Gaussian splatting for dynamic driving scene reconstruction |
| [[wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving]] | Original 3D occupancy world model with VQ-VAE + GPT |
| [[wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting]] | Fully self-supervised 3D occupancy via Gaussian splatting |
| [[wiki/sources/papers/gaussianflowocc-sparse-occupancy-with-gaussian-splatting-and-temporal-flow]] | Sparse Gaussian occupancy + temporal flow, 50x faster |
| [[wiki/sources/papers/gaussrender-learning-3d-occupancy-with-gaussian-rendering]] | Plug-and-play Gaussian rendering loss for occupancy |
| [[wiki/sources/papers/racformer-query-based-radar-camera-fusion-for-3d-object-detection]] | Radar-camera fusion surpassing LiDAR-only (CVPR 2025) |
| [[wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation]] | Fully sparse E2E driving, parallel prediction-planning |
| [[wiki/sources/papers/sparsedriveV2-end-to-end-autonomous-driving-via-sparse-scene-representation]] | Factorized trajectory vocabulary, 92.0 PDMS NAVSIM SOTA |
| [[wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving]] | Pseudo-simulation benchmark for E2E driving (CoRL 2025) |

## Related

- [[wiki/concepts/end-to-end-architectures]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/concepts/perception]]
- [[wiki/concepts/prediction]]
- [[wiki/concepts/planning]]
- [[wiki/sources/autonomous-driving-seminal-papers]]
