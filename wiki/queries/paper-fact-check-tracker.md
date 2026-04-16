# Paper Fact-Check Tracker

Updated: 2026-04-11

Purpose: coordinate a full factuality audit of every page in `wiki/sources/papers/` against the original paper.

Per-paper status lives in YAML frontmatter under `paper-faithfullness`.

## Status Legend

- `unchecked` — no direct paper-vs-summary audit completed yet
- `audited-solid` — sampled against the original paper and materially faithful
- `audited-needs-tightening` — mostly faithful but contains notable imprecision or unsupported framing
- `audited-needs-correction` — contains factual errors or materially misleading claims

## [2026-04-11] random-sample audit | 10 additional paper summaries (seed 20260417)

- Deterministic sample seed: `20260417`
- Sampled pages: `uniact-universal-actions-for-enhanced-embodied-foundation-models`, `swin-transformer-hierarchical-vision-transformer-using-shifted-windows`, `attention-is-all-you-need`, `driveadapter-breaking-the-coupling-barrier-of-perception-and-planning-in-end-to-end-autonomous-driving`, `vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation`, `scaling-instruction-finetuned-language-models`, `smolvla-a-vision-language-action-model-for-affordable-robotics`, `fb-bev-bev-representation-from-forward-backward-view-transformations`, `a-language-agent-for-autonomous-driving`, and `cosmos-world-foundation-model-platform-for-physical-ai`.
- Found `2` clear corrections: `vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation` understated the FLOP reduction as `70%` even though the paper reports `10.56G` vs `0.041G` FLOPs for the main comparison (about `200x` fewer / `99.6%` lower), and `smolvla-a-vision-language-action-model-for-affordable-robotics` overstated the memory advantage over `pi0` as `7x` even though the paper states `6x less memory`.
- The other `8` sampled pages did not show material paper-vs-summary failures in this pass and were left unchanged.
- Actual frontmatter counts after this sample remain mixed because legacy labels are still present elsewhere in the corpus: `audited-solid` `160`, `audited-clean` `15`, `audited-fixed` `20`, `audited-needs-tightening` `1`, `audited-needs-correction` `1`.

## [2026-04-11] random-sample audit | 20-paper serious-error check (seed 20260415)

- Deterministic sample seed: `20260415`
- Sampled pages: `law-enhancing-end-to-end-autonomous-driving-with-latent-world-model`, `gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction`, `qlora-efficient-finetuning-of-quantized-language-models`, `drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model`, `bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers`, `mamba-linear-time-sequence-modeling-with-selective-state-spaces`, `roboflamingo-vision-language-foundation-models-as-effective-robot-imitators`, `toolformer-language-models-can-teach-themselves-to-use-tools`, `hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers`, `flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin`, `vad-vectorized-scene-representation-for-efficient-autonomous-driving`, `s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation`, `yolov10-real-time-end-to-end-object-detection`, `bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising`, `an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale`, `helix-a-vla-for-generalist-humanoid-control`, `drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states`, `training-language-models-to-follow-instructions-with-human-feedback`, `driving-gaussian-composite-gaussian-splatting-for-surrounding-dynamic-driving-scenes`, and `rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control`.
- Found `1` serious error: `flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin` was downgraded to `audited-needs-correction` because the summary reported materially wrong mIoU/speed tradeoffs and mischaracterized the plug-in results. The corrected page now reflects the paper's actual BEVDetOcc / UniOcc / FBOcc comparisons and resource numbers.
- Found `1` smaller overstatement: `rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control` was downgraded to `audited-needs-tightening` because the page claimed a quantified chain-of-thought improvement even though the paper presents that variant qualitatively rather than as a main measured gain.
- The other `18` sampled pages did not show serious paper-vs-summary failures and were left unchanged.
- Actual frontmatter counts after this sample remain mixed because legacy labels are still present elsewhere in the corpus: `audited-solid` `164`, `audited-clean` `15`, `audited-fixed` `16`, `audited-needs-tightening` `1`, `audited-needs-correction` `1`.

## [2026-04-11] random-sample audit | 20 additional paper summaries (seed 20260416)

