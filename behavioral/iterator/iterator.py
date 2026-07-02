"""
Iterator Pattern
----------------
Provides a way to sequentially access elements of a collection
without exposing its underlying structure.

Use case: iterating over a document corpus for batch embedding —
stream chunks one at a time without loading everything into memory.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Document:
    doc_id: str
    content: str


# ── Iterator ───────────────────────────────────────────────────────────────────

class DocumentIterator:
    def __init__(self, documents: list[Document], batch_size: int = 2):
        self._docs = documents
        self._batch_size = batch_size
        self._index = 0

    def __iter__(self) -> DocumentIterator:
        return self

    def __next__(self) -> list[Document]:
        if self._index >= len(self._docs):
            raise StopIteration
        batch = self._docs[self._index:self._index + self._batch_size]
        self._index += self._batch_size
        return batch

    def has_next(self) -> bool:
        return self._index < len(self._docs)


# ── Collection ─────────────────────────────────────────────────────────────────

class DocumentCorpus:
    def __init__(self):
        self._documents: list[Document] = []

    def add(self, doc: Document) -> "DocumentCorpus":
        self._documents.append(doc)
        return self

    def batch_iterator(self, batch_size: int = 2) -> DocumentIterator:
        return DocumentIterator(self._documents, batch_size)

    def __iter__(self):
        return iter(self._documents)


if __name__ == "__main__":
    corpus = (
        DocumentCorpus()
        .add(Document("doc-1", "Transformers use self-attention."))
        .add(Document("doc-2", "RAG combines retrieval with generation."))
        .add(Document("doc-3", "Embeddings map text to vectors."))
        .add(Document("doc-4", "Fine-tuning adapts a model to a task."))
        .add(Document("doc-5", "Prompting guides model behavior."))
    )

    print("=== Batch embedding (batch_size=2) ===")
    for batch in corpus.batch_iterator(batch_size=2):
        ids = [d.doc_id for d in batch]
        print(f"  Embedding batch: {ids}")

    print("\n=== Single document iteration ===")
    for doc in corpus:
        print(f"  Processing: {doc.doc_id}")
