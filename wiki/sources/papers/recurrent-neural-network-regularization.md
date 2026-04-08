---
title: Recurrent Neural Network Regularization
type: source-summary
status: complete
updated: 2026-04-05
year: 2014
venue: arXiv (1409.2329)
tags:
  - paper
  - ilya-30
  - rnn
  - lstm
  - regularization
  - dropout
  - language-modeling
citations: 2986
---

📄 **[Read on arXiv](https://arxiv.org/abs/1409.2329)**

## Overview

This paper discovered that dropout can be successfully applied to LSTMs if it is restricted to non-recurrent (feedforward) connections only, preserving the LSTM's ability to propagate information across timesteps while dramatically reducing overfitting. Before this work, dropout -- the most successful regularization technique for feedforward networks -- failed catastrophically when applied to RNNs because naive dropout on recurrent connections injects different noise at each timestep, destroying the LSTM's carefully maintained cell state.

Zaremba, Sutskever, and Vinyals showed that applying dropout only to input-to-hidden, layer-to-layer, and hidden-to-output connections (while leaving recurrent-to-recurrent connections untouched) yields substantial generalization improvements. This simple but non-obvious insight became standard practice and enabled training of much larger LSTM models. The paper demonstrated that a 1500-unit LSTM with 65% dropout dramatically outperforms a smaller 650-unit LSTM with 50% dropout, establishing the principle that stronger regularization enables scaling model capacity -- a lesson that remains relevant in the transformer era.

The technique directly contributed to advances in language modeling, speech recognition, and machine translation throughout the LSTM era (2014-2017), and the paper's two-layer stacked LSTM with dropout became the canonical architecture for language modeling benchmarks.

## Key Contributions

- **Dropout only on non-recurrent connections**: The critical insight is that dropout masks must not be applied to W_hh (recurrent weight matrices); dropout is applied to input embeddings, between stacked LSTM layers, and before the output projection
- **Consistent masks across timesteps**: The same dropout mask is applied at every timestep for a given sequence, rather than sampling new masks at each step, preserving temporal coherence
- **Larger models with stronger regularization**: A 1500-unit LSTM with 65% dropout dramatically outperforms a 650-unit LSTM with 50% dropout, demonstrating that regularization enables scaling model capacity
- **Two-layer stacked LSTM architecture**: Establishes the input-embed-dropout-LSTM1-dropout-LSTM2-dropout-output pipeline that became the standard LSTM language model architecture
- **BPTT with 35-step unrolling**: Establishes training protocol with backpropagation through time using sequence length 35, batch size 20, on the Penn Treebank vocabulary of 10K words

## Architecture

```
          Input word w_t
               │
               ▼
      ┌────────────────┐
      │ Word Embedding │
      │   (D=200/650)  │
      └───────┬────────┘
              │
         ┌────┴────┐
         │ DROPOUT │  ◄── applied here
         └────┬────┘
              │
              ▼
      ┌───────────────────────────────────┐
      │        LSTM Layer 1               │
      │  h_{t-1} ──────────► h_t          │
      │     │   (NO dropout on            │
      │     │    recurrent connection)     │
      │  c_{t-1} ──────────► c_t          │
      └───────────────┬───────────────────┘
                      │
                 ┌────┴────┐
                 │ DROPOUT │  ◄── applied here
                 └────┬────┘
                      │
                      ▼
      ┌───────────────────────────────────┐
      │        LSTM Layer 2               │
      │  h_{t-1} ──────────► h_t          │
      │     │   (NO dropout on            │
      │     │    recurrent connection)     │
      │  c_{t-1} ──────────► c_t          │
      └───────────────┬───────────────────┘
                      │
                 ┌────┴────┐
                 │ DROPOUT │  ◄── applied here
                 └────┬────┘
                      │
                      ▼
            ┌──────────────────┐
            │ Linear + Softmax │
            │   (vocab=10K)    │
            └──────────────────┘
                      │
                      ▼
                  P(w_{t+1})
```

## Method

The architecture is a stacked LSTM language model with dropout applied at specific locations:

**Input layer**: Word embeddings of dimension D (200 or 650) are looked up from a learned embedding matrix. Dropout is applied to the embedding output before feeding into the first LSTM layer.

**LSTM layers**: Two stacked LSTM layers, each with H hidden units (650 or 1500). Within each LSTM cell, the standard gating equations operate without any dropout:
- f_t = sigmoid(W_f * [h_{t-1}, x_t] + b_f) (forget gate)
- i_t = sigmoid(W_i * [h_{t-1}, x_t] + b_i) (input gate)
- c_t = f_t * c_{t-1} + i_t * tanh(W_c * [h_{t-1}, x_t] + b_c) (cell state)
- h_t = o_t * tanh(c_t) (hidden state)

The critical detail: no dropout is applied within these equations. The recurrent connection h_{t-1} passes through cleanly, preserving the cell state's ability to carry information across long sequences. Formally, the proposed regularization modifies the standard LSTM by applying dropout operator D only to the non-recurrent input: the input from the previous layer h^{l-1}_t is passed through D(), while the hidden state from the previous timestep h^l_{t-1} passes through unmodified.

**Inter-layer dropout**: Between LSTM layer 1 and LSTM layer 2, and between LSTM layer 2 and the output projection, dropout masks are applied. These masks are sampled once per sequence and held constant across all timesteps. This strategy ensures information traversing through time remains intact while still providing regularization through corruption of layer-to-layer information flow.

**Output layer**: A linear projection from the LSTM hidden state to the vocabulary size (10K for PTB), followed by softmax. Standard cross-entropy loss is used.

**Training**: SGD with gradient clipping (max norm 5), learning rate 1.0 decayed by 1/1.15 after epoch 14 (for the large model). BPTT is truncated at 35 timesteps. Training on PTB takes a few hours on a single GPU.

## Results

| Task | Model | Metric | Value |
|------|-------|--------|-------|
| PTB LM | Medium LSTM (regularized) | Perplexity | 82.7 |
| PTB LM | Large LSTM (regularized) | Perplexity | 78.4 |
| PTB LM | Non-regularized baseline | Perplexity | 114.5 |
| PTB LM | Ensemble of 10 large | Perplexity | 69.5 |
| WMT'14 En-Fr | Regularized | BLEU | 29.03 |
| WMT'14 En-Fr | Non-regularized | BLEU | 25.9 |
| Speech (Icelandic) | Regularized | Val Accuracy | 70.5% |
| Speech (Icelandic) | Non-regularized | Val Accuracy | 68.9% |
| MSCOCO | Regularized | Perplexity | 7.99 |
| MSCOCO | Non-regularized | Perplexity | 8.47 |

- **Penn Treebank language modeling**: Medium regularized LSTM achieves test perplexity 82.7 (vs. 114.5 non-regularized); large regularized LSTM achieves 78.4; ensemble of 10 large regularized LSTMs achieves 69.5, setting a new benchmark
- **Speech recognition (Google Icelandic)**: Validation frame accuracy improved from 68.9% to 70.5%; training accuracy decreased due to dropout noise, but improved generalization demonstrated effective regularization on the relatively small dataset
- **Machine translation (WMT'14 English-French)**: Test perplexity decreased from 5.8 to 5.0; BLEU score increased from 25.9 to 29.03, a substantial translation quality improvement
- **Image captioning (MSCOCO)**: Single regularized models achieved better perplexity (7.99 vs 8.47) and BLEU scores (24.3 vs 23.5), with performance comparable to ensembles of non-regularized models
- Applying dropout to recurrent connections destroys LSTM memory and worsens performance compared to no dropout at all, validating the paper's core hypothesis about where dropout should be applied
- Scaling from 650 to 1500 hidden units improves perplexity from 82.7 to 78.4 when paired with increased dropout (50% to 65%), but hurts performance without dropout, demonstrating the regularization-scaling relationship

## Limitations & Open Questions

- The paper does not explore variational dropout (later proposed by Gal and Ghahramani, 2016) which provides a Bayesian interpretation and can apply dropout to recurrent connections with a fixed mask per sequence, often outperforming the feedforward-only strategy
- Weight tying between embedding and output layers (later shown to improve perplexity by ~5 points) is not explored
- The approach is specific to LSTMs; the Transformer era replaced this with attention dropout and layer-level dropout strategies, though the principle of careful dropout placement remains

## Connections

- [[wiki/concepts/machine-learning]] -- foundational regularization technique for RNNs
- [[wiki/sources/papers/understanding-lstm-networks]] -- LSTM architecture that this paper regularizes
- [[wiki/sources/papers/the-unreasonable-effectiveness-of-recurrent-neural-networks]] -- popularized the LSTM models this paper enables
- [[wiki/sources/papers/attention-is-all-you-need]] -- transformers superseded LSTMs but retained dropout as a regularization technique
