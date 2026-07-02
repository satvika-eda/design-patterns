# Decorator Pattern

## What problem does it solve?

You want to add behavior to an object — logging, caching, retry — without modifying the original class. Subclassing doesn't work well here because you'd need a separate subclass for every combination:

```
LoggingClaudeClient
CachingClaudeClient
RetryClaudeClient
LoggingCachingClaudeClient
LoggingRetryClaudeClient
...
```

Decorator lets you stack behaviors at runtime by wrapping objects, not subclassing them.

## What it does

A decorator implements the same interface as the object it wraps, holds a reference to it, and adds behavior before/after delegating to it. You can stack multiple decorators — each wraps the previous one.

```python
client = ClaudeClient()           # base
client = CachingDecorator(client) # wraps base
client = LoggingDecorator(client) # wraps caching
client = RetryDecorator(client)   # wraps logging
```

A call to `client.chat(...)` flows through each layer:

```
RetryDecorator
  → LoggingDecorator  (logs request + timing)
    → CachingDecorator  (checks/stores cache)
      → ClaudeClient    (actual API call, if not cached)
```

## The key insight

Every decorator implements `LLMClient` — the same interface as the thing it wraps. So from the outside, a decorated client looks identical to a plain `ClaudeClient`. The caller never knows how many layers are stacked.

```python
def run_pipeline(client: LLMClient):  # works with plain or decorated client
    return client.chat(system, user)
```

## Order matters

The order you stack decorators changes behavior:

```python
# Cache checked BEFORE logging — cache hits are not logged
client = LoggingDecorator(CachingDecorator(ClaudeClient()))

# Cache checked AFTER logging — all requests logged, including cache hits
client = CachingDecorator(LoggingDecorator(ClaudeClient()))
```

Think of it inside-out: the innermost decorator is called last, outermost first.

## Why it matters for AI engineering

- Add logging, cost tracking, rate limiting to any LLM client without touching its code
- Cache expensive LLM calls — identical prompts return instantly on second call
- Add retry logic for transient API errors without cluttering business logic
- Mix and match behaviors per use case — prod gets logging + retry + cache, tests get just the base client

## Decorator vs Inheritance

| | Decorator | Inheritance |
|---|---|---|
| Composition | At runtime | At compile time |
| Combinations | Stack freely | Subclass explosion |
| Modify original | No | No |
| Flexibility | High | Low |

## The structure

| Role | In this example |
|---|---|
| Component interface | `LLMClient` |
| Concrete component | `ClaudeClient` |
| Base decorator | `LLMDecorator` (delegates by default) |
| Concrete decorators | `LoggingDecorator`, `CachingDecorator`, `RetryDecorator` |

## Files

- `decorator.py` — full implementation with logging, caching, and retry decorators stacked on a Claude client
