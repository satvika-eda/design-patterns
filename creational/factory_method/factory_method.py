"""
Factory Method Pattern
----------------------
Defines an interface for creating an object, but lets subclasses decide which
class to instantiate. The creator doesn't need to know the concrete class.

Use case: LLM client factory — your pipeline asks for "a language model"
without caring whether it's Claude, OpenAI, or Gemini underneath.
"""

from abc import ABC, abstractmethod


# ── Product interface ──────────────────────────────────────────────────────────

class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass

    @abstractmethod
    def model_name(self) -> str:
        pass


# ── Concrete products ──────────────────────────────────────────────────────────

class ClaudeClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return f"[Claude] response to: '{prompt}'"

    def model_name(self) -> str:
        return "claude-sonnet-4-6"


class OpenAIClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return f"[OpenAI] response to: '{prompt}'"

    def model_name(self) -> str:
        return "gpt-4o"


class GeminiClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return f"[Gemini] response to: '{prompt}'"

    def model_name(self) -> str:
        return "gemini-2.0-flash"


# ── Creator interface ──────────────────────────────────────────────────────────

class LLMProvider(ABC):
    @abstractmethod
    def create_client(self) -> LLMClient:
        """The factory method — subclasses decide what to instantiate."""
        pass

    def run_prompt(self, prompt: str) -> str:
        """Uses the factory method — doesn't know which client it gets."""
        client = self.create_client()
        print(f"Using model: {client.model_name()}")
        return client.complete(prompt)


# ── Concrete creators ──────────────────────────────────────────────────────────

class AnthropicProvider(LLMProvider):
    def create_client(self) -> LLMClient:
        return ClaudeClient()


class OpenAIProvider(LLMProvider):
    def create_client(self) -> LLMClient:
        return OpenAIClient()


class GeminiProvider(LLMProvider):
    def create_client(self) -> LLMClient:
        return GeminiClient()


# ── Simple factory function (bonus) ───────────────────────────────────────────

def get_provider(name: str) -> LLMProvider:
    providers = {
        "anthropic": AnthropicProvider,
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
    }
    if name not in providers:
        raise ValueError(f"Unknown provider: {name}. Choose from {list(providers)}")
    return providers[name]()


if __name__ == "__main__":
    for name in ["anthropic", "openai", "gemini"]:
        provider = get_provider(name)
        result = provider.run_prompt("Summarize this document.")
        print(result)
        print()