- Deterministic sample seed: `20260416`
- Sampled pages: `knowledge-insulating-vision-language-action-models`, `openvla-an-open-source-vision-language-action-model`, `occmamba-semantic-occupancy-prediction-with-state-space-models`, `gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction`, `machine-super-intelligence`, `unleashing-large-scale-video-generative-pre-training-for-visual-robot-manipulation`, `wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model`, `orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation`, `gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting`, `drivor-driving-on-registers`, `keeping-neural-networks-simple-by-minimizing-the-description-length-of-the-weights`, `vista-a-generalizable-driving-world-model-with-high-fidelity-and-versatile-controllability`, `autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents`, `mixtral-of-experts`, `video-prediction-policy-a-generalist-robot-policy-with-predictive-visual-representations`, `gaussianflowocc-sparse-occupancy-with-gaussian-splatting-and-temporal-flow`, `chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst`, `palm-scaling-language-modeling-with-pathways`, `bevnext-reviving-dense-bev-frameworks-for-3d-object-detection`, and `imagenet-classification-with-deep-convolutional-neural-networks`.
- Found `1` clear correction: `gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction` had conflated the 25,600-Gaussian ablation setting with the 12,800-Gaussian nuScenes main result, so the summary overstated the number of Gaussians and cited the wrong main-result memory figure. The page now reflects the paper's actual nuScenes setup.
- Found `1` smaller but real overstatement: `chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst` summarized closed-loop gains as broad aggregate percentage reductions that the paper does not report. The results section now mirrors the paper's scenario-based evaluations and real-world demo claims instead of introducing unsupported aggregate numbers.
- The other `18` sampled pages did not show material paper-vs-summary failures in this pass and were left unchanged.
- Actual frontmatter counts after this sample remain mixed because legacy labels are still present elsewhere in the corpus: `audited-solid` `162`, `audited-clean` `15`, `audited-fixed` `18`, `audited-needs-tightening` `1`, `audited-needs-correction` `1`.

## [2026-04-11] targeted factuality audit | simlingo + talk2car

- Audited `2` papers against arxiv and AlphaXiv ground truth.
- `simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment`: **fixed** (`audited-fixed`). Action Dreaming success rates were wrong — wiki stated "28.22 to 72.96" but the paper (Table 5) reports baseline **24.52%** and SimLingo with dreaming data **81.13%**. Corrected in the Results section. All other claims (CVPR 2025 venue, Bench2Drive DS 85.07% / SR 67.27%, CARLA Leaderboard 2.0 state-of-the-art, camera-only, instruction refusal) are faithful.
- `talk2car-taking-control-of-your-self-driving-car`: **clean** (`audited-clean`). All factual claims verified: 11,959 commands over 850 nuScenes training videos, EMNLP-IJCNLP 2019 venue, authors (Deruyttere, Vandenhende, Grujicic, Van Gool, Moens), AP50 evaluation metric, two-tower baseline description, and Talk2Car-Trajectory extension characterization are all faithful to the source.
- Current corpus counts: `audited-solid` `188`, `audited-needs-tightening` `5`, `audited-needs-correction` `2`, `audited-fixed` `2`, `audited-clean` `2`, `unchecked` `0`.

## [2026-04-11] non-arxiv source audit | cs231n and understanding-lstm-networks

- Audited `2` non-arXiv blog/course sources against their live original URLs.
- `cs231n-convolutional-neural-networks-for-visual-recognition`: **fixed** (`audited-fixed`). The title in frontmatter and document heading was wrong — the course is officially titled "CS231n: Deep Learning for Computer Vision" (confirmed from both `http://cs231n.github.io/` and `https://cs231n.stanford.edu/`), not "Convolutional Neural Networks for Visual Recognition" (the older pre-2017 name). Fixed in frontmatter `title` field and `# h1` heading. All other factual claims (instructors Fei-Fei Li, Karpathy, Johnson; course structure; architectural descriptions) are consistent with the source.
- `understanding-lstm-networks`: **clean** (`audited-clean`). All factual claims verified against `https://colah.github.io/posts/2015-08-Understanding-LSTMs/`: three-gate architecture (forget, input, output), LSTM attribution to Hochreiter & Schmidhuber (1997), GRU attribution to Cho et al. (2014), cell state equations, and the additive gradient highway framing are all faithful to the source.
- Current corpus counts: `audited-solid` `188`, `audited-needs-tightening` `5`, `audited-needs-correction` `2`, `audited-fixed` `1`, `audited-clean` `1`, `unchecked` `0`.

## [2026-04-11] random-sample audit | 10 additional paper summaries (seed 20260414)

