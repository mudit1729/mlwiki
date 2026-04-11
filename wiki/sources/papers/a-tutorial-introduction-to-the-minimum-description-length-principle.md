---
title: A Tutorial Introduction to the Minimum Description Length Principle
type: source-summary
status: complete
updated: 2026-04-11
year: 2004
venue: arXiv / MIT Press
tags:
  - paper
  - ilya-30
  - information-theory
  - model-selection
  - compression
  - mdl
citations: 381
paper-faithfullness: audited-solid
---

📄 **[Read on arXiv](https://arxiv.org/abs/math/0406077)**

# A Tutorial Introduction to the Minimum Description Length Principle

## Citation

Grunwald, arXiv math/0406077 / MIT Press, 2004.

## Canonical link

- [Paper](https://arxiv.org/abs/math/0406077)

## Overview

The Minimum Description Length (MDL) principle formalizes Occam's razor via coding theory: the best model is the one that minimizes the total code length for describing both the model itself and the data given the model, thereby automatically trading off fit against complexity. This tutorial by Grunwald provides a comprehensive introduction to the MDL framework, connecting ideas from information theory, statistics, and algorithmic complexity into a unified model selection methodology.

MDL provides a principled, assumption-light framework for model selection that avoids the limitations of alternatives. Unlike cross-validation (which wastes data) or Bayesian model selection (which requires prior specification), MDL derives complexity penalties directly from coding theory. The tutorial makes explicit the deep connection between compression and learning -- any regularity in data can be exploited for compression, so the ability to compress is equivalent to the ability to generalize.

This idea underpins modern intuitions about why overparameterized models generalize and why simplicity biases matter in deep learning. The tutorial covers both the theoretical foundations (two-part codes, Kolmogorov complexity, Normalized Maximum Likelihood) and practical applications (polynomial regression, Markov chain order selection, histogram density estimation), making it accessible to both theorists and practitioners.

## Key Contributions

- **Two-part code framework**: Total description length = L(model) + L(data | model). Model complexity is penalized by the bits needed to specify it, providing automatic regularization without holdout sets.
- **Connection to Kolmogorov complexity**: The ideal MDL principle assigns probability proportional to 2^{-K(H)} to hypothesis H, grounding model selection in algorithmic information theory, though K is uncomputable in practice.
- **Normalized Maximum Likelihood (NML)**: Introduces NML as an optimal one-part universal code for finite model classes, resolving the arbitrary discretization problem of naive two-part codes.
- **Equivalence to other criteria**: Shows that MDL subsumes BIC asymptotically and relates to prequential (predictive) coding, bridging frequentist and Bayesian perspectives.
- **Practical model selection procedure**: Provides concrete recipes for polynomial regression, Markov chain order selection, and histogram density estimation using MDL.

## Architecture / Method

The MDL framework operates at two levels. The crude (two-part) MDL approach encodes data in two parts: first the model hypothesis H (requiring L(H) bits), then the data given the model (requiring L(data|H) bits). The best model minimizes L(H) + L(data|H). For parametric models, L(H) includes the bits to specify both the model class and the parameter values, naturally penalizing models with more parameters or higher precision parameter specifications.

The refined MDL approach uses one-part (universal) codes that avoid the arbitrary discretization of parameter space required by two-part codes. The Normalized Maximum Likelihood (NML) distribution is defined as p_NML(x) = p(x|theta_hat(x)) / sum_y p(y|theta_hat(y)), where theta_hat(x) is the maximum likelihood estimate for data x. The normalizing constant (the denominator) is called the parametric complexity and measures the inherent complexity of the model class. The tutorial shows NML is minimax optimal: it achieves the shortest worst-case regret among all universal codes.

The prequential (predictive) coding approach provides a computationally tractable alternative: encode data sequentially, using the model's prediction of each data point given all previous data points. The total prequential code length equals the sum of sequential negative log-likelihoods, relating MDL to online learning and predictive validation.

## Results

- **MDL avoids overfitting without cross-validation**: On polynomial regression examples, MDL selects the correct degree even when maximum likelihood overfits, because the cost of specifying extra parameters exceeds the reduction in residual code length.
- **Compression implies understanding**: The tutorial demonstrates on synthetic data that models achieving shorter total description length also have better predictive performance on held-out data, validating the compress-to-generalize principle.
- **NML is minimax optimal**: Among all universal codes for a parametric model class, NML achieves the shortest worst-case regret, providing a theoretically justified default.
- **MDL subsumes BIC**: For regular parametric models, the two-part MDL code length converges to BIC asymptotically, but MDL remains valid in finite-sample regimes where BIC's asymptotic approximation breaks down.

## Limitations & Open Questions

- Kolmogorov complexity is uncomputable, so practical MDL must use approximations (two-part codes, NML, prequential codes) that introduce design choices.
- NML is defined only for finite sample spaces and bounded parameter sets; extending it to continuous or infinite-dimensional model classes requires regularization or truncation.
- The tutorial focuses on classical statistical models; applying MDL principles to deep neural networks (where parameter counting is a poor proxy for complexity) remains an open research direction.

## Connections

- [[wiki/concepts/machine-learning]]
- [[wiki/sources/papers/keeping-neural-networks-simple-by-minimizing-the-description-length-of-the-weights]]
- [[wiki/sources/papers/kolmogorov-complexity-and-algorithmic-randomness]]
