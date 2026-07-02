# Mediator Pattern

## What it does
Defines a central object that encapsulates how a set of objects interact. Objects communicate through the mediator instead of directly — reducing coupling.

## Use case
Multi-agent coordinator — researcher, writer, and critic agents send messages through a central coordinator instead of holding references to each other.

## Key insight
Without Mediator, each agent would need a reference to every other agent it might talk to — N agents means N² potential connections. With Mediator, every agent holds one reference (the mediator) and routes all communication through it.

```python
# Without Mediator — tight coupling
writer.send_to(critic, "review this")  # writer imports Critic

# With Mediator — decoupled
writer.send("review this", to="Critic")  # writer only knows the mediator
```

## Why it matters for AI engineering
- Multi-agent systems need coordination without agents knowing about each other
- Adding a new agent means registering it with the coordinator — no other agents change
- The coordinator can log, filter, or transform messages centrally

## Files
- `mediator.py` — researcher, writer, critic pipeline coordinated through a central mediator
