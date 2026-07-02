# Bridge Pattern

## What problem does it solve?

You have two dimensions that vary independently — task type and provider. Without Bridge, every combination needs its own subclass:

```
SummarizationWithClaude
SummarizationWithGPT
ClassificationWithClaude
ClassificationWithGPT
QAWithClaude
QAWithGPT
...
```

M tasks × N providers = M×N subclasses. Add one new provider and you need M new classes. This explodes fast.

Bridge separates the two dimensions: M tasks + N providers = M+N classes. Any combination works.

## What it does

Splits a class into two hierarchies:
- **Abstraction** — the front end (what the task is: summarize, classify, QA)
- **Implementation** — the back end (how it's done: which provider)

The abstraction holds a reference to the implementation — that reference is the "bridge."

```
AITask (abstraction)
  └── _backend: LLMBackend  ← the bridge
        │
   ─────────────
   |             |
Anthropic      OpenAI
Backend        Backend

AITask subclasses:
  Summarizer, Classifier, QATask
```

## The key insight

`AITask` holds a `_backend` reference injected at construction. Tasks call `self._backend.generate(...)` — they don't care which backend they got:

```python
class Summarizer(AITask):
    def run(self, input_text: str) -> str:
        return self._backend.generate(
            system="You are a summarization assistant.",
            user=f"Summarize: {input_text}",
        )
```

To add a new provider (Gemini), add one `GeminiBackend` class. All existing tasks work with it immediately — no changes needed.

To add a new task (Translation), add one `Translator` class. All existing backends work with it immediately.

## Bridge vs Adapter

They look similar — both involve wrapping — but the intent is different:

| | Adapter | Bridge |
|---|---|---|
| Intent | Fix incompatible interfaces after the fact | Design for independent variation upfront |
| When | Working with existing code you can't change | Designing new code with two varying dimensions |
| Result | One interface talks to another | Two hierarchies that evolve independently |

## Why it matters for AI engineering

- Tasks (summarize, classify, extract, translate) and providers (Anthropic, OpenAI, Gemini, local) vary independently
- Adding a new provider doesn't touch task code; adding a new task doesn't touch provider code
- Swap backends at runtime — useful for fallback logic (try Anthropic, fall back to OpenAI)
- Test tasks with a `MockBackend` that returns fixed strings

## The structure

| Role | In this example |
|---|---|
| Abstraction | `AITask` |
| Refined abstractions | `Summarizer`, `Classifier`, `QATask` |
| Implementation interface | `LLMBackend` |
| Concrete implementations | `AnthropicBackend`, `OpenAIBackend` |

## Files

- `bridge.py` — full implementation with 3 tasks × 2 backends = 6 combinations, 5 classes
