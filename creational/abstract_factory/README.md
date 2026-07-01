# Abstract Factory Pattern

## What problem does it solve?

Factory Method creates one product. Abstract Factory creates a **family of related products** that must be used together.

In AI pipelines you often need an LLM, an embedder, and a tokenizer — and they need to come from the same provider to be compatible. If you mix an OpenAI embedder with a Claude tokenizer, you may get mismatched token counts, incompatible embedding spaces, or broken assumptions.

Abstract Factory ensures the whole family comes from the same source.

## What it does

Defines an interface with one factory method per product in the family. Each concrete factory implements all of them, guaranteeing compatibility across the family.

```
AIProviderFactory (abstract)
  create_llm()
  create_embedder()
  create_tokenizer()
        |
   ─────────────
   |             |
Anthropic      OpenAI
Factory        Factory
   |             |
Claude+        GPT4o+
Cohere+        OpenAI+
Anthropic      OpenAI
Tokenizer      Tokenizer
```

## The key insight

The client code (`RAGPipeline`) receives a factory and calls it to build all its components. It never imports or instantiates a concrete class directly:

```python
class RAGPipeline:
    def __init__(self, factory: AIProviderFactory):
        self.llm = factory.create_llm()
        self.embedder = factory.create_embedder()
        self.tokenizer = factory.create_tokenizer()
```

To switch the entire stack from Anthropic to OpenAI, you change one line at the call site:

```python
pipeline = RAGPipeline(get_factory("openai"))
```

## Abstract Factory vs Factory Method

| | Factory Method | Abstract Factory |
|---|---|---|
| Creates | One product | A family of related products |
| Override | One method | Multiple methods (one per product) |
| Use when | You need one object and want to defer which class | You need multiple objects that must be compatible |

## Why it matters for AI engineering

- Swap your entire provider stack (LLM + embedder + tokenizer) in one line
- Guarantee compatibility — the factory enforces that all components come from the same family
- Easy to add a new provider — add one factory class, implement the three methods, done
- Test with a `MockAIFactory` that returns deterministic fake components

## The structure

| Role | In this example |
|---|---|
| Abstract products | `LLM`, `Embedder`, `Tokenizer` |
| Concrete products | `ClaudeLLM`, `CohereEmbedder`, `AnthropicTokenizer`, `GPT4oLLM`, ... |
| Abstract factory | `AIProviderFactory` |
| Concrete factories | `AnthropicFactory`, `OpenAIFactory` |
| Client | `RAGPipeline` |

## Files

- `abstract_factory.py` — full implementation with a RAG pipeline as the client
