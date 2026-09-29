"""
Chapter 3: AI Orchestrator Pattern Implementation.
Demonstrates a Hierarchical Supervisor Orchestrator that plans,
delegates subtasks to specialized workers, and synthesizes results
using Google Gemini and Pydantic v2.
"""

import os
import json
from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field


# --- Pydantic Data Contracts ---

class SubAgentTask(BaseModel):
    """Represents a planned unit of work for a specialized sub-agent."""
    agent_type: Literal["data_retrieval", "calculation", "alert_dispatch"] = Field(
        description="The specialized agent domain required for the task"
    )
    instruction: str = Field(
        description="Precise prompt or query for the sub-agent"
    )


class OrchestrationPlan(BaseModel):
    """Structured plan emitted by the supervisor orchestrator."""
    reasoning: str = Field(
        description="Reasoning regarding how the user goal is decomposed"
    )
    tasks: List[SubAgentTask] = Field(
        description="Ordered sequence of subtasks to be executed"
    )


# --- Specialized Worker Functions (Simulated Sub-Agents) ---

def run_data_retrieval_agent(query: str) -> str:
    """Specialized worker for telemetry and database queries."""
    data_store = {
        "node_paris_01": "Node: node_paris_01 | Status: ONLINE | CPU: 92% | Mem: 28GB/32GB",
        "node_tokyo_02": "Node: node_tokyo_02 | Status: ONLINE | CPU: 41% | Mem: 12GB/32GB"
    }
    for key, value in data_store.items():
        if key in query.lower():
            return value
    return f"DataRetrievalWorker: No matching record found for '{query}'."


def run_calculation_agent(expression: str) -> str:
    """Specialized worker for mathematical evaluations."""
    try:
        clean_expr = "".join(ch for ch in expression if ch in "0123456789+-*/. ()")
        # pylint: disable=eval-used
        val = eval(clean_expr, {"__builtins__": None}, {})
        return f"CalculationWorker: Computed result = {val}"
    except Exception as exc:
        return f"CalculationWorker Error: {str(exc)}"


def run_alert_dispatch_agent(alert_msg: str) -> str:
    """Specialized worker for operational notifications."""
    return f"AlertDispatchWorker: Alert successfully dispatched -> [{alert_msg}]"


# --- Central Hierarchical Orchestrator ---

class HierarchicalOrchestrator:
    """
    Supervisor Orchestrator that analyzes requests, generates an execution plan,
    dispatches work to modular sub-agents, and aggregates outcomes.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")

    def _call_gemini_json(self, prompt: str) -> str:
        """Invokes Google Gemini requesting structured JSON output."""
        if not self.api_key:
            # Deterministic simulation fallback
            return json.dumps({
                "reasoning": "The user wants to inspect node_paris_01 CPU load and alert if critical.",
                "tasks": [
                    {
                        "agent_type": "data_retrieval",
                        "instruction": "Fetch telemetry metrics for node_paris_01"
                    },
                    {
                        "agent_type": "alert_dispatch",
                        "instruction": "Dispatch critical alert: node_paris_01 CPU exceeds 90%"
                    }
                ]
            })

        from google import genai
        from google.genai import types

        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                response_mime_type="application/json"
            )
        )
        return response.text or "{}"

    def plan(self, user_goal: str) -> OrchestrationPlan:
        """Supervisor decomposes the goal into structured sub-agent tasks."""
        prompt = (
            f"You are a High-Level AI Orchestrator supervising specialized sub-agents.\n"
            f"Available sub-agents:\n"
            f"- 'data_retrieval': Queries node telemetry and infrastructure records.\n"
            f"- 'calculation': Computes arithmetic expressions.\n"
            f"- 'alert_dispatch': Sends notifications to operational teams.\n\n"
            f"Goal: {user_goal}\n\n"
            f"Return a valid JSON object matching this schema:\n"
            f"{{\n"
            f'  "reasoning": "...",\n'
            f'  "tasks": [\n'
            f'    {{"agent_type": "data_retrieval|calculation|alert_dispatch", "instruction": "..."}}\n'
            f'  ]\n'
            f"}}"
        )
        raw_json = self._call_gemini_json(prompt)
        return OrchestrationPlan.model_validate_json(raw_json)

    def execute(self, user_goal: str) -> Dict[str, Any]:
        """Runs the full orchestration pipeline: Plan -> Delegate -> Synthesize."""
        print(f"\n[Orchestrator Initialized] User Goal: {user_goal}")
        print("=" * 65)

        # 1. Planning phase
        orchestration_plan = self.plan(user_goal)
        print(f"\n[Planning Phase] Reasoning: {orchestration_plan.reasoning}")
        print(f"[Planned Tasks] Total: {len(orchestration_plan.tasks)}")

        # 2. Execution phase across sub-agents
        execution_trace = []
        for idx, task in enumerate(orchestration_plan.tasks, 1):
            print(f"\n--- Subtask {idx}: Delegating to '{task.agent_type}' ---")
            print(f"Instruction: {task.instruction}")

            if task.agent_type == "data_retrieval":
                output = run_data_retrieval_agent(task.instruction)
            elif task.agent_type == "calculation":
                output = run_calculation_agent(task.instruction)
            elif task.agent_type == "alert_dispatch":
                output = run_alert_dispatch_agent(task.instruction)
            else:
                output = f"Unknown agent type: {task.agent_type}"

            print(f"Result: {output}")
            execution_trace.append({"task": task.model_dump(), "result": output})

        # 3. Final synthesis
        synthesis = (
            f"Orchestration completed successfully across {len(execution_trace)} workers. "
            f"Tasks executed: {[t['task']['agent_type'] for t in execution_trace]}."
        )

        return {
            "status": "COMPLETED",
            "goal": user_goal,
            "plan": orchestration_plan.model_dump(),
            "trace": execution_trace,
            "summary": synthesis
        }


if __name__ == "__main__":
    orchestrator = HierarchicalOrchestrator()
    sample_goal = "Check telemetry for node_paris_01 and trigger an alert if CPU is critical."
    result = orchestrator.execute(sample_goal)

    print("\n" + "=" * 65)
    print(f"Status: {result['status']}")
    print(f"Final Summary: {result['summary']}")