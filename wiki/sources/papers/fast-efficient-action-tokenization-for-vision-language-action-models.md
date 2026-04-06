---
title: "FAST: Efficient Action Tokenization for Vision-Language-Action Models"
type: source-summary
status: active
updated: 2026-04-05
year: 2025
venue: RSS 2025
tags:
  - paper
  - robotics
  - vla
  - tokenization
  - action-representation
citations: 353
arxiv_id: "2501.09747"
---

# FAST: Efficient Action Tokenization for Vision-Language-Action Models

[Read on arXiv](https://arxiv.org/abs/2501.09747)

## Overview

FAST (Frequency-space Action Sequence Tokenization) introduces a novel action tokenizer for VLA models that leverages signal processing to dramatically compress robot action sequences. Current VLA approaches use naive per-dimension binning to convert continuous actions into discrete tokens, which fails to capture temporal correlations in high-frequency robot control data and produces long token sequences that slow training and inference. FAST applies Discrete Cosine Transform (DCT) followed by Byte-Pair Encoding (BPE) to compress action chunks into far fewer tokens, achieving 2x-13x compression ratios depending on robot complexity.

Developed by Physical Intelligence and UC Berkeley, FAST consistently outperforms naive tokenization across diverse manipulation tasks while enabling 5x faster training. The paper also introduces FAST+, a pre-trained universal tokenizer trained on data from multiple robot embodiments that can be applied zero-shot to new robots without re-training the tokenizer.

## Key Contributions

- **DCT + BPE action tokenization**: Transforms continuous action sequences into frequency space via DCT, quantizes coefficients, then applies BPE compression -- achieving 2x-13x compression over naive binning
- **5x training speedup**: Shorter token sequences mean fewer autoregressive steps, dramatically accelerating VLA training convergence
- **FAST+ universal tokenizer**: A pre-trained tokenizer applicable across robot embodiments without re-fitting, enabling plug-and-play deployment
- **Enables complex dexterous tasks**: The compressed representation allows VLAs to learn high-DoF dexterous manipulation (e.g., shirt folding) that naive tokenization cannot handle due to sequence length constraints

## Architecture / Method

![FAST tokenization pipeline: normalize, DCT, quantize, flatten, BPE](https://paper-assets.alphaxiv.org/figures/2501.09747/x1.png)

The FAST pipeline consists of five steps:

1. **Normalization**: Raw action sequences are normalized per-dimension to zero mean and unit variance
2. **Discrete Cosine Transform (DCT)**: Each action dimension's time series is transformed into frequency components, concentrating energy in fewer coefficients (low-frequency components capture the dominant motion patterns)
3. **Quantization**: DCT coefficients are quantized to discrete integer values, with the quantization level controlling the precision-compression tradeoff
4. **Flattening**: The 2D matrix (dimensions x frequency coefficients) is flattened into a 1D sequence
5. **Byte-Pair Encoding (BPE)**: Standard BPE compression merges frequent coefficient patterns into single tokens, further reducing sequence length

![FAST vs naive tokenization: convergence comparison](https://paper-assets.alphaxiv.org/figures/2501.09747/convergence_2.jpg)

The compression ratio depends on the action space complexity: simple 7-DoF arms achieve ~13x compression, while high-DoF dexterous hands achieve ~2-3x. FAST+ trains the BPE vocabulary on a diverse cross-embodiment dataset, enabling a single tokenizer to work across robot morphologies.

## Results

![Task environments for evaluation](https://paper-assets.alphaxiv.org/figures/2501.09747/environments.jpg)

| Method | Training Speed | Compression | Dexterous Tasks | Cross-Embodiment |
|--------|---------------|-------------|-----------------|-----------------|
| Naive binning (per-dim) | 1x (baseline) | 1x | Cannot learn | Per-robot |
| FAST (task-specific) | ~5x | 2x-13x | Successful | Per-robot |
| FAST+ (universal) | ~5x | 2x-13x | Successful | Zero-shot transfer |

- FAST consistently outperforms naive tokenization across all tested tasks and robot platforms
- 5x faster training convergence due to shorter token sequences requiring fewer autoregressive steps
- Enables learning of complex dexterous tasks (shirt folding, grocery packing, toast preparation) that are infeasible with naive tokenization due to prohibitive sequence lengths
- FAST+ universal tokenizer matches task-specific FAST performance, demonstrating that a single tokenizer generalizes across embodiments
- The DCT transform is critical: ablating it (using only BPE on raw values) significantly degrades performance, confirming that frequency-space representation captures meaningful temporal structure

## Limitations

- Compression ratio is lower for high-DoF systems (dexterous hands) where action sequences are more complex and less temporally correlated
- The quantization step introduces irreversible information loss; very precise tasks may need careful tuning of quantization levels
- BPE vocabulary is fixed after training; novel action patterns not covered by the vocabulary fall back to uncompressed representation
- Evaluation focuses on Physical Intelligence's platforms; independent validation on other VLA architectures (e.g., OpenVLA, RT-2) is limited

## Connections

- [[wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control]] -- FAST was developed alongside pi0 at Physical Intelligence; pi0 uses flow matching instead of tokenization
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- OpenVLA uses naive 256-bin discretization; FAST provides a superior alternative
- [[wiki/concepts/vision-language-action]] -- addresses a core VLA design axis: action representation
- [[wiki/concepts/robotics]] -- enables more efficient robot policy training across embodiments
