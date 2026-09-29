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
(ai-agents-in-practice) oscar@llm-node:~/AI-Agents/ai-agents-in-practice$ python chapter-07-multi-agent/src/portfolio_supervisor.py

[Multi-Agent System Initialized]
Goal: Generate a well structured report on how to improve my portfolio given the market landscape in Q4 2025.
=================================================================

{'supervisor': {'next': 'search'}}
---
{'search': {'messages': ['**Portfolio Improvement Report Based on Market Landscape Q4 2025**\n\n### 1. Market Landscape Highlights for Q4 2025:\n- El...']}}
---

{'supervisor': {'next': 'read_portfolio'}}
---
{'read_portfolio': {'messages': ['Portfolio Overview:\n- AAPL (Technology): 13 shares @ $172.50 (Total: $2242.50)\n- MSFT (Technology): 8 shares @ $415.00 (...']}}
---

{'supervisor': {'next': 'doc_writer'}}
---
{'doc_writer': {'messages': ['Report successfully saved to /home/oscar/AI-Agents/ai-agents-in-practice/outputs/Portfolio_Optimization_Q4_2025.txt']}}
---

{'supervisor': {'next': '__end__'}}

=================================================================
Status: COMPLETED
Output: Report successfully saved to /home/oscar/AI-Agents/ai-agents-in-practice/outputs/Portfolio_Optimization_Q4_2025.txt
```

---

## 🔍 Trajectory Breakdown

| Step | Node / Actor | State Transition | Operational Feedback |
| :--- | :--- | :--- | :--- |
| **1** | `supervisor` | Evaluates prompt $\rightarrow$ Routes to `search` | Supervisor detects the need for macro market context and dispatches to the market research agent. |
| **2** | `search` | Gathers trends $\rightarrow$ Reports to `supervisor` | Returns Q4 2025 macro highlights: interest rate climate and tech equity dispersion. |
| **3** | `supervisor` | Evaluates state $\rightarrow$ Routes to `read_portfolio` | Supervisor notices lack of portfolio breakdown and routes to the portfolio reader agent. |
| **4** | `read_portfolio` | Reads JSON $\rightarrow$ Reports to `supervisor` | Parses `sample_portfolio.json` extracting positions in AAPL, MSFT, JPM, NVDA. |
| **5** | `supervisor` | Evaluates state $\rightarrow$ Routes to `doc_writer` | All context gathered; supervisor dispatches synthesis and document generation. |
| **6** | `doc_writer` | Saves report $\rightarrow$ Reports to `supervisor` | Synthesizes insights and writes `Portfolio_Optimization_Q4_2025.txt` to the `outputs/` folder. |
| **7** | `supervisor` | Evaluates state $\rightarrow$ Terminates (`__end__`) | All subtasks complete; supervisor exits graph loop with `Status: COMPLETED`. |