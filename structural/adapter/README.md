# Adapter Pattern

## What problem does it solve?

You have code that expects one interface, and a class that provides a different one. You can't change either — the calling code is yours and works fine, and the third-party SDK is not yours to modify.

Adapter sits in between and translates.

Real example: Anthropic and OpenAI SDKs have completely different method signatures:

```python
# Anthropic
sdk.messages_create(model=..., max_tokens=..., system=..., messages=[...])
response["content"][0]["text"]

# OpenAI
sdk.chat_completions_create(model=..., messages=[{"role": "system"}, {"role": "user"}])
response["choices"][0]["message"]["content"]
```

Your pipeline doesn't want to know about either of these. It just wants `chat(system, user) -> str`.

## What it does

Wraps an incompatible class (the adaptee) behind the interface the client expects (the target). The adapter translates calls on the target interface into calls on the adaptee.

```
SummarizationPipeline
    calls chat(system, user)
          │
          ▼
    LLMClient  ←── target interface
          │
    ┌─────┴─────┐
    │           │
AnthropicAdapter  OpenAIAdapter  ←── adapters
    │           │
AnthropicSDK  OpenAISDK  ←── adaptees (third-party, incompatible)
```

## The key insight

`SummarizationPipeline` only imports `LLMClient`. It has no idea Anthropic or OpenAI exist. Swapping providers means passing a different adapter — the pipeline code doesn't change.

```python
pipeline = SummarizationPipeline(AnthropicAdapter())  # use Anthropic
pipeline = SummarizationPipeline(OpenAIAdapter())      # swap to OpenAI — nothing else changes
```

## Why it matters for AI engineering

- Every LLM provider has a different SDK interface — Anthropic, OpenAI, Gemini, Cohere, Ollama
- Your pipeline logic (chunking, retrieval, prompting) shouldn't be coupled to any one SDK
- When a provider changes their API (it happens), you fix one adapter, not your entire codebase
- Write tests with a `MockLLMClient` that returns fixed strings — no real API calls, no adapter needed in tests

## Adapter vs Factory Method

Both decouple calling code from concrete classes, but differently:

| | Adapter | Factory Method |
|---|---|---|
| Problem | Incompatible interfaces | Which class to instantiate |
| Existing code | Wraps code you can't change | Creates new objects |
| Focus | Interface translation | Object creation |

## The structure

| Role | In this example |
|---|---|
| Target interface | `LLMClient` with `chat(system, user)` |
| Adaptees | `AnthropicSDK`, `OpenAISDK` |
| Adapters | `AnthropicAdapter`, `OpenAIAdapter` |
| Client | `SummarizationPipeline` |

## Files

- `adapter.py` — full implementation wrapping two simulated provider SDKs
