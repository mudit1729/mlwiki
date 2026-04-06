---
title: "VLP: Vision Language Planning for Autonomous Driving"
type: source-summary
status: complete
updated: 2026-04-05
year: 2024
venue: CVPR
tags:
  - paper
  - autonomous-driving
  - vla
  - vlm
  - planning
  - bev
citations: 155
---

📄 **[Read on arXiv](https://arxiv.org/abs/2401.05577)**

# VLP: Vision Language Planning for Autonomous Driving

## Overview

VLP (Vision Language Planning) by Pan et al. (CVPR 2024) represents a fundamentally different approach to using language in autonomous driving compared to instruction-following VLAs like LMDrive or reasoning-focused systems like Senna. Rather than using language as an explicit user interface or intermediate reasoning representation, VLP uses language model features as an internal knowledge prior that enhances BEV-based planning through feature-space alignment. No language input is needed at inference time.

The key insight is that pretrained language models encode vast world knowledge -- about object affordances, spatial relationships, traffic conventions, and physical common sense -- that is useful for driving even when language is not part of the driving interface. VLP injects this knowledge by aligning local BEV features with pretrained LM feature spaces (ALP module) and by using LM comprehension to align planning queries with navigation goals and ego status (SLP module). The result is a driving system that benefits from language model knowledge without requiring language input, language output, or any language-related computation at inference time.

This establishes "language as prior" as a distinct paradigm alongside "language as interface" (LMDrive, Talk2Car) and "language as reasoning channel" (Senna, ORION). VLP demonstrates that the boundaries of what constitutes a VLA system are blurry: the system uses vision-language alignment during training but is purely vision-action at deployment, raising interesting questions about how to classify and compare these architectures.

## Key Contributions

- **ALP (Aligned Language Planning)**: Aligns local BEV features with pretrained language model feature space through contrastive learning, injecting richer semantic representations into the spatial planning pipeline without requiring language input at test time
- **SLP (Structured Language Planning)**: Uses language model comprehension to align planning queries with navigation goals and ego status, providing high-level semantic guidance to the planner via feature-space conditioning
- **Language as internal prior paradigm**: LM knowledge improves planning without requiring language input at inference time, distinguishing VLP from instruction-following approaches and making it compatible with standard AD deployment
- **Compatible with existing BEV planning stacks**: The ALP/SLP modules can augment existing BEV-based AD systems without architectural overhaul, acting as plug-in improvements
- **Strong empirical validation at CVPR**: Published at a top venue with ~155 citations, demonstrating community interest in the language-as-prior approach

## Architecture / Method

![VLP Framework Overview: language models enhancing autonomous driving planning](https://paper-assets.alphaxiv.org/figures/2401.05577v4/x2.png)

VLP builds on a standard BEV-based autonomous driving pipeline and adds two language-guided modules during training. The base system extracts multi-camera features, lifts them to BEV space, and uses a transformer-based planner to predict ego trajectories.

**ALP (Aligned Language Planning)**: During training, scene descriptions are encoded by a frozen pretrained language model (e.g., CLIP text encoder or a small LM) to produce text feature vectors. A contrastive alignment loss encourages the local BEV features at specific spatial locations to match the text features describing what is at those locations (e.g., "pedestrian crossing ahead" aligns with the BEV features at the crosswalk location). At inference time, the language model is removed entirely -- the BEV encoder has learned to produce features that are semantically richer due to the training-time alignment.

**SLP (Structured Language Planning)**: The planner's ego queries are conditioned on structured language descriptions of the navigation goal ("turn left at the next intersection") and ego status ("currently traveling at 30 km/h in the right lane"). During training, these are encoded by the LM and fused with the planning queries via cross-attention. At inference, the SLP module can either be removed (if no language input is available) or used with template-based descriptions generated from the navigation system.

Both modules use training-time language supervision to shape the feature space of the vision-only driving system. The total loss combines standard planning losses (waypoint L2, collision penalty) with the ALP contrastive loss and SLP alignment loss.

## Results

![Cross-city generalization results: zero-shot performance on unseen urban environments](https://paper-assets.alphaxiv.org/figures/2401.05577v4/x1.png)

| Configuration | L2 Error Reduction | Collision Rate Reduction |
|---------------|-------------------|------------------------|
| VLP-VAD | 35.9% | 60.5% |
| VLP-UniAD | 28.1% | 48.4% |
| Cross-city (Boston) | 15.1% | 18.5% |
| Cross-city (Singapore) | 19.2% | 48.7% |

- **Improvements across multiple driving tasks on nuScenes**, particularly in long-tail and rare scenarios where LM world knowledge provides useful semantic priors that pure vision features lack
- **LM features enhance semantic understanding** of complex scenes that BEV features alone may not capture, with the largest improvements on scenarios involving unusual objects, ambiguous right-of-way, and complex intersections
- **No language input needed at inference**: The system is deployable in standard AD pipelines without a language interface, with all language benefit baked into the feature representations during training
- **Plug-in improvement to existing systems**: ALP and SLP can be added to multiple baseline BEV planners (e.g., UniAD, VAD) and consistently improve performance
- **Ablation validates both modules**: ALP alone improves performance, SLP alone improves performance, and the combination is additive, suggesting they capture complementary aspects of language knowledge

## Limitations & Open Questions

- Ambiguous VLA classification: language functions as an internal prior rather than explicit instruction-following, blurring the boundary of what constitutes a VLA system and making comparison with other VLA approaches methodologically challenging
- Primarily open-loop evaluation on nuScenes, which does not capture closed-loop driving challenges (compounding errors, reactive agents)
- Limited interpretability: LM features improve performance but do not generate human-readable reasoning or explanations, forgoing the interpretability benefits that explicit language reasoning provides
- Dependent on the quality and alignment of pretrained LM features with driving-relevant semantics; misalignment between web-trained LM representations and driving-specific concepts could limit benefit

## Connections

- [[wiki/concepts/autonomous-driving]]
- [[wiki/concepts/vision-language-action]]
- [[wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models]]
- [[wiki/sources/papers/simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment]]
- [[wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving]]
- [[wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving]]
