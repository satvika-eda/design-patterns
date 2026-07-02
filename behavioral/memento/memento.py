"""
Memento Pattern
---------------
Captures and restores an object's internal state without violating encapsulation.

Use case: conversation history snapshots — save the state of a chat session
so you can roll back to a previous point (e.g. before a bad tool call).
"""

from dataclasses import dataclass, field
from copy import deepcopy


# ── Memento — snapshot of state ────────────────────────────────────────────────

@dataclass
class ConversationSnapshot:
    messages: list[dict]
    turn: int


# ── Originator — the object whose state we save/restore ───────────────────────

class ConversationSession:
    def __init__(self):
        self._messages: list[dict] = []
        self._turn: int = 0

    def add_message(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
        self._turn += 1
        print(f"  [Turn {self._turn}] {role}: {content[:50]}")

    def save(self) -> ConversationSnapshot:
        return ConversationSnapshot(
            messages=deepcopy(self._messages),
            turn=self._turn,
        )

    def restore(self, snapshot: ConversationSnapshot) -> None:
        self._messages = deepcopy(snapshot.messages)
        self._turn = snapshot.turn
        print(f"  [Restored] rolled back to turn {self._turn}")

    def current_state(self) -> list[dict]:
        return self._messages


# ── Caretaker — manages snapshots ─────────────────────────────────────────────

class SessionCaretaker:
    def __init__(self, session: ConversationSession):
        self._session = session
        self._snapshots: list[ConversationSnapshot] = []

    def checkpoint(self) -> None:
        snapshot = self._session.save()
        self._snapshots.append(snapshot)
        print(f"  [Checkpoint] saved at turn {snapshot.turn}")

    def rollback(self) -> None:
        if not self._snapshots:
            print("  [Rollback] no checkpoints available")
            return
        snapshot = self._snapshots.pop()
        self._session.restore(snapshot)


if __name__ == "__main__":
    session = ConversationSession()
    caretaker = SessionCaretaker(session)

    session.add_message("user", "What is RAG?")
    session.add_message("assistant", "RAG combines retrieval with generation.")
    caretaker.checkpoint()  # save good state

    session.add_message("user", "Run the delete tool")
    session.add_message("assistant", "Deleted all documents.")  # bad tool call!

    print(f"\nMessages before rollback: {len(session.current_state())}")

    caretaker.rollback()

    print(f"Messages after rollback: {len(session.current_state())}")
    for msg in session.current_state():
        print(f"  {msg['role']}: {msg['content']}")
