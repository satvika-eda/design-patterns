# Factory Method Pattern

## What problem does it solve?

Your pipeline needs to call a language model, but you don't want the pipeline code to be hardwired to Claude, OpenAI, or Gemini. You want to swap providers without touching the code that uses them.

If you write `client = ClaudeClient()` everywhere, switching providers means hunting down every instantiation. Factory Method moves that decision to one place.

## What it does

Defines an interface for creating an object, but lets subclasses decide which class to instantiate. The code that *uses* the object never calls a constructor directly — it calls a factory method instead.

```
LLMProvider (abstract)          LLMClient (abstract)
    create_client() →               complete()
    run_prompt()                    model_name()
         |                               |
  ───────────────             ───────────────────────
  |      |       |            |          |           |
Anthropic OpenAI Gemini   Claude     OpenAI      Gemini
Provider  Provider Provider Client    Client      Client
```

## The key insight

`run_prompt()` in the base class uses `create_client()` without knowing what it returns:

```python
def run_prompt(self, prompt: str) -> str:
    client = self.create_client()   # factory method — returns whatever subclass decides
    return client.complete(prompt)  # works on the interface, not the concrete class
```

Each subclass overrides only `create_client()`. The rest of the logic is inherited and shared.

## Why it matters for AI engineering

- Swap Claude for GPT-4o by changing one line (`get_provider("openai")`)
- A/B test providers without touching your pipeline logic
- Add a new provider (Gemini, Mistral, local Ollama) by adding one class — nothing else changes
- Write tests with a `MockLLMClient` that returns fixed strings — no real API calls

## Factory Method vs just using a function

A plain factory function (`get_provider(name)`) works for simple cases and is included as a bonus. Factory Method as a class pattern becomes useful when:

- The creator has shared logic (`run_prompt`) that all subclasses reuse
- You need to subclass the creator itself for other reasons
- The creation logic is complex enough to warrant its own class

## The structure

| Role | In this example |
|---|---|
| Product interface | `LLMClient` |
| Concrete products | `ClaudeClient`, `OpenAIClient`, `GeminiClient` |
| Creator interface | `LLMProvider` (with `create_client` as the factory method) |
| Concrete creators | `AnthropicProvider`, `OpenAIProvider`, `GeminiProvider` |

## Files

- `factory_method.py` — full implementation with abstract base classes and a convenience factory function
