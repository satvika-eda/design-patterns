"""
Command Pattern
---------------
Encapsulates a request as an object, letting you parameterize clients,
queue requests, and support undo/redo.

Use case: agent action history — each LLM tool call is a command object
that can be executed, logged, and undone.
"""

from abc import ABC, abstractmethod


# ── Command interface ──────────────────────────────────────────────────────────

class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def undo(self) -> str:
        pass


# ── Receiver — the thing that does the actual work ────────────────────────────

class VectorStore:
    def __init__(self):
        self._docs: dict[str, str] = {}

    def add(self, doc_id: str, content: str) -> str:
        self._docs[doc_id] = content
        return f"Added doc '{doc_id}'"

    def remove(self, doc_id: str) -> str:
        self._docs.pop(doc_id, None)
        return f"Removed doc '{doc_id}'"

    def list_docs(self) -> list[str]:
        return list(self._docs.keys())


# ── Concrete commands ──────────────────────────────────────────────────────────

class AddDocumentCommand(Command):
    def __init__(self, store: VectorStore, doc_id: str, content: str):
        self._store = store
        self._doc_id = doc_id
        self._content = content

    def execute(self) -> str:
        return self._store.add(self._doc_id, self._content)

    def undo(self) -> str:
        return self._store.remove(self._doc_id)


class RemoveDocumentCommand(Command):
    def __init__(self, store: VectorStore, doc_id: str):
        self._store = store
        self._doc_id = doc_id
        self._backup: str | None = None

    def execute(self) -> str:
        self._backup = self._store._docs.get(self._doc_id)
        return self._store.remove(self._doc_id)

    def undo(self) -> str:
        if self._backup:
            return self._store.add(self._doc_id, self._backup)
        return "Nothing to undo"


# ── Invoker — queues and executes commands ─────────────────────────────────────

class AgentActionHistory:
    def __init__(self):
        self._history: list[Command] = []

    def execute(self, command: Command) -> str:
        result = command.execute()
        self._history.append(command)
        print(f"  [History] Executed: {result}")
        return result

    def undo_last(self) -> str:
        if not self._history:
            return "Nothing to undo"
        command = self._history.pop()
        result = command.undo()
        print(f"  [History] Undone: {result}")
        return result


if __name__ == "__main__":
    store = VectorStore()
    history = AgentActionHistory()

    history.execute(AddDocumentCommand(store, "doc-1", "Transformer architecture overview"))
    history.execute(AddDocumentCommand(store, "doc-2", "Attention mechanism explained"))
    history.execute(RemoveDocumentCommand(store, "doc-1"))

    print("Docs after commands:", store.list_docs())

    history.undo_last()
    print("Docs after undo:", store.list_docs())

    history.undo_last()
    print("Docs after second undo:", store.list_docs())
