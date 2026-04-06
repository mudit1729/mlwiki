---
title: DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models
type: source-summary
status: seed
updated: 2026-04-05
year: 2024
venue: arXiv
tags:
  - paper
  - autonomous-driving
  - vlm
  - planning
citations: 416
---

# DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models

📄 **[Read on arXiv](https://arxiv.org/abs/2402.12289)**

## Overview

DriveVLM proposes a hierarchical approach to integrating Vision-Language Models into autonomous driving, emphasizing scene understanding and multi-level planning rather than direct end-to-end control. The system uses a VLM to perform scene description, scene analysis, and hierarchical planning in a chain-of-thought fashion, producing driving decisions through structured reasoning about the environment before generating trajectories. This contrasts with purely end-to-end approaches that map directly from images to control outputs.

The paper also introduces DriveVLM-Dual, a hybrid system that combines the VLM-based reasoning pipeline with a traditional autonomous driving pipeline. The VLM branch handles complex scene understanding and provides high-level planning guidance, while the traditional branch handles routine driving with established perception and planning modules. A fusion mechanism combines outputs from both branches, allowing the system to leverage VLM capabilities for difficult scenarios while maintaining the reliability and efficiency of traditional methods for standard driving.

DriveVLM addresses a practical concern in the VLM-for-driving space: pure VLM-based systems are often too slow for real-time control, and their scene understanding capabilities are wasted on routine driving. By decomposing the problem hierarchically and combining VLM reasoning with traditional planning, DriveVLM offers a pragmatic path toward deploying language model capabilities in driving systems without sacrificing the reliability of established methods.

## Key Contributions

- **Chain-of-thought driving reasoning:** Structured multi-step reasoning pipeline that progresses from scene description to scene analysis to hierarchical planning, making the VLM's decision process transparent and auditable
- **DriveVLM-Dual hybrid architecture:** Combines VLM reasoning with traditional AD modules through a fusion mechanism, enabling the system to use VLM capabilities selectively for complex scenarios while relying on efficient traditional methods for routine driving
- **Hierarchical planning decomposition:** Breaks planning into meta-actions (17 distinct decision types), decision descriptions (natural language rationale), and trajectory waypoints, providing interpretability at multiple granularities
- **Scene understanding emphasis:** Prioritizes rich scene description and analysis before planning, rather than jumping directly from perception to control
- **SUP-AD benchmark:** Introduces a benchmark for scene understanding in planning for autonomous driving, focusing on complex and long-tail scenarios

## Architecture / Method

DriveVLM uses a large Vision-Language Model (based on InternVL) as its core reasoning engine. The VLM processes multi-camera images along with ego vehicle state information and produces outputs through a three-stage chain-of-thought pipeline.

Stage 1 (Scene Description): The VLM generates a natural language description of the driving scene, identifying key objects, their positions, velocities, and relationships. This creates a structured understanding of the environment.

Stage 2 (Scene Analysis): Building on the description, the VLM analyzes the scene for driving-relevant factors: potential hazards, right-of-way situations, traffic signal states, and the intentions of other road users. This stage produces a risk assessment and identifies the key factors that should influence the driving decision.

Stage 3 (Hierarchical Planning): The VLM generates a driving plan at three levels of abstraction: a meta-action (discrete high-level decision), a decision description (natural language explanation), and trajectory waypoints (continuous path coordinates).

In the DriveVLM-Dual variant, a parallel traditional AD pipeline runs simultaneously. The traditional pipeline uses standard perception (3D detection, tracking) and planning (cost-based trajectory optimization) modules. A learned fusion module combines the VLM branch output with the traditional branch output, with the fusion weights depending on scenario complexity -- the VLM branch receives higher weight in complex or unusual scenarios, while the traditional branch dominates in routine driving.

## Results

- DriveVLM achieves strong performance on the nuScenes planning benchmark, with the chain-of-thought reasoning pipeline producing more accurate trajectories than direct VLM-to-trajectory approaches. Outperformed GPT-4V and other open-source VLMs on scene understanding tasks
- DriveVLM-Dual outperforms both the pure VLM and pure traditional pipelines, with state-of-the-art nuScenes planning performance and lower collision rates. Successfully deployed on production vehicles with 410ms inference speed on real vehicle hardware, demonstrating real-time viability
- The hierarchical planning decomposition enables meaningful interpretability, with the natural language reasoning traces accurately reflecting the model's decision factors
- On the SUP-AD benchmark, the system demonstrates superior scene understanding for complex scenarios including construction zones, unusual road geometries, and multi-agent interactions
- Ablation studies confirm that each stage of the chain-of-thought pipeline contributes positively, with scene analysis being particularly important for complex scenarios

## Limitations & Open Questions

- VLM inference latency remains a bottleneck -- the chain-of-thought pipeline adds significant computation, and real-time performance requires the Dual architecture's traditional branch as a fallback
- The fusion mechanism between VLM and traditional branches is a learned module that may not generalize well to distribution shifts, and incorrect fusion weights could produce worse outcomes than either branch alone
- Evaluation is primarily open-loop on nuScenes; closed-loop validation in interactive environments would provide stronger evidence for the hybrid approach

## Connections

- [[wiki/concepts/foundation-models]]
- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/planning]]
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]]
- [[wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt]]
- [[wiki/sources/papers/drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states]]
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]]
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]]

