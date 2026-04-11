---
title: "GPT-Driver: Learning to Drive with GPT"
type: source-summary
status: complete
updated: 2026-04-05
year: 2023
venue: NeurIPS FMDM Workshop
tags:
  - paper
  - autonomous-driving
  - vla
  - llm
  - planning
  - reasoning
citations: 396
paper-faithfullness: audited-solid
---

# GPT-Driver: Learning to Drive with GPT

📄 **[Read on arXiv](https://arxiv.org/abs/2310.01415)**

## Overview

GPT-Driver reformulates autonomous driving motion planning as a language modeling problem. Scene context (object positions, velocities, lane geometry) and ego vehicle state are converted to text tokens, structured into prompts with traffic rules, and fed to a fine-tuned GPT-3.5 model that generates trajectory waypoints as token sequences. Before outputting the trajectory, the model produces chain-of-thought reasoning traces that explain its planning rationale in natural language, providing interpretability alongside action generation.

This is the first heavily-cited "LLM-as-planner" driving paper, catalyzing an entire research direction in language-conditioned autonomous driving. The key conceptual shift was replacing hand-crafted cost functions and domain-specific planning architectures with general-purpose language modeling, trading domain expertise for the world knowledge and reasoning capabilities of large language models. By demonstrating that trajectories can be meaningfully generated as token sequences with accompanying reasoning, GPT-Driver established the planning-as-language paradigm that directly inspired EMMA, ORION, and numerous follow-up papers.

The paper also raises important questions that persist in the field: can LLMs handle the numeric precision required for safety-critical trajectory generation? Are the reasoning traces causally connected to planning quality, or merely post-hoc rationalizations? Is open-loop evaluation on nuScenes sufficient to validate a planning-as-language approach? These questions continue to drive research in the VLA-for-driving space.

## Key Contributions

- **Planning-as-language formulation:** Convert numeric scene coordinates and ego states to text tokens, construct prompts with scene context and traffic rules, and generate waypoint trajectories as token sequences
- **Chain-of-thought reasoning traces:** The LLM generates natural-language reasoning ("the car ahead is braking, I should decelerate...") before outputting trajectory waypoints, providing interpretable planning rationale
- **Fine-tuning on driving trajectory data:** Adapts GPT-3.5 on nuScenes planning data for domain-specific trajectory generation
- **Prompt engineering for driving:** Includes scene descriptions, traffic rules, and ego state in structured prompts to leverage LLM context understanding
- **Demonstration of LLM generalization potential:** World knowledge from pretraining enables reasoning about scenarios beyond the driving training set

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│              GPT-Driver: LLM as Motion Planner               │
│                                                             │
│  Driving Scene (nuScenes)                                   │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────┐                                   │
│  │  Scene Tokenization  │                                   │
│  │  - 3D bbox ──► text  │  "car at (3.2, -1.5) vel 5.1m/s" │
│  │  - lanes  ──► text   │  "lane: (0,0),(0,5),(0.2,10)..."  │
│  │  - ego state ──► text│  "ego: vel 8.3m/s heading 0.02"   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│             ▼                                               │
│  ┌──────────────────────┐                                   │
│  │  Prompt Construction │                                   │
│  │  ┌────────────────┐  │                                   │
│  │  │ System: "You   │  │                                   │
│  │  │ are a planner" │  │                                   │
│  │  ├────────────────┤  │                                   │
│  │  │ Traffic Rules   │  │                                   │
│  │  ├────────────────┤  │                                   │
│  │  │ Scene Context   │  │                                   │
│  │  ├────────────────┤  │                                   │
│  │  │ Ego State       │  │                                   │
│  │  ├────────────────┤  │                                   │
│  │  │ "Plan trajectory│  │                                   │
│  │  │  with reasoning"│  │                                   │
│  │  └────────────────┘  │                                   │
│  └──────────┬───────────┘                                   │
│             │                                               │
│             ▼                                               │
│  ┌──────────────────────┐                                   │
│  │  GPT-3.5 (fine-tuned │                                   │
│  │  on nuScenes data)   │                                   │
│  │       │              │                                   │
│  │       ▼              │                                   │
│  │  Chain-of-Thought:   │  "The car ahead is braking..."    │
│  │       │              │                                   │
│  │       ▼              │                                   │
│  │  Waypoints:          │  "(x1,y1), (x2,y2), ..."         │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

![GPT-DRIVER system overview: perception and prediction data converted to language, processed through GPT as motion planner, outputting reasoning and trajectories](https://paper-assets.alphaxiv.org/figures/2310.01415v3/img-0.jpeg)

GPT-Driver's method involves three main components: scene tokenization, prompt construction, and trajectory generation.

Scene tokenization converts the driving scene into a text representation. Object detections from nuScenes (3D bounding boxes with position, velocity, heading, and class) are serialized as structured text strings. Lane geometry is represented as sequences of waypoint coordinates. The ego vehicle's state (position, velocity, heading, acceleration) is similarly converted to text. All coordinates use a consistent reference frame centered on the ego vehicle.

Prompt construction assembles the tokenized scene into a structured prompt for the LLM. The prompt includes: (1) a system message defining the model's role as a driving planner, (2) traffic rules and driving conventions as background knowledge, (3) the current scene description with all detected objects and road geometry, (4) the ego vehicle's current state, and (5) a request to generate a trajectory as a sequence of future waypoint coordinates. The prompt also instructs the model to provide reasoning before the trajectory output.

Trajectory generation is performed by GPT-3.5 fine-tuned on nuScenes planning data. The model generates a chain-of-thought reasoning passage explaining its assessment of the scene and its planned behavior, followed by a sequence of (x, y) coordinate pairs representing the future trajectory at fixed time intervals. The fine-tuning uses standard next-token prediction loss on the combined reasoning and trajectory output. Ground truth reasoning is automatically generated by computing a hypothetical ego-trajectory (assuming no interference from other agents) and identifying overlaps between objects' predicted paths and that hypothetical trajectory, providing chain-of-thought supervision without manual annotation.

A key challenge is the numeric precision of language-based coordinate generation. LLM tokenizers split numbers into individual digits or subword units, and the autoregressive generation of each digit introduces potential for accumulated error in coordinate values. GPT-Driver addresses this partially through fine-tuning on numeric driving data, but the fundamental tension between discrete token generation and continuous coordinate spaces remains.

## Results

![Interpretable reasoning examples across driving scenarios with critical objects highlighted and corresponding driving strategies](https://paper-assets.alphaxiv.org/figures/2310.01415v3/img-1.jpeg)

- Competitive trajectory prediction on the nuScenes open-loop planning benchmark with substantially lower L2 errors compared to state-of-the-art baselines, validating centimeter-level accuracy across prediction horizons
- LLM reasoning traces provide interpretable planning rationale, with the model generating contextually appropriate explanations such as identifying lead vehicles, noting traffic signals, and explaining lane change decisions
- The planning-as-language paradigm is validated as viable: trajectories generated as token sequences achieve performance within the range of established methods
- Fine-tuning on driving data effectively adapts the LLM's generation to the trajectory domain, with the model learning appropriate speed profiles, turning behaviors, and following distances
- World knowledge from pretraining appears to help with long-tail scenarios, though quantifying this benefit precisely is difficult
- **Data efficiency**: When trained on only 1-10% of available data, GPT-Driver significantly outperforms traditional methods under data scarcity conditions, demonstrating strong few-shot learning capability
- **Safety without post-processing**: Achieves competitive collision rates without relying on post-optimization techniques employed by baselines

## Limitations & Open Questions

- Open-loop evaluation only (nuScenes) with no closed-loop validation -- interactive driving competence with reactive agents is untested, and open-loop metrics are known to be weakly correlated with actual driving quality
- LLMs struggle with precise coordinate generation due to tokenization of numeric values -- this creates a fundamental precision ceiling that may be unacceptable for safety-critical applications
- Reasoning traces may not be causally tied to trajectory quality -- the model may generate fluent explanations that do not actually reflect its internal planning process

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning]]
- [[wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving]]
- [[wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation]]
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]]
- [[wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models]]
- [[wiki/sources/papers/language-models-are-few-shot-learners]]
