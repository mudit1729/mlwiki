---
title: Relational Recurrent Neural Networks
type: source-summary
status: complete
updated: 2026-04-05
year: 2018
venue: NeurIPS 2018
tags:
  - paper
  - ilya-30
  - recurrent-neural-networks
  - relational-reasoning
  - memory-augmented-networks
citations: 220
---

📄 **[Read on arXiv](https://arxiv.org/abs/1806.01822)**

# Relational Recurrent Neural Networks

## Overview

Traditional RNNs (LSTMs, GRUs) compress all sequential information into a single fixed-size hidden vector, which fundamentally limits their ability to store and reason about multiple independent facts or entity relationships simultaneously. This paper introduces the Relational Memory Core (RMC), which replaces the monolithic hidden state with a matrix of N memory slots that interact through multi-head dot-product attention at each timestep. This allows the network to explicitly model relations between stored memories, bridging the gap between recurrent architectures and attention-based relational reasoning.

The RMC architecture presaged the full transition to transformers by demonstrating that self-attention over memory representations dramatically improves sequential reasoning. The model achieved improvements over LSTMs on WikiText-103 language modeling and showed substantially stronger compositional generalization on relational reasoning tasks requiring tracking of multiple entities. The paper demonstrated that the inductive bias of relational computation over discrete memory slots is fundamentally more powerful than compressing everything into a single vector.

Santoro et al. (DeepMind) published this at NeurIPS 2018, and the work sits at the intersection of memory-augmented neural networks, relational reasoning, and the emerging attention paradigm. It is one of the clearest demonstrations that attention mechanisms could enhance recurrent architectures before transformers fully replaced them.

## Key Contributions

- **Relational Memory Core (RMC)**: Maintains memory as a matrix M_t of N slots (each D_m-dimensional) updated at each timestep via multi-head self-attention over slots, enabling explicit inter-memory relational computation
- **Attention-based memory update**: At each step, the input is projected into the memory slot space, then multi-head attention computes queries, keys, and values from the memory matrix, updating slots based on their relational content rather than through gating alone
- **Slot-based information decomposition**: Information naturally distributes across N independent memory slots, allowing the network to store multiple independent facts without interference
- **Gate integration with attention**: Combines attention-based updates with standard LSTM-style gating (forget and input gates per slot) to provide stable long-term memory alongside relational updates
- **Demonstration that relational inductive biases improve sequence modeling**: Explicit relational computation over memory slots outperforms implicit relational learning in standard recurrent architectures

## Architecture

```
                    Input x_t
                       │
                       ▼
              ┌────────────────┐
              │ Linear Project │
              └───────┬────────┘
                      │
    ┌─────────────────┼─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
┌────────┐      ┌────────┐       ┌────────┐
│ Slot 1 │      │ Slot 2 │  ...  │ Slot N │  M_{t-1}
└───┬────┘      └───┬────┘       └───┬────┘
    │               │                │
    └───────────────┼────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │   Multi-Head Self-Attention       │
    │   Q,K,V from [slots + input]      │
    │   (each slot attends to all       │
    │    other slots + input x_t)       │
    └───────────────┬───────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │   Residual MLP (per slot)         │
    └───────────────┬───────────────────┘
                    │
                    ▼
    ┌───────────────────────────────────┐
    │   LSTM-style Gating (per slot)    │
    │   f_t = σ(W_f[slot, attn_out])   │
    │   i_t = σ(W_i[slot, attn_out])   │
    │   M_t[i] = f*M_{t-1}[i] + i*out │
    └───────────────┬───────────────────┘
                    │
                    ▼
    ┌────────┐ ┌────────┐  ┌────────┐
    │ Slot 1 │ │ Slot 2 │  │ Slot N │  M_t
    └────────┘ └────────┘  └────────┘
                    │
                    ▼
            Linear Readout ──► Output
```

## Method

The RMC operates by maintaining a memory matrix M_t of shape (N, D_m) where N is the number of memory slots and D_m is the dimension per slot. At each timestep t, the current input x_t is first linearly projected and concatenated with the existing memory slots. Multi-head dot-product attention is then applied where each memory slot generates its own query, and keys and values come from all slots plus the input. This allows every slot to attend to every other slot and the input simultaneously.

The attention output is passed through a residual MLP (similar to a transformer block), and then combined with LSTM-style gating. Each slot has its own forget gate f_t and input gate i_t, computed as sigmoid functions of the concatenation of the previous slot value and the attention output. The final slot update is: M_t[i] = f_t[i] * M_{t-1}[i] + i_t[i] * attention_output[i]. This gating mechanism provides stability and allows the network to selectively preserve or overwrite slot contents.

The overall architecture can be seen as applying a single transformer layer recurrently at each timestep over the memory slots, with the input injected as an additional key-value pair. The output at each step is a linear readout from the concatenated memory slots.

## Results

- **Improved language modeling**: RMC achieves lower perplexity than LSTM baselines on WikiText-103 and GigaWord, suggesting that relational memory interactions capture useful linguistic structure beyond what compressed hidden states provide
- **Superior relational reasoning**: On synthetic tasks requiring tracking and reasoning about multiple entities (e.g., the nth-farthest task where the model must track positions of N objects and determine distance ordering), RMC significantly outperforms LSTMs, which fail to generalize beyond training sequence lengths
- **Compositional generalization**: RMC shows stronger generalization to longer sequences and more entities at test time compared to LSTMs, indicating that slot-based relational memory provides a more appropriate inductive bias for compositional tasks
- **Program evaluation tasks**: On tasks requiring execution of simple programs with multiple variables, RMC maintains accuracy where LSTMs degrade, demonstrating the benefit of discrete memory slots for variable binding
- **Modest but consistent LM gains**: While the improvement over LSTMs on standard language modeling benchmarks is smaller than the gap between LSTMs and full transformers, the gains are consistent and statistically significant

## Limitations & Open Questions

- The O(N^2) attention over memory slots at each timestep adds computational overhead compared to standard LSTM updates, limiting the practical number of slots that can be used
- The improvement over LSTMs on standard language modeling benchmarks is modest compared to the dramatic gains from full transformer architectures, raising the question of whether incremental RNN improvements were worth pursuing versus the full architectural shift
- The relationship between RMC and full self-attention over sequences (as in transformers) is not formally analyzed; in hindsight, RMC can be seen as a constrained version of transformer-style attention applied recurrently, suggesting that removing the recurrent bottleneck entirely (as transformers do) is the more powerful approach

## Connections

- [[wiki/concepts/machine-learning]]
- [[wiki/sources/papers/attention-is-all-you-need]]
- [[wiki/sources/papers/a-simple-neural-network-module-for-relational-reasoning]]
- [[wiki/sources/papers/neural-turing-machines]]
- [[wiki/sources/papers/recurrent-neural-network-regularization]]
- [[wiki/sources/papers/understanding-lstm-networks]]
