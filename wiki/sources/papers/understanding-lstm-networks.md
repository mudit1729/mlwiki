---
title: Understanding LSTM Networks
type: source-summary
status: complete
updated: 2026-04-11
year: 2015
venue: Blog Post (colah.github.io)
tags:
  - paper
  - ilya-30
  - lstm
  - rnn
  - sequence-modeling
  - vanishing-gradients
citations: 0
paper-faithfullness: audited-clean
---

📄 **[Read Blog Post](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)**

# Understanding LSTM Networks

## Overview

Christopher Olah's 2015 blog post is a widely used pedagogical reference for understanding LSTM internals. The post explains why vanilla RNNs fail on long sequences and how LSTMs address that problem through a different information-flow architecture.

The core insight explained is that vanilla RNNs fail because gradients must pass through a product of Jacobian matrices at each timestep during backpropagation, causing exponential decay when the spectral radius is below 1 (vanishing gradients) or explosion when above 1. LSTMs solve this by replacing the multiplicative hidden state update with an additive cell state pipeline: the cell state C_t travels through the entire sequence modified only by element-wise addition and gating, not matrix multiplication. This allows gradients to flow relatively unchanged over hundreds of timesteps.

The post covers three gates (forget, input, output) with careful mathematical detail and intuitive diagrams, and also discusses GRU as a simplified variant. While pedagogical rather than presenting new research, it synthesizes the foundational ideas from Hochreiter and Schmidhuber (1997) and subsequent work in a particularly accessible form. The broader links drawn here to later gated architectures are useful wiki synthesis rather than claims made by the original post.

## Key Contributions

