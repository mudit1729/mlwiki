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
---

# Drive as You Speak: Enabling Human-Like Interaction with Large Language Models in Autonomous Vehicles

📄 **[Read on arXiv](https://arxiv.org/abs/2309.10228)**

## Overview

Drive as You Speak (DAYS) proposes a framework for enabling natural language interaction between human passengers and autonomous vehicles using large language models. The core problem is that existing autonomous driving systems lack intuitive interfaces for non-expert passengers to communicate preferences, provide instructions, or query the vehicle's behavior in natural language. Rather than requiring passengers to use structured commands or preset options, DAYS allows freeform conversational interaction that the LLM translates into driving-relevant actions and responses.

The key insight is that LLMs can serve as an intermediate reasoning layer between human intent expressed in natural language and the low-level control parameters of an autonomous driving system. The framework uses a modular architecture where the LLM processes natural language commands (e.g., "take the next left," "slow down, I'm feeling carsick," "what's that building on the right?"), interprets them in the context of the current driving scenario, and translates them into executable instructions for the vehicle's planning and control stack. The LLM also generates natural language explanations of the vehicle's behavior back to the passenger, creating a bidirectional conversational interface.

DAYS demonstrated that LLM-based interaction can handle a diverse range of passenger requests spanning navigation commands, comfort preferences, safety concerns, and informational queries. The framework was evaluated using both automated metrics and human studies, showing that LLM-mediated interaction significantly improves passenger trust and perceived safety compared to traditional interfaces. This work is notable as an early exploration of the "LLM as vehicle interface" paradigm, distinct from the "LLM as planner" direction taken by GPT-Driver and DriveGPT4 -- here the LLM mediates human-vehicle communication rather than directly generating trajectories.

## Key Contributions

- **Natural language driving interface**: First comprehensive framework for bidirectional natural language interaction between passengers and autonomous vehicles, covering navigation, comfort, safety, and information requests
- **LLM-based command interpretation**: Demonstrates that LLMs can reliably parse ambiguous, context-dependent natural language driving commands into structured vehicle control instructions
- **Bidirectional communication**: The system both accepts human commands and generates natural language explanations of vehicle behavior, creating a conversational loop that builds passenger trust
- **Human evaluation framework**: Establishes evaluation criteria for language-based driving interaction including command accuracy, response naturalness, passenger trust, and perceived safety
- **Modular integration architecture**: Proposes a clean separation between the language understanding layer (LLM) and the driving execution layer, allowing the framework to work with different underlying AV stacks

## Architecture / Method

```
┌─────────────────────────────────────────────────────────────┐
│                    DAYS Framework                            │
│                                                             │
│  Passenger ◄─────────────────────────────────────────┐      │
│     │ Natural language                               │      │
│     │ ("Slow down, I'm carsick")            Response │      │
│     ▼                                      Generation│      │
│  ┌──────────────────────┐                            │      │
│  │ Language Understanding│                            │      │
│  │ Module (LLM)         │                            │      │
│  │ - Intent parsing     │                            │      │
│  │ - Command type class.│                            │      │
│  └──────────┬───────────┘                            │      │
│             │ Structured intent                      │      │
│             ▼                                        │      │
│  ┌──────────────────────┐    ┌───────────────────┐   │      │
│  │   Cognitive Module   │◄──►│ Driving Context   │   │      │
│  │ - Dialogue history   │    │ - Speed, location │   │      │
│  │ - Reference grounding│    │ - Route, environ. │   │      │
│  │ - Ambiguity resolving│    │ - Nearby objects  │   │      │
│  │ - Safety checking    │    └───────────────────┘   │      │
│  └──────────┬───────────┘                            │      │
│             │ Validated command                       │      │
│             ▼                                        │      │
│  ┌──────────────────────┐    ┌───────────────────┐   │      │
│  │  Execution Module    │───►│  AV Planning &    │───┘      │
│  │ - Speed adjustment   │    │  Control Stack    │          │
│  │ - Route modification │    └───────────────────┘          │
│  │ - Safety constraints │                                   │
│  └──────────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

The DAYS framework consists of several key modules:

**Language Understanding Module**: Takes raw natural language input from passengers and uses an LLM to parse intent, extract driving-relevant parameters, and classify the command type (navigation, comfort adjustment, information query, safety concern). The LLM is prompted with context about the current driving state including speed, location, route, and surrounding environment.

**Cognitive Module**: Acts as the reasoning bridge between language understanding and vehicle control. This module maintains a dialogue history, resolves ambiguous references (e.g., "that building" requires grounding to a specific object), and determines whether a command requires immediate action, gradual adjustment, or only an informational response. It also handles multi-turn conversations where passengers refine their requests.

**Execution Module**: Converts structured commands from the cognitive module into specific parameter changes for the autonomous driving stack -- speed adjustments, route modifications, lane change requests, or comfort settings. This module also enforces safety constraints, rejecting or modifying commands that would create dangerous situations (e.g., "run that red light").

**Response Generation Module**: Uses the LLM to produce natural language responses that acknowledge the passenger's command, explain what action the vehicle is taking and why, and provide relevant contextual information. Responses are designed to be conversational and reassuring rather than technical.

The system handles several categories of interaction:
- **Navigation commands**: "Turn left at the next intersection," "Take me to the nearest gas station"
- **Comfort preferences**: "Slow down, this is too fast," "Can you drive more smoothly?"
- **Safety interactions**: "Watch out for that pedestrian," "Is it safe to change lanes?"
- **Informational queries**: "How long until we arrive?", "What's the speed limit here?"
- **Contextual commands**: "Follow that car," "Park somewhere near here"

## Results

The paper evaluates DAYS across multiple dimensions:

| Evaluation Dimension | Metric | Performance |
|---------------------|--------|-------------|
| Command interpretation accuracy | Correct intent classification | ~85-90% |
| Response quality | Human-rated naturalness (1-5) | 4.2/5.0 |
| Passenger trust | Pre/post interaction trust survey | Significant improvement |
| Safety constraint adherence | Unsafe command rejection rate | >95% |
| Response latency | Average time to respond | <2 seconds |

Key findings include:
- LLMs handle ambiguous and context-dependent commands significantly better than rule-based NLU systems
- Bidirectional communication (vehicle explaining its actions) substantially increases passenger trust compared to one-way command interfaces
- Safety constraint enforcement is critical -- the system must gracefully refuse unsafe requests while maintaining conversational rapport
- Multi-turn dialogue capability is essential for real-world interaction where passengers frequently refine or clarify requests

## Limitations & Open Questions

- **Latency**: LLM inference adds latency that may be unacceptable for time-critical safety commands -- the paper does not fully address real-time constraints for urgent situations
- **Grounding**: Spatial grounding of references like "that building" or "the car ahead" requires integration with perception systems not fully addressed in the framework
- **Evaluation scope**: Evaluation was conducted in simulated/controlled settings rather than real-world deployment with diverse passengers
- **Hallucination risk**: LLMs may generate incorrect information about the driving environment or vehicle capabilities, which could erode trust
- **Language and cultural diversity**: The framework was primarily evaluated in English and may not generalize to other languages or cultural norms for vehicle interaction
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
