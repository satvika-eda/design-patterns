"""
Strategy Pattern
----------------
Defines a family of algorithms, encapsulates each one, and makes them
interchangeable. Lets you swap the algorithm at runtime.

Use case: chunking strategies for RAG — fixed size, sentence-based,
or semantic chunking — swappable without changing the pipeline.
"""

from abc import ABC, abstractmethod


# ── Strategy interface ─────────────────────────────────────────────────────────

class ChunkingStrategy(ABC):
    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        pass


# ── Concrete strategies ────────────────────────────────────────────────────────

class FixedSizeChunking(ChunkingStrategy):
    def __init__(self, size: int = 5):
        self._size = size

    def chunk(self, text: str) -> list[str]:
        words = text.split()
        return [" ".join(words[i:i+self._size]) for i in range(0, len(words), self._size)]


class SentenceChunking(ChunkingStrategy):
    def chunk(self, text: str) -> list[str]:
        return [s.strip() for s in text.split(".") if s.strip()]


class SemanticChunking(ChunkingStrategy):
    """Placeholder — real impl would use embeddings to find semantic breaks."""
    def chunk(self, text: str) -> list[str]:
        mid = len(text) // 2
        return [text[:mid].strip(), text[mid:].strip()]


# ── Context — uses a strategy ──────────────────────────────────────────────────

class DocumentIngester:
    def __init__(self, strategy: ChunkingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ChunkingStrategy) -> None:
        self._strategy = strategy

    def ingest(self, text: str) -> list[str]:
        chunks = self._strategy.chunk(text)
        print(f"[{self._strategy.__class__.__name__}] {len(chunks)} chunks")
        return chunks


if __name__ == "__main__":
    text = "The transformer uses attention. Attention is all you need. Embeddings capture meaning."

    ingester = DocumentIngester(FixedSizeChunking(size=4))
    ingester.ingest(text)

    ingester.set_strategy(SentenceChunking())
    ingester.ingest(text)

    ingester.set_strategy(SemanticChunking())
    ingester.ingest(text)
