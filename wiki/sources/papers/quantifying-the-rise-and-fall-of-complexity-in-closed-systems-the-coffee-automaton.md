---
title: "Quantifying the Rise and Fall of Complexity in Closed Systems: The Coffee Automaton"
type: source-summary
status: complete
updated: 2026-04-05
year: 2014
venue: arXiv 2014
tags:
  - paper
  - ilya-30
  - complexity-theory
  - information-theory
  - thermodynamics
citations: 26
paper-faithfullness: audited-solid
---

📄 **[Read on arXiv](https://arxiv.org/abs/1405.6903)**

## Overview

This paper bridges thermodynamics and computational complexity to formalize a deep intuition: mixing cream into coffee produces increasingly complex patterns (swirls, filaments) before eventually reaching boring uniformity. While entropy monotonically increases per the Second Law, the apparent complexity of coarse-grained descriptions is non-monotonic. The authors construct a concrete model -- the coffee automaton, a minimal 2D cellular automaton with binary cell states evolving under diffusion-like dynamics -- and define complexity via the compressibility of coarse-grained macroscopic states.

The key formal result is the separation of entropy and complexity: entropy S(t) increases monotonically toward equilibrium while complexity C(t) follows an inverted-U trajectory. At t=0, the state is simple (cream on top, coffee below). At intermediate times, intricate mixing patterns produce highly complex (incompressible) coarse-grained descriptions. At t=infinity, the uniform equilibrium is again simple. The paper shows that genuine complexity rise-and-fall requires particle interactions: the non-interacting model's apparent complexity rise is shown analytically and numerically to be a coarse-graining artifact, while the interacting model exhibits genuine complexity rise-and-fall that persists under refined coarse-graining.

Ilya Sutskever included this on his recommended reading list presumably because the same rise-and-fall pattern may characterize training dynamics in neural networks. Early in training, representations are simple (random). During training, they become increasingly structured and complex. At convergence, they may simplify again into clean, generalizable features. The connection is suggestive but not formally established.

## Key Contributions

- **Coarse-grained complexity measure**: Defines "apparent complexity" as the Kolmogorov complexity of a coarse-grained approximation of the automaton's state, practically approximated by the gzip compressed file size of the thresholded coarse-grained array, capturing the intuition that intermediate-scale structure is what makes a state "complex"
- **Coffee automaton model**: A minimal L x L cellular automaton with binary cell states (cream/coffee) evolving under diffusion-like dynamics, demonstrating the universal rise-and-fall pattern with periodic boundary conditions ensuring true isolation
- **Separation of entropy and complexity**: Proves that entropy S(t) increases monotonically while complexity C(t) follows an inverted-U trajectory
- **Connection to Kolmogorov complexity**: Relates the coarse-grained complexity measure to the compressibility of the macroscopic description, grounding the framework in algorithmic information theory

## Architecture / Method

The coffee automaton is not a neural architecture but a physical model. The setup is:

**Grid**: An L x L grid with periodic boundary conditions (torus topology), ensuring the system is truly closed. Each cell has a binary state: 0 (coffee) or 1 (cream).

**Initial condition**: Cream occupies the top half, coffee the bottom half, representing the moment cream is added to coffee.

**Dynamics**: The paper studies two model variants. In the interacting model, at each timestep a randomly selected pair of horizontally or vertically adjacent cells with *differing* states (one cream, one coffee) swap their values, enforcing single occupancy and modeling realistic diffusion. In the non-interacting model, each cream particle independently moves one step in a randomly chosen direction, allowing multiple particles per cell; this simpler model is used for theoretical analysis.

**Coarse-graining**: Each cell in the coarse-grained array is the average of cells within a g x g square (grain size) centered at the corresponding location in the original array. This sliding-window average is then thresholded into discrete buckets (e.g., three buckets: mostly coffee, mostly cream, mixed; experiments also use up to 7 buckets). The paper also studies an "adjusted" coarse-graining that applies a heuristic local adjustment to suppress artifactual complexity.

**Complexity measure**: The apparent complexity is the gzip compressed file size of the thresholded coarse-grained array, used as a practical proxy for Kolmogorov complexity. A high complexity score means the coarse-grained pattern is hard to compress -- it contains non-random structure. The paper also reports gzip of the fine-grained state as a proxy for entropy. Results are shown to be qualitatively robust across gzip, bzip2, and lzma compressors.

## Results

![Evolution of complexity and entropy over time -- entropy increases monotonically while complexity exhibits rise-and-fall pattern](https://paper-assets.alphaxiv.org/figures/1405.6903v1/img-0.jpeg)

- Simulation of the coffee automaton shows C(t) peaks at intermediate times while S(t) increases monotonically throughout, with the peak time depending on system size L and coarse-graining scale m
- Different coarse-graining resolutions m produce complexity peaks at different times: finer resolutions peak earlier and coarser resolutions peak later, confirming that complexity is a property of the observation scale
- The genuine rise-and-fall is specific to the interacting model; the non-interacting model's apparent complexity increase is eliminated by the adjusted coarse-graining method, confirming that particle interactions are necessary for genuine intermediate complexity
- The maximum complexity scales linearly with system size N (consistent with complexity developing along one primary mixing dimension), while the time to reach maximum complexity scales quadratically with N (consistent with diffusion timescales for N^2 particles)

## Limitations & Open Questions

- The complexity measure depends on the choice of coarse-graining function phi, which is somewhat arbitrary; different coarse-grainings yield different complexity trajectories, and there is no canonical choice
- The coffee automaton is a highly simplified model; extending the framework to continuous physical systems or high-dimensional state spaces (like neural network training) requires significant additional theoretical work
- The connection between thermodynamic complexity dynamics and the emergence of useful representations during ML training is suggestive but not formally established -- an exciting open direction

## Connections

- [[wiki/concepts/machine-learning]] -- potential analogy to training dynamics and representation learning
- [[wiki/sources/papers/kolmogorov-complexity-and-algorithmic-randomness]] -- mathematical foundation for the complexity measure
- [[wiki/sources/papers/the-first-law-of-complexodynamics]] -- related work on complexity dynamics in physical systems
- [[wiki/sources/papers/a-tutorial-introduction-to-the-minimum-description-length-principle]] -- connections to description length and compressibility
