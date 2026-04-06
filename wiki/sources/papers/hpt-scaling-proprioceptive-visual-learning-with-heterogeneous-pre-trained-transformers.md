---
title: "HPT: Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers"
tags: [robotics, foundation-model, cross-embodiment, proprioception]
status: active
type: paper
year: "2024"
venue: "NeurIPS"
citations: 134
arxiv_id: "2409.20537"
---

📄 **[Read on arXiv](https://arxiv.org/abs/2409.20537)**

## Overview

HPT tackles the fundamental challenge of building generalist robot representations that work across heterogeneous embodiments with different sensor configurations, action spaces, and morphologies. The key insight is a modular stem-trunk-head architecture: embodiment-specific stems tokenize diverse proprioceptive and visual inputs into a shared format, a large shared transformer trunk learns cross-embodiment representations, and task-specific heads decode actions. Trained on over 50 datasets spanning simulation and real robots, HPT demonstrates clear scaling laws for robotics -- performance improves predictably with data size, data diversity, model size (up to 1B+ parameters), and compute. This is one of the first works to establish that the scaling paradigm from language models transfers to robotic control.

## Key Contributions

- **Stem-trunk-head architecture:** Modular design enabling a single shared transformer to process inputs from heterogeneous embodiments with different sensors and action spaces
- **Cross-modal fusion via cross-attention:** Proprioceptive tokens serve as queries attending to visual tokens as keys/values, enabling effective sensor fusion without modality-specific architectures
- **Scaling laws for robotics:** Demonstrates predictable performance improvements across four axes -- data quantity, data diversity, model size, and compute -- analogous to LLM scaling laws
- **Joint modality training superiority:** Combined proprioceptive + visual training outperforms either modality alone or sequential modality addition
- **Multi-source data benefit:** Incorporating simulation and human video data alongside real robot data improves performance over single-source training

## Architecture / Method

HPT uses a three-component architecture:

**Stems (embodiment-specific):**
- Proprioceptive Tokenizer: processes joint positions and velocities into fixed-length token sequences
- Visual Tokenizer: handles multi-viewpoint camera inputs via vision encoders
- Each stem maps heterogeneous inputs to a consistent token format for the shared trunk

**Trunk (shared transformer):**
- Large transformer network shared across all embodiments and tasks
- Cross-attention mechanism fuses proprioceptive queries with visual keys/values
- Pre-trained on 50+ datasets spanning simulation (Fleet-Tools, Metaworld, Robomimic) and real robots
- Scales up to 1B+ parameters

**Heads (task-specific):**
- Three variants tested: pooling layers, diffusion models, and transformer layers
- Decode shared representations into embodiment-specific actions

## Results

| Setting | HPT vs. Scratch | Details |
|---------|-----------------|---------|
| Simulation (Fleet-Tools, Metaworld, Robomimic) | +10-30% success rate | Consistent gains across all benchmarks |
| Real robot (4 manipulation tasks) | +20%+ success rate | Sweep, water-filling, food-scooping, switch insertion |
| Data scaling | Monotonic improvement | More data always helps; diversity matters more than quantity |
| Model scaling | Monotonic improvement | Larger models consistently outperform smaller ones (up to 1B+) |
| Compute scaling | Monotonic improvement | More compute leads to better final performance |

Key ablation: joint proprioceptive + visual training outperforms either modality alone, and removing either modality degrades performance. Simulation and human video data provide complementary benefits to real robot data.

## Limitations

- Scaling laws are demonstrated but not yet at the scale of language model experiments (1B vs 100B+)
- Action spaces remain discretized per embodiment head -- no universal action representation
- Real-world evaluation limited to four manipulation tasks; generalization to locomotion, navigation, or more complex manipulation untested
- Pre-training data is predominantly manipulation; whether the scaling trends hold for other robot task families is unknown

## Connections

- Extends the cross-embodiment vision of [[wiki/sources/papers/openvla-an-open-source-vision-language-action-model]] and [[wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control]] to explicitly heterogeneous sensor/action spaces
- Scaling laws connect to [[wiki/sources/papers/scaling-laws-for-neural-language-models]] -- HPT is evidence that the language model scaling paradigm transfers to robotics
- The cross-attention fusion mechanism relates to [[wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots]] which also uses cross-attention between reasoning and action modules
- Relevant to [[wiki/concepts/robotics]] open problem of cross-embodiment transfer
- Informs [[wiki/concepts/foundation-models]] on whether pretrain-then-adapt works for embodied AI
