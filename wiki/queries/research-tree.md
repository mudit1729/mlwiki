---
title: Research Tree
type: query
status: active
updated: 2026-04-07
tags:
  - map
  - visualization
  - tree
---

# Research Tree

Interactive visual map of the wiki's structure. The tree flows from the **Overview** through five research pillars, each with concept pages, paper collections, and open questions.

<div id="research-tree" style="width:100%; min-height:700px; background:var(--bg-subtle); border-radius:12px; border:1px solid var(--border); overflow:hidden;"></div>

<script>
(function() {
  const treeData = {
    name: "Overview",
    link: "/wiki/overview",
    children: [
      {
        name: "End-to-End Driving",
        link: "/wiki/concepts/end-to-end-architectures",
        color: "#6C8EBF",
        children: [
          { name: "Concept Page", link: "/wiki/concepts/end-to-end-architectures", type: "concept" },
          { name: "Open Questions (9)", link: "/wiki/queries/open-questions-e2e", type: "questions" },
          {
            name: "Key Papers",
            type: "papers",
            children: [
              { name: "UniAD", link: "/wiki/sources/papers/planning-oriented-autonomous-driving" },
              { name: "DriveTransformer", link: "/wiki/sources/papers/drivetransformer-unified-transformer-for-scalable-end-to-end-autonomous-driving" },
              { name: "EMMA", link: "/wiki/sources/papers/emma-end-to-end-multimodal-model-for-autonomous-driving" },
              { name: "DiffusionDrive", link: "/wiki/sources/papers/diffusiondrive-truncated-diffusion-model-for-end-to-end-autonomous-driving" },
              { name: "CarPlanner", link: "/wiki/sources/papers/carplanner-consistent-autoregressive-rl-planner-for-autonomous-driving" },
              { name: "DriveGPT", link: "/wiki/sources/papers/drivegpt-scaling-autoregressive-behavior-models-for-driving" }
            ]
          }
        ]
      },
      {
        name: "Vision-Language-Action",
        link: "/wiki/concepts/vision-language-action",
        color: "#82B366",
        children: [
          { name: "Concept Page", link: "/wiki/concepts/vision-language-action", type: "concept" },
          { name: "Open Questions (10)", link: "/wiki/queries/open-questions-vla", type: "questions" },
          { name: "Paper Queue", link: "/wiki/sources/vla-and-driving", type: "collection" },
          {
            name: "Key Papers",
            type: "papers",
            children: [
              { name: "\u03C00", link: "/wiki/sources/papers/pi0-a-vision-language-action-flow-model-for-general-robot-control" },
              { name: "OpenVLA", link: "/wiki/sources/papers/openvla-an-open-source-vision-language-action-model" },
              { name: "CrossFormer", link: "/wiki/sources/papers/scaling-cross-embodied-learning-one-policy-for-manipulation-navigation-locomotion-and-aviation" },
              { name: "GR00T N1", link: "/wiki/sources/papers/groot-n1-an-open-foundation-model-for-generalist-humanoid-robots" },
              { name: "Gemini Robotics", link: "/wiki/sources/papers/gemini-robotics-bringing-ai-into-the-physical-world" },
              { name: "ECoT", link: "/wiki/sources/papers/ecot-embodied-chain-of-thought-reasoning-for-vision-language-action-models" }
            ]
          }
        ]
      },
      {
        name: "LLM Reasoning",
        link: "/wiki/queries/open-questions-llm-reasoning",
        color: "#D6B656",
        children: [
          { name: "Open Questions (9)", link: "/wiki/queries/open-questions-llm-reasoning", type: "questions" },
          {
            name: "Key Papers",
            type: "papers",
            children: [
              { name: "LLMs Can't Plan", link: "/wiki/sources/papers/llms-cant-plan-but-can-help-planning-in-llm-modulo-frameworks" },
              { name: "DeepSeek-R1", link: "/wiki/sources/papers/deepseek-r1-incentivizing-reasoning-capability-in-llms-via-reinforcement-learning" },
              { name: "Chain-of-Thought", link: "/wiki/sources/papers/chain-of-thought-prompting-elicits-reasoning-in-large-language-models" },
              { name: "Tree of Thoughts", link: "/wiki/sources/papers/tree-of-thoughts-deliberate-problem-solving-with-large-language-models" },
              { name: "DriveLM", link: "/wiki/sources/papers/drivelm-driving-with-graph-visual-question-answering" },
              { name: "Agent-Driver", link: "/wiki/sources/papers/a-language-agent-for-autonomous-driving" }
            ]
          }
        ]
      },
      {
        name: "Foundation Models",
        link: "/wiki/concepts/foundation-models",
        color: "#B85450",
        children: [
          { name: "Concept Page", link: "/wiki/concepts/foundation-models", type: "concept" },
          { name: "Open Questions (10)", link: "/wiki/queries/open-questions-foundation-models", type: "questions" },
          {
            name: "Key Papers",
            type: "papers",
            children: [
              { name: "Transformer", link: "/wiki/sources/papers/attention-is-all-you-need" },
              { name: "CLIP", link: "/wiki/sources/papers/learning-transferable-visual-models-from-natural-language-supervision" },
              { name: "LoRA", link: "/wiki/sources/papers/lora-low-rank-adaptation-of-large-language-models" },
              { name: "Qwen3", link: "/wiki/sources/papers/qwen3-technical-report" },
              { name: "Gemma 3", link: "/wiki/sources/papers/gemma-3-technical-report" },
              { name: "Cosmos", link: "/wiki/sources/papers/cosmos-world-foundation-model-platform-for-physical-ai" }
            ]
          }
        ]
      },
      {
        name: "BEV & 3D Occupancy",
        link: "/wiki/concepts/perception",
        color: "#9673A6",
        children: [
          { name: "Concept Page", link: "/wiki/concepts/perception", type: "concept" },
          { name: "Open Questions (10)", link: "/wiki/queries/open-questions-bev-perception", type: "questions" },
          {
            name: "Key Papers",
            type: "papers",
            children: [
              { name: "BEVFormer", link: "/wiki/sources/papers/bevformer-learning-birds-eye-view-representation-from-multi-camera-images-via-spatiotemporal-transformers" },
              { name: "GaussianFormer", link: "/wiki/sources/papers/gaussianformer-scene-as-gaussians-for-vision-based-3d-semantic-occupancy-prediction" },
              { name: "OccWorld", link: "/wiki/sources/papers/occworld-learning-a-3d-occupancy-world-model-for-autonomous-driving" },
              { name: "OccMamba", link: "/wiki/sources/papers/occmamba-semantic-occupancy-prediction-with-state-space-models" },
              { name: "LSS", link: "/wiki/sources/papers/lift-splat-shoot-encoding-images-from-arbitrary-camera-rigs-by-implicitly-unprojecting-to-3d" },
              { name: "SurroundOcc", link: "/wiki/sources/papers/surroundocc-multi-camera-3d-occupancy-prediction-for-autonomous-driving" }
            ]
          }
        ]
      },
      {
        name: "Research Thesis",
        link: "/wiki/syntheses/research-thesis",
        color: "#808080",
        children: [
          { name: "Cross-cutting: RL Frontier", type: "theme" },
          { name: "Cross-cutting: Scaling Laws", type: "theme" },
          { name: "Cross-cutting: Distillation", type: "theme" },
          { name: "Cross-cutting: Evaluation", type: "theme" },
          { name: "Cross-cutting: Structure vs. Learning", type: "theme" }
        ]
      }
    ]
  };

  const container = document.getElementById('research-tree');
  if (!container) return;

  const width = container.clientWidth || 900;
  const height = Math.max(700, container.clientHeight);

  // Create SVG
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', width);
  svg.setAttribute('height', height);
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  container.appendChild(svg);

  // Flatten tree into positioned nodes
  const nodes = [];
  const links = [];

  const pillarCount = treeData.children.length;
  const rootX = width / 2;
  const rootY = 50;

  // Root node
  nodes.push({ x: rootX, y: rootY, name: treeData.name, link: treeData.link, color: '#4A90D9', radius: 20, level: 0 });

  // Layout pillars in a fan
  treeData.children.forEach((pillar, i) => {
    const angle = (Math.PI * 0.15) + (Math.PI * 0.7 * i / (pillarCount - 1));
    const dist = 200;
    const px = rootX + Math.cos(angle - Math.PI/2) * dist * 1.8;
    const py = rootY + Math.sin(angle - Math.PI/2 + Math.PI) * dist;
    const pillarIdx = nodes.length;

    nodes.push({ x: px, y: py, name: pillar.name, link: pillar.link, color: pillar.color || '#666', radius: 16, level: 1 });
    links.push({ source: 0, target: pillarIdx });

    if (pillar.children) {
      const childCount = pillar.children.length;
      pillar.children.forEach((child, j) => {
        const childIdx = nodes.length;
        const spread = Math.min(120, 200 / childCount);
        const cx = px + (j - (childCount-1)/2) * spread * 0.6;
        const cy = py + 90 + (j % 2) * 25;

        let childColor = pillar.color || '#666';
        let childRadius = 8;
        if (child.type === 'questions') { childColor = '#E6A23C'; childRadius = 10; }
        else if (child.type === 'concept') { childColor = '#67C23A'; childRadius = 10; }
        else if (child.type === 'collection') { childColor = '#909399'; childRadius = 9; }
        else if (child.type === 'theme') { childColor = '#F56C6C'; childRadius = 7; }

        nodes.push({ x: cx, y: cy, name: child.name, link: child.link, color: childColor, radius: childRadius, level: 2 });
        links.push({ source: pillarIdx, target: childIdx });

        if (child.children) {
          child.children.forEach((paper, k) => {
            const paperIdx = nodes.length;
            const papersPerRow = 3;
            const row = Math.floor(k / papersPerRow);
            const col = k % papersPerRow;
            const ppx = cx + (col - 1) * 75;
            const ppy = cy + 55 + row * 35;

            nodes.push({ x: ppx, y: ppy, name: paper.name, link: paper.link, color: pillar.color + '99', radius: 5, level: 3 });
            links.push({ source: childIdx, target: paperIdx });
          });
        }
      });
    }
  });

  // Draw links
  links.forEach(l => {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', nodes[l.source].x);
    line.setAttribute('y1', nodes[l.source].y);
    line.setAttribute('x2', nodes[l.target].x);
    line.setAttribute('y2', nodes[l.target].y);
    line.setAttribute('stroke', 'var(--border)');
    line.setAttribute('stroke-width', nodes[l.target].level <= 1 ? '2' : '1');
    line.setAttribute('opacity', '0.5');
    svg.appendChild(line);
  });

  // Draw nodes
  nodes.forEach(n => {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('transform', `translate(${n.x},${n.y})`);
    if (n.link) g.style.cursor = 'pointer';

    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('r', n.radius);
    circle.setAttribute('fill', n.color);
    circle.setAttribute('stroke', 'var(--bg)');
    circle.setAttribute('stroke-width', '2');
    g.appendChild(circle);

    if (n.level <= 2) {
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('dy', n.radius + 14);
      text.setAttribute('fill', 'var(--text-secondary)');
      text.setAttribute('font-size', n.level === 0 ? '13px' : n.level === 1 ? '11px' : '9px');
      text.setAttribute('font-weight', n.level <= 1 ? '700' : '500');
      text.textContent = n.name;
      g.appendChild(text);
    }

    if (n.link) {
      g.addEventListener('click', () => { window.location.href = n.link; });
      g.addEventListener('mouseenter', () => { circle.setAttribute('r', n.radius + 3); circle.setAttribute('stroke', n.color); });
      g.addEventListener('mouseleave', () => { circle.setAttribute('r', n.radius); circle.setAttribute('stroke', 'var(--bg)'); });
    }

    // Tooltip for level 3
    if (n.level === 3) {
      const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
      title.textContent = n.name;
      g.appendChild(title);
    }

    svg.appendChild(g);
  });

  // Legend
  const legend = [
    { color: '#67C23A', label: 'Concept Page' },
    { color: '#E6A23C', label: 'Open Questions' },
    { color: '#909399', label: 'Paper Collection' },
    { color: '#F56C6C', label: 'Cross-cutting Theme' }
  ];

  legend.forEach((item, i) => {
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('transform', `translate(${20},${height - 80 + i * 18})`);
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('r', 5); c.setAttribute('fill', item.color);
    g.appendChild(c);
    const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    t.setAttribute('x', 12); t.setAttribute('dy', 4); t.setAttribute('fill', 'var(--text-secondary)');
    t.setAttribute('font-size', '10px'); t.textContent = item.label;
    g.appendChild(t);
    svg.appendChild(g);
  });
})();
</script>

