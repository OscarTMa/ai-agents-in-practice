# AI Agents in Practice: From Cognitive Foundations to Next-Gen Protocols

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-brightgreen.svg)](https://www.python.org/)
[![Engine: Google Gemini](https://img.shields.io/badge/Engine-Google%20Gemini%202.5%20Flash-orange.svg)](https://ai.google.dev/)
[![Schemas: Pydantic v2](https://img.shields.io/badge/Contracts-Pydantic%20v2-red.svg)](https://docs.pydantic.dev/)
[![Platform: Linux Ubuntu](https://img.shields.io/badge/Runtime-Linux%20Ubuntu-informational.svg)](https://ubuntu.com/)

A practical, code-first technical repository covering the entire agentic architecture lifecycle: from cognitive inference foundations and ReAct loops to distributed multi-agent systems, open interoperability protocols (MCP, A2A, ACP), and production-grade ethical guardrail pipelines.

<div align="center">
  <img src=".assets/Capture d'écran 2026-09-29 205506.png" alt="ai-agents-in-practice" width="340"/>
  <p><em>AI Agents in Practice: Design, implement, and scale autonomous AI systems for production. Valentina Alto (Packt Publishing).</em></p>
</div>

---

## 🏗️ Repository Architecture & Navigation

The repository follows a modular, code-first directory structure. Every chapter features its own theoretical design, validated Pydantic v2 schemas, and runtime execution logs executed in a Linux Ubuntu environment (`llm-node`):

```text
ai-agents-in-practice/
├── README.md                                  # Repository overview and master blueprint (this file)
├── chapter-01-foundations/                    # Foundations: LLM Inference & Static Retrieval
│   ├── README.md
│   └── src/
├── chapter-02-rise-of-agents/                 # The ReAct Loop & Core Agent Anatomy
│   ├── README.md
│   └── src/
├── chapter-03-orchestrators/                  # Orchestrators: Abstraction, Workflows & Hierarchies
│   ├── README.md
│   └── src/orchestrator.py
├── chapter-04-memory/                         # Memory Taxonomy: STM, Semantic Cache & Episodic LTM
│   ├── README.md
│   └── src/memory_agent.py
├── chapter-05-tools/                          # Tool Integrations: Sync, Async (I/O) & Agentic RAG
│   ├── README.md
│   └── src/tool_integration_agent.py
├── chapter-06-langchain-agent/                # End-to-End E-Commerce Agent (AskMamma)
│   ├── README.md
│   └── src/ask_mamma_agent.py
├── chapter-07-multi-agent/                    # Multi-Agent Systems & Graph Routing (LangGraph)
│   ├── README.md
│   └── src/portfolio_supervisor.py
├── chapter-08-protocols/                      # Next-Gen Protocols: MCP, A2A & ACP
│   ├── README.md
│   └── src/agent_protocols.py
└── chapter-09-ethics-guardrails/              # Safety: PII Redaction, Injection Filters, HITL & Audit
    ├── README.md
    └── src/guardrail_pipeline.py
```

---

## 🧠 End-to-End System Blueprint

Across the chapters, the architecture transitions from simple monolithic API calls to a multi-tiered distributed ecosystem:

```mermaid
graph TD
    subgraph Ingress_and_Agentic_Web [Ingress & Agentic Web Plane]
        User[User / Client Event] --> IngressShield[Ingress Guardrail: PII & Injection Defense]
        IngressShield --> AgentCore[Core Agent Brain: Gemini 2.5 Flash]
    end

    subgraph Reasoning_and_Memory [Reasoning & State Management Plane]
        AgentCore <--> STM[Short-Term Memory / Rolling Window]
        AgentCore <--> SemCache[Semantic In-Memory Cache]
        AgentCore <--> LTM[Episodic & Semantic Vector Store]
        AgentCore --> Supervisor[Supervisor / Orchestration Engine]
    end

    subgraph Execution_and_Protocols [Execution & Protocol Interoperability Plane]
        Supervisor -->|JSON-RPC 2.0| MCP[MCP Server: APIs, SQL DBs, Tools]
        Supervisor -->|Agent Card P2P| A2A[A2A Protocol: Federated Peer Agents]
        Supervisor -->|Smart Contract Escrow| ACP[ACP Commerce: Settlement & AI Oracle]
    end

    subgraph Governance_and_Egress [Governance & Egress Enforcement Plane]
        Supervisor --> PolicyGate{Policy & Value Threshold Check}
        PolicyGate -->|High Stakes / Value > $500| HITL[Human-in-the-Loop Escalation]
        PolicyGate -->|Autonomous Safe Lane| TargetExec[Production System Execution]
        HITL -->|Approved| TargetExec
        TargetExec --> AuditTrail[(Immutable Audit Ledger: EU AI Act)]
    end
```

---

## 📚 Curriculum Breakdown & Implementations

### 1. Foundations of Agentic AI (`chapter-01-foundations`)
* **Core Concept:** Moving from deterministic generation to agentic deliberation.
* **Deliverable:** Baseline inference configurations, prompt grounding, and static retrieval pipelines.

### 2. The Rise of AI Agents (`chapter-02-rise-of-agents`)
* **Core Concept:** The foundational **Thought $\rightarrow$ Action $\rightarrow$ Observation** (ReAct) cycle.
* **Deliverable:** Single-agent ReAct loop capable of iterative tool selection, execution, and intermediate reflection.

### 3. The Need for an AI Orchestrator (`chapter-03-orchestrators`)
* **Core Concept:** Overcoming brittle hardcoded `if...else` logic through abstraction, modularity, and runtime autonomy.
* **Deliverable:** A supervisor orchestrator that decomposes user goals into structured sub-tasks and delegates execution across specialized worker modules (`data_retrieval`, `alert_dispatch`).

### 4. Memory and Context Management (`chapter-04-memory`)
* **Core Concept:** Cognitive architectures (CoALA framework) applied to AI: Short-Term, Semantic, Episodic, and Procedural memory.
* **Deliverable:** A multi-tier memory system featuring rolling context condensation, zero-token **semantic caching in memory**, and vector similarity retrieval over past interaction episodes.

```mermaid
graph LR
    UserQuery[User Query] --> CacheCheck{Semantic Cache Hit?}
    CacheCheck -->|HIT: Cosine >= 0.88| ReturnCached[Instant Response: 0 Token Cost]
    CacheCheck -->|MISS| QueryEpisodic[Retrieve Past Episodes from LTM]
    QueryEpisodic --> BuildContext[Build Augmented Prompt: STM + LTM]
    BuildContext --> Inference[LLM Inference]
    Inference --> UpdateState[Update STM Buffer & Populate Cache]
```

### 5. Tools and External Integrations (`chapter-05-tools`)
* **Core Concept:** Tools as the functional actuators of an agent.
* **Deliverable:** Synchronous Text-to-SQL querying against SQLite, non-blocking asynchronous multi-region metrics polling (`asyncio.gather`), and agentic RAG with intent-driven query reformulation.

### 6. Building Your First AI Agent with LangChain (`chapter-06-langchain-agent`)
* **Core Concept:** Unifying the **Build**, **Run**, and **Manage** (LangSmith) lifecycle.
* **Deliverable:** **AskMamma**, an interactive digital eatery assistant (*Mammachepiada*) orchestrating conversational dialogue, structured SQLite menu queries, RAG over hygiene/compliance documentation, and transactional cart mutations.

### 7. Multi-Agent Applications (`chapter-07-multi-agent`)
* **Core Concept:** Microservice architecture applied to AI agents: loose coupling, horizontal scalability, and fault isolation.
* **Deliverable:** A hierarchical supervisor state graph (LangGraph pattern) coordinating macro research (`search`), portfolio ingestion (`read_portfolio`), and structured document synthesis (`doc_writer`).

```mermaid
sequenceDiagram
    autonumber
    participant Supervisor as Supervisor Router
    participant Search as Search Specialist
    participant Reader as Portfolio Reader
    participant Writer as Document Writer

    Supervisor->>Search: Task: Research Macro Landscape Q4 2025
    Search-->>Supervisor: Macro Report (Interest rates, tech dispersion)
    Supervisor->>Reader: Task: Ingest sample_portfolio.json
    Reader-->>Supervisor: Structured Positions (AAPL, MSFT, NVDA, JPM)
    Supervisor->>Writer: Task: Synthesize Optimization Strategy
    Writer-->>Supervisor: Saved Portfolio_Optimization_Q4_2025.txt
    Supervisor->>Supervisor: Graph Termination (__end__)
```

### 8. Blueprint for Next-Gen Agent Protocols (`chapter-08-protocols`)
* **Core Concept:** The transition toward an open **Agentic Web** via standard communication, discovery, and value-exchange protocols.
* **Deliverable:** 
  * **Model Context Protocol (MCP - Anthropic):** Client-server architecture communicating over JSON-RPC 2.0.
  * **Agent2Agent Protocol (A2A - Google):** Peer-to-peer delegation, structured task routing, and discovery via `agent-card.json`.
  * **Agent Commerce Protocol (ACP - Virtuals):** Trustless escrow smart contracts, cryptographic wallet identities, and AI oracle verification.

```mermaid
graph LR
    subgraph MCP_Scope [Model Context Protocol]
        AgentCore[Agent] <-->|JSON-RPC 2.0| ToolsDB[Local Tools, APIs & File Resources]
    end

    subgraph A2A_Scope [Agent2Agent Protocol]
        AgentCore <-->|P2P Task Cards| ExternalAgent[Specialist External Agent Networks]
    end

    subgraph ACP_Scope [Agent Commerce Protocol]
        AgentCore <-->|Smart Contract Escrow| CryptoLedger[Economic Settlement with AI Oracle]
    end
```

### 9. Navigating Ethical Challenges in Real-World AI (`chapter-09-ethics-guardrails`)
* **Core Concept:** Operationalizing Responsible AI, bias auditing, prompt injection mitigation, and EU AI Act compliance.
* **Deliverable:** A layered guardrail pipeline featuring PII masking (emails, credit cards), adversarial prompt injection rejection, **Human-in-the-Loop** escalation on transactions exceeding policy limits (> $500), and immutable audit logging.

```mermaid
graph LR
    Input[User Input] --> Ingress[Ingress Filter]
    Ingress -->|Sanitized| Core[Agent Brain]
    Ingress -->|Prompt Injection / Jailbreak| Block[Immediate Safe Refusal]
    
    Core --> Proposal[Proposed Financial Action]
    Proposal --> PolicyCheck{Transaction > $500?}
    
    PolicyCheck -->|Yes: Exceeds Bound| Escalation[Escalate to Human-in-the-Loop]
    PolicyCheck -->|No: Safe Lane| AutoExec[Autonomous Execution]
    
    Escalation -->|Approved| AutoExec
    Escalation -->|Rejected| Rollback[Abort & Alert]
    
    AutoExec --> Audit[(Immutable Audit Trail)]
```

---

## 🛠️ Technology Stack

| Layer | Technology | Primary Functionality |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Unified agent runtime and script execution |
| **Inference Engine** | Google Gemini (`gemini-2.5-flash`) | Context reasoning, structured planning, and generation |
| **SDK** | `google-genai` | Native, typed client interface for Google models |
| **Data Contracts** | Pydantic v2 | Input validation, schema enforcement, and JSON-RPC framing |
| **Graph Runtime** | LangGraph / StateGraph | Cyclic state machines and dynamic conditional edges |
| **Storage Engines** | SQLite (in-memory & persistent) | Structured catalog relational data and audit forensics |
| **Vector Search** | Dense Embeddings & Cosine Metrics | Low-latency semantic caching and episodic retrieval |
| **Protocol Standards** | MCP (JSON-RPC 2.0), A2A, ACP | Tool binding, agent federation, and value settlement |

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone git@github.com:OscarTMa/ai-agents-in-practice.git
cd ai-agents-in-practice
```

### 2. Environment Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY="your-google-gemini-api-key"
```

### 4. Execute Verified Chapter Modules
```bash
# Chapter 3: Hierarchical Supervisor Orchestrator
python3 chapter-03-orchestrators/src/orchestrator.py

# Chapter 4: Cognitive Memory Agent (STM, Semantic Cache, Episodic LTM)
python3 chapter-04-memory/src/memory_agent.py

# Chapter 5: Tool Integration Agent (Sync SQL, Async Batch I/O, Agentic RAG)
python3 chapter-05-tools/src/tool_integration_agent.py

# Chapter 6: End-to-End E-Commerce Assistant (AskMamma)
python3 chapter-06-langchain-agent/src/ask_mamma_agent.py

# Chapter 7: Multi-Agent Investment Portfolio Supervisor
python3 chapter-07-multi-agent/src/portfolio_supervisor.py

# Chapter 8: Protocol Suite (MCP JSON-RPC, A2A Agent Card, ACP Escrow)
python3 chapter-08-protocols/src/agent_protocols.py

# Chapter 9: Ethical Guardrail Pipeline & Human-in-the-Loop Gateway
python3 chapter-09-ethics-guardrails/src/guardrail_pipeline.py
```

---

## 📜 License

Distributed under the **MIT** License. See `LICENSE` for details.
