"""
Tool interfaces and execution registry for Chapter 2 Baseline Agent.
Provides deterministic external actuators with strict Pydantic validation.
"""

from typing import Any, Callable, Dict
from pydantic import BaseModel, Field


class Tool(BaseModel):
    """Encapsulates tool metadata and its callable executor."""
    name: str
    description: str
    func: Callable[..., str]
    args_schema: type[BaseModel]

    def run(self, **kwargs) -> str:
        """Validates arguments against schema and executes the tool."""
        try:
            validated_args = self.args_schema(**kwargs)
            return self.func(**validated_args.model_dump())
        except Exception as exc:
            return f"ToolExecutionError in {self.name}: {str(exc)}"


# --- Tool Argument Schemas ---

class CalculatorArgs(BaseModel):
    expression: str = Field(
        description="A mathematical expression to evaluate, e.g., '24 * 365 + 12'"
    )


class DatabaseLookupArgs(BaseModel):
    query_key: str = Field(
        description="The target entity key to query from mock persistent storage"
    )


# --- Concrete Tool Implementations ---

def calculate(expression: str) -> str:
    """Safe evaluation of basic mathematical expressions."""
    allowed_chars = set("0123456789+-*/(). %")
    if not set(expression).issubset(allowed_chars):
        return "Error: Invalid characters in arithmetic expression."
    try:
        # pylint: disable=eval-used
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as err:
        return f"Error evaluating expression: {err}"


def query_mock_db(query_key: str) -> str:
    """Simulates querying external structured storage."""
    mock_data: Dict[str, str] = {
        "node_paris_01": "Status: ONLINE | Load: 42% | Memory: 18.4GB/32GB | Uptime: 45d",
        "node_tokyo_02": "Status: WARNING | Load: 89% | Memory: 31.1GB/32GB | Uptime: 12d",
        "cluster_alpha": "Active Nodes: 12 | Total Capacity: 384 cores | Region: eu-west-3"
    }
    key_normalized = query_key.strip().lower()
    return mock_data.get(key_normalized, f"Record '{query_key}' not found in database.")


# --- Tool Registry ---

class ToolRegistry:
    """Registry maintaining active tool instances accessible to the agent."""
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered.")
        return self._tools[name]

    def get_descriptions(self) -> str:
        """Formats tool definitions for injection into system prompts."""
        descriptions = []
        for tool in self._tools.values():
            schema = tool.args_schema.model_json_schema()
            properties = schema.get("properties", {})
            param_details = ", ".join(
                [f"{k}: {v.get('type', 'any')} ({v.get('description', '')})" 
                 for k, v in properties.items()]
            )
            descriptions.append(
                f"- **{tool.name}**: {tool.description} | Parameters: {{{param_details}}}"
            )
        return "\n".join(descriptions)


def get_default_registry() -> ToolRegistry:
    """Factory creating the initial tool environment."""
    registry = ToolRegistry()
    registry.register(Tool(
        name="calculator",
        description="Useful for calculating arithmetic expressions safely.",
        func=calculate,
        args_schema=CalculatorArgs
    ))
    registry.register(Tool(
        name="database_lookup",
        description="Retrieves live node status and metrics from infrastructure database.",
        func=query_mock_db,
        args_schema=DatabaseLookupArgs
    ))
    return registry