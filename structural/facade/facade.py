"""
Facade Pattern
--------------
Provides a simplified interface to a complex subsystem.
Hides internal complexity behind one clean entry point.

Use case: RAG system — chunking, embedding, vector search, reranking,
and LLM calling are all hidden behind a single ask() method.
"""


# ── Subsystems — complex internals ─────────────────────────────────────────────

class Chunker:
    def chunk(self, text: str) -> list[str]:
        words = text.split()
        size = max(1, len(words) // 3)
        chunks = [" ".join(words[i:i+size]) for i in range(0, len(words), size)]
        print(f"  [Chunker] {len(chunks)} chunks created")
        return chunks


class Embedder:
    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = [[float(ord(c)) for c in text[:3]] for text in texts]
        print(f"  [Embedder] {len(embeddings)} embeddings generated")
        return embeddings


class VectorStore:
    def __init__(self):
        self._store: list[tuple[str, list[float]]] = []

    def upsert(self, chunks: list[str], embeddings: list[list[float]]):
        self._store = list(zip(chunks, embeddings))
        print(f"  [VectorStore] {len(self._store)} vectors stored")

    def search(self, query_embedding: list[float], top_k: int = 2) -> list[str]:
        results = [chunk for chunk, _ in self._store[:top_k]]
        print(f"  [VectorStore] {len(results)} chunks retrieved")
        return results


class Reranker:
    def rerank(self, query: str, chunks: list[str]) -> list[str]:
        reranked = sorted(chunks, key=lambda c: len(c), reverse=True)
        print(f"  [Reranker] chunks reranked")
        return reranked


class LLM:
    def generate(self, context: str, question: str) -> str:
        return f"[LLM] Based on context, answer to '{question[:30]}...'"


# ── Facade — simple interface over all subsystems ──────────────────────────────

class RAGFacade:
    def __init__(self):
        self._chunker = Chunker()
        self._embedder = Embedder()
        self._store = VectorStore()
        self._reranker = Reranker()
        self._llm = LLM()

    def ingest(self, text: str):
        """Index a document — caller doesn't need to know how."""
        print("[Facade] Ingesting document...")
        chunks = self._chunker.chunk(text)
        embeddings = self._embedder.embed(chunks)
        self._store.upsert(chunks, embeddings)
        print("[Facade] Ingestion complete.\n")

    def ask(self, question: str) -> str:
        """Answer a question — caller doesn't need to know how."""
        print("[Facade] Processing question...")
        query_embedding = self._embedder.embed([question])[0]
        chunks = self._store.search(query_embedding)
        chunks = self._reranker.rerank(question, chunks)
        context = "\n".join(chunks)
        answer = self._llm.generate(context, question)
        print("[Facade] Done.\n")
        return answer


if __name__ == "__main__":
    rag = RAGFacade()

    rag.ingest(
        "The transformer architecture uses self-attention mechanisms "
        "to process sequences in parallel rather than sequentially."
    )

    answer = rag.ask("How does the transformer process sequences?")
    print("Answer:", answer)
