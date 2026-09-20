"""Business tool definitions for Agentic RAG invocation."""

from typing import Any, Callable, Dict


class ToolRegistry:
    """Registry of typed business tools accessible to LangGraph agents."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, fn: Callable):
        self._tools[name] = fn

    def get(self, name: str) -> Callable:
        return self._tools.get(name)