- Deterministic sample seed: `20260414`
- Sampled pages: `on-the-opportunities-and-risks-of-foundation-models`, `drivegpt-scaling-autoregressive-behavior-models-for-driving`, `prefix-tuning-optimizing-continuous-prompts-for-generation`, `planning-oriented-autonomous-driving`, `vlp-vision-language-planning-for-autonomous-driving`, `pi0-a-vision-language-action-flow-model-for-general-robot-control`, `blip-bootstrapping-language-image-pre-training-for-unified-vision-language-understanding-and-generation`, `rdt-1b-a-diffusion-foundation-model-for-bimanual-manipulation`, `qwen3-technical-report`, `gr-2-a-generative-video-language-action-model-with-web-scale-knowledge-for-robot-manipulation`
- Found `2` summaries needing changes: `pi0-a-vision-language-action-flow-model-for-general-robot-control` was downgraded to `audited-needs-tightening` because the page asserted positive cross-embodiment transfer that the paper does not isolate in a dedicated ablation; `rdt-1b-a-diffusion-foundation-model-for-bimanual-manipulation` was downgraded to `audited-needs-tightening` because its limitation section incorrectly implied the evaluation was primarily in simulation even though the paper's main experiments are on real ALOHA dual-arm robots.
- The other `8` sampled pages matched the source papers closely enough to keep their current `audited-solid` status: `on-the-opportunities-and-risks-of-foundation-models`, `drivegpt-scaling-autoregressive-behavior-models-for-driving`, `prefix-tuning-optimizing-continuous-prompts-for-generation`, `planning-oriented-autonomous-driving`, `vlp-vision-language-planning-for-autonomous-driving`, `blip-bootstrapping-language-image-pre-training-for-unified-vision-language-understanding-and-generation`, `qwen3-technical-report`, and `gr-2-a-generative-video-language-action-model-with-web-scale-knowledge-for-robot-manipulation`.
- Current corpus counts after this sample: `audited-solid` `183`, `audited-needs-tightening` `11`, `audited-needs-correction` `3`, `unchecked` `0`.

## [2026-04-11] targeted correction audit | lift-splat-shoot and occgen

- Audited `2` pages flagged `audited-needs-correction` against arxiv and AlphaXiv ground truth.
- `lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d`: **clean** (`audited-clean`). All factual claims verified — authors (Philion, Fidler), venue (ECCV 2020), backbone (EfficientNet-B0), BEV encoder (ResNet-18), depth binning, cumulative-sum splat trick, nuScenes/Lyft evaluation, and planning formulation all match the arxiv abstract and AlphaXiv overview. No material corrections needed.
- `occgen-generative-multi-modal-3d-occupancy-prediction-for-autonomous-driving`: **fixed** (`audited-fixed`). Three locations had camera-only and LiDAR-only mIoU scores swapped. Paper Table 9 shows C-OccGen (camera-only) = **14.5** mIoU and L-OccGen (LiDAR-only) = **16.8** mIoU; wiki had these reversed. The results table comparison baseline rows were also mislabelled: C-CONet = 12.8 is camera-only (not LiDAR-only) and L-CONet = 15.8 is LiDAR-only (not camera-only). The TPVFormer row (15.1) was relabelled to OpenOccupancy (multi-modal baseline); TPVFormer's actual nuScenes-Occupancy score is 7.8 (camera-only). Fixed in overview paragraph, key-contributions bullet, and results table.
- Current corpus counts: `audited-solid` `186`, `audited-needs-tightening` `8`, `audited-needs-correction` `1`, `audited-clean` `1`, `audited-fixed` `1`, `unchecked` `0`.

## [2026-04-11] random-sample audit | 10 additional paper summaries (seed 20260413)

- Deterministic sample seed: `20260413`
- Sampled pages: `alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving`, `gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting`, `simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment`, `drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving`, `voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models`, `senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving`, `unisim-learning-interactive-real-world-simulators`, `variational-lossy-autoencoder`, `emerging-properties-in-self-supervised-vision-transformers`, `momad-momentum-aware-planning-in-end-to-end-autonomous-driving`
- Found `1` summary needing changes: `simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment` was downgraded to `audited-needs-tightening` because the page overstated the effect of Action Dreaming on closed-loop driving and treated the benchmark evidence more broadly than the paper supports.
- The other `9` sampled pages matched the source papers closely enough to keep their current `audited-solid` status: `alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving`, `gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting`, `drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving`, `voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models`, `senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving`, `unisim-learning-interactive-real-world-simulators`, `variational-lossy-autoencoder`, `emerging-properties-in-self-supervised-vision-transformers`, and `momad-momentum-aware-planning-in-end-to-end-autonomous-driving`.
- Current corpus counts after this sample: `audited-solid` `185`, `audited-needs-tightening` `9`, `audited-needs-correction` `3`, `unchecked` `0`.

## [2026-04-11] random-sample audit | 10 additional paper summaries

