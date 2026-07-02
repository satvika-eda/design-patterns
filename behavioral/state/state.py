"""
State Pattern
-------------
Allows an object to alter its behavior when its internal state changes.
The object appears to change its class.

Use case: agent lifecycle — an agent behaves differently depending on
whether it is idle, thinking, executing a tool, or done.
"""

from abc import ABC, abstractmethod


# ── State interface ────────────────────────────────────────────────────────────

class AgentState(ABC):
    @abstractmethod
    def handle(self, agent: "Agent", input: str) -> None:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


# ── Concrete states ────────────────────────────────────────────────────────────

class IdleState(AgentState):
    def handle(self, agent: "Agent", input: str) -> None:
        print(f"  [Idle] Received input: '{input[:40]}' — transitioning to Thinking")
        agent.set_state(ThinkingState())

    def name(self) -> str:
        return "Idle"


class ThinkingState(AgentState):
    def handle(self, agent: "Agent", input: str) -> None:
        if "search" in input.lower():
            print(f"  [Thinking] Decided to use a tool — transitioning to Executing")
            agent.set_state(ExecutingState())
        else:
            print(f"  [Thinking] No tool needed — transitioning to Done")
            agent.set_state(DoneState())

    def name(self) -> str:
        return "Thinking"


class ExecutingState(AgentState):
    def handle(self, agent: "Agent", input: str) -> None:
        print(f"  [Executing] Tool call complete — transitioning to Done")
        agent.set_state(DoneState())

    def name(self) -> str:
        return "Executing"


class DoneState(AgentState):
    def handle(self, agent: "Agent", input: str) -> None:
        print(f"  [Done] Agent finished. Reset to Idle.")
        agent.set_state(IdleState())

    def name(self) -> str:
        return "Done"


# ── Context ────────────────────────────────────────────────────────────────────

class Agent:
    def __init__(self):
        self._state: AgentState = IdleState()

    def set_state(self, state: AgentState) -> None:
        self._state = state

    def process(self, input: str) -> None:
        print(f"\nState: {self._state.name()} | Input: '{input[:40]}'")
        self._state.handle(self, input)


if __name__ == "__main__":
    agent = Agent()

    # Flow 1: simple question, no tool needed
    agent.process("What is RAG?")
    agent.process("What is RAG?")  # thinking → done
    agent.process("")              # done → idle

    print()

    # Flow 2: question requiring tool use
    agent.process("Search for the latest AI papers")
    agent.process("Search for the latest AI papers")  # thinking → executing
    agent.process("Search for the latest AI papers")  # executing → done
