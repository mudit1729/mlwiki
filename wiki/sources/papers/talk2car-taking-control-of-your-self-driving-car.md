---
title: "Talk2Car: Taking Control of Your Self-Driving Car"
type: source-summary
status: complete
updated: 2026-04-05
year: 2019
venue: EMNLP-IJCNLP
tags:
  - paper
  - autonomous-driving
  - vla
  - grounding
  - benchmark
  - natural-language
citations: 182
---

📄 **[Read on arXiv](https://arxiv.org/abs/1909.10838)**

# Talk2Car: Taking Control of Your Self-Driving Car

## Overview

For autonomous vehicles to be truly useful as personal transportation, passengers should be able to issue natural-language commands like "park behind that blue car" or "follow the taxi ahead." Talk2Car established the first widely-referenced benchmark for this natural-language command grounding task in driving, built on the nuScenes dataset. Each example consists of a driving scene paired with a natural-language command that refers to a specific object, and the model must predict the correct bounding box of the referred object.

The key distinction from generic visual grounding datasets (like RefCOCO) is that Talk2Car's commands are action-oriented rather than descriptive -- they express what the vehicle should do with respect to visible objects, not just which object to look at. Commands like "stop behind the white SUV" implicitly define a driving action grounded through a referenced object. This framing positions natural-language interaction as a driving interface, not just a perception output.

The companion Talk2Car-Trajectory extension (IEEE Access, 2022) moved beyond "which object?" to "what path should the car follow?", decomposing language commands into object referral followed by trajectory prediction. Together, Talk2Car and Talk2Car-Trajectory form an early bridge from language+scene understanding to language-conditioned planning that later full VLA systems like LMDrive would realize in closed-loop settings.

## Key Contributions

- **First driving-specific natural-language command grounding dataset**: 11,959 commands over 850 nuScenes scenes, with human-annotated bounding boxes for referred objects
- **Action-oriented command framing**: Commands express vehicle actions grounded via visible objects (e.g., "park behind the white car on the right"), unlike descriptive grounding datasets that just identify objects
- **AP/IoU evaluation protocol**: Establishes AP50 as the standard metric for measuring referred object localization accuracy in driving contexts
- **Talk2Car-Trajectory extension**: Decomposes language commands into object referral followed by trajectory prediction, bridging grounding and planning in a two-stage pipeline
- **Reusable benchmark**: Catalyzed a stream of driving-focused language grounding models and provided a standard evaluation for the community

## Architecture / Method

```
              Talk2Car Baseline: Two-Tower Grounding

  ┌─────────────────┐       ┌─────────────────────┐
  │  Driving Scene   │       │  NL Command          │
  │  (Camera Image)  │       │  "Park behind the    │
  └────────┬────────┘       │   white car"         │
           │                 └──────────┬──────────┘
           ▼                            ▼
  ┌─────────────────┐       ┌─────────────────────┐
  │  Visual Encoder  │       │  Language Encoder    │
  │  (ResNet / FRCNN)│       │  (LSTM / BERT)       │
  └────────┬────────┘       └──────────┬──────────┘
           │                            │
           ▼                            ▼
  ┌─────────────────┐       ┌─────────────────────┐
  │ Region Features  │       │ Sentence Embedding   │
  │ [r1, r2, ..., rN]│       │        s             │
  └────────┬────────┘       └──────────┬──────────┘
           │                            │
           └──────────┬─────────────────┘
                      ▼
             ┌────────────────┐
             │ Fusion Module   │  score(ri, s) for each region
             │ (dot-product /  │
             │  MLP scoring)   │
             └───────┬────────┘
                     ▼
             ┌────────────────┐
             │ argmax ──► Box  │  ──►  Eval: AP50
             └────────────────┘
```

The Talk2Car benchmark provides a dataset and evaluation protocol rather than a single dominant architecture. The dataset is constructed by asking human annotators to write natural-language commands for nuScenes driving scenes. Each command refers to a specific object in the scene (a detected or annotated 3D bounding box), and annotators write action-oriented instructions that a passenger might give.

The baseline models follow a two-tower approach: a visual encoder (e.g., ResNet or Faster R-CNN) extracts region features for detected objects in the scene, while a language encoder (e.g., LSTM or BERT) produces a sentence embedding for the command. A fusion module computes similarity scores between each candidate region and the command, and the region with the highest score is selected as the referred object. Evaluation uses AP50 -- the average precision at 50% IoU threshold between predicted and ground-truth bounding boxes.

The Talk2Car-Trajectory extension adds a second stage: once the referred object is identified, a trajectory prediction module generates a path for the ego vehicle conditioned on the object location and the command semantics. This is trained on nuScenes trajectory data with the grounding output as a conditioning signal.

## Results

- **Baseline AP50 of ~50-60%** for initial models, with subsequent work pushing to ~70%+ through better vision-language fusion techniques
- **Command diversity**: The dataset contains commands covering a wide variety of driving actions (stop, park, follow, turn, yield) and object references (vehicles, pedestrians, landmarks)
- **Talk2Car-Trajectory demonstrates language-to-trajectory feasibility**: Given a command, the system predicts both the referred object and a path the car should follow to execute the command
- **Community adoption**: The benchmark enabled a stream of follow-up papers improving grounding accuracy through better cross-modal attention, graph-based reasoning, and transformer architectures
- **Practical passenger interaction framing**: Commands are action-oriented rather than descriptive, making the benchmark relevant to real deployment scenarios

## Limitations & Open Questions

- The benchmark is object grounding, not full end-to-end driving -- action semantics are implicit in the referred object rather than explicit trajectory or control outputs
- Language diversity is limited by the annotation process and nuScenes scene coverage, with some command types (e.g., complex multi-step instructions) underrepresented
- No trajectory or control output evaluation in the original Talk2Car (addressed by Talk2Car-Trajectory, but even that provides only open-loop evaluation)
- Talk2Car-Trajectory provides local trajectory prediction without closed-loop validation, leaving a gap between grounding benchmarks and deployable language-conditioned driving systems

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]]
- [[wiki/sources/papers/textual-explanations-for-self-driving-vehicles]]
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]]
- [[wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving]]
