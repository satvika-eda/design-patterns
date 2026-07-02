# Strategy Pattern

## What it does
Defines a family of algorithms, encapsulates each one, and makes them interchangeable. The algorithm can be swapped at runtime without changing the context that uses it.

## Use case
Chunking strategies for RAG — fixed size, sentence-based, or semantic chunking — all swappable without touching the ingestion pipeline.

## Key insight
The context (`DocumentIngester`) holds a reference to a `ChunkingStrategy`. Calling `set_strategy()` swaps the algorithm at runtime. The context never knows which algorithm it's running.

```python
ingester = DocumentIngester(FixedSizeChunking())
ingester.ingest(text)

ingester.set_strategy(SentenceChunking())  # swap at runtime
ingester.ingest(text)
```

## Strategy vs Template Method
- **Strategy** — swaps the entire algorithm at runtime via composition
- **Template Method** — fixes the algorithm skeleton in a base class, subclasses fill in steps via inheritance

## Files
- `strategy.py` — three chunking strategies swapped on a single ingester
