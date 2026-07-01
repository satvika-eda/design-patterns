"""
Abstract Factory Pattern
------------------------
Provides an interface for creating families of related objects without
specifying their concrete classes.

Use case: AI provider suite — when you pick a provider, you get a whole
family of compatible components (LLM, embedder, tokenizer) that work together.

The problem with Factory Method: it creates ONE product.
Abstract Factory creates a FAMILY of related products.
"""

from abc import ABC, abstractmethod


# ── Product interfaces ─────────────────────────────────────────────────────────

class LLM(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass

class Embedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass

class Tokenizer(ABC):
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass


# ── Anthropic family ───────────────────────────────────────────────────────────

class ClaudeLLM(LLM):
    def complete(self, prompt: str) -> str:
        return f"[Claude] {prompt}"

class CohereEmbedder(Embedder):  # Anthropic doesn't have embeddings, teams often pair with Cohere
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]  # placeholder

class AnthropicTokenizer(Tokenizer):
    def count_tokens(self, text: str) -> int:
        return len(text.split())  # placeholder


# ── OpenAI family ──────────────────────────────────────────────────────────────

class GPT4oLLM(LLM):
    def complete(self, prompt: str) -> str:
        return f"[GPT-4o] {prompt}"

class OpenAIEmbedder(Embedder):
    def embed(self, text: str) -> list[float]:
        return [0.4, 0.5, 0.6]  # placeholder

class OpenAITokenizer(Tokenizer):
    def count_tokens(self, text: str) -> int:
        return len(text.split())  # placeholder


# ── Abstract Factory ───────────────────────────────────────────────────────────

class AIProviderFactory(ABC):
    @abstractmethod
    def create_llm(self) -> LLM:
        pass

    @abstractmethod
    def create_embedder(self) -> Embedder:
        pass

    @abstractmethod
    def create_tokenizer(self) -> Tokenizer:
        pass


# ── Concrete factories ─────────────────────────────────────────────────────────

class AnthropicFactory(AIProviderFactory):
    def create_llm(self) -> LLM:
        return ClaudeLLM()

    def create_embedder(self) -> Embedder:
        return CohereEmbedder()

    def create_tokenizer(self) -> Tokenizer:
        return AnthropicTokenizer()


class OpenAIFactory(AIProviderFactory):
    def create_llm(self) -> LLM:
        return GPT4oLLM()

    def create_embedder(self) -> Embedder:
        return OpenAIEmbedder()

    def create_tokenizer(self) -> Tokenizer:
        return OpenAITokenizer()


# ── Client code ────────────────────────────────────────────────────────────────

class RAGPipeline:
    """Uses a factory to build its components — never touches concrete classes."""

    def __init__(self, factory: AIProviderFactory):
        self.llm = factory.create_llm()
        self.embedder = factory.create_embedder()
        self.tokenizer = factory.create_tokenizer()

    def run(self, query: str) -> str:
        tokens = self.tokenizer.count_tokens(query)
        embedding = self.embedder.embed(query)
        response = self.llm.complete(query)
        return f"Tokens: {tokens} | Embedding dims: {len(embedding)} | Response: {response}"


def get_factory(provider: str) -> AIProviderFactory:
    factories = {
        "anthropic": AnthropicFactory,
        "openai": OpenAIFactory,
    }
    if provider not in factories:
        raise ValueError(f"Unknown provider: {provider}")
    return factories[provider]()


if __name__ == "__main__":
    for provider in ["anthropic", "openai"]:
        print(f"--- {provider.upper()} ---")
        pipeline = RAGPipeline(get_factory(provider))
        print(pipeline.run("What is retrieval augmented generation?"))
        print()
