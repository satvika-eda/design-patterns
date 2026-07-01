# Builder Pattern

## What problem does it solve?

Some objects have many optional parameters. The naive solution is a constructor with 10 arguments:

```python
LLMRequest("claude-sonnet-4-6", "summarize this", None, 0.3, 2048, [...tools...], [...stops...])
```

This is unreadable — you can't tell what each positional argument means. You also can't skip optional ones cleanly. Builder lets you construct the object step by step, only setting what you need.

## What it does

Separates construction from representation. A builder object accumulates configuration through method calls, then produces the final object via `build()`.

```python
request = (
    LLMRequestBuilder("claude-sonnet-4-6", "Summarize AI news.")
    .system("You are a research assistant.")
    .temperature(0.3)
    .max_tokens(2048)
    .tool("web_search", "Search the web", schema)
    .stop_on("</answer>")
    .build()
)
```

Each method returns `self`, enabling chaining. `build()` validates and assembles the final `LLMRequest`.

## The key insight

The builder methods return `self`:

```python
def temperature(self, value: float) -> "LLMRequestBuilder":
    self._temperature = value
    return self   # ← enables chaining
```

This is called a **fluent interface**. It reads like a sentence — you configure what you need, skip what you don't, and call `build()` at the end.

## Why it matters for AI engineering

- LLM requests are naturally complex — model, messages, system prompt, tools, temperature, max tokens, stop sequences, top_p, etc.
- Not every request needs every parameter — simple completions need 3 fields, agentic requests need 8
- Validation lives in one place (`build()` or in individual setters) — catches bad config early
- Easy to create preset builders for common patterns:

```python
def analyst_request(question: str) -> LLMRequest:
    return (
        LLMRequestBuilder("claude-sonnet-4-6", question)
        .system("You are a data analyst. Be precise.")
        .temperature(0.0)
        .max_tokens(1024)
        .build()
    )
```

## Builder vs just using keyword arguments

Python's keyword arguments handle simple cases:

```python
LLMRequest(model="claude-sonnet-4-6", user_message="...", temperature=0.3)
```

Builder wins when:
- Construction involves logic or validation across multiple steps
- You want to build objects incrementally (add tools in a loop, for example)
- You want to reuse a partially-configured builder across multiple requests

## The structure

| Role | In this example |
|---|---|
| Product | `LLMRequest` |
| Builder | `LLMRequestBuilder` |

The GoF pattern also includes a `Director` class that drives the builder through a fixed sequence. In practice this is often skipped — the client drives the builder directly, as shown here.

## Files

- `builder.py` — full implementation with simple and agentic request examples