- Deterministic sample seed: `20260412`
- Sampled pages: `multi-scale-context-aggregation-by-dilated-convolutions`, `rt-h-action-hierarchies-using-language`, `embodiment-scaling-laws-in-robot-locomotion`, `occgen-generative-multi-modal-3d-occupancy-prediction-for-autonomous-driving`, `selfocc-self-supervised-vision-based-3d-occupancy-prediction`, `rt-1-robotics-transformer-for-real-world-control-at-scale`, `lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d`, `llarva-vision-action-instruction-tuning-enhances-robot-learning`, `3d-vla-a-3d-vision-language-action-generative-world-model`, `occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving`
- Found `3` summaries needing changes: `multi-scale-context-aggregation-by-dilated-convolutions` was downgraded to `audited-needs-tightening` after fixing the basic context-module description (seven layers, no batch normalization claim); `occgen-generative-multi-modal-3d-occupancy-prediction-for-autonomous-driving` was downgraded to `audited-needs-correction` after correcting the swapped camera-only vs. LiDAR-only nuScenes numbers; `lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d` remained `audited-needs-correction` with unsupported transfer/runtime overclaims removed.
- The other `7` sampled pages matched the source papers closely enough to keep their current `audited-solid` status: `rt-h-action-hierarchies-using-language`, `embodiment-scaling-laws-in-robot-locomotion`, `selfocc-self-supervised-vision-based-3d-occupancy-prediction`, `rt-1-robotics-transformer-for-real-world-control-at-scale`, `llarva-vision-action-instruction-tuning-enhances-robot-learning`, `3d-vla-a-3d-vision-language-action-generative-world-model`, and `occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving`.
- Current corpus counts after this sample: `audited-solid` `186`, `audited-needs-tightening` `8`, `audited-needs-correction` `3`, `unchecked` `0`.

## [2026-04-11] corpus metadata validation | 197 source pages

- Validated all `wiki/sources/papers/` entries at the primary-record level: `197` total pages, `187` arXiv-backed entries, `10` non-arXiv entries.
- arXiv-backed coverage is structurally clean after link fixes: `158` exact title matches to arXiv records, `27` acceptable title variants or acronym-prefix variants, `2` shortened-title variants (`gpipe`, `drive-occworld`) that still point to the correct paper, and `0` unresolved arXiv-record misses.
- Fixed three broken primary-source references: `solve` now points to arXiv `2505.16805`, `simlingo` now points to arXiv `2503.09594`, and `para-drive` now points to the CVPR 2024 Open Access page with the incorrect `arxiv_id` removed.
- Frontmatter year vs. arXiv upload year differs by at most `1` across all arXiv-backed entries, which is consistent with conference-year vs. preprint-year drift rather than broken metadata.
- This pass established source identity and metadata correctness; the follow-up source-faithfulness audit below resolves the old legacy status vocabulary and clears the remaining unchecked backlog.
- Non-arXiv entries now explicitly accounted for: `cs231n`, `helix`, `imagenet-classification-with-deep-convolutional-neural-networks`, `keeping-neural-networks-simple-by-minimizing-the-description-length-of-the-weights`, `kolmogorov-complexity-and-algorithmic-randomness`, `machine-super-intelligence`, `para-drive-parallelized-architecture-for-real-time-autonomous-driving`, `the-first-law-of-complexodynamics`, `the-unreasonable-effectiveness-of-recurrent-neural-networks`, `understanding-lstm-networks`.

## [2026-04-11] remaining source-faithfulness audit | 14 pages

- Audited the final `14` pages that were still literally marked `unchecked` in frontmatter.
- Marked `10` of those pages `audited-solid`: `a-tutorial-introduction-to-the-minimum-description-length-principle`, `imagenet-classification-with-deep-convolutional-neural-networks`, `keeping-neural-networks-simple-by-minimizing-the-description-length-of-the-weights`, `kolmogorov-complexity-and-algorithmic-randomness`, `machine-super-intelligence`, `multi-scale-context-aggregation-by-dilated-convolutions`, `neural-machine-translation-by-jointly-learning-to-align-and-translate`, `recurrent-neural-network-regularization`, `simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment`, and `talk2car-taking-control-of-your-self-driving-car`.
- Marked `4` pages `audited-needs-tightening` and softened their wording because they are blog/course-style sources whose summaries mixed source content with broader field-impact interpretation: `cs231n-convolutional-neural-networks-for-visual-recognition`, `the-first-law-of-complexodynamics`, `the-unreasonable-effectiveness-of-recurrent-neural-networks`, and `understanding-lstm-networks`.
- Normalized `110` legacy `audited-clean` / `audited-fixed` labels to `audited-solid` so the corpus now uses only the tracker legend.
- Current corpus counts: `audited-solid` `188`, `audited-needs-tightening` `7`, `audited-needs-correction` `2`, `unchecked` `0`.

## [2026-04-11] random-sample audit | 10 paper summaries

