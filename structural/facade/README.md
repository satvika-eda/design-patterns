# Facade Pattern

## What problem does it solve?

A RAG system has many moving parts — chunker, embedder, vector store, reranker, LLM. Callers shouldn't need to know the order of operations, which subsystems exist, or how they connect. Facade hides all of that behind two methods: `ingest()` and `ask()`.

Without Facade, every caller has to orchestrate the full pipeline themselves — and if the pipeline changes, every caller breaks.

## What it does

Provides a simplified interface to a complex subsystem. The facade knows how the subsystems fit together; callers only know the facade.

```
Caller
  rag.ingest(text)
  rag.ask(question)
       │
  RAGFacade  ← facade
  ├── Chunker
  ├── Embedder
  ├── VectorStore
  ├── Reranker
  └── LLM
```

The caller never imports or touches any subsystem directly.

## The key insight

The facade doesn't add new functionality — it orchestrates existing subsystems in the right order. If the pipeline changes (add a guardrails step, swap the reranker), you update the facade in one place. All callers are unaffected.

```python
rag = RAGFacade()
rag.ingest("your document")
answer = rag.ask("your question")  # 5 subsystems, 1 method call
```

## Facade vs other patterns

| | Facade | Adapter | Composite |
|---|---|---|---|
| Intent | Simplify a complex subsystem | Fix incompatible interfaces | Treat tree of objects uniformly |
| Hides | Internal complexity | Interface mismatch | Leaf vs composite distinction |
| Subsystems | Multiple | One | One tree |

## Why it matters for AI engineering

- RAG, agents, eval pipelines are complex — exposing all internals makes integration hard
- A facade gives teammates a clean API without needing to understand the full pipeline
- Swap a subsystem (different vector store, different embedder) without changing any calling code
- Easy to version — `RAGFacadeV2` can introduce a new pipeline while `RAGFacade` stays stable

## The structure

| Role | In this example |
|---|---|
| Facade | `RAGFacade` |
| Subsystems | `Chunker`, `Embedder`, `VectorStore`, `Reranker`, `LLM` |
| Client | `__main__` block |

## Files

- `facade.py` — full RAG pipeline hidden behind `ingest()` and `ask()`
