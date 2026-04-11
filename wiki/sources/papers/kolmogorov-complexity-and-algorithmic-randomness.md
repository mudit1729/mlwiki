---
title: Kolmogorov Complexity and Algorithmic Randomness
type: source-summary
status: complete
updated: 2026-04-11
year: 2017
venue: AMS Mathematical Surveys and Monographs
tags:
  - paper
  - ilya-30
  - information-theory
  - kolmogorov-complexity
  - algorithmic-randomness
  - computability
citations: 106
paper-faithfullness: audited-solid
---

📄 **[AMS Book Page](https://bookstore.ams.org/surv-220)**

# Kolmogorov Complexity and Algorithmic Randomness

## Overview

This monograph by Shen, Uspensky, and Vereshchagin is the definitive modern reference on algorithmic information theory. The central concept is Kolmogorov complexity K(x) -- the length of the shortest program that produces string x on a universal Turing machine -- which provides a rigorous, distribution-free definition of information content and randomness. A string is random if and only if it is incompressible: no program significantly shorter than the string itself can generate it.

The book presents a comprehensive treatment of the field, connecting three seemingly different mathematical phenomena: compressibility of strings, passing statistical tests for randomness, and unpredictability against betting strategies. The deep result that these three characterizations are equivalent (Martin-Lof randomness theorem) establishes that the definition of algorithmic randomness captures a genuine mathematical property rather than an artifact of any particular formalization.

For machine learning, the core insight is that compression ability equals pattern recognition ability. This directly motivates the Minimum Description Length principle, Solomonoff induction, and information-theoretic approaches to generalization. Models that find shorter descriptions of training data tend to generalize better because they have discovered genuine patterns rather than memorizing noise. The book also establishes the fundamental uncomputability of K(x), which sets hard limits on what any learning algorithm can know about the true complexity of its data.

## Key Contributions

- **Three equivalent definitions of randomness:** A sequence is Martin-Lof random if and only if it is (1) incompressible, (2) passes all effective statistical tests, and (3) no computable betting strategy can profit from it -- a deep unification theorem
- **Plain vs. prefix complexity:** Plain complexity C(x) uses arbitrary programs; prefix complexity K(x) restricts to prefix-free codes, yielding cleaner additivity properties K(x,y) <= K(x) + K(y) + O(1) essential for applications in coding theory and statistics
- **Invariance theorem:** K(x) is independent of the choice of universal Turing machine up to an additive constant, making it an objective property of the string itself rather than an artifact of the computing model
- **Symmetry of information:** K(x,y) = K(x) + K(y|x) + O(log n), formalizing the intuition that the information in a pair equals the information in one plus the conditional information in the other
- **Uncomputability and approximation:** K(x) is provably not computable (reducible to the halting problem), but can be approximated from above by practical compressors, connecting the theory to engineering applications

## Architecture / Method

The book develops algorithmic information theory through a careful progression of definitions and results. The foundational concept is the universal Turing machine U, which can simulate any other Turing machine given a description of that machine. Kolmogorov complexity is defined relative to U: K_U(x) = min{|p| : U(p) = x}, where |p| is the length of program p in bits.

The invariance theorem shows that for any two universal Turing machines U and V, |K_U(x) - K_V(x)| <= c for some constant c independent of x. This means the complexity is determined (up to a constant) by the string itself, not the computing model -- a remarkable and non-obvious result.

Plain complexity C(x) allows arbitrary programs; prefix complexity K(x) restricts to prefix-free programs (no program is a proper prefix of another). The prefix-free restriction is mathematically essential because it yields the Kraft inequality property: the sum of 2^{-K(x)} over all strings x converges, making 2^{-K(x)} a valid (semi-)probability distribution. This distribution -- the universal prior -- is central to Solomonoff's theory of inductive inference.

The book then develops conditional complexity K(x|y) (the complexity of x given access to y), mutual information I(x:y) = K(x) + K(y) - K(x,y), and the symmetry of information theorem. These tools parallel Shannon information theory but apply to individual strings rather than probability distributions.

The chapter on randomness establishes the equivalence of three definitions: (1) incompressibility: K(x_1...x_n) >= n - O(1) for all prefixes, (2) typicality: x passes every effectively constructible statistical test (Martin-Lof test), (3) unpredictability: no computable martingale can make unbounded profit betting on successive bits of x. The proof of equivalence is one of the deepest results in the field.

## Results

- For binary strings of length n, the fraction of strings with K(x) < n - c is at most 2^{-c}, so almost all strings are nearly incompressible, confirming that randomness is the typical state
- Martin-Lof randomness is robust: the three characterizations (compression, statistical tests, betting) are proven equivalent, establishing that the definition is natural and canonical
- Kolmogorov complexity dominates all computable measures: for any computable probability distribution P, -log P(x) >= K(x) - O(1) for all x, meaning K(x) is the ultimate lower bound on description length
- The symmetry of information K(x,y) = K(x) + K(y|x) + O(log n) holds up to logarithmic precision, confirming that mutual information is a symmetric concept even in the algorithmic setting
- Incompressible strings exist at every length (in fact, at least half of all strings of length n have K(x) >= n), but no algorithm can certify that a given string is incompressible

## Limitations & Open Questions

- K(x) is uncomputable; practical applications must use upper-bound approximations (gzip, LZ77, neural compressors) that can be arbitrarily loose for structured data, limiting the direct applicability of the theory
- The theory applies to discrete strings; extending Kolmogorov complexity to continuous objects, function spaces, or infinite-dimensional representations requires additional formalism that is not fully developed
- Connections between algorithmic randomness and the generalization behavior of deep neural networks remain largely informal and conjectural, though the compression-generalization link is increasingly supported by empirical evidence

## Connections

- [[wiki/concepts/machine-learning]]
- [[wiki/sources/papers/keeping-neural-networks-simple-by-minimizing-the-description-length-of-the-weights]]
- [[wiki/sources/papers/a-tutorial-introduction-to-the-minimum-description-length-principle]]
- [[wiki/sources/papers/the-first-law-of-complexodynamics]]
- [[wiki/sources/papers/quantifying-the-rise-and-fall-of-complexity-in-closed-systems-the-coffee-automaton]]