- Deterministic sample seed: `20260411`
- Hard factual issues fixed across 5 summaries: `carla`, `surroundocc`, `self-improving-embodied-foundation-models`, `bert`, `drivedreamer`
- Audited with no material paper-faithfulness fixes needed: `sparsedrive`, `language-models-are-few-shot-learners`, `scaling-laws-for-neural-language-models`, `s4-driver`, `scaling-cross-embodied-learning`
- Main error types: wrong benchmark values, incorrect loss descriptions, inaccurate venue/training metadata, and one limitation claim contradicted by the paper

## Batch Tracker

### Batch 01 — active
- `wiki/sources/papers/3d-vla-a-3d-vision-language-action-generative-world-model.md`
- `wiki/sources/papers/a-generalist-agent.md`
- `wiki/sources/papers/a-language-agent-for-autonomous-driving.md`
- `wiki/sources/papers/a-simple-neural-network-module-for-relational-reasoning.md`
- `wiki/sources/papers/a-tutorial-introduction-to-the-minimum-description-length-principle.md`
- `wiki/sources/papers/alpamayo-r1-bridging-reasoning-and-action-prediction-for-autonomous-driving.md`
- `wiki/sources/papers/alphadrive-unleashing-the-power-of-vlms-in-autonomous-driving.md`
- `wiki/sources/papers/an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md`
- `wiki/sources/papers/asyncdriver-asynchronous-large-language-model-enhanced-planner-for-autonomous-driving.md`
- `wiki/sources/papers/attention-is-all-you-need.md`

### Batch 02 — active
- `wiki/sources/papers/autort-embodied-foundation-models-for-large-scale-orchestration-of-robotic-agents.md`
- `wiki/sources/papers/autovala-vision-language-action-model-for-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md`
- `wiki/sources/papers/bevdiffuser-plug-and-play-diffusion-model-for-bev-denoising.md`
- `wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers.md`
- `wiki/sources/papers/bevformer-v2-adapting-modern-image-backbones-to-birds-eye-view-recognition-via-perspective-supervision.md`
- `wiki/sources/papers/bevnext-reviving-dense-bev-frameworks-for-3d-object-detection.md`
- `wiki/sources/papers/blip-bootstrapping-language-image-pre-training-for-unified-vision-language-understanding-and-generation.md`
- `wiki/sources/papers/bridgead-bridging-past-and-future-end-to-end-autonomous-driving-with-historical-prediction.md`
- `wiki/sources/papers/carla-an-open-urban-driving-simulator.md`

### Batch 03 — active
- `wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving.md`
- `wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md`
- `wiki/sources/papers/chauffeurnet-learning-to-drive-by-imitating-the-best-and-synthesizing-the-worst.md`
- `wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai.md`
- `wiki/sources/papers/covla-comprehensive-vision-language-action-dataset-for-autonomous-driving.md`
- `wiki/sources/papers/cs231n-convolutional-neural-networks-for-visual-recognition.md`
- `wiki/sources/papers/deep-residual-learning-for-image-recognition.md`
- `wiki/sources/papers/deep-speech-2.md`
- `wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning.md`
- `wiki/sources/papers/denoising-diffusion-probabilistic-models.md`

### Batch 04 — active
- `wiki/sources/papers/dexvla-vision-language-model-with-plug-in-diffusion-expert.md`
- `wiki/sources/papers/diffusion-models-beat-gans-on-image-synthesis.md`
- `wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/dima-distilling-multi-modal-large-language-models-for-autonomous-driving.md`
- `wiki/sources/papers/direct-preference-optimization-your-language-model-is-secretly-a-reward-model.md`
- `wiki/sources/papers/dita-scaling-diffusion-transformer-for-generalist-vla-policy.md`
- `wiki/sources/papers/drive-as-you-speak-enabling-human-like-interaction-with-large-language-models-in-autonomous-vehicles.md`
- `wiki/sources/papers/drive-occworld-driving-in-the-occupancy-world.md`
- `wiki/sources/papers/driveadapter-breaking-the-coupling-barrier-of-perception-and-planning-in-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/drivedreamer-towards-real-world-driven-world-models.md`

### Batch 05 — active
- `wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving.md`
- `wiki/sources/papers/drivegpt4-interpretable-end-to-end-autonomous-driving-via-large-language-model.md`
- `wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering.md`
- `wiki/sources/papers/drivemlm-aligning-multi-modal-llms-with-behavioral-planning-states.md`
- `wiki/sources/papers/drivemoe-mixture-of-experts-for-vision-language-action-in-autonomous-driving.md`
- `wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/drivevlm-the-convergence-of-autonomous-driving-and-large-vision-language-models.md`
- `wiki/sources/papers/driving-gaussian-composite-gaussian-splatting-for-surrounding-dynamic-driving-scenes.md`
- `wiki/sources/papers/driving-with-llms-fusing-object-level-vector-modality-for-explainable-autonomous-driving.md`
- `wiki/sources/papers/drivor-driving-on-registers.md`

