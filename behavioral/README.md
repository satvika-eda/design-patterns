# Behavioral Patterns

Concerned with how objects communicate and distribute responsibility.

---

## Observer
**One change, many reactions — automatically.**

When an LLM generates a response, multiple subscribers (logger, cost tracker, UI streamer) are notified without the agent knowing who's listening. Subscribe/unsubscribe at runtime.

→ [observer/README.md](observer/README.md)

---

## Strategy
**Swap the algorithm at runtime.**

Same ingestion pipeline, different chunking strategy — fixed size, sentence-based, or semantic. The context holds a reference to a strategy and delegates to it.

→ [strategy/README.md](strategy/README.md)

---

## Command
**Encapsulate a request as an object — enabling undo.**

Each agent tool call (add/remove document) is a command object with `execute()` and `undo()`. An invoker queues and replays them without knowing what they do.

→ [command/README.md](command/README.md)

---

## Chain of Responsibility
**Pass a request down a chain until someone handles it.**

LLM request validation: rate limit → safety → token budget. Each handler either blocks or passes through. Add/reorder checks without touching others.

→ [chain_of_responsibility/README.md](chain_of_responsibility/README.md)

---

## Iterator
**Traverse a collection without exposing its internals.**

Batch embedding over a document corpus — stream documents two at a time without loading everything into memory. Implements Python's native `__iter__`/`__next__` protocol.

→ [iterator/README.md](iterator/README.md)

---

## Mediator
**Route communication through a central hub.**

Researcher, writer, and critic agents send messages via a coordinator instead of holding references to each other. N agents → one mediator, not N² connections.

→ [mediator/README.md](mediator/README.md)

---

## Memento
**Save and restore state without exposing internals.**

Checkpoint a conversation session before a risky tool call. Roll back if the agent does something bad. The caretaker manages snapshots without reading their contents.

→ [memento/README.md](memento/README.md)

---

## State
**Object changes behavior when its state changes.**

Agent lifecycle: idle → thinking → executing → done. Each state is a class — no giant `if/elif`. Transitions are explicit and each state is independently testable.

→ [state/README.md](state/README.md)

---

## Template Method
**Fix the algorithm skeleton, vary the steps.**

RAG pipeline flow is always: load → chunk → embed → retrieve → generate. Simple and hybrid pipelines share the skeleton but implement steps differently via inheritance.

→ [template_method/README.md](template_method/README.md)

---

## Visitor
**Add operations to a structure without modifying it.**

Token counter and safety checker run over a conversation history without touching the message classes. Add a new analysis = add one visitor class.

→ [visitor/README.md](visitor/README.md)

---

## Interpreter
**Define and execute a mini-language.**

A simple agent DSL: `search`, `summarize`, `if/then`, `sequence`. Each grammar rule is a class with `interpret(context)`. Foundation for agent orchestration languages.

→ [interpreter/README.md](interpreter/README.md)

---

## When to use which

| Pattern | Reach for it when |
|---|---|
| Observer | One event, multiple independent reactions |
| Strategy | Same operation, swappable algorithm |
| Command | Requests need to be queued, logged, or undone |
| Chain of Responsibility | Ordered validation/processing steps |
| Iterator | Sequential access to a collection without exposing internals |
| Mediator | Many objects communicate — reduce N² coupling to N |
| Memento | Need to snapshot and restore object state |
| State | Object behavior depends on internal state — avoid if/elif explosion |
| Template Method | Algorithm skeleton is fixed, steps vary by subclass |
| Visitor | New operations on a stable structure, without modifying it |
| Interpreter | Small DSL or structured command language |
