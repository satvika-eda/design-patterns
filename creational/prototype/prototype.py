"""
Prototype Pattern
-----------------
Creates new objects by cloning an existing object (the prototype)
instead of building from scratch.

Use case: Agent config cloning — start from a base agent and clone it
into variants with slight tweaks, without rebuilding the full config each time.
"""

import copy
from dataclasses import dataclass, field


# ── Prototype ──────────────────────────────────────────────────────────────────

@dataclass
class AgentConfig:
    name: str
    model: str
    system_prompt: str
    tools: list[str] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 1024

    def clone(self) -> "AgentConfig":
        """Shallow clone — use when nested objects don't need independence."""
        return copy.copy(self)

    def deep_clone(self) -> "AgentConfig":
        """Deep clone — use when nested objects (like tools list) must be independent."""
        return copy.deepcopy(self)

    def __str__(self):
        return (
            f"AgentConfig(name={self.name!r}, model={self.model!r}, "
            f"tools={self.tools}, temp={self.temperature})"
        )


if __name__ == "__main__":
    # Base prototype — expensive to configure in real life (loads tool schemas, validates, etc.)
    base_agent = AgentConfig(
        name="base",
        model="claude-sonnet-4-6",
        system_prompt="You are a helpful AI assistant.",
        tools=["web_search", "calculator"],
        temperature=0.7,
    )

    # Clone and tweak — no rebuilding from scratch
    researcher = base_agent.deep_clone()
    researcher.name = "researcher"
    researcher.system_prompt = "You are a research assistant. Cite all sources."
    researcher.tools.append("fetch_url")
    researcher.temperature = 0.3

    analyst = base_agent.deep_clone()
    analyst.name = "analyst"
    analyst.system_prompt = "You are a data analyst. Be precise and show your work."
    analyst.tools = ["calculator", "code_interpreter"]
    analyst.temperature = 0.0

    print("Base:      ", base_agent)
    print("Researcher:", researcher)
    print("Analyst:   ", analyst)
    print()

    # Prove they're independent — mutating one doesn't affect the others
    print("Base tools still intact:", base_agent.tools)
