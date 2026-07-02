# Design Patterns — Gang of Four

All 23 GoF design patterns implemented in Python with AI engineering use cases.

Each pattern has a working implementation and a README explaining the problem, key insight, and when to use it.

---

## Creational Patterns
Control how objects are created — decouple calling code from construction details.

| Pattern | One line | Use case |
|---|---|---|
| [Singleton](creational/singleton/README.md) | One instance, globally shared | Model config manager |
| [Factory Method](creational/factory_method/README.md) | Let a subclass decide what to instantiate | LLM provider clients |
| [Abstract Factory](creational/abstract_factory/README.md) | Create a family of compatible objects | AI provider suite (LLM + embedder + tokenizer) |
| [Builder](creational/builder/README.md) | Construct a complex object step by step | LLM request builder |
| [Prototype](creational/prototype/README.md) | Clone an existing object instead of rebuilding | Agent config variants |

→ [creational/README.md](creational/README.md)

---

## Structural Patterns
Concerned with how objects and classes are composed into larger structures.

| Pattern | One line | Use case |
|---|---|---|
| [Adapter](structural/adapter/README.md) | Convert one interface to another | Wrap Anthropic/OpenAI SDKs behind a common interface |
| [Bridge](structural/bridge/README.md) | Decouple abstraction from implementation | AI tasks × providers (M+N not M×N) |
| [Composite](structural/composite/README.md) | Treat individual objects and groups uniformly | RAG pipeline tree |
| [Decorator](structural/decorator/README.md) | Add behavior by wrapping, not subclassing | Logging, caching, retry on LLM client |
| [Facade](structural/facade/README.md) | Simplify a complex subsystem | RAG system behind `ingest()` and `ask()` |
| [Flyweight](structural/flyweight/README.md) | Share common state across many objects | Model config shared across agent workers |
| [Proxy](structural/proxy/README.md) | Control access to an object | Lazy init, auth, rate limiting on LLM client |

→ [structural/README.md](structural/README.md)

---

## Behavioral Patterns
Concerned with how objects communicate and distribute responsibility.

| Pattern | One line | Use case |
|---|---|---|
| [Observer](behavioral/observer/README.md) | One change, many reactions automatically | LLM response events → logger, cost tracker, UI |
| [Strategy](behavioral/strategy/README.md) | Swap the algorithm at runtime | Chunking strategies for RAG |
| [Command](behavioral/command/README.md) | Encapsulate a request as an object | Agent tool calls with undo |
| [Chain of Responsibility](behavioral/chain_of_responsibility/README.md) | Pass request down a chain until handled | LLM request validation pipeline |
| [Iterator](behavioral/iterator/README.md) | Traverse a collection without exposing internals | Batch embedding over document corpus |
| [Mediator](behavioral/mediator/README.md) | Route communication through a central hub | Multi-agent coordinator |
| [Memento](behavioral/memento/README.md) | Save and restore state without exposing internals | Conversation session checkpoints |
| [State](behavioral/state/README.md) | Object changes behavior when its state changes | Agent lifecycle (idle → thinking → executing → done) |
| [Template Method](behavioral/template_method/README.md) | Fix the algorithm skeleton, vary the steps | RAG pipeline variants |
| [Visitor](behavioral/visitor/README.md) | Add operations to a structure without modifying it | Token count + safety check over message history |
| [Interpreter](behavioral/interpreter/README.md) | Define and execute a mini-language | Agent instruction DSL |

→ [behavioral/README.md](behavioral/README.md)

---

## Pattern relationships worth knowing

**Factory Method vs Abstract Factory** — Factory Method creates one product; Abstract Factory creates a compatible family.

**Adapter vs Bridge** — Adapter fixes incompatible interfaces after the fact; Bridge designs for independent variation upfront.

**Decorator vs Proxy** — Both wrap an object behind the same interface. Decorator adds behavior; Proxy controls access. The line is intent.

**Composite vs Iterator** — Composite structures a tree; Iterator traverses any collection. Often used together.

**Strategy vs Template Method** — Strategy swaps the whole algorithm at runtime (composition); Template Method fixes the skeleton and varies steps (inheritance).

**Command vs Memento** — Command encapsulates actions (enabling undo by re-execution or reversal); Memento captures state snapshots (enabling undo by restoration).

**Observer vs Mediator** — Observer is one-to-many event broadcasting; Mediator centralizes many-to-many communication. Observer is simpler; Mediator reduces coupling in complex systems.

---

## Quick reference — pick by problem

| Problem | Pattern |
|---|---|
| Only one instance should exist | Singleton |
| Caller shouldn't know which class to instantiate | Factory Method |
| Need a compatible suite of objects | Abstract Factory |
| Object has too many constructor parameters | Builder |
| Need variants of an object with minimal differences | Prototype |
| Two incompatible interfaces need to work together | Adapter |
| Two dimensions vary independently | Bridge |
| Tree structure should be traversable uniformly | Composite |
| Add behavior without modifying the class | Decorator |
| Hide a complex subsystem behind a simple interface | Facade |
| Many objects share most of their state | Flyweight |
| Control or delay access to an object | Proxy |
| One event should trigger multiple independent reactions | Observer |
| Same operation, different algorithm | Strategy |
| Actions need to be queued, logged, or undone | Command |
| Ordered processing steps, any can handle or pass | Chain of Responsibility |
| Sequential access without exposing collection internals | Iterator |
| Many objects communicate — reduce coupling | Mediator |
| Need to snapshot and restore object state | Memento |
| Behavior depends on internal state — avoid if/elif chains | State |
| Algorithm skeleton fixed, steps vary per subclass | Template Method |
| New operations on a stable object structure | Visitor |
| Small structured command language | Interpreter |
