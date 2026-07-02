# Visitor Pattern

## What it does
Lets you add new operations to an existing object structure without modifying those objects. Each new operation is a visitor class.

## Use case
Running analysis over a conversation history — token counting, safety checking, cost estimation — without modifying the message classes themselves.

## Key insight
Each message class has an `accept(visitor)` method that calls the right visitor method for its type. The visitor implements one method per message type. To add a new operation (e.g. cost estimation), add one visitor class — the message classes are untouched.

```python
# Adding a new operation = one new class
class CostEstimator(MessageVisitor):
    def visit_user_message(self, msg): ...
    def visit_assistant_message(self, msg): ...
    def visit_tool_call(self, msg): ...

for msg in history:
    msg.accept(CostEstimator())
```

## The double dispatch trick
`msg.accept(visitor)` calls `visitor.visit_user_message(self)` — the message picks the right visitor method based on its own type. This is called double dispatch: the method called depends on both the visitor type AND the message type.

## Why it matters for AI engineering
- Conversation histories are stable structures — you add new analysis operations frequently
- Visitor separates data (messages) from operations (analysis) cleanly
- Each visitor is independently testable

## Files
- `visitor.py` — token counter and safety checker visitors over a mixed message history
