"""
Baseline ReAct Agent implementation for Chapter 2.
Orchestrates prompt decomposition, tool execution loops, and stop criteria
using the Google Gemini API with GOOGLE_API_KEY.
"""

import os
import re
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from tools import ToolRegistry, get_default_registry


class AgentStep(BaseModel):
    """Tracks intermediate deliberation and environmental feedback."""
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None


class BaselineAgent:
    """
    Autonomous Baseline Agent executing the ReAct (Reason + Act) loop.
    Integrates directly with Google Gemini models.
    """
    def __init__(
        self,
        registry: ToolRegistry,
        model_name: str = "gemini-2.5-flash",
        max_iterations: int = 5
    ):
        self.registry = registry
        self.model_name = model_name
        self.max_iterations = max_iterations
        self.system_prompt_template = (
            "You are an autonomous AI Agent designed to solve tasks step by step.\n"
            "You have access to the following tools:\n\n"
            "{tool_descriptions}\n\n"
            "Use the following strict execution format:\n"
            "Thought: Your reasoning about the current situation and what to do next.\n"
            "Action: The name of the tool to use (must be one of [{tool_names}]).\n"
            "Action Input: A valid JSON object containing tool arguments matching the schema.\n"
            "Observation: [This will be provided by the environment]\n\n"
            "When you have enough information to answer the user request, finish with:\n"
            "Thought: I now have the final answer.\n"
            "Final Answer: The complete answer to the original user query.\n"
        )

    def _call_llm(self, prompt: str) -> str:
        """
        Dispatches call to Google Gemini API using GOOGLE_API_KEY.
        Falls back to deterministic simulation if no key is found.
        """
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            # Deterministic simulation for local testing without active API credits
            if "node_paris_01" in prompt and "Action: database_lookup" not in prompt:
                return (
                    "Thought: I need to query the database to obtain status for node_paris_01.\n"
                    "Action: database_lookup\n"
                    "Action Input: {\"query_key\": \"node_paris_01\"}"
                )
            if "Status: ONLINE" in prompt:
                return (
                    "Thought: The node data is retrieved. I can now provide the final answer.\n"
                    "Final Answer: Node node_paris_01 is ONLINE with a load of 42% and 18.4GB memory used."
                )
            return "Final Answer: No active GOOGLE_API_KEY detected. Fallback executed."

        # Production call to Google GenAI SDK
        from google import genai  # pylint: disable=import-outside-toplevel
        from google.genai import types  # pylint: disable=import-outside-toplevel

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,
                stop_sequences=["\nObservation:"]
            )
        )
        return response.text or ""

    def run(self, user_goal: str) -> Dict[str, Any]:
        """Executes the autonomous deliberation and action cycle."""
        tool_names = ", ".join(self.registry._tools.keys())
        system_prompt = self.system_prompt_template.format(
            tool_descriptions=self.registry.get_descriptions(),
            tool_names=tool_names
        )

        scratchpad = f"{system_prompt}\nUser Goal: {user_goal}\n"
        steps: List[AgentStep] = []

        print(f"\n[Agent Initialized] Goal: {user_goal}")
        print("=" * 60)

        for iteration in range(1, self.max_iterations + 1):
            print(f"\n--- Iteration {iteration}/{self.max_iterations} ---")
            llm_output = self._call_llm(scratchpad)
            print(llm_output)

            # Check for termination condition
            if "Final Answer:" in llm_output:
                final_answer = llm_output.split("Final Answer:")[-1].strip()
                return {
                    "status": "COMPLETED",
                    "final_answer": final_answer,
                    "iterations": iteration,
                    "trajectory": steps
                }

            # Parse Thought, Action, and Action Input
            thought_match = re.search(r"Thought:(.*?)(?=Action:|$)", llm_output, re.DOTALL)
            action_match = re.search(r"Action:\s*([^\n]+)", llm_output)
            input_match = re.search(r"Action Input:\s*(\{.*?\})", llm_output, re.DOTALL)

            thought = thought_match.group(1).strip() if thought_match else "Deliberating..."
            action = action_match.group(1).strip() if action_match else None

            if not action or not input_match:
                observation = "Format Error: Provide both 'Action:' and valid JSON 'Action Input:'."
                scratchpad += f"{llm_output}\nObservation: {observation}\n"
                steps.append(AgentStep(thought=thought, observation=observation))
                continue

            raw_input = input_match.group(1).strip()
            try:
                action_args = json.loads(raw_input)
            except json.JSONDecodeError:
                observation = f"Invalid JSON payload: {raw_input}"
                scratchpad += f"{llm_output}\nObservation: {observation}\n"
                continue

            # Execute tool from registry
            try:
                tool = self.registry.get(action)
                observation = tool.run(**action_args)
            except Exception as err:
                observation = f"Execution Failure: {str(err)}"

            print(f"Observation: {observation}")

            # Record execution history and update scratchpad state
            steps.append(AgentStep(
                thought=thought,
                action=action,
                action_input=action_args,
                observation=observation
            ))
            scratchpad += f"{llm_output}\nObservation: {observation}\n"

        return {
            "status": "MAX_ITERATIONS_EXCEEDED",
            "final_answer": "Agent reached iteration ceiling before completing goal.",
            "iterations": self.max_iterations,
            "trajectory": steps
        }


if __name__ == "__main__":
    registry = get_default_registry()
    agent = BaselineAgent(registry=registry)

    # Test execution
    result = agent.run("Check the health status of node_paris_01 and summarize it.")
    print("\n" + "=" * 60)
    print(f"Status: {result['status']}")
    print(f"Final Outcome: {result['final_answer']}")