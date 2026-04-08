---
title: "Order Matters: Sequence to Sequence for Sets"
type: source-summary
status: complete
updated: 2026-04-05
year: 2016
venue: ICLR
tags:
  - paper
  - ilya-30
  - sequence-to-sequence
  - set-modeling
  - attention
  - permutation-invariance
citations: 1018
---

📄 **[Read on arXiv](https://arxiv.org/abs/1511.06391)**

## Overview

This paper systematically demonstrates that input and output ordering dramatically affects seq2seq performance on set-structured data. Sequence models like RNNs have an inherent position bias -- early positions receive more attention and gradient signal. This creates a fundamental mismatch when the input is a set (where {a,b,c} = {c,a,b}) rather than a sequence. Naively feeding sets to seq2seq models in random order causes high variance and poor learning, while sorting inputs by a canonical ordering (e.g., magnitude) gives consistent gradients and dramatically better results.

The paper proposes the read-process-write architecture that explicitly separates input encoding, computation, and output generation into modular phases. The "read" phase encodes all set elements, the "process" phase applies attention-based computation over the encoded elements without any ordering assumption, and the "write" phase generates the output sequence. This separation improves both performance and interpretability over standard encoder-decoder architectures.

This work is foundational for understanding how to apply sequence models to inherently unordered data, a problem that recurs in point clouds, graph neural networks, and set-based reasoning. The insights about ordering sensitivity directly influenced later work on permutation-equivariant architectures (Deep Sets, Set Transformer) and informed the design of attention mechanisms in transformers.

## Key Contributions

- **Canonical ordering matters**: Random input ordering means the model sees n! possible permutations of the same set, causing high gradient variance; sorting by magnitude reduces this to a single canonical order, yielding 10-20% faster convergence
- **Read-Process-Write architecture**: A modular three-phase framework: (1) Read -- encode input set elements, (2) Process -- perform computation via attention over encoded elements, (3) Write -- generate output sequence
- **Attention over permutations**: The model learns position-independent attention scores that determine which set elements are relevant at each output step, effectively learning an implicit ordering strategy
- **Set-to-sequence and set-to-set tasks**: Evaluates on permutation prediction, set intersection/union, and pointer-based selection, demonstrating generality
- **Position bias in RNNs**: Systematic empirical evidence that RNN encoders attend more strongly to early positions, creating an ordering-dependent bias that must be explicitly counteracted for set inputs

## Architecture / Method

```
              Read-Process-Write Architecture
              ───────────────────────────────

  Input Set: {x₁, x₂, ..., xₙ}  (unordered)
                    │
         ┌──────── ▼ ────────┐
         │    READ Phase      │
         │  ┌────┐ ┌────┐    │
         │  │RNN │ │RNN │... │    Encode each element
         │  └─┬──┘ └─┬──┘    │    (order discarded after)
         │    ▼      ▼       │
         │  {h₁, h₂, ..., hₙ}   Unordered hidden states
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │   PROCESS Phase   │
         │                   │
         │  for t = 1..P:    │    P rounds of attention
         │    rₜ = Σ αᵢ·hᵢ  │    (no ordering assumption)
         │    qₜ = LSTM(     │
         │      qₜ₋₁, rₜ)   │
         │                   │
         └────────┬──────────┘
                  │ processed state
         ┌────────▼──────────┐
         │    WRITE Phase    │
         │                   │
         │  Decoder attends  │    Generate output sequence
         │  over {hᵢ} +      │    (with pointer mechanism
         │  processed state  │     for selection tasks)
         │                   │
         └────────┬──────────┘
                  ▼
         Output: (y₁, y₂, ..., yₘ)
```

![The Read-Process-Write (RPW) architecture for handling input sets](https://paper-assets.alphaxiv.org/figures/1511.06391v4/img-0.jpeg)

The read-process-write (RPW) architecture consists of three phases:

**Read phase**: An RNN encoder processes each element of the input set to produce a set of hidden states {h_1, ..., h_n}. Crucially, these are treated as an unordered set of feature vectors after encoding, discarding positional information.

**Process phase**: An iterative attention mechanism operates over the encoded elements for P steps. At each step, a "process" LSTM maintains a state that attends over {h_i} and updates itself: q_t = LSTM(q_{t-1}, r_t) where r_t = sum_i alpha_i * h_i is an attention-weighted combination. This allows T rounds of "thinking" about the set without any ordering assumption. The number of processing steps P is a hyperparameter that controls compute.

**Write phase**: A decoder generates the output sequence, attending over both the processed representations and the original encoded elements. For sorting tasks, the decoder uses a pointer mechanism to select input elements in the correct order.

The paper experiments with multiple input orderings: random (different permutation each epoch), fixed random (same random order), sorted by magnitude, and learned ordering (the model optimizes over orderings via REINFORCE). The experiments span three task types: sorting numbers, computing set intersection/union, and predicting canonical orderings.

Training uses standard cross-entropy loss for the output sequence, with curriculum learning (starting from small sets, increasing size).

## Results

![Impact of different tree traversal orders on parsing performance](https://paper-assets.alphaxiv.org/figures/1511.06391v4/img-1.jpeg)

| Task | Model / Ordering | Metric | Value |
|------|-----------------|--------|-------|
| Sorting (N=5) | RPW | Accuracy | 94% |
| Sorting (N=5) | Pointer Network | Accuracy | 90% |
| Sorting (N=10) | RPW | Accuracy | 57% |
| Sorting (N=10) | Pointer Network | Accuracy | 28% |
| Sorting (N=15) | RPW | Accuracy | 10% |
| Sorting (N=15) | Pointer Network | Accuracy | 4% |
| 5-gram LM | Natural ordering | Perplexity | 225 |
| 5-gram LM | Arbitrary fixed ordering | Perplexity | 280 |
| Parsing | Depth-first traversal | F1 | 89.5% |
| Parsing | Breadth-first traversal | F1 | 81.5% |

- On number sorting tasks, feeding inputs in sorted order vs. random order improves convergence speed by 10-20% and final accuracy by significant margins
- The RPW architecture achieves better results on set intersection and union tasks than a standard encoder-decoder, demonstrating that explicit separation of phases helps
- When the model is allowed to learn its own input ordering via REINFORCE, it converges to something close to magnitude sorting, validating the hypothesis that canonical ordering is beneficial
- Visualization shows the model learns to attend to specific set elements at each output step based on their value rather than position
- The process phase with multiple steps consistently outperforms single-step processing, suggesting iterative computation over sets is valuable

## Limitations & Open Questions

- The approach still processes elements sequentially via an RNN, limiting scalability to large sets; modern set encoders (Deep Sets, Set Transformer) use permutation-equivariant architectures that avoid ordering entirely
- The canonical ordering strategy (sort by magnitude) is domain-specific and may not generalize to complex structured objects where no natural ordering exists
- The paper does not explore the connection to graph neural networks, which handle similar unordered-input challenges through message passing rather than sorting

## Connections

- [[wiki/concepts/machine-learning]] -- set processing with sequence models
- [[wiki/sources/papers/pointer-networks]] -- pointer mechanism used in the write phase
- [[wiki/sources/papers/attention-is-all-you-need]] -- transformers address set processing through self-attention
- [[wiki/sources/papers/neural-message-passing-for-quantum-chemistry]] -- GNNs as an alternative approach to unordered inputs
