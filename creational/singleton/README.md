# Singleton Pattern

## What problem does it solve?

Some things should only exist once — a config manager, a logger, a DB connection pool. If you just do `ModelConfigManager()` twice, Python normally gives you two separate objects with separate state. They'd be out of sync.

## What it does

Singleton hijacks `__new__` to check "has one been made before?" If yes, return that same object. If no, create it, save it to `_instance`, and return it. Every call after the first just gets the cached `_instance` back.

```python
config1 = ModelConfigManager()   # _instance is None → create, save, return
config2 = ModelConfigManager()   # _instance exists → return it directly

config1 is config2  # True — literally the same object in memory
```

## __new__ vs __init__

Python object creation is two steps:

- `__new__` — creates the object (allocates memory, returns the instance). Called first.
- `__init__` — initializes the object (sets attributes). Called second.

Singleton intercepts `__new__` because that's where the object is born. By the time `__init__` runs, it's too late — a new object already exists.

## Why it matters for AI engineering

- You load your API keys and model settings once at startup
- 10 different modules (retriever, LLM caller, evaluator) all call `ModelConfigManager()` thinking they're getting "their own" config
- They're all sharing one — so if you change `temperature` anywhere, everyone sees it instantly
- No config drift, no duplicate initialization, no passing config objects around everywhere

## Thread safety

The problem: two threads can call `ModelConfigManager()` at the exact same moment, both see `_instance is None`, and both create a new instance — now you have two. Singleton is broken.

The fix — double-checked locking:

```python
if cls._instance is None:         # check 1 — no lock, fast path
    with cls._lock:               # only one thread gets in at a time
        if cls._instance is None: # check 2 — in case another thread just set it
            cls._instance = super().__new__(cls)
```

**Why two checks?**

Say threads A and B both hit check 1 at the same time. Both see `None`, both try to acquire the lock. A wins, B waits.

- A enters the lock, sees `None` again (check 2), creates the instance, releases the lock.
- B enters the lock, hits check 2 — now `_instance` is set. Skips creation.

Without check 2, B would create a second instance, overwriting A's.

**Why not just always use the lock?**

```python
with cls._lock:
    if cls._instance is None:
        cls._instance = super().__new__(cls)
```

This works but is slower — every single call to `ModelConfigManager()` acquires a lock, even after the instance exists. Check 1 (outside the lock) lets the 99% case (instance already exists) skip the lock entirely. Lock acquisition is expensive when you have hundreds of parallel inference calls hitting this.

So: check 1 = fast path for the common case. Lock = safety. Check 2 = correctness inside the lock.

## The tradeoff

Singleton is essentially a global variable with a fancier name. It makes testing harder (state leaks between tests) and creates hidden coupling between modules. Use it for truly shared infrastructure — config, logging, DB connection pools — not for business logic.
