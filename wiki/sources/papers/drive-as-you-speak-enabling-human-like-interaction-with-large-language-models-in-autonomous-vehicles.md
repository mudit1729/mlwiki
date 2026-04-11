---
title: "Drive as You Speak: Enabling Human-Like Interaction with Large Language Models in Autonomous Vehicles"
tags:
  - paper
  - autonomous-driving
  - llm
  - planning
  - nlp
  - multimodal
  - human-interaction
type: paper
status: active
year: "2023"
venue: "arXiv"
citations: ~60
arxiv_id: "2309.10228"
paper-faithfullness: audited-solid
---

# Drive as You Speak: Enabling Human-Like Interaction with Large Language Models in Autonomous Vehicles

📄 **[Read on arXiv](https://arxiv.org/abs/2309.10228)**

## Overview

Drive as You Speak (DAYS) proposes a framework for enabling natural language interaction between human passengers and autonomous vehicles using large language models. The core problem is that existing autonomous driving systems lack intuitive interfaces for non-expert passengers to communicate preferences, provide instructions, or query the vehicle's behavior in natural language. Rather than requiring passengers to use structured commands or preset options, DAYS allows freeform conversational interaction that the LLM translates into driving-relevant actions and responses.

The key insight is that LLMs can serve as an intermediate reasoning layer between human intent expressed in natural language and the low-level control parameters of an autonomous driving system. The framework uses a modular architecture where the LLM processes natural language commands (e.g., "take the next left," "slow down, I'm feeling carsick," "what's that building on the right?"), interprets them in the context of the current driving scenario, and translates them into executable instructions for the vehicle's planning and control stack. The LLM also generates natural language explanations of the vehicle's behavior back to the passenger, creating a bidirectional conversational interface.

DAYS demonstrates that LLM-based interaction can handle a diverse range of passenger requests spanning navigation commands, comfort preferences, safety concerns, and informational queries. The framework is illustrated through qualitative case studies in the HighwayEnv simulator, showing how chain-of-thought prompting enables the LLM to interpret verbal commands, reason over the driving context, and produce appropriate actions and explanations. This work is notable as an early exploration of the "LLM as vehicle interface" paradigm, distinct from the "LLM as planner" direction taken by GPT-Driver and DriveGPT4 -- here the LLM mediates human-vehicle communication rather than directly generating trajectories.

## Key Contributions

- **Natural language driving interface**: Early framework for bidirectional natural language interaction between passengers and autonomous vehicles, covering navigation, comfort, safety, and information requests
- **LLM-based command interpretation**: Demonstrates that an LLM with chain-of-thought prompting can parse ambiguous, context-dependent natural language driving commands into driving-relevant actions
- **Bidirectional communication**: The system both accepts human commands and generates natural language explanations of vehicle behavior, creating a conversational loop
- **HighwayEnv case studies**: Illustrates the framework through qualitative scenarios in the HighwayEnv simulator, showcasing interpretation, interaction, and reasoning across several driving situations
- **Modular integration architecture**: Proposes a separation between the language/reasoning layer (LLM with tool use) and the driving execution layer, allowing the framework to work with different underlying AV stacks

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                    DAYS Framework                            │
│                                                             │
│  Passenger ◄─────────────────────────────────────────┐      │
│     │ Natural language                               │      │
│     │ ("Slow down, I'm carsick")      NL explanation │      │
│     ▼                                                │      │
│  ┌────────────────────────────────────┐              │      │
│  │  LLM (chain-of-thought reasoning)  │──────────────┘      │
│  │  - Intent understanding            │                     │
│  │  - Personalization / memory        │                     │
│  │  - Action + explanation generation │                     │
│  └───┬────────────────────┬───────────┘                     │
│      │ tool / module calls│                                 │
│      ▼                    ▼                                 │
│  ┌─────────────┐   ┌───────────────────┐                    │
│  │ Perception, │   │  AV Planning &    │                    │
│  │ localization│   │  Control Stack    │                    │
│  │ route info  │   │  (HighwayEnv)     │                    │
│  └─────────────┘   └───────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

The DAYS framework positions the LLM as the central reasoner that connects the passenger to the vehicle's driving stack, with the following functional roles:

**Language understanding and reasoning**: The LLM takes raw natural language input from passengers along with contextual information about the current driving state (speed, location, route, surrounding environment) and reasons about intent using chain-of-thought prompting. This covers navigation requests, comfort adjustments, information queries, and safety concerns.

**Tool / module use**: Rather than operating on raw sensor data directly, the LLM interacts with specialized modules of the autonomous driving stack (perception, localization, planning, etc.) via tool-style calls, grounding its language reasoning in the vehicle's real state and capabilities.

**Memory and personalization**: The framework maintains history across interactions so the LLM can adapt driving behavior to individual passenger preferences over time, enabling continuous personalization from verbal feedback.

**Action and response generation**: The LLM produces both structured instructions that influence the planner/controller (e.g., adjust speed, change lanes, update route) and natural language responses that explain what the vehicle is doing and why, creating the bidirectional conversational loop.

The system handles several categories of interaction:
- **Navigation commands**: "Turn left at the next intersection," "Take me to the nearest gas station"
- **Comfort preferences**: "Slow down, this is too fast," "Can you drive more smoothly?"
- **Safety interactions**: "Watch out for that pedestrian," "Is it safe to change lanes?"
- **Informational queries**: "How long until we arrive?", "What's the speed limit here?"
- **Contextual commands**: "Follow that car," "Park somewhere near here"

## Results

Evaluation in the paper is qualitative: the authors walk through case studies in HighwayEnv to illustrate how the framework handles different verbal commands and driving situations rather than reporting large-scale quantitative benchmarks or human-subject surveys.

Key observations include:
- Chain-of-thought prompting leads to noticeably better driving decisions than direct prompting, by letting the LLM reason step-by-step about the scene, rules, and passenger intent before selecting an action
- The LLM can personalize driving behavior in real time based on verbal feedback (e.g., requests to drive more cautiously, maintain more following distance, or prefer a particular lane)
- Natural-language explanations of the vehicle's actions improve the transparency of the decision-making process, supporting the paper's goal of "human-like" interaction
- Integrating the LLM with tool/module calls (perception, localization, routing, etc.) is central to grounding language in the real driving state

## Limitations & Open Questions

- **Latency**: LLM inference adds latency that may be unacceptable for time-critical safety commands -- the paper does not fully address real-time constraints for urgent situations
- **Grounding**: Spatial grounding of references like "that building" or "the car ahead" requires integration with perception systems not fully addressed in the framework
- **Evaluation scope**: Evaluation is limited to qualitative case studies in HighwayEnv rather than large-scale quantitative benchmarking or real-world user studies
- **Hallucination risk**: LLMs may generate incorrect information about the driving environment or vehicle capabilities, which could erode trust
- **Open question**: How should an LLM-based interface handle conflicting commands from multiple passengers?
- **Open question**: What is the right level of autonomy for the LLM -- should it proactively suggest route changes or only respond to explicit commands?

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt]] -- contemporaneous work using LLMs for driving, but focused on LLM-as-planner rather than LLM-as-interface
- [[wiki/sources/papers/drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model]] -- shares the goal of explainable driving via language but focuses on VLM instruction tuning for joint control + explanation
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]] -- language-conditioned driving in closed-loop, complementary to DAYS's focus on human interaction
- [[wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering]] -- uses graph VQA for structured driving reasoning, related to DAYS's informational query handling
- [[wiki/sources/papers/driving-with-llms-fusing-object-level-vector-modality-for-explainable-autonomous-driving]] -- Wayve's LLM-for-driving with vector modality, shares explainability goals
- [[wiki/sources/papers/talk2car-taking-control-of-your-self-driving-car]] -- earlier work on natural language command grounding for driving
- [[wiki/concepts/planning]] -- broader context on planning evolution toward language-integrated systems
- [[wiki/concepts/autonomous-driving]] -- application domain context
