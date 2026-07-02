# Chain of Responsibility Pattern

## What it does
Passes a request along a chain of handlers. Each handler either processes it or passes it to the next. The sender doesn't know which handler will handle it.

## Use case
LLM request validation pipeline — rate limit → safety → token budget. Each check either blocks the request or passes it forward.

## Key insight
Handlers are linked via `set_next()`. Each handler's `handle()` method calls `self._next.handle(request)` to pass through, or returns an error to block. Adding a new check means adding one handler and inserting it in the chain — nothing else changes.

```python
rate_limit.set_next(safety).set_next(token_budget)
result = rate_limit.handle(request)  # flows through the whole chain
```

## Why it matters for AI engineering
- LLM request pipelines naturally have ordered validation steps
- Each concern (rate limit, safety, cost) is isolated in its own handler
- Reorder, add, or remove checks without touching other handlers

## Files
- `chain_of_responsibility.py` — three-handler validation chain with block and pass-through examples
