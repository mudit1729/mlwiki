---
title: "QLoRA: Efficient Finetuning of Quantized Language Models"
tags: [nlp, transformer, language-modeling, foundation-model, parameter-efficient-fine-tuning, quantization]
status: active
type: paper
year: "2023"
venue: "NeurIPS 2023"
citations: 5975
arxiv_id: "2305.14314"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2305.14314)**

## Overview

Full fine-tuning of large language models requires enormous GPU memory -- a 65B-parameter model in 16-bit precision needs over 780 GB of GPU memory for parameters and optimizer states alone. QLoRA solves this by combining 4-bit quantization of the frozen pretrained weights with Low-Rank Adaptation (LoRA), enabling fine-tuning of a 65B model on a single 48GB GPU while matching the task performance of full 16-bit fine-tuning. The result is a roughly 10x reduction in memory compared to standard fine-tuning and 3-4x reduction compared to standard LoRA.

The paper introduces three technical innovations that together make this possible: (1) 4-bit NormalFloat (NF4), a new quantization data type that is information-theoretically optimal for normally distributed weights; (2) Double Quantization, which quantizes the quantization constants themselves to save an additional ~0.37 bits per parameter; and (3) Paged Optimizers, which use NVIDIA unified memory to handle memory spikes during gradient checkpointing by automatically paging optimizer states between GPU and CPU. These components are orthogonal and composable.

Using QLoRA, the authors fine-tuned over 1,000 models across 8 instruction-following datasets, multiple model families (LLaMA, T5), and scales from 7B to 65B parameters. Their best model family, Guanaco, achieves 99.3% of ChatGPT's performance on the Vicuna benchmark while requiring only 24 hours of fine-tuning on a single GPU. The paper also provides an extensive analysis of chatbot evaluation, finding that GPT-4-based evaluation is a reasonable proxy for human judgment but that current chatbot benchmarks are unreliable for fine-grained quality assessment. QLoRA democratized LLM fine-tuning by making it accessible on consumer hardware, and has since become one of the most widely adopted techniques in the LLM ecosystem.

## Key Contributions

- **4-bit NormalFloat (NF4) data type:** An information-theoretically optimal quantization format for normally distributed data, computed by mapping quantile-spaced values through the inverse normal CDF. NF4 outperforms standard 4-bit integer and 4-bit float formats on downstream tasks.
- **Double Quantization:** Quantizes the FP32 quantization constants (one per block of 64 weights) down to 8-bit, saving ~0.37 bits per parameter (roughly 3 GB on a 65B model) with negligible quality loss.
- **Paged Optimizers:** Leverages NVIDIA unified memory (managed via CUDA `cudaMallocManaged`) to automatically page optimizer state between GPU and CPU memory, preventing OOM errors during the memory spikes that occur with gradient checkpointing on long sequences.
- **Extensive instruction-tuning analysis:** Systematic study of data quality vs. quantity across 8 datasets, finding that a small high-quality dataset (OASST1, 9K examples) produces better chatbot performance than large but noisier datasets (FLAN v2, 450K examples).
- **Chatbot evaluation methodology:** Demonstrates that GPT-4 evaluation correlates well with human tournament-style evaluation, but also shows via "lemon-picked" failure analysis where Guanaco falls short of ChatGPT (factual accuracy, mathematical reasoning).

## Architecture / Method

QLoRA's approach can be decomposed into three layers: quantization of the base model, low-rank adaptation for learning, and memory management for training stability.

### Quantization: NF4

Standard quantization maps continuous weight values into a fixed grid of 2^k discrete levels. For normally distributed weights (which LLM weights approximately are), a uniform grid wastes precision in the tails. NF4 instead places quantization levels at the quantiles of the standard normal distribution, ensuring each bin covers equal probability mass. The procedure:

1. Estimate quantiles q_i = Phi^{-1}(i / (2^k + 1)) for i = 1, ..., 2^k - 1, where Phi^{-1} is the inverse normal CDF.
2. Normalize input weights to the range [-1, 1] by dividing by the absmax of each block (block size = 64).
3. Map each normalized weight to the nearest NF4 level via a lookup table.

The result is a 4-bit representation that minimizes expected quantization error under a Gaussian assumption. Empirically NF4 matches FP4 and outperforms Int4 on all benchmarks tested.

### Double Quantization

Each block of 64 weights requires one FP32 quantization constant (the absmax scaling factor). For a 65B model, these constants alone consume ~1.6 GB. Double quantization groups 256 of these FP32 constants, computes a second-level absmax, and quantizes the constants to FP8. This reduces the per-parameter overhead from 32/64 = 0.5 bits to approximately 8/64 + 32/(64*256) = 0.127 bits, a savings of ~0.37 bits per parameter.

### LoRA on Quantized Weights

The frozen 4-bit base model weights W are dequantized to BFloat16 only during the forward and backward pass (on the fly, not stored). Trainable low-rank adapters B * A (with B in R^{d x r}, A in R^{r x k}) are added in BFloat16. Gradients flow through the dequantized weights into the LoRA parameters. At inference time, the LoRA matrices can be merged with the dequantized weights. LoRA is applied to all linear layers in the transformer (attention Q, K, V, O projections and feedforward layers), not just attention -- the paper finds that applying LoRA to all layers is critical for maintaining quality at 4-bit precision.

