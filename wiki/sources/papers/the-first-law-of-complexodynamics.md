---
title: The First Law of Complexodynamics
type: source-summary
status: complete
updated: 2026-04-11
year: 2011
venue: Blog Post (Shtetl-Optimized)
tags:
  - paper
  - ilya-30
  - complexity-theory
  - information-theory
  - thermodynamics
citations: 0
paper-faithfullness: audited-fixed
---

📄 **[Read Blog Post](https://scottaaronson.blog/?p=762)**

# The First Law of Complexodynamics

## Overview

Scott Aaronson's blog post highlights an asymmetry between entropy and complexity as a way of thinking about structure formation in physical and computational systems. While the second law of thermodynamics dictates that entropy monotonically increases, complexity -- the "interestingness" or structural richness of a system -- is argued to follow a non-monotonic arc: low at early times (ordered initial state), high at intermediate times (transitional dynamics with rich structure), and low again at equilibrium (featureless thermal noise).

This observation, while intuitively obvious (a cup of coffee is most "interesting" while cooling, not when uniformly hot or uniformly room-temperature), resists formal mathematical treatment. Aaronson proposes "complextropy" as a formal measure based on Kolmogorov complexity that could capture this phenomenon: roughly, the number of bits in the shortest efficient program (running in n log(n) time) that outputs a nearly-uniform sample from a set S containing the target string x, such that no efficient program can reconstruct x from samples of S in fewer than log2(|S|)-c bits. Pure randomness has low complextropy (S is just all n-bit strings, trivially described), perfect order has low complextropy (S is a singleton, trivially described), but structured intermediate states have high complextropy.

In this wiki, the post is useful mainly as a conceptual prompt linking entropy, description length, and emergent structure. It is explicitly a speculative blog essay rather than a finished theorem or an empirical study of learning dynamics.

## Key Contributions

- **Complexity vs. entropy distinction**: Entropy measures the number of possible microstates (monotonically increasing); complexity measures structural richness or difficulty of description (non-monotonic). A fully random system has maximum entropy but low complexity
- **The complexity arc**: For natural dynamical systems, complexity is small at t~0 (ordered initial state), large at intermediate t (transitional dynamics with rich structure), and small as t approaches infinity (thermalized equilibrium)
- **Complextropy measure**: A proposed formal complexity measure based on Kolmogorov complexity -- the number of bits in the shortest efficient program (running in n log(n) time) that outputs a nearly-uniform sample from a set S containing the target string x, subject to the constraint that no efficient program can reconstruct x from S-samples using fewer than log2(|S|)-c bits
- **Randomness is not complexity**: Pure noise is highly compressible as "sample from uniform distribution" and thus has low complextropy; true complexity requires structure that distinguishes a system from both perfect order and white noise
- **Connection to phase transitions**: Complexity peaks at the boundary between order and chaos, linking to self-organized criticality, edge-of-chaos phenomena, and critical points in statistical mechanics

## Architecture / Method

This is a conceptual/theoretical blog post rather than an empirical paper, so there is no architecture or experimental method. The argument proceeds through physical examples and proposed formalizations.

Aaronson builds the argument through concrete examples: a cup of cooling coffee (uniform hot liquid -> complex convection patterns -> uniform room-temperature liquid), star formation (homogeneous gas cloud -> turbulent accretion with jets and proto-planetary disks -> stable stellar system), and cosmic evolution (near-uniform initial state -> galaxies, stars, planets, life -> eventual heat death). In each case, the system passes through a complexity peak during transitional dynamics.

The proposed formalization uses algorithmic information theory. For an n-bit string x, the complextropy is defined as the number of bits in the shortest program P running in n log(n) time such that: (1) P outputs a nearly-uniform sample from some set S with x∈S, and (2) any program that reconstructs x in n log(n) time using samples from S as an oracle requires at least log2(|S|)-c bits. Condition (2) is what excludes both low-entropy ordered states (x is easily reconstructed without needing a large S) and maximum-entropy random states (S is all n-bit strings, described trivially).

## Results

- **Physical systems exhibit complexity arcs**: Demonstrated through multiple examples including cooling coffee, star formation, biological evolution, and cosmic structure formation -- in each case the system transitions from low complexity through a peak to low complexity again
- **Entropy and complexity are decoupled**: A system can have simultaneously high entropy and low complexity (thermal noise) or low entropy and low complexity (perfect crystal), proving they measure fundamentally different properties of physical systems
- **The formalization challenge is identified precisely**: Aaronson explicitly characterizes what theorems would need to be proved and where the mathematical difficulties lie, providing a roadmap for future formalization
- **Connection to computational complexity**: The complextropy definition connects to circuit complexity and pseudorandomness theory, suggesting that complexity peaks correspond to computationally hard-to-describe distributions

## Limitations & Open Questions

- The complextropy measure lacks a rigorous formal proof that it exhibits the predicted non-monotonic trajectory across natural physical systems -- the framework remains primarily conceptual and qualitative
- Quantitative predictions for specific physical systems remain unestablished; there is no way to compute complextropy for real systems, limiting practical applicability
- The connection to neural network training dynamics (double descent, grokking, phase transitions in learning) is suggestive and philosophically illuminating but not formalized or empirically validated

## Connections

- [[wiki/concepts/machine-learning]]
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]]
- [[wiki/sources/papers/quantifying-the-rise-and-fall-of-complexity-in-closed-systems-the-coffee-automaton]]
- [[wiki/sources/papers/kolmogorov-complexity-and-algorithmic-randomness]]
- [[wiki/sources/papers/a-tutorial-introduction-to-the-minimum-description-length-principle]]