### Batch 06 — active
- `wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models.md`
- `wiki/sources/papers/embodiment-scaling-laws-in-robot-locomotion.md`
- `wiki/sources/papers/emerging-properties-in-self-supervised-vision-transformers.md`
- `wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving.md`
- `wiki/sources/papers/end-to-end-driving-via-conditional-imitation-learning.md`
- `wiki/sources/papers/end-to-end-learning-for-self-driving-cars.md`
- `wiki/sources/papers/exploring-simple-siamese-representation-learning.md`
- `wiki/sources/papers/fast-efficient-action-tokenization-for-vision-language-action-models.md`
- `wiki/sources/papers/fb-bev-bev-representation-from-forward-backward-view-transformations.md`
- `wiki/sources/papers/flamingo-a-visual-language-model-for-few-shot-learning.md`

### Batch 07 — active
- `wiki/sources/papers/flashocc-fast-and-memory-efficient-occupancy-prediction-via-channel-to-height-plugin.md`
- `wiki/sources/papers/gaussianbev-3d-gaussian-representation-meets-perception-models-for-bev-segmentation.md`
- `wiki/sources/papers/gaussianflowocc-sparse-occupancy-with-gaussian-splatting-and-temporal-flow.md`
- `wiki/sources/papers/gaussianformer-2-probabilistic-gaussian-superposition-for-efficient-3d-occupancy-prediction.md`
- `wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction.md`
- `wiki/sources/papers/gaussianlss-toward-real-world-bev-perception-with-depth-uncertainty-via-gaussian-splatting.md`
- `wiki/sources/papers/gaussianocc-fully-self-supervised-3d-occupancy-estimation-with-gaussian-splatting.md`
- `wiki/sources/papers/gaussianworld-gaussian-world-model-for-streaming-3d-occupancy-prediction.md`
- `wiki/sources/papers/gaussrender-learning-3d-occupancy-with-gaussian-rendering.md`
- `wiki/sources/papers/gausstr-foundation-model-aligned-gaussian-transformer-for-self-supervised-3d.md`

### Batch 08 — active
- `wiki/sources/papers/gemini-25-pushing-the-frontier-with-advanced-reasoning-multimodality-long-context-and-next-generation-agentic-capabilities.md`
- `wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world.md`
- `wiki/sources/papers/gemma-3-technical-report.md`
- `wiki/sources/papers/genad-generalized-predictive-model-for-autonomous-driving.md`
- `wiki/sources/papers/genad-generative-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/goalflow-goal-driven-flow-matching-for-multimodal-trajectory-generation.md`
- `wiki/sources/papers/gpipe-easy-scaling-with-micro-batch-pipeline-parallelism.md`
- `wiki/sources/papers/gpt-4-technical-report.md`
- `wiki/sources/papers/gpt-driver-learning-to-drive-with-gpt.md`
- `wiki/sources/papers/gr-2-a-generative-video-language-action-model-with-web-scale-knowledge-for-robot-manipulation.md`

### Batch 09 — active
- `wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots.md`
- `wiki/sources/papers/helix-a-vla-for-generalist-humanoid-control.md`
- `wiki/sources/papers/hermes-a-unified-self-driving-world-model-for-simultaneous-3d-scene-understanding-and-generation.md`
- `wiki/sources/papers/hierarchical-text-conditional-image-generation-with-clip-latents.md`
- `wiki/sources/papers/high-resolution-image-synthesis-with-latent-diffusion-models.md`
- `wiki/sources/papers/hpt-scaling-proprioceptive-visual-learning-with-heterogeneous-pre-trained-transformers.md`
- `wiki/sources/papers/hydra-mdp-end-to-end-multimodal-planning-with-multi-target-hydra-distillation.md`
- `wiki/sources/papers/identity-mappings-in-deep-residual-networks.md`
- `wiki/sources/papers/imagenet-classification-with-deep-convolutional-neural-networks.md`
- `wiki/sources/papers/is-ego-status-all-you-need-for-open-loop-end-to-end-autonomous-driving.md`

### Batch 10 — active
- `wiki/sources/papers/keeping-neural-networks-simple-by-minimizing-the-description-length-of-the-weights.md`
- `wiki/sources/papers/knowledge-insulating-vision-language-action-models.md`
- `wiki/sources/papers/kolmogorov-complexity-and-algorithmic-randomness.md`
- `wiki/sources/papers/language-models-are-few-shot-learners.md`
- `wiki/sources/papers/languagempc-large-language-models-as-decision-makers-for-autonomous-driving.md`
- `wiki/sources/papers/law-enhancing-end-to-end-autonomous-driving-with-latent-world-model.md`
- `wiki/sources/papers/learning-by-cheating.md`
- `wiki/sources/papers/learning-lane-graph-representations-for-motion-forecasting.md`
- `wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision.md`
- `wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d.md`

