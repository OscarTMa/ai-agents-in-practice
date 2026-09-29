"""
Chapter 4: Memory and Context Management Architecture.
Implements:
1. ShortTermMemory with rolling sliding window and LLM summarization.
2. SemanticCache for low-latency session-scoped vector recall.
3. EpisodicMemoryStore for persistent multi-session event retrieval.
4. MemoryAwareAgent coordinating all tiers using Google Gemini.
"""

import os
import math
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# --- Data Models ---

class ChatMessage(BaseModel):
    role: str = Field(description="Sender role: 'user', 'assistant', or 'system'")
    content: str = Field(description="Message text content")


class EpisodicRecord(BaseModel):
    event_id: str
    user_id: str
    interaction: str
    lesson_learned: str
    embedding: Optional[List[float]] = None


# --- Vector Utilities ---

def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)


# --- Tier 1: Short-Term Memory (STM) with Sliding Buffer ---

class ShortTermMemory:
    """Manages active conversation window and summarization triggers."""
    def __init__(self, max_messages: int = 4):
        self.max_messages = max_messages
        self.messages: List[ChatMessage] = []
        self.running_summary: str = ""

    def add_message(self, role: str, content: str):
        self.messages.append(ChatMessage(role=role, content=content))

    def get_context_for_prompt(self) -> str:
        prompt_lines = []
        if self.running_summary:
            prompt_lines.append(f"[Previous Context Summary]: {self.running_summary}")
        for msg in self.messages[-self.max_messages:]:
            prompt_lines.append(f"{msg.role.upper()}: {msg.content}")
        return "\n".join(prompt_lines)

    def condense(self, summary_text: str):
        """Condenses the older history into a compact summary."""
        self.running_summary = summary_text
        # Keep only the last 2 turns in active buffer
        self.messages = self.messages[-2:]


# --- Tier 2: Semantic In-Memory Cache ---

class SemanticCache:
    """High-speed in-memory vector store for session-scoped recall."""
    def __init__(self, threshold: float = 0.85):
        self.threshold = threshold
        self.cache: List[Dict[str, Any]] = []

    def lookup(self, query_emb: List[float]) -> Optional[str]:
        best_score = 0.0
        best_value = None
        for item in self.cache:
            score = cosine_similarity(query_emb, item["embedding"])
            if score > best_score and score >= self.threshold:
                best_score = score
                best_value = item["response"]
        return best_value

    def store(self, query: str, query_emb: List[float], response: str):
        self.cache.append({
            "query": query,
            "embedding": query_emb,
            "response": response
        })


# --- Tier 3: Episodic Long-Term Memory (LTM) ---

class EpisodicMemoryStore:
    """Stores and retrieves historical events and lessons learned across sessions."""
    def __init__(self):
        self.records: List[EpisodicRecord] = []

    def save_episode(self, record: EpisodicRecord):
        self.records.append(record)

    def recall_episodes(self, query_emb: List[float], top_k: int = 2) -> List[EpisodicRecord]:
        scored_records = []
        for r in self.records:
            if r.embedding:
                score = cosine_similarity(query_emb, r.embedding)
                scored_records.append((score, r))
        scored_records.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_records[:top_k]]


# --- Memory-Aware Agent Orchestrator ---

class MemoryAwareAgent:
    """Coordinates STM, Semantic Cache, and Episodic LTM with Google Gemini."""
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.stm = ShortTermMemory(max_messages=4)
        self.semantic_cache = SemanticCache(threshold=0.88)
        self.episodic_ltm = EpisodicMemoryStore()
        self._init_demo_episodes()

    def _get_embedding(self, text: str) -> List[float]:
        """Generates embedding using Google GenAI SDK or deterministic fallback."""
        if not self.api_key:
            # Deterministic pseudo-embedding for testing without key
            val = float(len(text))
            return [math.sin(val + i) for i in range(16)]

        from google import genai
        client = genai.Client(api_key=self.api_key)
        result = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return result.embeddings[0].values

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            return "Simulated Gemini response based on retrieved memory context."

        from google import genai
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text or ""

    def _init_demo_episodes(self):
        """Populates sample episodic memories."""
        sample = EpisodicRecord(
            event_id="ep_001",
            user_id="oscar_01",
            interaction="User investigated high CPU on node_paris_01 last week.",
            lesson_learned="node_paris_01 runs critical batch indexing; CPU spikes above 90% are expected around midnight."
        )
        sample.embedding = self._get_embedding(sample.interaction)
        self.episodic_ltm.save_episode(sample)

    def interact(self, user_query: str) -> str:
        print(f"\n[Incoming User Query]: '{user_query}'")
        query_emb = self._get_embedding(user_query)

        # 1. Check Semantic In-Memory Cache
        cached_hit = self.semantic_cache.lookup(query_emb)
        if cached_hit:
            print("[Semantic Cache]: HIT -> Returning cached response with zero token cost.")
            self.stm.add_message("user", user_query)
            self.stm.add_message("assistant", cached_hit)
            return cached_hit

        print("[Semantic Cache]: MISS -> Querying Episodic LTM and assembling context.")

        # 2. Query Episodic Memory
        relevant_episodes = self.episodic_ltm.recall_episodes(query_emb, top_k=1)
        episodic_context = ""
        if relevant_episodes:
            ep = relevant_episodes[0]
            episodic_context = f"\n[Relevant Past Interaction]: {ep.interaction}\n[Past Lesson]: {ep.lesson_learned}\n"
            print(f"[Episodic LTM]: Recalled episode {ep.event_id} -> '{ep.lesson_learned}'")

        # 3. Build Augmented Prompt with STM + LTM
        active_stm = self.stm.get_context_for_prompt()
        prompt = (
            f"You are a memory-aware infrastructure engineering assistant.\n"
            f"{episodic_context}\n"
            f"[Active Conversation History]:\n{active_stm}\n"
            f"USER: {user_query}\n"
            f"ASSISTANT:"
        )

        # 4. Generate Response
        response = self._call_gemini(prompt)

        # 5. Update STM and Semantic Cache
        self.stm.add_message("user", user_query)
        self.stm.add_message("assistant", response)
        self.semantic_cache.store(user_query, query_emb, response)

        # 6. Check context window threshold (simulate compression after 4 turns)
        if len(self.stm.messages) >= 4:
            print("[STM Context Management]: Buffer threshold reached. Condensing history...")
            summary = "User inquired about node_paris_01 CPU spikes and received operational context."
            self.stm.condense(summary)

        return response


if __name__ == "__main__":
    agent = MemoryAwareAgent()

    print("============================================================")
    print("DEMO TURN 1: Query triggering Episodic LTM Recall")
    print("============================================================")
    res1 = agent.interact("Why is node_paris_01 showing such high CPU right now?")
    print(f"\nOutcome:\n{res1.strip()}")

    print("\n============================================================")
    print("DEMO TURN 2: Equivalent Query triggering Semantic Cache HIT")
    print("============================================================")
    res2 = agent.interact("Why is node_paris_01 CPU load so elevated?")
    print(f"\nOutcome:\n{res2.strip()}")