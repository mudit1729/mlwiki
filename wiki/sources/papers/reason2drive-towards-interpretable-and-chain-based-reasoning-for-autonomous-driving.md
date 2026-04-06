---
title: "Reason2Drive: Towards Interpretable and Chain-Based Reasoning for Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2024
venue: ECCV
tags:
  - paper
  - autonomous-driving
  - vla
  - reasoning
  - benchmark
  - evaluation
citations: 128
---

📄 **[Read on arXiv](https://arxiv.org/abs/2312.03661)**

## Overview

Reason2Drive provides the largest reasoning chain dataset for driving (>600K video-text pairs from nuScenes, Waymo, and ONCE) and introduces an aggregated evaluation metric that addresses fundamental problems with using BLEU/CIDEr to assess driving reasoning quality. Driving VLM research lacked datasets with annotated reasoning chains and suffered from inappropriate evaluation metrics where standard language metrics are ambiguous for driving reasoning -- a correct but differently-worded chain scores low while a fluent but incorrect one can score high.

Reason2Drive addresses both gaps simultaneously. The dataset provides >600K pairs spanning perception, prediction, reasoning, and decision stages collected from three open-source driving datasets, offering cross-dataset diversity in scenarios, geographies, and driving conditions. The aggregated evaluation metric combines multiple scoring components to reduce individual metric biases and correlates better with human judgment of reasoning quality.

This is a benchmark-first contribution that stress-tests whether driving VLMs actually reason correctly rather than just producing fluent text. The baseline evaluations show that current VLMs have significant room for improvement on chain reasoning for driving, establishing both the difficulty and the value of the benchmark. Reason2Drive fills a critical role in the driving VLA ecosystem by providing a standardized way to evaluate the reasoning capabilities that are supposed to justify using large language models for driving.

## Key Contributions

- **Large-scale reasoning chain dataset**: >600K video-text pairs automatically collected from nuScenes, Waymo Open Dataset, and ONCE, organized as perception -> prediction -> reasoning -> decision chains
- **Cross-dataset diversity**: Spans three major driving datasets, providing varied scenarios, geographies, and driving conditions that no single-dataset benchmark can match
- **Aggregated evaluation metric**: Combines multiple scoring components to reduce the noise and ambiguity of individual metrics (BLEU, CIDEr, GPT-Score) for assessing driving reasoning quality
- **Reasoning chain structure**: Characterizes driving as a sequential chain (perception -> prediction -> reasoning -> decision) with explicit stage annotations
- **Baseline VLM evaluation**: Evaluates multiple VLMs on chain reasoning, establishing difficulty and room for improvement

## Architecture / Method

![Reason2Drive dataset construction process](https://paper-assets.alphaxiv.org/figures/2312.03661v3/img-0.jpeg)

Reason2Drive is a dataset and benchmark contribution, not an architectural one. The methodology covers data construction and evaluation design:

**Data construction pipeline**: Starting from three source datasets (nuScenes, Waymo Open, ONCE), the pipeline extracts structured information from 3D annotations (object positions, velocities, trajectories) and map data (lanes, traffic signals). This structured information is converted into natural language chains through template-based generation, with each chain following the four-stage structure:
1. Perception: "There is a car 15m ahead in the left lane, traveling at 30 km/h"
2. Prediction: "The car will likely merge into our lane within 3 seconds"
3. Reasoning: "We should slow down to maintain safe following distance because the car is merging"
4. Decision: "Decelerate gradually and maintain lane position"

ChatGPT augmentation diversifies the phrasing of templates to reduce linguistic monotony while preserving semantic content. Quality filtering removes chains with contradictions or implausible reasoning.

**Aggregated evaluation metric**: For each reasoning chain, the metric computes: (1) BLEU-based n-gram overlap, (2) CIDEr consensus score, (3) GPT-based semantic similarity score, and (4) stage-specific accuracy for perception facts (object counts, distances). These are combined with learned weights that maximize correlation with human quality judgments on a calibration set. The aggregation reduces the failure modes of individual metrics (BLEU penalizing paraphrases, CIDEr rewarding frequent phrases).

**Baseline evaluation protocol**: VLMs receive the driving video frames and a prompt asking for a structured reasoning chain. Generated chains are evaluated at each stage independently and as a whole, revealing where models succeed (perception description) and fail (causal reasoning, decision justification).

## Results

- Standard metrics are inadequate for driving reasoning: concrete examples show BLEU/CIDEr penalize valid paraphrases and reward fluent but incorrect reasoning chains
- The aggregated metric achieves 0.78 Spearman correlation with human quality judgments, compared to 0.52 for BLEU-4 and 0.61 for CIDEr alone
- Baseline VLMs (LLaVA, InstructBLIP, etc.) achieve only 35-55% stage-wise accuracy on the benchmark, with the largest gaps in the reasoning and decision stages
- Cross-dataset construction provides scenario diversity: models trained only on nuScenes data perform 12% worse on Waymo scenarios, highlighting the value of multi-dataset evaluation
- Perception stage accuracy is consistently highest (60-70%), while reasoning stage accuracy is lowest (25-40%), suggesting current VLMs describe what they see better than they reason about what to do

## Limitations & Open Questions

- This is a reasoning benchmark, not an action policy -- it evaluates reasoning about actions, not action generation itself; the gap between correct reasoning and safe driving persists
- Automatic QA generation may encode biases from source datasets and collection scripts, potentially rewarding memorization of template patterns
- Reasoning evaluation remains fundamentally difficult even with improved metrics -- the gap between language-level correctness and driving-level safety is not fully bridged

## Connections

- [[wiki/concepts/autonomous-driving]] -- driving reasoning evaluation
- [[wiki/concepts/vision-language-action]] -- evaluates VLA reasoning capabilities
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] -- related driving VQA benchmark
- [[wiki/sources/papers/textual-explanations-for-self-driving-vehicles]] -- earlier work on driving explanations
- [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]] -- VLA evaluated on reasoning
- [[wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving]] -- source dataset for Reason2Drive
