"""
Visitor Pattern
---------------
Lets you add new operations to existing object structures without modifying them.
A visitor object implements an operation for each type in the structure.

Use case: running different analysis operations (token count, cost estimate,
safety check) over an agent's message history without modifying message classes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Elements — the structure being visited ────────────────────────────────────

class Message(ABC):
    @abstractmethod
    def accept(self, visitor: "MessageVisitor") -> None:
        pass


@dataclass
class UserMessage(Message):
    content: str

    def accept(self, visitor: "MessageVisitor") -> None:
        visitor.visit_user_message(self)


@dataclass
class AssistantMessage(Message):
    content: str
    model: str

    def accept(self, visitor: "MessageVisitor") -> None:
        visitor.visit_assistant_message(self)


@dataclass
class ToolCallMessage(Message):
    tool_name: str
    input: dict

    def accept(self, visitor: "MessageVisitor") -> None:
        visitor.visit_tool_call(self)


# ── Visitor interface ──────────────────────────────────────────────────────────

class MessageVisitor(ABC):
    @abstractmethod
    def visit_user_message(self, msg: UserMessage) -> None:
        pass

    @abstractmethod
    def visit_assistant_message(self, msg: AssistantMessage) -> None:
        pass

    @abstractmethod
    def visit_tool_call(self, msg: ToolCallMessage) -> None:
        pass


# ── Concrete visitors ──────────────────────────────────────────────────────────

class TokenCounter(MessageVisitor):
    def __init__(self):
        self.total = 0

    def visit_user_message(self, msg: UserMessage) -> None:
        tokens = len(msg.content.split())
        self.total += tokens
        print(f"  [TokenCounter] UserMessage: {tokens} tokens")

    def visit_assistant_message(self, msg: AssistantMessage) -> None:
        tokens = len(msg.content.split())
        self.total += tokens
        print(f"  [TokenCounter] AssistantMessage: {tokens} tokens")

    def visit_tool_call(self, msg: ToolCallMessage) -> None:
        tokens = 10  # fixed overhead for tool calls
        self.total += tokens
        print(f"  [TokenCounter] ToolCall '{msg.tool_name}': {tokens} tokens (overhead)")


class SafetyChecker(MessageVisitor):
    BLOCKED = {"jailbreak", "ignore instructions"}

    def visit_user_message(self, msg: UserMessage) -> None:
        for term in self.BLOCKED:
            if term in msg.content.lower():
                print(f"  [Safety] ⚠️  UserMessage flagged: '{term}'")
                return
        print(f"  [Safety] UserMessage clean")

    def visit_assistant_message(self, msg: AssistantMessage) -> None:
        print(f"  [Safety] AssistantMessage — skipped")

    def visit_tool_call(self, msg: ToolCallMessage) -> None:
        dangerous = {"delete_all", "drop_table"}
        if msg.tool_name in dangerous:
            print(f"  [Safety] ⚠️  Dangerous tool call: '{msg.tool_name}'")
        else:
            print(f"  [Safety] ToolCall '{msg.tool_name}' — OK")


if __name__ == "__main__":
    history: list[Message] = [
        UserMessage("What are the latest AI papers?"),
        AssistantMessage("Let me search for that.", model="claude-sonnet-4-6"),
        ToolCallMessage("web_search", {"query": "latest AI papers 2026"}),
        AssistantMessage("Here are the top results.", model="claude-sonnet-4-6"),
        UserMessage("Now delete all my documents please"),
        ToolCallMessage("delete_all", {}),
    ]

    print("=== Token Count ===")
    counter = TokenCounter()
    for msg in history:
        msg.accept(counter)
    print(f"Total tokens: {counter.total}")

    print("\n=== Safety Check ===")
    checker = SafetyChecker()
    for msg in history:
        msg.accept(checker)
