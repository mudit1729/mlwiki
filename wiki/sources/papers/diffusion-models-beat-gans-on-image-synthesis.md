---
title: "Diffusion Models Beat GANs on Image Synthesis"
tags: [computer-vision, diffusion, generative-models, image-generation, classifier-guidance]
status: active
type: paper
year: "2021"
venue: "NeurIPS 2021"
citations: 13548
arxiv_id: "2105.05233"
paper-faithfullness: audited-solid
---

# Diffusion Models Beat GANs on Image Synthesis

📄 **[Read on arXiv](https://arxiv.org/abs/2105.05233)**

## Overview

This paper by Dhariwal and Nichol (OpenAI, 2021) demonstrates that diffusion models can surpass GANs on image synthesis for the first time, achieving state-of-the-art FID scores on ImageNet across multiple resolutions. While GANs had dominated image generation for years, they suffered from training instability, mode collapse, and limited diversity. Diffusion models offered stable training but had lagged behind on sample quality for complex, class-conditional datasets like ImageNet. This paper closes that gap decisively.

The core contributions are twofold. First, the authors systematically improve the U-Net architecture used in diffusion models (producing what they call the "ADM" -- Ablated Diffusion Model), finding that wider models with multi-resolution attention and adaptive group normalization substantially outperform deeper ones. Second, they introduce **classifier guidance**, a technique that uses the gradients of a separately trained classifier to steer the diffusion sampling process toward higher-fidelity samples of the target class. A guidance scale parameter `s` controls the diversity-fidelity tradeoff, and at moderate values, the guided diffusion model beats BigGAN-deep on FID across all ImageNet resolutions.

The significance of this work extends well beyond the specific benchmarks. By proving that diffusion models could match and exceed GAN quality while retaining training stability and better mode coverage, this paper catalyzed the shift of the generative modeling community away from GANs and toward diffusion-based approaches. It directly paved the way for DALL-E 2, Stable Diffusion, Imagen, and the explosion of diffusion-based generative systems across images, video, audio, 3D, and planning.

## Key Contributions

- **Improved U-Net architecture (ADM)**: Systematic ablation showing that increasing channel width is more compute-efficient than depth, with multi-resolution attention (32x32, 16x16, 8x8), BigGAN-style residual blocks, and Adaptive Group Normalization (AdaGN) that injects timestep and class embeddings
- **Classifier guidance**: A method to condition diffusion sampling using gradients from a pretrained classifier, shifting the reverse-process mean by a term proportional to the gradient of the classifier's log-probability with respect to the noisy image, scaled by a guidance strength `s`
- **First diffusion model to beat GANs on ImageNet**: Achieved FID of 2.97 (128x128), 4.59 (256x256), and 7.72 (512x512), surpassing BigGAN-deep across all resolutions
- **Diversity-fidelity tradeoff analysis**: Demonstrated that classifier guidance enables a smooth, controllable tradeoff between sample diversity and fidelity, with the guidance scale `s` acting as the control knob
- **Upsampling diffusion models**: Introduced a two-stage pipeline with a base diffusion model at low resolution followed by an upsampling diffusion model, enabling high-resolution synthesis

## Architecture / Method

```
┌──────────────────────────────────────────────────────────┐
│              Ablated Diffusion Model (ADM)                │
│                                                          │
│  x_t (noisy image) ──► ┌─────────────────────────────┐   │
│                         │      Improved U-Net         │   │
│                         │                             │   │
│                         │  Encoder:                   │   │
│                         │   ResBlock ──► ResBlock      │   │
│                         │   + Attn@32  + Attn@16      │   │
│                         │   ──► downsample ──►        │   │
│                         │   ResBlock + Attn@8         │   │
│                         │                             │   │
│  ┌──────────────┐       │  Bottleneck (Attn@8)        │   │
│  │ Timestep t   ├──────►│                             │   │
│  │ + Class y    │ AdaGN │  Decoder (skip connections): │   │
│  │ (embedding)  │       │   upsample ──► ResBlock     │   │
│  └──────────────┘       │   + Attn@8 ──► Attn@16      │   │
│                         │   ──► Attn@32 ──► output    │   │
│                         └──────────┬──────────────────┘   │
│                                    ▼                      │
│                              ε_θ(x_t, t, y)              │
└──────────────────────────────────────────────────────────┘

Classifier Guidance (at sampling time):
┌────────────┐     ┌──────────────────┐
│ ADM output │     │ Classifier p(y|x)│
│  ε_θ(x_t)  │     │ (trained on noisy│
└─────┬──────┘     │  images)         │
      │            └────────┬─────────┘
      │                     │ ∇_{x_t} log p(y|x_t)
      ▼                     ▼
   ε_hat = ε_θ - s·√(1-ᾱ_t)·∇_{x_t} log p(y|x_t)
      │
      ▼  (DDPM or DDIM step)
   x_{t-1}

Upsampling Pipeline:
  Base Model (64×64) ──► Upsample Model ──► 256×256 / 512×512
```

![Class-conditional ImageNet samples demonstrating high fidelity and diversity](https://paper-assets.alphaxiv.org/figures/2105.05233v4/img-0.jpeg)

### Improved U-Net (ADM)

The architecture builds on the DDPM U-Net but with several critical improvements found through ablation:

- **Width over depth**: Increasing the number of base channels (e.g., from 128 to 256) proved more effective per FLOP than adding more residual blocks per resolution level
- **Multi-resolution attention**: Self-attention applied at 32x32, 16x16, and 8x8 resolution levels (DDPM used only 16x16), capturing both fine-grained and coarse spatial relationships
- **Attention head dimension**: Using 64 channels per attention head rather than a fixed number of heads, which scales more naturally with model width
- **BigGAN residual blocks**: Adopting the residual block design from BigGAN, with upsampling/downsampling in residual paths
- **Adaptive Group Normalization (AdaGN)**: Replaces standard group normalization by incorporating both timestep and class label embeddings into the normalization parameters: `AdaGN(h, y) = y_s * GroupNorm(h) + y_b`, where `y_s` and `y_b` are obtained from a linear projection of the concatenated timestep and class embeddings

### Classifier Guidance

The key innovation is modifying the reverse diffusion sampling process using gradients from a classifier `p(y|x_t)` trained on noisy images at various noise levels. The conditional reverse process becomes:

```
p_theta,phi(x_{t-1} | x_t, y) ~ N(mu_theta(x_t, t) + s * sigma_t^2 * grad_{x_t} log p_phi(y | x_t), sigma_t^2 * I)
```

where:
- `mu_theta(x_t, t)` is the unconditional diffusion model's predicted mean
- `p_phi(y | x_t)` is the classifier evaluated on the noisy image
- `s` is the guidance scale (s=1 corresponds to exact conditional sampling; s>1 amplifies the classifier signal)
- `sigma_t^2` is the noise variance at step t

For DDIM sampling, the modification adjusts the predicted noise directly:

```
epsilon_hat = epsilon_theta(x_t, t) - s * sqrt(1 - alpha_bar_t) * grad_{x_t} log p_phi(y | x_t)
```

The classifier is a standard architecture (similar to the U-Net's downsampling path) trained on noisy ImageNet images at all noise levels, producing class predictions from intermediate features via attention pooling.

### Upsampling Pipeline

For high-resolution synthesis (256x256, 512x512), a two-stage approach is used:
1. A base diffusion model generates low-resolution images (e.g., 64x64 or 128x128)
2. An upsampling diffusion model conditions on the low-resolution image and generates the high-resolution output

Both stages can use classifier guidance independently.

## Results

| Model | Resolution | FID (down) | Precision | Recall |
|-------|-----------|-----|-----------|--------|
| **ADM-G (guided)** | **128x128** | **2.97** | 0.78 | 0.59 |
| BigGAN-deep | 128x128 | 6.02 | 0.86 | 0.35 |
| **ADM-G (guided)** | **256x256** | **4.59** | 0.82 | 0.52 |
| BigGAN-deep | 256x256 | 6.95 | 0.87 | 0.28 |
| **ADM-G + upsampling** | **256x256** | **3.94** | 0.83 | 0.53 |
| **ADM-G (guided)** | **512x512** | **7.72** | 0.87 | 0.42 |
| **ADM-G + upsampling** | **512x512** | **3.85** | 0.84 | 0.53 |

Key findings:

- **FID improvements are dramatic**: The guided diffusion model (ADM-G) achieves FID 2.97 on ImageNet 128x128, cutting BigGAN-deep's 6.02 by more than half
- **Better diversity**: While BigGAN achieves higher precision (sharper samples), ADM-G achieves substantially higher recall (better mode coverage), meaning diffusion models generate more diverse samples while maintaining quality
- **Guidance scale tradeoff**: Increasing `s` from 1.0 to ~2.5 steadily improves FID by trading recall for precision; beyond ~4.0, FID begins to degrade as diversity drops too far
- **Architecture ablations matter**: The improved U-Net alone (without guidance) substantially narrows the gap to GANs; guidance then closes it entirely
- **Efficient sampling via DDIM**: With DDIM, competitive results are achievable with as few as 25 forward passes per sample, compared to the 1000 steps of standard DDPM sampling

## Limitations & Open Questions

- **Classifier dependency**: Classifier guidance requires training a separate classifier on noisy images, adding complexity and limiting applicability to labeled datasets. This limitation was addressed by classifier-free guidance (Ho & Salimans, 2022), which removes the need for a separate classifier entirely
- **Sampling speed**: Even with DDIM (25 steps), diffusion models remain slower than GANs (single forward pass). Subsequent work on consistency models, progressive distillation, and latent diffusion has significantly narrowed this gap
- **Guidance as a crutch for diversity-fidelity**: The guidance scale `s` trades off diversity for quality in a somewhat blunt way; more principled approaches to conditional generation emerged later
- **Limited to class-conditional**: This work demonstrates guidance with class labels; extension to text-conditional generation required further innovations (GLIDE, DALL-E 2, Imagen)
- **Compute cost**: Training the large ADM models required substantial compute (256 V100 GPUs), and the two-stage upsampling pipeline adds further cost

## Connections

Related papers in the wiki:
- [[wiki/sources/papers/denoising-diffusion-probabilistic-models]] -- The foundational DDPM paper that this work directly builds upon and improves; ADM inherits the epsilon-prediction parameterization and U-Net backbone
- [[wiki/sources/papers/variational-lossy-autoencoder]] -- Related generative modeling approach connecting VAEs and information-theoretic perspectives
- [[wiki/sources/papers/deep-residual-learning-for-image-recognition]] -- ResNet residual block design that the ADM U-Net adapts via BigGAN-style residual connections
- [[wiki/sources/papers/attention-is-all-you-need]] -- Self-attention mechanism used at multiple resolutions in the ADM architecture
- [[wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving]] -- Applies truncated diffusion to trajectory planning, showing how diffusion models from image synthesis transfer to driving
- [[wiki/sources/papers/dita-scaling-diffusion-transformer-for-generalist-vla-policy]] -- DiT-based VLA using diffusion for robotic action generation, descending from the diffusion paradigm this paper established
- [[wiki/sources/papers/rdt-1b-a-diffusion-foundation-model-for-bimanual-manipulation]] -- Largest diffusion transformer for robotics, building on the diffusion architecture innovations pioneered here
