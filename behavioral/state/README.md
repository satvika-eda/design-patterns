# State Pattern

## What it does
Allows an object to change its behavior when its internal state changes. Each state is a separate class — the object delegates behavior to its current state object.

## Use case
Agent lifecycle — an agent behaves differently when idle, thinking, executing a tool, or done. Instead of a giant `if/elif` block, each state is its own class.

## Key insight
The agent holds a `_state` reference and calls `self._state.handle(self, input)`. Each state decides what to do and what state to transition to next. The agent doesn't contain any state logic itself.

```python
# Without State — one giant if/elif in the agent
if self._status == "idle":
    ...
elif self._status == "thinking":
    ...

# With State — each state handles its own logic
self._state.handle(self, input)  # delegates completely
```

## Why it matters for AI engineering
- Agentic loops are inherently stateful — idle → thinking → tool call → done
- State pattern makes transitions explicit and testable — each state class is independent
- Easy to add new states (e.g. `WaitingForHumanState`) without touching existing states

## Files
- `state.py` — agent lifecycle with idle, thinking, executing, and done states
