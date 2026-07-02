# Memento Pattern

## What it does
Captures and restores an object's internal state without violating encapsulation. The object saves its own snapshot — outside code can't read or modify it directly.

## Use case
Conversation session snapshots — checkpoint the chat history before a risky tool call so you can roll back if the agent does something bad.

## Key insight
Three roles: the **originator** (`ConversationSession`) creates and restores snapshots. The **memento** (`ConversationSnapshot`) stores the state. The **caretaker** (`SessionCaretaker`) holds snapshots and calls rollback — but never reads the snapshot's contents directly.

```python
caretaker.checkpoint()          # save good state
session.add_message(...)        # risky operation
caretaker.rollback()            # restore to checkpoint
```

## Why it matters for AI engineering
- Agents can take irreversible actions (delete, modify) — checkpointing before tool calls enables recovery
- Useful in long-running agentic sessions where a bad step shouldn't lose all prior context
- The caretaker can hold multiple snapshots — full undo history

## Files
- `memento.py` — conversation session with checkpoint and rollback around a bad tool call
