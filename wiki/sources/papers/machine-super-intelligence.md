---
title: Machine Super Intelligence
type: source-summary
status: complete
updated: 2026-04-11
year: 2008
venue: PhD Thesis, University of Lugano
tags:
  - paper
  - ilya-30
  - agi
  - intelligence-measurement
  - algorithmic-information-theory
citations: 63
paper-faithfullness: audited-clean
---

📄 **[Read Thesis](https://www.vetta.org/documents/Machine_Super_Intelligence.pdf)**

## Overview

Shane Legg's 2008 PhD thesis provides perhaps the most rigorous mathematical definition of general intelligence, grounding informal intuitions in algorithmic information theory and sequential decision theory. The Universal Intelligence Measure (UIM) defines intelligence as an agent's expected reward across all computable environments, weighted by each environment's algorithmic simplicity (inverse Kolmogorov complexity). This yields a single scalar that applies to humans, animals, and machines without reference to any specific task.

By proving that AIXI -- an agent that combines Solomonoff's universal prior over environments with sequential decision theory -- is Pareto-optimal under this measure, the thesis establishes an upper bound on achievable intelligence and gives the AGI safety community a formal target to reason about. Shane Legg co-founded DeepMind shortly after this work, and the thesis's framing of superintelligence risk directly influenced early AI safety discourse.

The thesis also provides a comprehensive survey and formal unification of over 70 definitions of intelligence from psychology, cognitive science, and AI, showing that most informal definitions are special cases of the UIM. This unification gave the field a common mathematical language for discussing intelligence and its limits.

## Key Contributions

- **Universal Intelligence Measure**: Phi(pi) = sum over all computable environments mu of 2^{-K(mu)} * V_mu^pi, where K(mu) is the Kolmogorov complexity of the environment and V is cumulative reward -- defines intelligence without reference to any particular task
- **AIXI as optimal agent**: Combines Solomonoff's universal prior over environments with sequential decision theory; proven to be Pareto-optimal (no computable agent dominates it across all environments)
- **Simplicity weighting is necessary**: Without weighting environments by 2^{-K(mu)}, the measure becomes trivial (dominated by adversarial or random environments); the Solomonoff prior provides the principled weighting
- **Survey and formal unification of 70+ intelligence definitions**: Synthesizes definitions from psychology, cognitive science, and AI into a single formal framework, showing most informal definitions are special cases of the UIM
- **Formal definition of superintelligence**: An agent whose UIM exceeds that of any human, providing a mathematically precise threshold for the concept

## Architecture / Method

The thesis is primarily theoretical rather than architectural, but the key formal construction is:

**Universal Intelligence Measure**: For an agent pi interacting with environment mu through actions and observations, define Phi(pi) = sum_mu 2^{-K(mu)} * V_mu^pi, where K(mu) is the Kolmogorov complexity (shortest program length) of environment mu, and V_mu^pi is the expected cumulative reward of pi in mu. The sum runs over all computable environments, with simpler environments weighted exponentially more.

**AIXI agent**: At each timestep, AIXI selects the action that maximizes expected future reward under the mixture over all computable environments consistent with the interaction history so far. Formally, AIXI maintains a Bayesian posterior over environments using the Solomonoff universal prior, and acts optimally with respect to this posterior. This requires enumeration of all programs and is therefore incomputable.

**Computable approximations**: The thesis discusses AIXItl (time-bounded AIXI that considers only programs of length at most l that run in at most t steps) and other bounded approximations that trade optimality for computability. These establish a spectrum from the incomputable ideal to practical agents.

**Intelligence ordering**: The UIM induces a total ordering on agents, allowing formal comparison of intelligence levels across different agent types, embodiments, and domains.

## Results

- AIXI achieves maximal intelligence under the UIM: proven via construction that no computable agent can uniformly outperform it across all environments (Pareto optimality theorem)
- The measure correlates with intuitive intelligence rankings: when evaluated on simple environments, AIXI-approximations outperform random agents and simple learners, consistent with the ordering humans would assign
- Incomputability is fundamental: AIXI requires solving the halting problem; practical approximations (AIXItl, MC-AIXI) trade optimality for computability, establishing a complexity-intelligence tradeoff
- The survey reveals that most informal definitions of intelligence emphasize learning, adaptation, and goal-achievement -- all captured by the UIM's reward-maximization-across-environments formulation

## Limitations & Open Questions

- AIXI and the UIM are incomputable; all practical agents are computable approximations with unknown approximation quality on real-world problems
- The measure is sensitive to the choice of universal Turing machine (UTM) up to a constant; while asymptotically irrelevant, for finite agents this constant matters and could reorder agents
- The framework assumes a single scalar reward signal; it does not address multi-objective intelligence, social intelligence, or embodied cognition where reward specification itself is the hard problem

## Connections

- [[wiki/concepts/machine-learning]] -- foundational theoretical framework for ML agents
- [[wiki/sources/papers/kolmogorov-complexity-and-algorithmic-randomness]] -- mathematical foundation for the simplicity prior
- [[wiki/sources/papers/a-tutorial-introduction-to-the-minimum-description-length-principle]] -- related information-theoretic framework
