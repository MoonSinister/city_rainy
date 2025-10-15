# LLMArena 基准测试

## 概述

近年来，大型语言模型（LLMs）的进步揭示了其实现具有人类级别智能的自主智能体的潜力。然而，现有的用于评估LLM智能体的基准测试要么使用静态数据集（可能导致数据泄露），要么仅关注单智能体场景，忽视了多智能体交互的复杂性。目前缺乏一个能够在多智能体动态环境中评估LLM智能体多样化能力的基准测试。

为此，我们推出了LLMArena，这是一个新颖且易于扩展的框架，用于在多智能体动态环境中评估LLM的多样化能力。LLMArena包含七个不同的游戏环境，采用Trueskill评分系统来评估LLM智能体的关键能力，包括：

- **空间推理**：理解和导航空间关系的能力
- **战略规划**：制定和执行长期策略的能力
- **数值推理**：处理和理解数值信息的能力
- **风险评估**：识别和评估潜在风险的能力
- **沟通能力**：与其他智能体有效交流的能力
- **对手建模**：理解和预测对手行为的能力
- **团队协作**：与其他智能体协同工作的能力

## 研究发现

我们对不同规模和类型的LLM进行了广泛的实验和人类评估，结果表明LLM在发展成为完全自主的智能体方面仍有很长的路要走，特别是在对手建模和团队协作方面。

## 研究意义

我们希望LLMArena能够引导未来的研究朝着增强LLM这些能力的方向发展，最终在动态的多智能体环境中实现更复杂和实用的应用。

---

## LLMArena Benchmark

### Overview

Recent advancements in large language models (LLMs) have revealed their potential for achieving autonomous agents possessing human-level intelligence. However, existing benchmarks for evaluating LLM Agents either use static datasets, potentially leading to data leakage or focus only on single-agent scenarios, overlooking the complexities of multi-agent interactions. There is a lack of a benchmark that evaluates the diverse capabilities of LLM agents in multi-agent, dynamic environments.

To this end, we introduce LLMArena, a novel and easily extensible framework for evaluating the diverse capabilities of LLM in multi-agent dynamic environments. LLMArena encompasses seven distinct gaming environments, employing Trueskill scoring to assess crucial abilities in LLM agents, including:

- **Spatial reasoning**: Ability to understand and navigate spatial relationships
- **Strategic planning**: Ability to develop and execute long-term strategies
- **Numerical reasoning**: Ability to process and understand numerical information
- **Risk assessment**: Ability to identify and evaluate potential risks
- **Communication**: Ability to effectively communicate with other agents
- **Opponent modeling**: Ability to understand and predict opponent behavior
- **Team collaboration**: Ability to work cooperatively with other agents

### Research Findings

We conduct an extensive experiment and human evaluation among different sizes and types of LLMs, showing that LLMs still have a significant journey ahead in their development towards becoming fully autonomous agents, especially in opponent modeling and team collaboration.

### Research Significance

We hope LLMArena could guide future research towards enhancing these capabilities in LLMs, ultimately leading to more sophisticated and practical applications in dynamic, multi-agent settings.
