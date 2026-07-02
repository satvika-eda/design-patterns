# Command Pattern

## What it does
Encapsulates a request as an object. This lets you queue requests, log them, and support undo/redo.

## Use case
Agent action history — each tool call (add document, remove document) is a command object that can be executed and undone.

## Key insight
The invoker (`AgentActionHistory`) doesn't know what the command does — it just calls `execute()` and stores it. To undo, it pops the last command and calls `undo()`. The undo logic lives in each command, not the invoker.

```python
history.execute(AddDocumentCommand(store, "doc-1", "content"))
history.undo_last()  # removes doc-1 — no special-casing needed
```

## Why it matters for AI engineering
- Agent tool calls are naturally commands — they change state and should be reversible
- Queue commands for rate-limited execution
- Replay a sequence of actions for debugging or auditing

## The structure
| Role | In this example |
|---|---|
| Command interface | `Command` with `execute()` and `undo()` |
| Concrete commands | `AddDocumentCommand`, `RemoveDocumentCommand` |
| Receiver | `VectorStore` |
| Invoker | `AgentActionHistory` |

## Files
- `command.py` — vector store actions with full undo support
