# Observer Pattern

## What problem does it solve?

When an LLM generates a response, multiple things need to happen — log it, track the cost, stream it to the UI. If you hardcode all of this inside the agent, it becomes a tangled mess. Adding a new behavior means modifying the agent.

Observer decouples the agent (subject) from the things that react to it (observers). The agent just fires an event — it doesn't know or care who's listening.

## What it does

Defines a one-to-many dependency. When the subject changes state (generates a response), it notifies all registered observers automatically.

```
LLMAgent (subject)
  _notify(event)
       │
  ─────────────────
  │        │      │
Logger  CostTracker  UIStreamer  ← observers
```

## The key insight

The agent calls `self._notify(event)` — it has no imports or references to `Logger`, `CostTracker`, or `UIStreamer`. Observers register themselves at runtime:

```python
agent.subscribe(Logger())
agent.subscribe(CostTracker())
agent.subscribe(UIStreamer())
```

To add a new behavior (e.g. alert on high cost), add one observer class and subscribe it. The agent is untouched.

## Why it matters for AI engineering

- LLM calls are natural event sources — token usage, latency, response content all matter to multiple consumers
- Cost tracking, logging, monitoring, and UI streaming are independent concerns — Observer keeps them separate
- Add/remove observers at runtime — e.g. attach a debugger observer only in dev
- `unsubscribe()` lets you detach observers cleanly (e.g. stop streaming when client disconnects)

## Observer vs direct calls

```python
# Without Observer — agent knows everything
def chat(self, prompt):
    response = self._call_llm(prompt)
    self.logger.log(response)        # tightly coupled
    self.cost_tracker.track(response)
    self.ui.stream(response)
    return response

# With Observer — agent knows nothing about consumers
def chat(self, prompt):
    response = self._call_llm(prompt)
    self._notify(LLMEvent(...))      # fire and forget
    return response
```

## The structure

| Role | In this example |
|---|---|
| Subject | `LLMAgent` |
| Observer interface | `Observer` with `on_event()` |
| Concrete observers | `Logger`, `CostTracker`, `UIStreamer` |
| Event | `LLMEvent` dataclass |

## Files

- `observer.py` — LLM agent with 3 observers: logger, cost tracker, UI streamer
