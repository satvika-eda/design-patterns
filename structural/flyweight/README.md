# Flyweight Pattern

## What problem does it solve?

You have thousands of agent workers all using the same model config, tokenizer, and settings. Without Flyweight, each worker holds its own copy of that shared data — massive memory waste.

Flyweight says: separate what's shared from what's unique, and share the shared parts across all instances.

## The core idea — intrinsic vs extrinsic state

| | Intrinsic | Extrinsic |
|---|---|---|
| What | Shared, immutable | Unique per instance |
| Stored | In the flyweight | In the worker, or passed at call time |
| Example | Model name, tokenizer, max_tokens | Session ID, conversation history |

The flyweight holds only intrinsic state. Extrinsic state is either stored in the worker or passed in when calling the flyweight's methods.

## What it does

A factory maintains a pool of flyweights keyed by their intrinsic state. When you ask for a flyweight, it returns an existing one if the state matches — otherwise creates a new one.

```
5 AgentWorkers using claude-sonnet-4-6
  → all hold a reference to the SAME ModelFlyweight
  → 1 shared object in memory, not 5
```

```python
flyweight = factory.get("claude-sonnet-4-6", "cl100k", 4096)
# first call: creates and stores
# subsequent calls: returns the cached instance
```

## The key insight

Extrinsic state (session ID, history) is passed in at call time — it's never stored in the flyweight:

```python
def run(self, system: str, user: str, session_id: str) -> str:
    # session_id is extrinsic — passed in, not stored
    return f"[{self.model}] session={session_id} | {user}"
```

This keeps the flyweight small and safely shareable across workers.

## Why it matters for AI engineering

- Multi-agent systems can have hundreds or thousands of concurrent workers
- Model configs, tokenizers, tool schemas are large and identical across workers
- Flyweight avoids duplicating that shared state — significant memory savings at scale
- In practice: loaded tokenizers (`tiktoken`, `transformers` tokenizer) are expensive to initialize — share one instance across all workers

## Flyweight vs Singleton

| | Flyweight | Singleton |
|---|---|---|
| Instances | One per unique intrinsic state | Always exactly one |
| Use case | Many similar objects | One global object |
| Factory | Pool keyed by state | Simple `_instance` check |

## The structure

| Role | In this example |
|---|---|
| Flyweight | `ModelFlyweight` (holds intrinsic state) |
| Flyweight factory | `ModelFlyweightFactory` (manages the pool) |
| Context | `AgentWorker` (holds extrinsic state + flyweight reference) |

## Files

- `flyweight.py` — 5 workers sharing 1 flyweight, plus a second model showing pool grows only when needed
