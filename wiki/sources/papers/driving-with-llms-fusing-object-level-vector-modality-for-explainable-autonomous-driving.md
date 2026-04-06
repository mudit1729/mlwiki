---
title: "Driving with LLMs: Fusing Object-Level Vector Modality for Explainable Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2023
venue: ICRA
tags:
  - paper
  - autonomous-driving
  - language-model
  - explainability
  - planning
citations: ~328
arxiv_id: "2310.01957"
---

# Driving with LLMs: Fusing Object-Level Vector Modality for Explainable Autonomous Driving

[Read on arXiv](https://arxiv.org/abs/2310.01957)

## Overview

Driving with LLMs (Wayve, ICRA 2024) is one of the first concrete demonstrations of using a large language model as the decision-making "brain" for autonomous driving. The paper addresses the "black box" problem in E2E driving by fusing object-level vector representations with a frozen LLaMA-7B model, enabling both driving action prediction and natural language explanations of driving decisions.

The system introduces a novel three-component architecture (Vector Encoder, Vector Former, and LLM with LoRA) trained in two stages: vector representation pretraining followed by driving QA finetuning. A key innovation is the data generation pipeline using a PPO-trained RL agent in simulation, with a `lanGen` function translating vector state into natural language, and GPT-3.5 generating 160k QA pairs for training. The system demonstrates improved perception and action prediction while providing interpretable explanations.

## Key Contributions

- **First concrete LLM-for-driving system**: Among the earliest papers to demonstrate a working LLM integrated into an autonomous driving pipeline with measurable driving performance
- **Object-level vector modality**: Novel approach of representing driving scenes as vectorized object-level features (positions, velocities, types) rather than raw images, enabling efficient LLM integration
- **Two-stage training pipeline**: Vector representation pretraining captures driving-relevant features before QA finetuning aligns the model with language-based driving reasoning
- **Scalable data generation**: Uses PPO-trained RL agent + GPT-3.5 to generate 160k driving QA pairs, establishing a template for LLM driving data creation
- **Explainable decision-making**: The LLM can articulate reasons for its driving decisions in natural language, addressing the black-box problem

## Architecture / Method

![System overview](https://paper-assets.alphaxiv.org/figures/2310.01957v2/LLMs_more.png)

The architecture consists of three main components:

### 1. Vector Encoder

Encodes the driving scene as a set of object-level vectors:
- Each traffic participant is represented by a feature vector: position (x, y, z), velocity (vx, vy), heading, dimensions, and object type
- Road elements (lanes, traffic lights, signs) are similarly vectorized
- Ego vehicle state (velocity, acceleration, heading) is included

### 2. Vector Former

![Architecture details](https://paper-assets.alphaxiv.org/figures/2310.01957v2/arc.png)

A transformer module that processes the vectorized scene:
- Self-attention across all object tokens captures inter-object relationships
- Produces a fixed-size scene embedding that summarizes the driving context
- Acts as a bridge between the vector representation and the LLM's token space

### 3. Frozen LLaMA-7B with LoRA

The scene embedding from Vector Former is projected into the LLM's input space:
- LLaMA-7B is kept frozen; only LoRA adapters are trained
- Input: scene embedding tokens + text query tokens
- Output: driving action tokens + natural language explanation

### Training Pipeline

**Stage 1 -- Vector Pretraining**: The Vector Encoder and Vector Former are pretrained on perception tasks (object counting, distance estimation, speed estimation) to learn driving-relevant representations.

**Stage 2 -- QA Finetuning**: The full system (Vector Former + LoRA adapters) is finetuned on 160k driving QA pairs:

![Data generation](https://paper-assets.alphaxiv.org/figures/2310.01957v2/self_qa.png)

- A PPO-trained RL agent drives in CARLA simulation
- The `lanGen` function translates simulator state vectors into structured natural language descriptions
- GPT-3.5 generates diverse question-answer pairs about driving decisions, perceptions, and explanations
- Questions cover: "What should you do?", "Why?", "How many cars ahead?", "What is the speed limit?"

## Results

![Results](https://paper-assets.alphaxiv.org/figures/2310.01957v2/main3.png)

| Metric | Without Pretraining | With Pretraining | Improvement |
|--------|-------------------|-----------------|-------------|
| Car count MAE | 0.101 | 0.066 | 35% |
| Action prediction | baseline | improved | significant |
| Explanation quality | baseline | improved | qualitative |

- **Pretraining substantially improves perception**: Car count MAE drops from 0.101 to 0.066 with vector pretraining
- **Improved action prediction**: Vector pretraining leads to better driving action prediction compared to Perceiver-BC baselines
- **Qualitative explanation quality**: The system generates coherent natural language explanations for its driving decisions
- **Multi-task capability**: A single model handles perception queries, action prediction, and explanation generation

![Additional results](https://paper-assets.alphaxiv.org/figures/2310.01957v2/more_results.png)

## Limitations & Open Questions

- **Simulation only**: All experiments are in CARLA; real-world transfer is not demonstrated
- **Open-loop evaluation**: No closed-loop driving evaluation; the LLM predicts actions but does not drive in a feedback loop
- **Vector input only**: Does not process raw camera images, limiting applicability to scenarios where a good perception system is already available
- **Frozen LLM**: LLaMA-7B is not fine-tuned end-to-end; full fine-tuning might unlock better integration
- **Latency concerns**: LLM inference at 7B parameters may be too slow for real-time driving (not measured in paper)
- **GPT-3.5 data quality**: Generated QA pairs may contain errors or inconsistencies that limit training quality

## Connections

- [[wiki/concepts/autonomous-driving]] -- LLM integration in driving systems
- [[wiki/concepts/planning]] -- language-model-based planning
- [[wiki/concepts/vision-language-action]] -- early driving VLA work
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3, foundation for LLM capabilities
- [[wiki/sources/papers/carla-an-open-urban-driving-simulator]] -- simulation environment for training and evaluation
- [[wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt]] -- concurrent LLM-for-planning approach
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]] -- subsequent closed-loop LLM driving
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] -- subsequent driving QA approach
- [[wiki/sources/papers/drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model]] -- concurrent multimodal instruction tuning for driving
