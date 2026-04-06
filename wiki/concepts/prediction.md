---
title: Prediction
type: concept
status: active
updated: 2026-04-05
tags:
  - prediction
  - behavior-forecasting
---

# Prediction

Prediction forecasts the future behavior of other agents (vehicles, pedestrians, cyclists) and the evolution of the scene. It is the bridge between perception and planning: the ego vehicle must anticipate what others will do in order to act safely. The field has evolved from simple physics-based extrapolation through learned trajectory regression to joint scene-level forecasting conditioned on maps and interactions.

## Core challenges

Prediction is fundamentally difficult because of:

- **Multimodality:** A vehicle at an intersection might go straight, turn left, or turn right. The predictor must represent multiple plausible futures, not collapse to a single mean trajectory (which may be physically impossible, e.g., driving into a median).
- **Interaction:** Agents influence each other. The ego vehicle's future behavior changes others' responses, creating a coupled prediction-planning problem.
- **Long horizons:** Useful prediction for highway merging or intersection negotiation requires 5-8 second horizons, where uncertainty compounds rapidly.
- **Map conditioning:** Agent behavior is strongly constrained by road geometry, lane topology, and traffic rules. Incorporating this structure is essential.

## Key approaches

### Vectorized scene encoding

[[wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation]] (VectorNet, 2020) introduced a unified vectorized representation for both HD map elements and agent trajectories. Polylines (lanes, crosswalks, agent tracks) are encoded as sequences of vectors, then aggregated via a global interaction graph. This replaced rasterized bird's-eye-view rendering with a more efficient and expressive representation that preserves topological structure.

### Graph-based lane conditioning

[[wiki/sources/papers/learning-lane-graph-representations-for-motion-forecasting]] (LaneGCN, 2020) built graph convolutions directly on lane topology. Lanes are nodes in a graph connected by successor, predecessor, and neighbor edges. Agent features are fused with lane features through cross-attention, allowing the model to reason about which lanes an agent is likely to follow. LaneGCN established that structured map representations improve prediction accuracy significantly over flat feature maps.

### Joint prediction in end-to-end systems

The trend toward end-to-end architectures has folded prediction into jointly trained systems rather than treating it as a standalone module.

[[wiki/sources/papers/planning-oriented-autonomous-driving]] (UniAD) includes a motion forecasting module that predicts multi-agent futures jointly, with these predictions feeding directly into the planner. Crucially, UniAD showed that training the predictor with a planning-oriented loss (rather than purely minimizing prediction error) improves both prediction and planning quality.

[[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] (VAD) extends the vectorized paradigm to joint perception-prediction-planning, representing predicted agent futures as vectorized trajectories that the planner can reason over efficiently.

### Language-enhanced prediction

Recent work augments prediction with language-based reasoning. [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]] uses chain-of-thought structures to decompose prediction into interpretable steps: first describe the scene, then reason about agent intentions, then predict trajectories. [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] structures prediction as graph-based QA, where language queries extract agent behavior reasoning from a VLM.

### Interaction-aware prediction

Multi-agent interaction remains a frontier. Simple independent prediction (forecast each agent separately) misses the conditional dependencies that govern real traffic. Scene-level joint prediction models all agents simultaneously, capturing that if vehicle A yields, vehicle B accelerates, and vice versa. [[wiki/sources/papers/planning-oriented-autonomous-driving]] models these interactions through agent-agent attention in the motion forecasting stage.

## Prediction in the VLA era

In VLA systems, prediction is often implicit rather than explicit. [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] (EMMA) does not produce explicit agent future trajectories; instead, the VLM's internal representations capture predictive information that influences the output trajectory tokens. [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] similarly folds prediction into its holistic vision-language-action pipeline.

Whether implicit prediction is sufficient or whether explicit forecasting provides essential structure for safety and interpretability is a key open question.

### Temporal consistency in prediction

[[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] identifies temporal inconsistency as a critical failure mode: consecutive predictions lack coherence, causing vehicle trembling and vulnerability to occlusions. MomAD introduces trajectory momentum (Hausdorff-distance-based consistency) and perception momentum (LSTM-based historical fusion), achieving 33% improvement in trajectory prediction consistency.

## Evaluation

Prediction is typically evaluated by:
- **minADE/minFDE:** Minimum average/final displacement error across K predicted modes. Standard on [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] and Argoverse.
- **Miss rate:** Fraction of scenarios where no predicted mode is within a threshold of ground truth.
- **Diversity:** Whether predicted modes cover the true distribution of futures.

A persistent concern is that prediction metrics do not correlate well with planning quality. A predictor with slightly worse minADE but better mode coverage may produce far better downstream planning.

## Present state and open problems

- **Prediction-planning coupling:** Marginal prediction (forecasting others independently of the ego plan) is inherently limited. Conditional prediction (forecasting others given an ego plan) is more useful but creates a chicken-and-egg problem with planning.
- **Calibration:** Predicted probabilities over modes should be well-calibrated for risk-aware planning, but most models are poorly calibrated.
- **Rare behaviors:** Prediction models trained on normal driving data struggle with aggressive, erratic, or rule-violating behavior, which is precisely when accurate prediction matters most.
- **Generalization:** Models trained on one city's driving patterns often fail in others. Cross-domain prediction generalization is largely unsolved.
- **Implicit vs. explicit:** Whether the trend toward implicit prediction in VLA systems sacrifices essential safety-relevant information remains contested.

## Key papers

| Paper | Contribution |
|-------|-------------|
| [[wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation]] | Vectorized encoding for maps and agents |
| [[wiki/sources/papers/learning-lane-graph-representations-for-motion-forecasting]] | Graph convolutions on lane topology for prediction |
| [[wiki/sources/papers/planning-oriented-autonomous-driving]] | Joint prediction-planning with planning-centric loss |
| [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]] | Vectorized joint prediction-planning |
| [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]] | Chain-of-thought reasoning for prediction |
| [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] | Graph QA for driving scene reasoning |
| [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]] | Implicit prediction in VLM-based driving |
| [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] | Standard prediction benchmark |
| [[wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving]] | Momentum-aware temporal consistency for prediction |
| [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] | Holistic VLA with integrated prediction |
| [[wiki/sources/papers/bridgead-bridging-past-and-future-end-to-end-autonomous-driving-with-historical-prediction]] | Multi-step temporal queries for fine-grained motion prediction |
| [[wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world]] | 4D occupancy forecasting as prediction via world model |

## Related

- [[wiki/concepts/perception]]
- [[wiki/concepts/planning]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/end-to-end-architectures]]
