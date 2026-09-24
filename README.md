# AI Agents in Practice: Design, Implement, and Scale Autonomous AI Systems
> ⚠️ **Under Construction**: This repository is actively being developed. Theory synthesis, architectural patterns, and code implementations are added as chapters progress.

[![Status](https://img.shields.io/badge/Status-Under%20Construction-yellow.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain%20%2F%20LangGraph-orange)](https://github.com/langchain-ai)
[![Packt Publishing](https://img.shields.io/badge/Publisher-Packt-red)](https://www.packtpub.com/)

Engineering repository and technical knowledge base based on *AI Agents in Practice: Design, implement, and scale autonomous AI systems for production* by Valentina Alto (Packt Publishing).

This repository contains synthesized architectural theory, conceptual breakdowns, execution patterns, and production-grade implementations of autonomous, goal-oriented agentic workflows.

---

## 🏗️ Repository Architecture

```text
ai-agents-in-practice/
├── README.md                                  # Repository overview, architecture & roadmap
├── requirements.txt                           # Project dependencies and environment specs
├── pyproject.toml                             # Packaging and tool configurations
├── docs/
│   ├── glossary.md                            # Comprehensive glossary of agentic AI terminology
│   └── architecture_patterns.md               # Common design patterns (ReAct, Plan-and-Solve, Multi-Agent)
│
├── part-1-foundations/
│   ├── chapter-01-evolution-genai/
│   │   ├── README.md                          # Theory: Foundation models, PEFT, RLMs, and limits of LLMs
│   │   └── notes.md                           # Extended reading notes and academic citations
│   └── chapter-02-rise-of-agents/
│       ├── README.md                          # Theory: Anatomy of an Agent (Brain, Tools, Memory, Planning)
│       └── src/                               # Baseline agent primitives and tool interfaces
│
├── part-2-agentic-frameworks-and-patterns/
│   ├── chapter-03-langchain-langgraph/
│   │   ├── README.md
│   │   └── src/                               # StateGraph workflows, cyclical execution, persistence
│   ├── chapter-04-autogen-crewai/
│   │   ├── README.md
│   │   └── src/                               # Multi-agent role-playing, conversational orchestration
│   └── chapter-05-reasoning-planning/
│       ├── README.md
│       └── src/                               # Self-reflection, ReAct, tree-of-thoughts implementations
│
├── part-3-production-and-scaling/
│   ├── chapter-06-memory-systems/
│   │   ├── README.md
│   │   └── src/                               # Episodic, semantic, and working memory implementations
│   ├── chapter-07-tool-calling-mcp/
│   │   ├── README.md
│   │   └── src/                               # Model Context Protocol (MCP) integrations & API calling
│   └── chapter-08-evaluation-observability/
│       ├── README.md
│       └── src/                               # Tracing, LangSmith/OpenTelemetry, evaluations & guardrails
│
└── tests/                                     # Unit and integration test suites
```

# 📚 Study Guide & Deep Dives
Part 1: Foundations of AI Workflows and the Rise of AI Agents
Chapter 1: Evolution of GenAI Workflows
Status: Theoretical Foundation (No direct agent build)

Summary: Deep dive into how generative AI evolved from task-specific narrow models to foundation models via transfer learning, emerging capabilities at scale, efficiency methods (PEFT, Knowledge Distillation), the rise of Reasoning Language Models (RLMs), and the structural limits of vanilla LLMs that necessitate agentic orchestration.

Detailed Module Documentation: part-1-foundations/chapter-01-evolution-genai/README.md

## 🔬 Chapter 1 Synthesis: Evolution of GenAI Workflows

       1. Narrow AI vs. Foundation Models
Narrow AI (Pre-2022): Bespoke pipelines with dedicated architectures, custom datasets, and rigid routines for single tasks (e.g., spam classifiers, NER, isolated summarizers). Highly brittle to distribution shift and costly to maintain.

Foundation Models: Massively pre-trained over multimodal, web-scale corpora. Leverages transfer learning to encode general latent representations of syntax, semantics, and world dynamics, allowing zero-shot/few-shot adaptation with minimal compute.

       2. Emergent Capabilities at Scale
Properties not explicitly programmed into smaller architectures that manifest purely through parameter and compute scaling:

In-Context Learning (ICL): Adapting behavior dynamically from prompt demonstrations without backpropagation.

Chain-of-Thought (CoT): Step-by-step intermediate reasoning generation to solve compositional and symbolic problems.

Analogical & Cross-Domain Generalization: Disentangling abstract concepts across disparate disciplines.

       3. Structural Mechanics: Tokenization, Embeddings & Transformers                     

[Raw Text Input]
       │
       ▼
[Tokenization] ──> Discrete subword units (BPE, WordPiece)
       │
       ▼
[Embedding Layer] ──> High-dimensional continuous dense vectors
       │
       ▼
[Transformer Backbone] ──> Multi-Head Self-Attention + Feed-Forward Layers
       │
       ▼
[Logits / Softmax] ──> Next-token probability distribution (Autoregressive decoding)

Inference Modes: Consumed via cloud APIs (stateless HTTP endpoints or token streaming for low perceived latency) or hosted open-weights (e.g., LLaMA, Mistral) on sovereign infrastructure.

       4. Parameter-Efficient Fine-Tuning (PEFT) & Optimization
LoRA (Low-Rank Adaptation): Freezes pre-trained backbone weights and injects trainable rank-decomposition matrices into attention projections, radically lowering VRAM requirements.

Adapters & Prefix/Prompt Tuning: Inserts small auxiliary layers or learnable prefix vectors while preserving foundational parameters intact.

Knowledge Distillation (KD): Compresses high-capacity Teacher models into compact Student models (SLMs) by supervising the student on soft label probability distributions, retaining nuanced latent reasoning.

       5. Reasoning Language Models (RLMs)
Inference-Time Deliberation: Shift from single-pass autoregression to allocating test-time compute for internal multi-step deliberation (private chain-of-thought), exemplified by OpenAI o1/o3 and DeepSeek-R1.

Reinforcement Learning Breakthroughs: DeepSeek demonstrated that pure RL (R1-Zero) followed by cold-start supervised fine-tuning and iterative rejection sampling can match elite reasoning benchmarks without requiring massive human-annotated datasets.

       6. The Bridge to Agents: Overcoming the 4 Bottlenecks of LLMs
While RAG grounded LLMs in non-parametric data and Multimodality expanded their sensory boundaries, classical LLMs remain fundamentally bottlenecked:

Bottleneck in Classical LLMs	Agentic Architecture Solution
Volatile / Limited Memory	Persistent memory stores (Episodic vector memory, semantic state, user profiles)
Passive & Reactive	Goal-directed autonomy, proactive task decomposition, and dynamic replanning
Fragile Multi-Step Execution	State graphs, loop controls, validation checkpoints, and reflection routines
Environment Isolation	Deterministic tool calling, API execution, DB querying, and MCP protocol integration
🛠️ Tech Stack & Prerequisites
Runtime: Python 3.10+

Orchestration Frameworks: LangChain, LangGraph, AutoGen, CrewAI

Data & Persistence: Pydantic v2, ChromaDB, SQLite, PostgreSQL / pgvector

Inference & Models: OpenAI API, Anthropic Claude, DeepSeek API, Ollama / Local Transformers

Observability & Tracing: LangSmith, OpenTelemetry

🚀 Quickstart
1. Clone the Repository
Bash
git clone [https://github.com/](https://github.com/)<your-username>/ai-agents-in-practice.git
cd ai-agents-in-practice
2. Environment Setup

```Bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. Environment Variables
Create a .env file in the project root:

```Bash
Ini, TOML
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
DEEPSEEK_API_KEY=your_deepseek_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
```

## 📄 License
This repository is licensed under the MIT License.

