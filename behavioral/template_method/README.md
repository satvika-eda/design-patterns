# Template Method Pattern

## What it does
Defines the skeleton of an algorithm in a base class and lets subclasses fill in specific steps. The overall structure is fixed — the details vary.

## Use case
RAG pipeline variants — the flow (load → chunk → embed → retrieve → generate) is always the same, but how each step works differs between a simple pipeline and a hybrid one.

## Key insight
The base class `run()` method calls abstract methods in order — this is the template. Subclasses implement the abstract methods but never override `run()` itself. Some steps have default implementations that subclasses can optionally override.

```python
def run(self, query):           # fixed in base class — never overridden
    chunks = self.chunk(self.load())
    embeddings = self.embed(chunks)
    context = self.retrieve(embeddings, query)  # has default, can override
    return self.generate(context, query)        # has default, can override
```

## Template Method vs Strategy
- **Template Method** — algorithm structure fixed in base class, steps filled in by subclasses (inheritance)
- **Strategy** — entire algorithm swapped at runtime via a reference (composition)

Use Template Method when the skeleton is stable and steps vary. Use Strategy when the whole algorithm can change.

## Files
- `template_method.py` — simple and hybrid RAG pipelines sharing the same flow skeleton
