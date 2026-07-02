"""
Template Method Pattern
-----------------------
Defines the skeleton of an algorithm in a base class, deferring some
steps to subclasses. Subclasses override specific steps without changing
the overall algorithm structure.

Use case: RAG pipeline variants — the overall flow (load → chunk → embed
→ retrieve → generate) is fixed, but each step can vary by subclass.
"""

from abc import ABC, abstractmethod


# ── Abstract class — defines the template ─────────────────────────────────────

class RAGPipeline(ABC):

    # Template method — fixed algorithm structure
    def run(self, query: str) -> str:
        print(f"\n[Pipeline: {self.__class__.__name__}]")
        chunks = self.chunk(self.load())
        embeddings = self.embed(chunks)
        context = self.retrieve(embeddings, query)
        return self.generate(context, query)

    # Steps subclasses must implement
    @abstractmethod
    def load(self) -> str:
        pass

    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        pass

    @abstractmethod
    def embed(self, chunks: list[str]) -> list[list[float]]:
        pass

    # Steps with defaults subclasses can optionally override
    def retrieve(self, embeddings: list[list[float]], query: str) -> str:
        print(f"  [Retrieve] top-2 chunks from {len(embeddings)} embeddings")
        return "retrieved context"

    def generate(self, context: str, query: str) -> str:
        print(f"  [Generate] answering: '{query[:40]}'")
        return f"Answer based on: {context}"


# ── Concrete pipelines ─────────────────────────────────────────────────────────

class SimpleRAGPipeline(RAGPipeline):
    def load(self) -> str:
        print("  [Load] loading plain text file")
        return "The transformer uses self-attention. RAG combines retrieval with generation."

    def chunk(self, text: str) -> list[str]:
        chunks = text.split(". ")
        print(f"  [Chunk] {len(chunks)} sentence chunks")
        return chunks

    def embed(self, chunks: list[str]) -> list[list[float]]:
        print(f"  [Embed] embedding {len(chunks)} chunks with simple embedder")
        return [[float(i)] for i in range(len(chunks))]


class HybridRAGPipeline(RAGPipeline):
    def load(self) -> str:
        print("  [Load] loading from PDF + web sources")
        return "Advanced retrieval systems use hybrid search combining dense and sparse vectors."

    def chunk(self, text: str) -> list[str]:
        words = text.split()
        chunks = [" ".join(words[i:i+5]) for i in range(0, len(words), 5)]
        print(f"  [Chunk] {len(chunks)} fixed-size chunks")
        return chunks

    def embed(self, chunks: list[str]) -> list[list[float]]:
        print(f"  [Embed] embedding {len(chunks)} chunks with dense + sparse embedder")
        return [[float(i), float(i*2)] for i in range(len(chunks))]

    def retrieve(self, embeddings: list[list[float]], query: str) -> str:
        print(f"  [Retrieve] hybrid search: dense + BM25 over {len(embeddings)} chunks")
        return "hybrid retrieved context"


if __name__ == "__main__":
    SimpleRAGPipeline().run("What is self-attention?")
    HybridRAGPipeline().run("How does hybrid search work?")