- **Clear explanation of the vanishing gradient problem**: In vanilla RNNs, dh_t/dh_{t-tau} involves a product of tau Jacobian matrices with eigenvalues typically less than 1, causing exponential gradient decay and making learning beyond 10-20 steps practically impossible
- **Cell state as gradient highway**: The LSTM cell state C_t travels through the sequence modified only by element-wise operations (multiply by forget gate, add input gate contribution), not matrix multiplication, enabling gradient flow over hundreds of steps
- **Three-gate decomposition with intuitive explanations**: Forget gate (what to discard), input gate + candidate (what to write), and output gate (what to expose), each explained with both mathematical formulas and visual diagrams
- **GRU as simplified alternative**: Covers Gated Recurrent Units which merge forget and input gates into a single update gate, reducing parameters while achieving comparable performance on many tasks
- **Connection to broader architectural principles**: Implicitly demonstrates that additive skip connections (the cell state highway) are the key to training deep/long sequential models, a principle that extends to residual networks and transformers

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    LSTM Cell at time t                     │
│                                                           │
│  C_{t-1} ──────────────────────────────────────► C_t      │
│         │          ┌─────┐        ┌─────┐    │            │
│         │    ×◄────┤  f_t│   +◄───┤ i_t │    │            │
│         │    │     │Forget│   │   │Input │    │            │
│         │    │     │ Gate │   │   │ Gate │    │            │
│         │    │     └──┬──┘   │   └──┬──┘    │            │
│         │    │        │      │      │        │            │
│         └────┘        │      │   ┌──┴──┐     │            │
│                       │      └───┤C_tld│     │            │
│                       │          │tanh │     │            │
│                       │          └──┬──┘     │            │
│                       │             │        │            │
│  h_{t-1}──┬───────────┼─────────────┘   ┌───┴───┐        │
│           │           │                 │ tanh  │        │
│           │           │                 └───┬───┘        │
│           │           │              ┌──────┤            │
│           │           │              │  ×◄──┘            │
│           │           │              │  │                │
│           │           │              │  └──────► h_t     │
│           │           │         ┌────┴──┐                │
│           │           └─────────┤  o_t  │                │
│           │                     │Output │                │
│           └─────────────────────┤ Gate  │                │
│                                 └───────┘                │
│  x_t ──────────────────[concat with h_{t-1}]──► gates    │
│                                                           │
│  Key: f_t = sigmoid(W_f·[h,x]+b)  forget gate            │
│       i_t = sigmoid(W_i·[h,x]+b)  input gate             │
│       o_t = sigmoid(W_o·[h,x]+b)  output gate            │
│       C_t = f_t*C_{t-1} + i_t*tanh(W_c·[h,x]+b)         │
│       h_t = o_t * tanh(C_t)                               │
└───────────────────────────────────────────────────────────┘
```

## Architecture / Method

The LSTM cell processes inputs sequentially, maintaining two state vectors: the hidden state h_t (exposed as output) and the cell state C_t (internal memory). At each timestep t, given input x_t and previous states h_{t-1}, C_{t-1}:

**Forget gate**: f_t = sigmoid(W_f * [h_{t-1}, x_t] + b_f). Decides what information to discard from cell state. When f_t[i] is near 0, channel i is erased; near 1, it is preserved.

**Input gate + candidate**: i_t = sigmoid(W_i * [h_{t-1}, x_t] + b_i) and C_tilde = tanh(W_c * [h_{t-1}, x_t] + b_c). The input gate decides what to update; the candidate provides the new values. Together they control what new information enters the cell state.

**Cell state update**: C_t = f_t * C_{t-1} + i_t * C_tilde. This is the crucial additive update -- the gradient dC_t/dC_{t-1} = f_t (a diagonal matrix), which can stay near 1 if the forget gate is open, preventing exponential decay.

**Output gate**: o_t = sigmoid(W_o * [h_{t-1}, x_t] + b_o). Controls which parts of the cell state to expose: h_t = o_t * tanh(C_t). This decouples internal memory from the output representation.

The GRU variant merges the forget and input gates into a single update gate z_t and removes the separate cell state, using: h_t = (1 - z_t) * h_{t-1} + z_t * h_tilde, which is simpler but retains the additive update property.

## Results

- **Additive updates preserve gradients**: Because C_t = f_t * C_{t-1} + i_t * C_tilde is additive in C_{t-1}, the gradient dC_t/dC_{t-1} = f_t (diagonal), which stays near 1 when the forget gate is open, enabling learning of dependencies spanning 100+ timesteps
- **Empirical superiority on long-range tasks**: LSTMs consistently outperform vanilla RNNs on tasks requiring memory over 100+ timesteps, including language modeling, speech recognition, machine translation, and handwriting generation
- **GRU as competitive simplified variant**: GRUs achieve comparable performance to LSTMs on many benchmarks with fewer parameters and faster training, making them practical for resource-constrained settings
- **Universal adoption**: LSTMs became the dominant sequence model from 2014-2017, powering Google Translate, Apple Siri, Amazon Alexa, and virtually all NLP systems before the Transformer revolution
- **Pedagogical impact**: The blog post itself became a standard reference, demonstrating the value of clear technical communication in accelerating research adoption

## Limitations & Open Questions

- LSTMs still process tokens sequentially, making them fundamentally slower to train than parallel architectures like the Transformer, which can process all positions simultaneously
- The cell state capacity is finite (bounded by hidden dimension), so practical long-range memory still degrades over very long sequences (thousands of tokens), limiting LSTMs compared to attention mechanisms that can attend to arbitrary positions
- The post is pedagogical rather than presenting new research; it synthesizes and visualizes existing LSTM theory from Hochreiter and Schmidhuber (1997) and subsequent improvements

## Connections

- [[wiki/concepts/machine-learning]]
- [[wiki/sources/papers/the-unreasonable-effectiveness-of-recurrent-neural-networks]]
- [[wiki/sources/papers/recurrent-neural-network-regularization]]
- [[wiki/sources/papers/attention-is-all-you-need]]
- [[wiki/sources/papers/relational-recurrent-neural-networks]]
- [[wiki/sources/papers/neural-turing-machines]]
