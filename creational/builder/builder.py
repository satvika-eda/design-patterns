"""
Builder Pattern
---------------
Separates the construction of a complex object from its representation,
letting you build it step by step.

Use case: LLM request builder — a request can have many optional parts
(system prompt, tools, temperature, stop sequences, etc.).
Builder avoids a constructor with 10 parameters.
"""

from dataclasses import dataclass, field


# ── Product ────────────────────────────────────────────────────────────────────

@dataclass
class LLMRequest:
    model: str
    user_message: str
    system_prompt: str | None = None
    temperature: float = 1.0
    max_tokens: int = 1024
    tools: list[dict] = field(default_factory=list)
    stop_sequences: list[str] = field(default_factory=list)

    def __str__(self):
        lines = [
            f"model:        {self.model}",
            f"user:         {self.user_message}",
            f"system:       {self.system_prompt or '(none)'}",
            f"temperature:  {self.temperature}",
            f"max_tokens:   {self.max_tokens}",
            f"tools:        {[t['name'] for t in self.tools] or '(none)'}",
            f"stop_seqs:    {self.stop_sequences or '(none)'}",
        ]
        return "\n".join(lines)


# ── Builder ────────────────────────────────────────────────────────────────────

class LLMRequestBuilder:
    def __init__(self, model: str, user_message: str):
        self._model = model
        self._user_message = user_message
        self._system_prompt = None
        self._temperature = 1.0
        self._max_tokens = 1024
        self._tools = []
        self._stop_sequences = []

    def system(self, prompt: str) -> "LLMRequestBuilder":
        self._system_prompt = prompt
        return self

    def temperature(self, value: float) -> "LLMRequestBuilder":
        if not 0.0 <= value <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        self._temperature = value
        return self

    def max_tokens(self, value: int) -> "LLMRequestBuilder":
        self._max_tokens = value
        return self

    def tool(self, name: str, description: str, input_schema: dict) -> "LLMRequestBuilder":
        self._tools.append({
            "name": name,
            "description": description,
            "input_schema": input_schema,
        })
        return self

    def stop_on(self, *sequences: str) -> "LLMRequestBuilder":
        self._stop_sequences.extend(sequences)
        return self

    def build(self) -> LLMRequest:
        return LLMRequest(
            model=self._model,
            user_message=self._user_message,
            system_prompt=self._system_prompt,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            tools=self._tools,
            stop_sequences=self._stop_sequences,
        )


if __name__ == "__main__":
    # Simple request
    simple = (
        LLMRequestBuilder("claude-sonnet-4-6", "What is the capital of France?")
        .temperature(0.0)
        .max_tokens(256)
        .build()
    )
    print("=== Simple request ===")
    print(simple)
    print()

    # Complex agentic request
    agentic = (
        LLMRequestBuilder("claude-sonnet-4-6", "Search the web and summarize recent AI news.")
        .system("You are a research assistant. Be concise and cite sources.")
        .temperature(0.3)
        .max_tokens(2048)
        .tool(
            name="web_search",
            description="Search the web for information",
            input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
        )
        .tool(
            name="fetch_url",
            description="Fetch the content of a URL",
            input_schema={"type": "object", "properties": {"url": {"type": "string"}}},
        )
        .stop_on("</answer>", "[DONE]")
        .build()
    )
    print("=== Agentic request ===")
    print(agentic)
