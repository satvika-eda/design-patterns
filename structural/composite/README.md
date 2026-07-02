# Composite Pattern

## What problem does it solve?

You have a pipeline that can contain individual tasks or groups of tasks (sub-pipelines), and those sub-pipelines can contain further sub-pipelines. You want to run the whole thing with one call — without special-casing whether a node is a leaf or a group.

Without Composite, calling code has to check: "is this a single task or a pipeline?" everywhere. With Composite, both look identical from the outside.

## What it does

Composes objects into a tree. Both leaves (single tasks) and composites (pipelines) implement the same interface, so the caller treats them uniformly.

```
RAG Pipeline
├── Ingestion Pipeline
│   ├── Chunker (leaf)
│   └── Embedder (leaf)
├── Retrieval Pipeline
│   ├── Retriever (leaf)
│   └── Reranker (leaf)
├── LLM (leaf)
└── Guardrails (leaf)
```

Every node — whether a single `Task` or a nested `Pipeline` — responds to `run()` and `describe()` the same way.

## The key insight

The composite (`Pipeline`) holds a list of `PipelineComponent` — the abstract type. It doesn't know or care if its children are leaves or other composites:

```python
class Pipeline(PipelineComponent):
    def run(self, input_text: str) -> str:
        for component in self._components:  # could be Task or Pipeline — doesn't matter
            result = component.run(current)
```

This means you can nest arbitrarily deep. A pipeline inside a pipeline inside a pipeline all runs with one `rag.run(input)` call at the top.

## Why it matters for AI engineering

- RAG pipelines, agent workflows, and eval suites are naturally tree-shaped
- You want to run a sub-pipeline the same way you run a single task
- Easy to add/remove steps without changing the calling code
- `describe()` gives you a free visual tree of your pipeline structure — useful for debugging

## Leaf vs Composite

| | Leaf (`Task`) | Composite (`Pipeline`) |
|---|---|---|
| Children | None | List of `PipelineComponent` |
| `run()` | Does the actual work | Delegates to children |
| Add/remove | N/A | `add(component)` |

## The structure

| Role | In this example |
|---|---|
| Component interface | `PipelineComponent` |
| Leaf | `Task` |
| Composite | `Pipeline` |
| Client | `__main__` block |

## Files

- `composite.py` — full RAG pipeline tree with nested sub-pipelines and uniform `run()` interface
