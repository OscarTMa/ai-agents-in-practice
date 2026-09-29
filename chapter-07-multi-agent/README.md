# Chapter 7: Multi-Agent Applications

> **Status:** Completed & Validated  
> **Source Target:** `chapter-07-multi-agent/src/portfolio_supervisor.py`  
> **Engine:** Google Gemini (`gemini-2.5-flash` via `google-genai` SDK)

---

## 📌 Overview & Learning Objectives

Single-agent systems reach scalability and reasoning ceilings when tasks demand multiple orthogonal skillsets, conflicting operational objectives, or complex division of labor. Multi-Agent Systems (MAS) solve this by applying microservice architecture principles to AI: decomposing large goals into autonomous, decoupled, specialized agents that communicate via structured protocols.

By completing this module, you will understand:
1. **Agents as Tools:** Treating subordinate agents as callable tools from the perspective of higher-level orchestrators via natural language contracts.
2. **Microservice Parallels:** Why modular agent design mirrors cloud-native software architecture (independent scaling, fault isolation, polyglot runtimes, and single-responsibility boundaries).
3. **Multi-Agent Interaction Topologies:**
   - **Network (Mesh):** Decentralized peer-to-peer collaboration without central bottlenecks.
   - **Reflection:** Critic-evaluator feedback loops for self-correction.
   - **Sequential:** Deterministic pipelines with strict ordered handoffs.
   - **Hierarchical:** Supervisor nodes delegating subtasks and aggregating worker outcomes.
   - **Hybrid:** Composite topologies combining pipelines with supervisory subnetworks.
4. **State of the Multi-Agent Framework Ecosystem:** Comparing AutoGen (conversational group chats), TaskWeaver (code-first DataFrame state execution), OpenAI Agents SDK (native hand-offs and guardrails), and LangGraph (state machine graphs).
5. **Hands-On LangGraph Orchestration:** Building a financial investment portfolio optimization team with dynamic routing, persistent shared state, and document generation.

---

## 🧠 Architectural Concepts & Theoretical Deep Dive

### 1. Multi-Agent Topologies

```text
1. NETWORK (Mesh)            2. REFLECTION                   3. SEQUENTIAL
   [Agent A] <─> [Agent B]      [Writer Agent] ──(Draft)──>     [Agent A] ──> [Agent B] ──> [Agent C]
       ▲             ▲                 ▲              │
       └───> [Agent C] <─┘             └───(Critique)─[Critic]

4. HIERARCHICAL (Supervisor)
               ┌───────────────────────────────┐
               │          Supervisor           │
               └───────────────┬───────────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
         [Worker A]       [Worker B]     [Worker C]
```

---

### 2. Microservice Architecture Mapping

| Microservice Characteristic | Multi-Agent Equivalent | Architectural Benefit |
| :--- | :--- | :--- |
| **Single Responsibility** | Specialized Agent (e.g., `search_agent`) | Minimizes prompt clutter and avoids model capability dilution. |
| **Loose Coupling** | Schema-driven message passing (`State`) | Upgrading or replacing an agent does not break dependencies. |
| **Horizontal Scaling** | Containerized worker replication | High-latency tasks (e.g., web scraping) can scale independently. |
| **Observability** | Per-agent run tracing (`LangSmith`) | Debugging targets specific agent trajectories instead of monolithic prompts. |

---

### 3. Investment Portfolio Supervisor Pattern

```text
                                  ┌─────────────────────────────┐
                                  │      User Prompt State      │
                                  └──────────────┬──────────────┘
                                                 │
                                                 ▼
                                  ┌─────────────────────────────┐
                                  │      Team Supervisor        │
                                  │   LLM Router Node (Gemini)  │
                                  └──────────────┬──────────────┘
                                                 │
                  ┌──────────────────────────────┼──────────────────────────────┐
                  │ (Route: search)              │ (Route: read_portfolio)      │ (Route: doc_writer)
                  ▼                              ▼                              ▼
   ┌─────────────────────────────┐┌─────────────────────────────┐┌─────────────────────────────┐
   │        Search Agent         ││     Read Portfolio Agent    ││      Doc Writer Agent       │
   │  • Market Trends Analysis   ││  • Reads JSON Portfolios    ││  • Synthesizes Insights     │
   │  • Macro Economic Context   ││  • Quantities & Exposures   ││  • Exports .txt Report      │
   └──────────────┬──────────────┘└──────────────┬──────────────┘└──────────────┬──────────────┘
                  │                              │                              │
                  └──────────────────────────────┴──────────────────────────────┘
                                                 │
                                           (Always Report)
                                                 ▼
                                  ┌─────────────────────────────┐
                                  │     Supervisor Review       │
                                  │  Decides NEXT or __END__    │
                                  └─────────────────────────────┘
```

---

## 📂 Source Code Structure

```text
chapter-07-multi-agent/
├── README.md                      # Architecture documentation and runtime traces (this file)
└── src/
    ├── __init__.py                # Package exports
    ├── sample_portfolio.json      # Structured equity position data
    └── portfolio_supervisor.py    # Hierarchical multi-agent implementation
```

---

## 🚀 Execution & Verification

### 1. Environment Activation
```bash
cd ~/AI-Agents/ai-agents-in-practice
source .venv/bin/activate
```

### 2. Run the Multi-Agent Application
```bash
export GOOGLE_API_KEY="your-api-key"
python chapter-07-multi-agent/src/portfolio_supervisor.py
```

---

## 📊 Execution Log & Runtime Trajectory

Below is the verified multi-agent supervisor trace obtained running on `llm-node`:

```text
(ai-agents-in-practice) oscar@