# Creational Patterns

Control how objects are created. The goal is to decouple the calling code from the details of construction.

---

## Singleton
**One instance, globally shared.**

Some things should only exist once — config, logger, DB connection pool. Singleton intercepts `__new__` to return the same object every time instead of creating a new one.

→ [singleton/README.md](singleton/README.md)

---

## Factory Method
**Let a subclass decide what to instantiate.**

Your code needs an object but shouldn't be hardwired to a specific class. Define a factory method in a base class; subclasses override it to return their own concrete type. The calling code works on the interface, not the class.

→ [factory_method/README.md](factory_method/README.md)

---

## Abstract Factory
**Create a family of compatible objects.**

Like Factory Method but for multiple related products at once. Pick a factory (e.g. `AnthropicFactory`) and it gives you a whole compatible suite — LLM, embedder, tokenizer — guaranteed to work together.

→ [abstract_factory/README.md](abstract_factory/README.md)

---

## Builder
**Construct a complex object step by step.**

When an object has many optional parts, a giant constructor is unreadable. Builder lets you chain only the settings you need and call `build()` at the end. Each setter returns `self` to enable fluent chaining.

→ [builder/README.md](builder/README.md)

---

## Prototype
**Clone an existing object instead of building from scratch.**

When objects are expensive to create and variants share most of their config, clone a base prototype and only tweak the differences. Use shallow clone when nested objects can be shared; use deep clone when they must be independent.

→ [prototype/README.md](prototype/README.md)

---

## Anti-patterns and misuse

**Singleton** is the most controversial — some consider it an anti-pattern outright:
- It's a global variable in disguise — any code anywhere can reach in and change state
- Hidden coupling — modules depend on it without declaring it in their interface
- Hard to test — state leaks between tests, you can't easily inject a mock
- Violates single responsibility — manages its own lifecycle AND does its job

**Factory Method / Abstract Factory** — overengineered when a simple function would do. If you have one concrete class and no plans to add more, the abstraction adds complexity for no gain.

**Builder** — overkill for simple objects. Python keyword arguments handle most cases. Only reach for Builder when construction has real logic or validation.

**Prototype** — misusing shallow clone when you needed deep clone (or vice versa). Silent bugs where mutations bleed across clones.

The honest take: none of these are inherently bad. They become anti-patterns when applied to problems they don't fit. Singleton gets the most criticism because its downsides show up even when used correctly.

---

## When to use which

| Pattern | Reach for it when |
|---|---|
| Singleton | One shared instance is a hard requirement (config, logger) |
| Factory Method | You want to defer "which class" to a subclass |
| Abstract Factory | You need a suite of related objects that must be compatible |
| Builder | Object construction has many optional parts or steps |
| Prototype | New objects are mostly copies of an existing one |
