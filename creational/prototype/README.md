# Prototype Pattern

## What problem does it solve?

Sometimes creating an object from scratch is expensive — it involves loading schemas, making API calls, running validation, or filling in many fields. If you need several similar objects, rebuilding each one from zero is wasteful.

Prototype says: build one good object, then clone it and tweak the clone.

## What it does

Creates new objects by copying an existing object (the prototype) instead of constructing from scratch. The clone starts as an exact copy — you only change what's different.

```python
base_agent = AgentConfig(
    model="claude-sonnet-4-6",
    tools=["web_search", "calculator"],
    ...
)

researcher = base_agent.deep_clone()
researcher.system_prompt = "You are a research assistant."
researcher.temperature = 0.3
```

## Shallow vs deep clone

This is the most important thing to understand about Prototype.

**Shallow clone (`copy.copy`)** — copies the object, but nested objects (lists, dicts) are shared between the original and the clone.

```python
clone = copy.copy(base)
clone.tools.append("new_tool")  # also modifies base.tools — same list in memory!
```

**Deep clone (`copy.deepcopy`)** — recursively copies everything. The clone is fully independent.

```python
clone = copy.deepcopy(base)
clone.tools.append("new_tool")  # base.tools is untouched — separate list
```

Use shallow clone only when you know nested objects won't be mutated. Default to deep clone when in doubt.

**With real ML models (e.g. a loaded `transformers` model):**

- Shallow clone — both configs point to the **same model weights** in memory. No duplication. This is what you want.
- Deep clone — would try to copy the entire model weights. Huge, slow, almost never correct.

So in practice: shallow clone the config and only deep clone the parts that need to be independent (tools list, config dicts), not the model itself.

**Safe vs unsafe mutations with shallow clone:**

```python
clone = copy.copy(base)

clone.system_prompt = "new prompt"   # ✅ safe — reassigning creates a new attribute on clone only
clone.temperature = 0.3              # ✅ safe — same, primitive value

clone.tools.append("new_tool")       # ⚠️ mutates base.tools too — same list in memory
clone.tools = ["new_tool"]           # ✅ safe — reassigning creates a new list on clone only
```

The rule: **reassigning** is always safe. **Mutating** a nested object in place is dangerous.

## Does the model have context of the base config?

No. The model object (if it were a real loaded model) is just weights and architecture — it has no memory of which config pointed to it.

```
base_agent  ──→  AgentConfig { system_prompt: "...", tools: [...] }
                      │
                      └──→  model_weights (just math, no awareness)

clone       ──→  AgentConfig { system_prompt: "new...", tools: [...] }
                      │
                      └──→  same model_weights (still just math)
```

The model doesn't "know" it's being shared. It just receives inputs at inference time — the system prompt, the user message, the tools — and produces outputs. All that context is passed **at call time**, not stored in the model object itself.

So two clones sharing the same model but having different system prompts will behave completely differently at inference — because the system prompt is passed in the request, not baked into the model.

## Why it matters for AI engineering

- You have a base agent config with validated tool schemas, system prompt templates, model settings
- You need 5 variants — researcher, analyst, coder, summarizer, reviewer — that share most settings
- Clone the base, tweak only what's different — no rebuilding, no risk of missing a field
- Useful in multi-agent systems where agents share a common base but have specialized roles

## Prototype vs Builder

| | Prototype | Builder |
|---|---|---|
| Start from | An existing object | Nothing (blank slate) |
| Best when | Variants share most config | Object has many optional parts |
| Customization | Mutate after cloning | Chain setter methods |

Use Prototype when objects are mostly alike. Use Builder when objects are constructed from scratch with varying parts.

## The structure

| Role | In this example |
|---|---|
| Prototype | `AgentConfig` with `clone()` and `deep_clone()` methods |
| Client | The `__main__` block that clones and tweaks |

In Python, `copy.copy` and `copy.deepcopy` handle the cloning mechanics — you just need to expose them through a meaningful interface.

## Files

- `prototype.py` — full implementation showing shallow vs deep clone and independent mutation