### Batch 11 — active
- `wiki/sources/papers/llama-2-open-foundation-and-fine-tuned-chat-models.md`
- `wiki/sources/papers/llarva-vision-action-instruction-tuning-enhances-robot-learning.md`
- `wiki/sources/papers/llms-cant-plan-but-can-help-planning-in-llm-modulo-frameworks.md`
- `wiki/sources/papers/lmdrive-closed-loop-end-to-end-driving-with-large-language-models.md`
- `wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models.md`
- `wiki/sources/papers/machine-super-intelligence.md`
- `wiki/sources/papers/mamba-linear-time-sequence-modeling-with-selective-state-spaces.md`
- `wiki/sources/papers/mistral-7b.md`
- `wiki/sources/papers/mixtral-of-experts.md`
- `wiki/sources/papers/momad-momentum-aware-planning-in-end-to-end-autonomous-driving.md`

### Batch 12 — active
- `wiki/sources/papers/multi-scale-context-aggregation-by-dilated-convolutions.md`
- `wiki/sources/papers/navsim-data-driven-non-reactive-autonomous-vehicle-simulation.md`
- `wiki/sources/papers/navsim-v2-pseudo-simulation-for-autonomous-driving.md`
- `wiki/sources/papers/neural-machine-translation-by-jointly-learning-to-align-and-translate.md`
- `wiki/sources/papers/neural-message-passing-for-quantum-chemistry.md`
- `wiki/sources/papers/neural-turing-machines.md`
- `wiki/sources/papers/nuscenes-a-multimodal-dataset-for-autonomous-driving.md`
- `wiki/sources/papers/occformer-dual-path-transformer-for-vision-based-3d-semantic-occupancy-prediction.md`
- `wiki/sources/papers/occgen-generative-multi-modal-3d-occupancy-prediction-for-autonomous-driving.md`
- `wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models.md`

### Batch 13 — active
- `wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving.md`
- `wiki/sources/papers/octo-an-open-source-generalist-robot-policy.md`
- `wiki/sources/papers/on-the-opportunities-and-risks-of-foundation-models.md`
- `wiki/sources/papers/opendrivevla-towards-end-to-end-autonomous-driving-with-large-vision-language-action-model.md`
- `wiki/sources/papers/openvla-an-open-source-vision-language-action-model.md`
- `wiki/sources/papers/openvla-oft-optimizing-speed-and-success-for-vla-fine-tuning.md`
- `wiki/sources/papers/order-matters-sequence-to-sequence-for-sets.md`
- `wiki/sources/papers/orion-holistic-end-to-end-autonomous-driving-by-vision-language-instructed-action-generation.md`
- `wiki/sources/papers/palm-e-an-embodied-multimodal-language-model.md`
- `wiki/sources/papers/palm-scaling-language-modeling-with-pathways.md`

### Batch 14 — active
- `wiki/sources/papers/para-drive-parallelized-architecture-for-real-time-autonomous-driving.md`
- `wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control.md`
- `wiki/sources/papers/pi05-a-vision-language-action-model-with-open-world-generalization.md`
- `wiki/sources/papers/pi06-a-vla-that-learns-from-experience.md`
- `wiki/sources/papers/planning-oriented-autonomous-driving.md`
- `wiki/sources/papers/pointer-networks.md`
- `wiki/sources/papers/prefix-tuning-optimizing-continuous-prompts-for-generation.md`
- `wiki/sources/papers/qlora-efficient-finetuning-of-quantized-language-models.md`
- `wiki/sources/papers/quantifying-the-rise-and-fall-of-complexity-in-closed-systems-the-coffee-automaton.md`
- `wiki/sources/papers/qwen3-technical-report.md`

### Batch 15 — active
- `wiki/sources/papers/racformer-query-based-radar-camera-fusion-for-3d-object-detection.md`
- `wiki/sources/papers/rdt-1b-a-diffusion-foundation-model-for-bimanual-manipulation.md`
- `wiki/sources/papers/react-synergizing-reasoning-and-acting-in-language-models.md`
- `wiki/sources/papers/reason2drive-towards-interpretable-and-chain-based-reasoning-for-autonomous-driving.md`
- `wiki/sources/papers/recurrent-neural-network-regularization.md`
- `wiki/sources/papers/relational-recurrent-neural-networks.md`
- `wiki/sources/papers/robocat-a-self-improving-generalist-agent-for-robotic-manipulation.md`
- `wiki/sources/papers/roboflamingo-vision-language-foundation-models-as-effective-robot-imitators.md`
- `wiki/sources/papers/robovlms-what-matters-in-building-vision-language-action-models.md`
- `wiki/sources/papers/rt-1-robotics-transformer-for-real-world-control-at-scale.md`