## Text tree

```
Wiki Overview
│
├─── End-to-End Driving
│    ├── Concept: end-to-end-architectures
│    ├── Open Questions (9): open-questions-e2e
│    └── Papers: UniAD, DriveTransformer, EMMA, Senna,
│        DiffusionDrive, GoalFlow, CarPlanner, DriveGPT...
│
├─── Vision-Language-Action
│    ├── Concept: vision-language-action
│    ├── Open Questions (10): open-questions-vla
│    ├── Collection: vla-and-driving (90+ papers)
│    └── Papers: pi0, OpenVLA, CrossFormer, GR00T N1,
│        Gemini Robotics, ECoT, Octo, Helix...
│
├─── LLM Reasoning for Autonomy
│    ├── Open Questions (9): open-questions-llm-reasoning
│    └── Papers: LLMs Can't Plan, DeepSeek-R1, CoT,
│        Tree of Thoughts, DriveLM, Agent-Driver...
│
├─── Foundation Models & Cross-Embodiment
│    ├── Concept: foundation-models
│    ├── Open Questions (10): open-questions-foundation-models
│    └── Papers: Transformer, CLIP, LoRA, Scaling Laws,
│        HPT, Qwen3, Gemma 3, Cosmos...
│
├─── BEV Perception & 3D Occupancy
│    ├── Concept: perception
│    ├── Open Questions (10): open-questions-bev-perception
│    └── Papers: BEVFormer, GaussianFormer, OccWorld,
│        OccMamba, LSS, SurroundOcc, BEVNeXt...
│
└─── Research Thesis (synthesis)
     ├── Cross-cutting: RL Frontier
     ├── Cross-cutting: Scaling Laws for Embodied AI
     ├── Cross-cutting: Distillation as Deployment
     ├── Cross-cutting: Evaluation Adequacy
     └── Cross-cutting: Structure vs. Learning
```

## Related

- [[wiki/overview]]
- [[wiki/queries/open-questions]]
- [[wiki/syntheses/research-thesis]]
