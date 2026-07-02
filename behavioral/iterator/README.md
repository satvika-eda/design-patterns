# Iterator Pattern

## What it does
Provides a way to sequentially access elements of a collection without exposing its underlying structure.

## Use case
Batch embedding over a document corpus — stream documents in configurable batches without loading everything into memory at once.

## Key insight
`DocumentIterator` implements `__iter__` and `__next__` — making it a Python-native iterator that works with `for` loops. The collection (`DocumentCorpus`) exposes a `batch_iterator(batch_size)` factory so the caller controls batch size without knowing how iteration works internally.

```python
for batch in corpus.batch_iterator(batch_size=2):
    embed(batch)  # 2 docs at a time, memory-efficient
```

## Why it matters for AI engineering
- Embedding large corpora in batches is standard — you never load everything at once
- Decouples "how to iterate" from "what to do with each batch"
- Python's iterator protocol (`__iter__`/`__next__`) means it works natively with `for`, `list()`, `next()`

## Files
- `iterator.py` — batch and single-document iteration over a document corpus