### Paged Optimizers

During training with gradient checkpointing, memory usage spikes when a long sequence triggers recomputation of activations. Paged optimizers use CUDA unified memory to allocate optimizer states (e.g., Adam momentum and variance) so that the GPU driver can automatically evict pages to CPU RAM during spikes and page them back when needed. This prevents OOM errors without manual CPU offloading logic.

### Memory Budget (65B model, single GPU)

| Component | Standard FT (16-bit) | LoRA (16-bit base) | QLoRA (NF4 + DQ) |
|-----------|---------------------|-------------------|-------------------|
| Model weights | ~130 GB | ~130 GB | ~33 GB |
| Quantization constants | 0 | 0 | ~0.5 GB |
| LoRA parameters | 0 | ~0.2 GB | ~0.2 GB |
| Optimizer states | ~260 GB | ~0.4 GB | ~0.4 GB |
| Activations/gradients | ~50+ GB | ~10 GB | ~10 GB |
| **Total** | **~440+ GB** | **~140+ GB** | **~44 GB** |

## Results

QLoRA's core claim is that 4-bit fine-tuning matches 16-bit fine-tuning. On standard NLP benchmarks:

| Setup | MMLU (5-shot) | Mean (11 tasks) |
|-------|--------------|-----------------|
| LLaMA 7B full 16-bit FT | 38.7 | -- |
| LLaMA 7B LoRA 16-bit | 36.4 | -- |
| LLaMA 7B QLoRA NF4 | 39.0 | -- |
| LLaMA 7B QLoRA FP4 | 38.2 | -- |

The Guanaco model family (QLoRA-finetuned LLaMA on OASST1) achieved strong chatbot performance:

| Model | Vicuna Elo (GPT-4 eval) | Params | Training |
|-------|------------------------|--------|----------|
| ChatGPT | 1348 | -- | -- |
| Guanaco-65B | 1336 (99.3% of ChatGPT) | 65B | 24h, 1x A100-48GB |
| Guanaco-33B | 1311 | 33B | 12h, 1x A100-24GB |
| Vicuna-13B | 1264 | 13B | -- |
| Guanaco-7B | 1218 | 7B | 5h, 1x A100-24GB |

### Key ablation findings

- **NF4 vs FP4 vs Int4:** NF4 consistently outperforms FP4 and Int4 across model sizes and tasks. The gap is largest on harder benchmarks (MMLU).
- **LoRA on all layers vs. attention only:** Applying LoRA to all linear projections recovers the full 16-bit performance; attention-only LoRA underperforms.
- **Data quality vs. quantity:** The 9K-sample OASST1 dataset produces better chatbot performance than the 450K-sample FLAN v2, supporting the hypothesis that data quality matters more than quantity for instruction tuning.
- **Double quantization impact:** Saves ~0.4 bits per parameter with no measurable quality degradation on any benchmark.

## Limitations & Open Questions

- **Inference speed not improved:** QLoRA reduces training memory but does not accelerate inference -- the model must be dequantized for each forward pass. Separate inference-time quantization (GPTQ, AWQ) is needed for deployment.
- **Evaluation reliability:** The paper's own analysis shows that Elo-based chatbot benchmarks are noisy and sensitive to prompt phrasing and judge model, raising questions about the robustness of the Guanaco results.
- **Factual accuracy gap:** Lemon-picked analysis reveals Guanaco makes more factual errors than ChatGPT, suggesting that parameter-efficient fine-tuning on small datasets may not fully capture factual knowledge.
- **Architecture specificity:** Tested primarily on LLaMA and T5; generalization to other architectures (e.g., mixture-of-experts models) is assumed but not verified.
- **Interaction with RLHF:** QLoRA + LoRA produces strong SFT models, but the paper does not explore whether the quantized base + LoRA setup is compatible with RLHF or DPO training, which is now the standard alignment step.

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models]] -- QLoRA builds directly on LoRA, extending it to work with 4-bit quantized base models
- [[wiki/sources/papers/language-models-are-few-shot-learners]] -- GPT-3 established the scale of models that QLoRA makes fine-tunable on consumer hardware
- [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- Scaling laws motivate larger models; QLoRA makes training them accessible
- [[wiki/sources/papers/training-compute-optimal-large-language-models]] -- Chinchilla's compute-optimal insights are complementary: QLoRA addresses the memory barrier, Chinchilla the data barrier
- [[wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding]] -- BERT established the pretrain-then-finetune paradigm that QLoRA makes dramatically more efficient
- [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] -- Uses LoRA/QLoRA-style adaptation for fine-tuning VLA models on robotic tasks
- [[wiki/sources/papers/openvla-oft-optimizing-speed-and-success-for-vla-fine-tuning]] -- Advances VLA fine-tuning efficiency, building on QLoRA's democratization of parameter-efficient training
- [[wiki/concepts/foundation-models]] -- QLoRA is a key enabler of the foundation model paradigm by making adaptation accessible
- [[wiki/concepts/machine-learning]] -- Represents the efficiency frontier of the pretrain-then-adapt paradigm
