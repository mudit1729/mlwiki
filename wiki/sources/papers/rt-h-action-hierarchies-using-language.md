---
title: "RT-H: Action Hierarchies Using Language"
tags: [robotics, vla, transformer, imitation-learning, language-modeling, multimodal]
status: active
type: paper
year: "2024"
venue: "RSS 2024"
citations: 0 <!-- TODO: fetch citation count -->
arxiv_id: "2403.01823"
---

# RT-H: Action Hierarchies Using Language

📄 **[Read on arXiv](https://arxiv.org/abs/2403.01823)**

## Overview

RT-H (Robot Transformer with Action Hierarchies) introduces a hierarchical approach to multi-task robot control that uses natural language as an intermediate representation between high-level task instructions and low-level robot actions. The core problem it addresses is that flat policy architectures like RT-1 and RT-2 struggle with data sharing across semantically diverse manipulation tasks -- a model trained on "pick up the apple" and "open the drawer" cannot easily share low-level motion primitives because the tasks look completely different at the instruction level.

The key insight is that many diverse tasks share common fine-grained motions (e.g., "move arm forward", "close gripper") even when their high-level descriptions differ entirely. RT-H introduces "language motions" -- short natural language descriptions of immediate robot movements -- as a learned intermediate layer. A high-level policy maps observations and task instructions to language motions, and a low-level policy maps observations, tasks, and the predicted language motion to robot actions. Critically, these language motions are not rigid primitives; they are contextual and flexible, adapting execution based on the visual scene and task context.

RT-H achieves a 15% higher average success rate compared to RT-2 on real robot evaluations, with 20% lower action prediction error in offline metrics. The framework also enables an intuitive human intervention mechanism: correcting robot behavior at the language motion level (e.g., changing "move left" to "move right") is far more sample-efficient than correcting low-level actions, with just 30 correction episodes improving success from 40% to 63%. The model also generalizes better to novel objects, achieving 65% success vs. 55% for the baseline.

## Key Contributions

- **Language motions as intermediate representation**: Introduces fine-grained natural language descriptions of robot movements as a learned bridge between task instructions and low-level actions, enabling better data sharing across diverse tasks
- **Hierarchical two-phase policy**: Decomposes robot control into a high-level policy (observation + task -> language motion) and a low-level policy (observation + task + language motion -> action), both implemented as VLM queries
- **Contextual flexibility**: Language motions are not rigid skill primitives -- the same motion description adapts its execution based on visual context and task, avoiding the brittleness of traditional skill libraries
- **Sample-efficient human intervention**: Enables humans to correct robot behavior at the semantic language motion level rather than at low-level action dimensions, requiring far fewer correction demonstrations (30 episodes for significant improvement)
- **Improved generalization**: Demonstrates better transfer to novel objects and task variations through the shared language motion vocabulary

## Architecture / Method

![RT-H teaser showing the hierarchical language motion approach](https://paper-assets.alphaxiv.org/figures/2403.01823v2/teaser_v3.png)

RT-H builds on the RT-2 architecture (a VLM fine-tuned for robot control) but adds a hierarchical decomposition. The system operates in two phases:

**Phase 1 -- High-level policy (Language Motion Prediction):** Given the current camera observation and the task instruction (e.g., "pick up the apple"), the VLM predicts a language motion -- a short natural language description of the immediate robot movement (e.g., "move arm down toward the apple"). This is generated as free-form text by the VLM.

**Phase 2 -- Low-level policy (Action Generation):** The same or a separate VLM receives the camera observation, the task instruction, AND the predicted language motion, then outputs discretized robot actions (following the RT-2 action tokenization scheme). The language motion serves as an additional conditioning signal that disambiguates what the robot should do next.

![Contextual language motions adapt based on scene and task](https://paper-assets.alphaxiv.org/figures/2403.01823v2/contextual_v2.png)

The language motions are learned from demonstrations that have been annotated (either manually or via an automated labeling process using a VLM) with fine-grained motion descriptions. During training, the model learns to predict these annotations; at inference, the predicted language motion provides an interpretable intermediate reasoning step that also improves action quality.

The two-phase structure can be implemented as either: (a) two separate forward passes through the same VLM with different prompting, or (b) a single autoregressive generation where language motions are produced first, followed by action tokens. The hierarchical structure enables the low-level policy to share knowledge across tasks that have different high-level instructions but similar motion patterns.

**Human intervention mechanism:** When the robot fails or behaves suboptimally, a human can observe the predicted language motion and provide a correction at that level (e.g., "you should move right, not left"). This correction is far more natural and efficient than providing corrected low-level action vectors. A small number of corrected demonstrations (as few as 30 episodes) can be used to fine-tune the high-level policy, significantly improving performance.

## Results

![Main evaluation results comparing RT-H to baselines](https://paper-assets.alphaxiv.org/figures/2403.01823v2/phase4_results_v7_err.png)

| Method | Average Success Rate | Action Prediction Error | Novel Object Success |
|--------|---------------------|------------------------|---------------------|
| **RT-H** | **+15% vs RT-2** | **-20% vs RT-2** | **65%** |
| RT-2 (baseline) | baseline | baseline | 55% |

Key experimental findings:

- **15% higher success rate** on average across real robot manipulation tasks compared to RT-2, demonstrating the benefit of the hierarchical language motion decomposition
- **20% lower offline action prediction error**, indicating that the intermediate language motion representation provides a useful inductive bias for action prediction
- **Generalization to novel objects**: 65% success rate on tasks involving objects not seen during training, compared to 55% for the flat RT-2 baseline
- **Sample-efficient correction**: Training on just 30 human correction episodes at the language motion level improves success rate from 40% to 63%, demonstrating the practical value of the interpretable intermediate layer

![Human intervention results showing sample efficiency](https://paper-assets.alphaxiv.org/figures/2403.01823v2/phase4_intervention_results_v9_err.png)

![Generalization to new tasks](https://paper-assets.alphaxiv.org/figures/2403.01823v2/new_tasks_v2.png)

## Limitations & Open Questions

- **Language motion annotation**: The approach requires language motion annotations for training data, which adds a labeling burden. Automated VLM-based annotation helps but may introduce noise
- **Two-pass inference cost**: Running two VLM forward passes (one for language motion, one for action) increases inference latency compared to a flat policy
- **Language motion vocabulary**: The expressiveness and granularity of language motions is not formally characterized -- it is unclear what the optimal level of description is (e.g., "move arm" vs. "move arm 5cm forward and 2cm down")
- **Scale of evaluation**: The evaluation is on Google's robot manipulation setup; transferability of the hierarchical language motion idea to other embodiments and domains (e.g., humanoids, driving) is not demonstrated
- **Comparison to non-language hierarchies**: The paper does not extensively compare against hierarchical policies that use learned latent skills rather than language as the intermediate representation

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale]] — RT-H builds directly on RT-1's architecture and dataset
- [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] — RT-H extends RT-2 with hierarchical language motions; RT-2 is the primary baseline
- [[wiki/sources/papers/palm-e-an-embodied-multimodal-language-model]] — provides the VLM backbone paradigm that RT-H leverages
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] — open-source VLA that could benefit from RT-H's hierarchical approach
- [[wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models]] — similar idea of using language as intermediate reasoning for VLAs, but via chain-of-thought rather than motion descriptions
- [[wiki/sources/papers/pi05-a-vision-language-action-model-with-open-world-generalization]] — pi0.5 uses a hierarchical VLA design conceptually similar to RT-H's two-level decomposition
- [[wiki/concepts/vision-language-action]] — RT-H advances the VLA paradigm with hierarchical action decomposition
- [[wiki/concepts/robotics]] — broader context of the robotics VLA lineage
