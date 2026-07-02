"""
Interpreter Pattern
-------------------
Defines a grammar for a language and provides an interpreter to deal with it.

Use case: a simple agent instruction DSL — parse and execute structured
commands like "search <query>", "summarize <text>", "if <condition> then <cmd>".
"""

from abc import ABC, abstractmethod


# ── Context ────────────────────────────────────────────────────────────────────

class Context:
    def __init__(self):
        self.output: list[str] = []
        self.variables: dict[str, str] = {}


# ── Abstract expression ────────────────────────────────────────────────────────

class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Context) -> str:
        pass


# ── Terminal expressions ───────────────────────────────────────────────────────

class SearchExpression(Expression):
    def __init__(self, query: str):
        self._query = query

    def interpret(self, context: Context) -> str:
        result = f"[Search results for: '{self._query}']"
        context.variables["last_result"] = result
        context.output.append(result)
        return result


class SummarizeExpression(Expression):
    def __init__(self, text: str):
        self._text = text

    def interpret(self, context: Context) -> str:
        result = f"[Summary of: '{self._text[:30]}...']"
        context.output.append(result)
        return result


class PrintExpression(Expression):
    def __init__(self, variable: str):
        self._var = variable

    def interpret(self, context: Context) -> str:
        value = context.variables.get(self._var, f"<undefined: {self._var}>")
        print(f"  [Print] {self._var} = {value}")
        return value


# ── Non-terminal expressions ───────────────────────────────────────────────────

class SequenceExpression(Expression):
    def __init__(self, expressions: list[Expression]):
        self._expressions = expressions

    def interpret(self, context: Context) -> str:
        results = [expr.interpret(context) for expr in self._expressions]
        return results[-1] if results else ""


class IfExpression(Expression):
    def __init__(self, condition_var: str, then_expr: Expression, else_expr: Expression | None = None):
        self._var = condition_var
        self._then = then_expr
        self._else = else_expr

    def interpret(self, context: Context) -> str:
        if self._var in context.variables:
            print(f"  [If] '{self._var}' exists — executing then branch")
            return self._then.interpret(context)
        elif self._else:
            print(f"  [If] '{self._var}' not found — executing else branch")
            return self._else.interpret(context)
        return ""


# ── Parser — turns text commands into expression trees ────────────────────────

class AgentDSLParser:
    def parse(self, command: str) -> Expression:
        parts = command.strip().split(" ", 1)
        op = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if op == "search":
            return SearchExpression(arg)
        elif op == "summarize":
            return SummarizeExpression(arg)
        elif op == "print":
            return PrintExpression(arg)
        else:
            raise ValueError(f"Unknown command: {op}")


if __name__ == "__main__":
    ctx = Context()
    parser = AgentDSLParser()

    # Build and run a sequence
    program = SequenceExpression([
        parser.parse("search latest transformer papers"),
        parser.parse("print last_result"),
        IfExpression(
            condition_var="last_result",
            then_expr=parser.parse("summarize found papers on transformers"),
            else_expr=parser.parse("search fallback query"),
        ),
    ])

    print("=== Running agent DSL program ===")
    result = program.interpret(ctx)

    print("\n=== Output log ===")
    for line in ctx.output:
        print(" ", line)
