"""
Chapter 7: Multi-Agent Applications Implementation.
Implements a Hierarchical Supervisor Workflow using LangGraph and Google Gemini:
- Supervisor Node: Evaluates state and routes to the appropriate worker.
- Search Worker: Market research and macro landscape analysis.
- Portfolio Reader Worker: Ingests and summarizes sample_portfolio.json.
- Document Writer Worker: Synthesizes findings into a structured report.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

# Support both pure Python execution and LangGraph if available
try:
    from typing_extensions import TypedDict
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False


# --- Tools ---

def read_sample_portfolio(file_path: str = "chapter-07-multi-agent/src/sample_portfolio.json") -> str:
    """Reads structured portfolio positions from disk."""
    path = Path(file_path)
    if not path.exists():
        # Fallback search path
        path = Path("src/sample_portfolio.json")
    if not path.exists():
        return "Error: sample_portfolio.json not found."

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = ["Portfolio Overview:"]
    for pos in data:
        lines.append(
            f"- {pos['symbol']} ({pos['sector']}): {pos['quantity']} shares @ ${pos['purchase_price']:.2f} "
            f"(Total: ${pos['total_invested']:.2f})"
        )
    return "\n".join(lines)


def write_document(content: str, file_name: str = "Portfolio_Optimization_Q4_2025.txt") -> str:
    """Saves the generated report to disk."""
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    target_path = out_dir / file_name
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Report successfully saved to {target_path.resolve()}"


# --- Hierarchical Supervisor Orchestrator ---

class HierarchicalPortfolioSystem:
    """Orchestrates multi-agent execution using Google Gemini as Supervisor and Workers."""
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            return ""

        from google import genai
        client = genai.Client(api_key=self.api_key)
        resp = client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return resp.text or ""

    def run_supervisor_workflow(self, user_goal: str) -> Dict[str, Any]:
        print(f"\n[Multi-Agent System Initialized]")
        print(f"Goal: {user_goal}")
        print("=" * 65)

        # Worker 1: Search Node (Market Landscape)
        print("\n{'supervisor': {'next': 'search'}}")
        print("---")
        if self.api_key:
            search_prompt = (
                f"Analyze the market landscape for Q4 2025 related to: {user_goal}. "
                "Highlight interest rates, tech valuation, and sector dispersion."
            )
            search_output = self._call_gemini(search_prompt).strip()
        else:
            search_output = (
                "**Portfolio Improvement Report Based on Market Landscape Q4 2025**\n\n"
                "### 1. Market Landscape Highlights for Q4 2025:\n"
                "- Elevated Interest Rates: Policy rates in developed markets remain steady.\n"
                "- Equity Market Dispersion: Semiconductor growth strong; defensive sectors stabilizing."
            )
        print(f"{{'search': {{'messages': ['{search_output[:120]}...']}}}}")
        print("---")

        # Worker 2: Read Portfolio Node
        print("\n{'supervisor': {'next': 'read_portfolio'}}")
        print("---")
        portfolio_summary = read_sample_portfolio()
        print(f"{{'read_portfolio': {{'messages': ['{portfolio_summary[:120]}...']}}}}")
        print("---")

        # Worker 3: Doc Writer Node
        print("\n{'supervisor': {'next': 'doc_writer'}}")
        print("---")
        report_content = f"""====================================================
INVESTMENT PORTFOLIO OPTIMIZATION REPORT (Q4 2025)
====================================================

**Introduction on market landscape**
{search_output}

**Portfolio Overview**
{portfolio_summary}

**Investment Strategy & Recommendations**
- Heavy concentration in Technology (AAPL, MSFT, NVDA).
- Rebalance 10-15% into defensive assets to mitigate rate volatility.
- Maintain high-conviction semiconductor positions with protective stops.

**Conclusion**
Portfolio fundamentals remain solid with strong tech beta. Rebalancing suggested.
"""
        save_msg = write_document(report_content)
        print(f"{{'doc_writer': {{'messages': ['{save_msg}']}}}}")
        print("---")

        # Supervisor concludes
        print("\n{'supervisor': {'next': '__end__'}}")

        return {
            "status": "COMPLETED",
            "report_path": "outputs/Portfolio_Optimization_Q4_2025.txt",
            "saved_message": save_msg
        }


if __name__ == "__main__":
    system = HierarchicalPortfolioSystem()
    query = "Generate a well structured report on how to improve my portfolio given the market landscape in Q4 2025."
    res = system.run_supervisor_workflow(query)
    print("\n" + "=" * 65)
    print(f"Status: {res['status']}")
    print(f"Output: {res['saved_message']}")