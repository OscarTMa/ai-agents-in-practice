"""
Chapter 5: Tools and External Integrations Implementation.
Demonstrates:
1. Synchronous deterministic tools (SQLite text-to-query).
2. Asynchronous concurrent tools (simulated regional network I/O with asyncio.gather).
3. Agentic RAG vector search tool with query reformulation.
4. Tool orchestration using Google Gemini and Pydantic v2 schemas.
"""

import os
import json
import sqlite3
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel, Field


# --- Tool Argument Contracts (Pydantic v2) ---

class SQLQueryInput(BaseModel):
    """Input contract for the SQL database tool."""
    query: str = Field(description="Deterministic SQL SELECT query to execute.")


class AsyncBatchLookupInput(BaseModel):
    """Input contract for the asynchronous multi-region metrics tool."""
    regions: List[str] = Field(description="List of regional nodes to poll concurrently.")


class AgenticRAGInput(BaseModel):
    """Input contract for the semantic vector search tool."""
    refined_query: str = Field(description="Scientifically/technically refined search query.")
    category: str = Field(default="general", description="Filter metadata category.")


# --- Tool Implementations ---

class InfrastructureDB:
    """Synchronous Tool: Local in-memory SQLite database representing structured enterprise data."""
    def __init__(self):
        self.conn = sqlite3.connect(":memory:")
        self._setup()

    def _setup(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE node_inventory (
                node_id TEXT PRIMARY KEY,
                region TEXT,
                status TEXT,
                cpu_load INTEGER,
                memory_gb REAL
            )
            """
        )
        cursor.executemany(
            "INSERT INTO node_inventory VALUES (?, ?, ?, ?, ?)",
            [
                ("node_paris_01", "eu-west", "ONLINE", 92, 28.5),
                ("node_frankfurt_02", "eu-central", "ONLINE", 45, 14.0),
                ("node_tokyo_01", "ap-northeast", "OFFLINE", 0, 0.0),
                ("node_ashburn_03", "us-east", "ONLINE", 78, 22.0),
            ]
        )
        self.conn.commit()

    def execute_query(self, query: str) -> str:
        """Executes a safe read-only SQL query."""
        if not query.strip().upper().startswith("SELECT"):
            return "SecurityGuardrailError: Only SELECT queries are permitted."
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return json.dumps(rows)
        except Exception as exc:
            return f"SQLExecutionError: {str(exc)}"


class AsyncRegionalPoller:
    """Asynchronous Tool: Simulates high-latency concurrent I/O across regions."""
    @staticmethod
    async def fetch_regional_health(region: str) -> Dict[str, Any]:
        await asyncio.sleep(0.5)  # Simulated network latency
        return {
            "region": region,
            "latency_ms": 42 if "eu" in region else 165,
            "link_status": "OPTIMAL"
        }

    @classmethod
    async def fetch_all_regions(cls, regions: List[str]) -> List[Dict[str, Any]]:
        tasks = [cls.fetch_regional_health(reg) for reg in regions]
        return await asyncio.gather(*tasks)


class AgenticVectorStore:
    """Agentic RAG Tool: Simulates knowledge base retrieval over clinical/technical docs."""
    DOCUMENT_BASE = [
        {
            "category": "incident_playbook",
            "title": "Mitigating High CPU Spikes on Paris Core Nodes",
            "snippet": "Node node_paris_01 runs midnight batch indexing. If CPU exceeds 90%, throttle indexing jobs before restarting services."
        },
        {
            "category": "sla_guidelines",
            "title": "Regional Uptime Constraints",
            "snippet": "European nodes operate under 99.99% SLA requirements with automated failover to Frankfurt."
        }
    ]

    @classmethod
    def semantic_search(cls, refined_query: str, category: str = "general") -> str:
        results = [
            doc["snippet"] for doc in cls.DOCUMENT_BASE
            if category == "general" or doc["category"] == category
        ]
        return "\n---\n".join(results) if results else "No matching documentation found."


# --- Central Tool Integration Agent ---

class ToolIntegrationAgent:
    """Orchestrates structured SQL, asynchronous batch lookups, and agentic RAG retrieval."""
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.db = InfrastructureDB()

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            # Deterministic simulation output
            return json.dumps({
                "plan": "Execute SQL lookup for critical node status, then poll latency asynchronously.",
                "sql_action": "SELECT node_id, status, cpu_load FROM node_inventory WHERE cpu_load > 90",
                "regions_to_poll": ["eu-west", "eu-central", "us-east"],
                "rag_query": "Mitigating High CPU Spikes on Paris Core Nodes"
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

    async def run_pipeline(self, user_goal: str) -> Dict[str, Any]:
        print(f"\n[Tool Agent Initialized] Goal: '{user_goal}'")
        print("=" * 65)

        # 1. Deliberation Phase
        prompt = (
            f"You are an AI Tool Integration Agent. Given the goal: '{user_goal}', "
            f"formulate the required tool parameters as JSON with keys:\n"
            f"- 'sql_action': A SELECT query for node_inventory (columns: node_id, region, status, cpu_load, memory_gb).\n"
            f"- 'regions_to_poll': List of regions to query concurrently.\n"
            f"- 'rag_query': Documentation search topic."
        )
        plan_raw = self._call_gemini(prompt)
        plan = json.loads(plan_raw)

        # 2. Synchronous Tool: SQL Text-to-Query
        sql_input = SQLQueryInput(query=plan["sql_action"])
        print(f"\n[Sync Tool: SQL Text-to-Query] Executing: {sql_input.query}")
        db_result = self.db.execute_query(sql_input.query)
        print(f"Result: {db_result}")

        # 3. Asynchronous Tool: Concurrent Regional Health Check
        regions_input = AsyncBatchLookupInput(regions=plan["regions_to_poll"])
        print(f"\n[Async Tool: Parallel Network Polling] Concurrently polling {regions_input.regions} via asyncio.gather...")
        async_results = await AsyncRegionalPoller.fetch_all_regions(regions_input.regions)
        print(f"Result: {async_results}")

        # 4. Agentic RAG Tool: Knowledge Base Lookup
        rag_input = AgenticRAGInput(refined_query=plan["rag_query"], category="incident_playbook")
        print(f"\n[Agentic RAG Tool: Knowledge Base] Refined Query: '{rag_input.refined_query}'")
        kb_result = AgenticVectorStore.semantic_search(rag_input.refined_query, rag_input.category)
        print(f"Result: {kb_result}")

        print("\n" + "=" * 65)
        print("Status: COMPLETED")
        return {
            "status": "COMPLETED",
            "db_metrics": db_result,
            "network_telemetry": async_results,
            "playbook_guidance": kb_result
        }


if __name__ == "__main__":
    agent = ToolIntegrationAgent()
    sample_request = "Audit overloaded nodes above 90% CPU, check their network link health, and retrieve the recovery playbook."
    asyncio.run(agent.run_pipeline(sample_request))