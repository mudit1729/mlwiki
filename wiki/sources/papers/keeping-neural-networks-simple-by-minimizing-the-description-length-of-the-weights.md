---
title: Keeping Neural Networks Simple by Minimizing the Description Length of the Weights
type: source-summary
status: complete
updated: 2026-04-11
year: 1993
venue: COLT
tags:
  - paper
  - ilya-30
  - regularization
  - information-theory
  - minimum-description-length
  - bayesian-inference
  - generalization
citations: 1279
paper-faithfullness: audited-solid
---

📄 **[Read Paper](https://www.cs.toronto.edu/~hinton/absps/colt93.pdf)**

# Keeping Neural Networks Simple by Minimizing the Description Length of the Weights

## Overview

This paper by Hinton and van Camp bridges information theory and neural network generalization by proposing that model complexity should be measured by the literal number of bits required to encode the network weights. Rather than using ad-hoc regularization techniques like weight decay, the authors derive regularization from first principles using the Minimum Description Length (MDL) principle: the best model is the one that minimizes the total number of bits needed to describe both the weights and the training errors given those weights.

The key technical innovation is bits-back coding, which shows that the cost of encoding weights using a posterior distribution q(w) relative to a prior p(w) equals exactly the KL divergence KL[q(w) || p(w)]. This creates a precise, computable measure of model complexity that directly connects MDL to Bayesian inference. Minimizing description length is formally equivalent to maximizing the posterior probability of the weights, and standard L2 regularization (weight decay) emerges as a special case when the prior is Gaussian.

This paper predates modern Bayesian deep learning by over 25 years and provides the theoretical justification for why simpler models generalize: they require fewer bits to specify, leaving more of the data's information content to be explained by genuine patterns rather than memorized noise. The framework is foundational for understanding regularization, compression, pruning, and the bias-variance tradeoff from information-theoretic first principles, and it connects directly to Kolmogorov complexity and algorithmic information theory.

## Key Contributions

- **MDL for neural networks:** Reframing regularization as a two-part coding problem where total cost = bits to describe weights + bits to describe training errors given weights, with the optimal model minimizing this sum
- **Bits-back coding:** The encoding cost equals KL[q(w) || p(w)] = E_q[log q(w)/p(w)], giving a precise and computable measure of model complexity directly from the weight distribution
- **Equivalence to Bayesian inference:** Minimizing description length under MDL is formally equivalent to maximizing the posterior probability of weights under a Bayesian framework, unifying two seemingly different approaches to model selection
- **Posterior weight distributions:** The framework naturally considers distributions over weights rather than point estimates, with high-entropy posteriors (uncertain weights) costing fewer bits and providing an automatic Occam's razor
- **Derivation of standard regularizers:** Weight decay (L2) emerges as a special case when the prior is Gaussian; other priors yield other regularizers, providing a principled way to choose regularization from prior beliefs

## Architecture / Method

```
┌─────────────────────────────────────────────────────────┐
│              MDL Two-Part Coding Framework               │
│                                                         │
│  Sender (has data + trained model)                      │
│    │                                                    │
│    ├──► Part 1: Encode Weights                          │
│    │    ┌───────────┐    ┌───────────┐                  │
│    │    │ Posterior  │    │   Prior   │                  │
│    │    │   q(w)     │───►│   p(w)    │                  │
│    │    └───────────┘    └───────────┘                  │
│    │    Cost = KL[ q(w) || p(w) ] bits                  │
│    │                                                    │
│    ├──► Part 2: Encode Data Errors                      │
│    │    ┌───────────┐    ┌───────────┐                  │
│    │    │  Network   │───►│ Residuals │                  │
│    │    │  w ~ q(w)  │    │  D - f(w) │                  │
│    │    └───────────┘    └───────────┘                  │
│    │    Cost = E_q[ -log P(D|w) ] bits                  │
│    │                                                    │
│    └──► Total: L_MDL = KL[q||p] + E_q[-log P(D|w)]     │
│         (= negative ELBO from variational inference)    │
│                                                         │
│  Special Case: Gaussian prior p(w) = N(0, σ²)          │
│    ┌─────────┐                                          │
│    │ q(w) =  │──► KL term = ||w*||² / (2σ²) + const    │
│    │ δ(w-w*) │    = L2 weight decay!                    │
│    └─────────┘                                          │
└─────────────────────────────────────────────────────────┘
```

The paper formulates the learning problem as a communication problem. Imagine a sender who has observed both the training data and the trained network, and must transmit enough information for a receiver to reconstruct the training data. The sender and receiver agree on a prior distribution p(w) over weights. The transmission consists of two parts:

Part 1 (Model description): The sender transmits the network weights. Using bits-back coding, the cost of transmitting weights drawn from posterior q(w) when the receiver expects prior p(w) is KL[q(w) || p(w)] bits. If q(w) concentrates near the prior, this cost is small; if q(w) is very different from p(w), this cost is large.

Part 2 (Data description): Given the transmitted weights, the sender transmits the training errors (residuals). If the network fits the data well, these residuals are small and cheap to encode. If the network fits poorly, the residuals are large and expensive.

The total MDL cost is: L_MDL = KL[q(w) || p(w)] + E_q[-log P(D|w)], which is exactly the evidence lower bound (ELBO) from variational Bayesian inference, with the sign flipped. Minimizing L_MDL is equivalent to maximizing the ELBO, which is equivalent to approximate Bayesian inference with variational posterior q(w).

For the special case where p(w) = N(0, sigma^2) and q(w) is a delta function at w*, the KL term reduces to ||w*||^2 / (2*sigma^2) + const, which is exactly L2 weight decay. This shows that weight decay has been implicitly performing MDL minimization all along.

The bits-back argument works as follows: to encode a weight sampled from q(w), the sender uses -log q(w) bits. But the receiver can "give back" -log p(w) bits by using the prior. The net cost is E_q[log q(w) - log p(w)] = KL[q||p].

## Results

- Weight decay is derived as an MDL special case: when the prior p(w) is N(0, sigma^2), minimizing description length reduces exactly to the standard L2 penalty, but now justified from first principles rather than heuristics
- The KL divergence between posterior and prior provides a continuous, differentiable measure of model complexity, unlike discrete model selection criteria that count parameters
- The framework provides a theoretical bound on the generalization gap: models that explain data with fewer bits for weights are provably less likely to overfit, because the description length directly bounds the amount of information the model has memorized about the training set
- The information-geometric interpretation connects model complexity to the geometry of weight space, with the KL divergence measuring the "distance" the model has traveled from the prior during training
- Networks with weights clustered near zero have low MDL cost because the posterior concentrates near the prior, providing a principled justification for sparsity-inducing regularization

## Limitations & Open Questions

- The paper is primarily theoretical with limited empirical validation on real-world networks; practical computation of KL divergence for large networks remained intractable until variational inference methods matured decades later
- The choice of prior distribution strongly affects the MDL cost, and the "right" prior for neural networks remains debated -- Gaussian priors yield L2, Laplace priors yield L1, but the appropriate prior for modern deep networks may be neither
- Modern connections to neural network compression, pruning, and quantization (which literally reduce description length) were not explored but are natural extensions of this framework

## Connections

- [[wiki/concepts/machine-learning]]
- [[wiki/sources/papers/kolmogorov-complexity-and-algorithmic-randomness]]
- [[wiki/sources/papers/recurrent-neural-network-regularization]]
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]]
- [[wiki/sources/papers/a-tutorial-introduction-to-the-minimum-description-length-principle]]
- [[wiki/sources/papers/variational-lossy-autoencoder]]
