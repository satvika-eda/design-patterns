# Interpreter Pattern

## What it does
Defines a grammar for a language and an interpreter that processes sentences in that language. Each grammar rule becomes a class.

## Use case
A simple agent instruction DSL — parse and execute structured commands like `search <query>`, `summarize <text>`, and `if <var> then <cmd>`.

## Key insight
Each expression type is a class with an `interpret(context)` method. Terminal expressions do the actual work (search, summarize). Non-terminal expressions compose others (sequence runs a list, if checks a condition). A parser turns text commands into an expression tree, which is then interpreted.

```
SequenceExpression
  ├── SearchExpression("latest papers")
  ├── PrintExpression("last_result")
  └── IfExpression("last_result")
        └── SummarizeExpression("found papers")
```

## Why it matters for AI engineering
- Agent orchestration often involves structured instruction languages
- Interpreter is the foundation of prompt parsers, tool call DSLs, and eval schemas
- Easy to extend — add a new command by adding one `Expression` subclass and one parser rule

## Interpreter in practice
The full GoF Interpreter is rarely used directly for complex languages (use a proper parser library instead). It shines for small, well-defined DSLs — agent instruction sets, filter expressions, eval conditions.

## Files
- `interpreter.py` — agent DSL with search, summarize, print, sequence, and if expressions