### Batch 16 — active
- `wiki/sources/papers/rt-2-vision-language-action-models-transfer-web-knowledge-to-robotic-control.md`
- `wiki/sources/papers/rt-h-action-hierarchies-using-language.md`
- `wiki/sources/papers/s4-driver-scalable-self-supervised-driving-mllm-with-spatio-temporal-visual-representation.md`
- `wiki/sources/papers/sam-2-segment-anything-in-images-and-videos.md`
- `wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation.md`
- `wiki/sources/papers/scaling-instruction-finetuned-language-models.md`
- `wiki/sources/papers/scaling-laws-for-neural-language-models.md`
- `wiki/sources/papers/segment-anything.md`
- `wiki/sources/papers/self-improving-embodied-foundation-models.md`
- `wiki/sources/papers/selfocc-self-supervised-vision-based-3d-occupancy-prediction.md`

### Batch 17 — active
- `wiki/sources/papers/senna-bridging-large-vision-language-models-and-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/simlingo-vision-only-closed-loop-autonomous-driving-with-language-action-alignment.md`
- `wiki/sources/papers/smolvla-a-vision-language-action-model-for-affordable-robotics.md`
- `wiki/sources/papers/solve-synergy-of-language-vision-and-end-to-end-networks-for-autonomous-driving.md`
- `wiki/sources/papers/sparsedrive-end-to-end-autonomous-driving-via-sparse-scene-representation.md`
- `wiki/sources/papers/sparsedriveV2-end-to-end-autonomous-driving-via-sparse-scene-representation.md`
- `wiki/sources/papers/sparseocc-fully-sparse-3d-occupancy-prediction.md`
- `wiki/sources/papers/sparseocc-rethinking-sparse-latent-representation.md`
- `wiki/sources/papers/spatialvla-exploring-spatial-representations-for-vla-models.md`
- `wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving.md`

### Batch 18 — active
- `wiki/sources/papers/swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md`
- `wiki/sources/papers/talk2car-taking-control-of-your-self-driving-car.md`
- `wiki/sources/papers/talk2drive-towards-personalized-autonomous-driving-with-large-language-models.md`
- `wiki/sources/papers/textual-explanations-for-self-driving-vehicles.md`
- `wiki/sources/papers/the-first-law-of-complexodynamics.md`
- `wiki/sources/papers/the-unreasonable-effectiveness-of-recurrent-neural-networks.md`
- `wiki/sources/papers/think-twice-before-driving-towards-scalable-decoders-for-end-to-end-autonomous-driving.md`
- `wiki/sources/papers/toolformer-language-models-can-teach-themselves-to-use-tools.md`
- `wiki/sources/papers/training-compute-optimal-large-language-models.md`
- `wiki/sources/papers/training-language-models-to-follow-instructions-with-human-feedback.md`

### Batch 19 — active
- `wiki/sources/papers/transfuser-imitation-with-transformer-based-sensor-fusion-for-autonomous-driving.md`
- `wiki/sources/papers/tree-of-thoughts-deliberate-problem-solving-with-large-language-models.md`
- `wiki/sources/papers/understanding-lstm-networks.md`
- `wiki/sources/papers/uniact-universal-actions-for-enhanced-embodied-foundation-models.md`
- `wiki/sources/papers/unisim-learning-interactive-real-world-simulators.md`
- `wiki/sources/papers/unleashing-large-scale-video-generative-pre-training-for-visual-robot-manipulation.md`
- `wiki/sources/papers/vad-vectorized-scene-representation-for-efficient-autonomous-driving.md`
- `wiki/sources/papers/vadv2-end-to-end-vectorized-autonomous-driving-via-probabilistic-planning.md`
- `wiki/sources/papers/variational-lossy-autoencoder.md`
- `wiki/sources/papers/vectornet-encoding-hd-maps-and-agent-dynamics-from-vectorized-representation.md`

### Batch 20 — active
- `wiki/sources/papers/video-prediction-policy-a-generalist-robot-policy-with-predictive-visual-representations.md`
- `wiki/sources/papers/vista-a-generalizable-driving-world-model-with-high-fidelity-and-versatile-controllability.md`
- `wiki/sources/papers/visual-instruction-tuning.md`
- `wiki/sources/papers/vlp-vision-language-planning-for-autonomous-driving.md`
- `wiki/sources/papers/voxposer-composable-3d-value-maps-for-robotic-manipulation-with-language-models.md`
- `wiki/sources/papers/wote-end-to-end-driving-with-online-trajectory-evaluation-via-bev-world-model.md`
- `wiki/sources/papers/yolov10-real-time-end-to-end-object-detection.md`
