# 📚 Analyzed Papers / 分析论文

[English](#english) | [中文](#chinese)

---

<a name="english"></a>

## 📖 English Version

This directory contains three carefully selected papers that form a **complete technical evolution chain** in Vision-Language-Action (VLA) models for robotic manipulation.

### 📄 Paper Selection Rationale

These papers were chosen based on:
- ✅ **Recency**: Published in 2025-2026 (within 3-5 year requirement)
- ✅ **Quality**: Top-tier venues (AAAI Best Paper) and arXiv preprints
- ✅ **Relevance**: All address VLA for manipulation
- ✅ **Complementarity**: Each tackles a different aspect (language, space, vision)
- ✅ **Impact**: Collectively represent state-of-the-art progress

---

## 📑 Paper Summaries

### 1️⃣ RSS: Residual Semantic Steering (arXiv 2026)

**File**: [`RSS_Stable_Language_Guidance_2026.pdf`](./RSS_Stable_Language_Guidance_2026.pdf)

**Full Title**: *Stable Language Guidance for Vision-Language-Action Models*

**Authors**: Zhan et al.

**Key Contribution**: Addresses **modality collapse** where visual priors overwhelm linguistic signals

**Core Innovation**:
- **Monte Carlo Syntactic Integration (MCSI)**: LLM-driven distributional expansion
- **Residual Affordance Steering (RAS)**: Dual-stream decoding isolating language influence

**Results**: 82.2% success on LIBERO M8 (corrupted instructions)

**Gap**: ❌ Does not address visual attention mechanisms or temporal modeling

---

### 2️⃣ SpatialVLA (arXiv 2025)

**File**: [`SpatialVLA_2025.pdf`](./SpatialVLA_2025.pdf)

**Full Title**: *SpatialVLA: Exploring Spatial Representations for Visual-Language-Action Model*

**Authors**: Qu, Song, Chen et al.

**Key Contribution**: Claims **spatial understanding is the keypoint** in robot manipulation

**Core Innovation**:
- **Ego3D Position Encoding**: Injects 3D spatial information
- **Adaptive Action Grids**: Dynamic spatial discretization

**Training**: 1.1M real-world episodes from OXE + RH20T

**Results**: 71.9% on SimplerEnv visual matching, 88.2% on spatial reasoning

**Gap**: ❌ Lacks temporal modeling, doesn't improve long-horizon performance

---

### 3️⃣ ⭐ ReconVLA (AAAI 2026 Best Paper)

**File**: [`ReconVLA_AAAI2026.pdf`](./ReconVLA_AAAI2026.pdf)

**Full Title**: *ReconVLA: Reconstructive Vision-Language-Action Model as Effective Robot Perceiver*

**Authors**: Song, Zhou, Zhao et al.

**Venue**: AAAI 2026 🏆 **Best Paper Award**

**Key Contribution**: First **implicit grounding** via gaze region reconstruction

**Core Innovation**:
- Diffusion transformer reconstructs target manipulation area
- Simulates human eye "gaze" mechanism
- End-to-end, no external models required

**Results**:
- 64.1% on CALVIN 5-task chains
- 95.6% on single tasks
- **31.5% degradation** from 1→5 tasks

**Critical Gap We Identified** ⚠️:
- ❌ **Frame-independent reconstruction** → no temporal coherence
- ❌ **Attention jumps** in sequential tasks
- ❌ This is the main focus of our TGM proposal

---

## 📊 Comparative Analysis

| Dimension | RSS | SpatialVLA | ReconVLA | **Our TGM** |
|-----------|-----|------------|----------|-------------|
| Language Robustness | ✓✓ | ✓ | ✓ | ✓ |
| Spatial Understanding | ✗ | ✓✓ | ✓ | ✓ |
| Visual Grounding | ✗ | ✓ | ✓✓ | ✓✓ |
| **Temporal Consistency** | ✗ | ✗ | ✗ | **✓✓** |

### Evolution Chain

```
RSS (Language) → SpatialVLA (Space) → ReconVLA (Vision) → TGM (Temporal) ← Our Work
```

---

## 🔍 Key Insights

1. **Convergence on Implicit Methods**: All recent works move from explicit (bounding boxes) to implicit representations

2. **Performance Paradox**: ReconVLA achieves 95.6% on single tasks but only 64.1% on 5-task chains

3. **Missing Dimension**: None address temporal attention stability across frames

---

## 📖 Reading Guide

**Quick Overview (30 min)**:
1. ReconVLA Abstract + Figure 1
2. SpatialVLA Section 3 (Architecture)
3. RSS Table 1 (Results)

**Deep Dive (2-3 hours)**:
1. ReconVLA Section 4.3 (Ablation) + Figure 4 (Attention)
2. SpatialVLA Section 3.2 (Ego3D Encoding)
3. RSS Section 3.1 (MCSI Algorithm)

---

<a name="chinese"></a>

## 📖 中文版本

本目录包含三篇精心挑选的论文，形成了机器人操作VLA模型的**完整技术演进链**。

### 📄 选择依据

- ✅ **时效性**: 2025-2026年发表（符合3-5年要求）
- ✅ **质量**: 顶级会议（AAAI最佳论文）和arXiv
- ✅ **相关性**: 均针对VLA操作任务
- ✅ **互补性**: 各自解决不同方面（语言、空间、视觉）
- ✅ **影响力**: 代表最先进进展

---

## 📑 论文摘要

### 1️⃣ RSS: 残差语义引导（arXiv 2026）

**文件**: [`RSS_Stable_Language_Guidance_2026.pdf`](./RSS_Stable_Language_Guidance_2026.pdf)

**标题**: *VLA模型的稳定语言引导*

**作者**: Zhan等

**核心贡献**: 解决**模态坍缩**（视觉先验压倒语言信号）

**核心创新**:
- **蒙特卡洛句法集成**: LLM驱动的分布式扩展
- **残差能供性引导**: 隔离语言影响的双流解码

**结果**: LIBERO M8上82.2%成功率

**缺陷**: ❌ 未关注视觉注意力或时序建模

---

### 2️⃣ SpatialVLA（arXiv 2025）

**文件**: [`SpatialVLA_2025.pdf`](./SpatialVLA_2025.pdf)

**标题**: *探索VLA模型的空间表示*

**作者**: Qu, Song, Chen等

**核心贡献**: 声称**空间理解是关键**

**核心创新**:
- **Ego3D位置编码**: 注入3D空间信息
- **自适应动作网格**: 动态空间离散化

**训练**: OXE + RH20T的110万真实片段

**结果**: SimplerEnv 71.9%，空间推理88.2%

**缺陷**: ❌ 缺乏时序建模，未改善长时序性能

---

### 3️⃣ ⭐ ReconVLA（AAAI 2026最佳论文）

**文件**: [`ReconVLA_AAAI2026.pdf`](./ReconVLA_AAAI2026.pdf)

**标题**: *重建式VLA模型作为有效机器人感知器*

**作者**: Song, Zhou, Zhao等

**会议**: AAAI 2026 🏆 **最佳论文奖**

**核心贡献**: 首个通过gaze区域重建的**隐式定位**方法

**核心创新**:
- 扩散transformer重建目标操作区域
- 模拟人眼"gaze"机制
- 端到端，无需外部模型

**结果**:
- CALVIN 5任务链64.1%
- 单任务95.6%
- 1→5任务**下降31.5%**

**我们识别的关键缺陷** ⚠️:
- ❌ **逐帧独立重建** → 无时序连贯性
- ❌ 顺序任务中**注意力跳变**
- ❌ 这是我们TGM提案的主要关注点

---

## 📊 对比分析

| 维度 | RSS | SpatialVLA | ReconVLA | **我们的TGM** |
|------|-----|------------|----------|--------------|
| 语言鲁棒性 | ✓✓ | ✓ | ✓ | ✓ |
| 空间理解 | ✗ | ✓✓ | ✓ | ✓ |
| 视觉定位 | ✗ | ✓ | ✓✓ | ✓✓ |
| **时序一致性** | ✗ | ✗ | ✗ | **✓✓** |

### 演进链

```
RSS(语言) → SpatialVLA(空间) → ReconVLA(视觉) → TGM(时序) ← 我们的工作
```

---

## 🔍 关键洞察

1. **向隐式方法收敛**: 所有最新工作都从显式（边界框）转向隐式表示

2. **性能悖论**: ReconVLA单任务95.6%但5任务链仅64.1%

3. **缺失维度**: 无方法关注跨帧时序注意力稳定性

---

## 📖 阅读指南

**快速概览（30分钟）**:
1. ReconVLA摘要 + 图1
2. SpatialVLA第3节（架构）
3. RSS表1（结果）

**深入研读（2-3小时）**:
1. ReconVLA第4.3节（消融）+ 图4（注意力）
2. SpatialVLA第3.2节（Ego3D编码）
3. RSS第3.1节（MCSI算法）

---

## 📚 Citation / 引用

```bibtex
@article{zhan2026stable,
  title={Stable Language Guidance for Vision-Language-Action Models},
  author={Zhan, Zhihao and others},
  journal={arXiv preprint arXiv:2601.04052},
  year={2026}
}

@article{qu2025spatialvla,
  title={SpatialVLA: Exploring Spatial Representations for VLA Model},
  author={Qu, Delin and Song, Haoming and others},
  journal={arXiv preprint arXiv:2501.15830},
  year={2025}
}

@inproceedings{song2026reconvla,
  title={ReconVLA: Reconstructive VLA Model as Effective Robot Perceiver},
  author={Song, Wenxuan and Zhou, Ziyang and others},
  booktitle={AAAI},
  note={Best Paper Award},
  year={2026}
}
```
