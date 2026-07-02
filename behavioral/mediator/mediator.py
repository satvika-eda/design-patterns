"""
Mediator Pattern
----------------
Defines an object that encapsulates how a set of objects interact.
Promotes loose coupling by keeping objects from referring to each other directly.

Use case: multi-agent coordinator — agents (researcher, writer, critic)
communicate through a central mediator instead of calling each other directly.
"""

from abc import ABC, abstractmethod


# ── Mediator interface ─────────────────────────────────────────────────────────

class AgentMediator(ABC):
    @abstractmethod
    def send(self, message: str, sender: "Agent", recipient_name: str) -> None:
        pass


# ── Base agent ─────────────────────────────────────────────────────────────────

class Agent(ABC):
    def __init__(self, name: str, mediator: AgentMediator):
        self.name = name
        self._mediator = mediator

    def send(self, message: str, to: str) -> None:
        print(f"  [{self.name}] → [{to}]: {message[:60]}")
        self._mediator.send(message, self, to)

    @abstractmethod
    def receive(self, message: str, from_name: str) -> None:
        pass


# ── Concrete agents ────────────────────────────────────────────────────────────

class ResearcherAgent(Agent):
    def receive(self, message: str, from_name: str) -> None:
        print(f"  [Researcher] received from [{from_name}]: {message[:60]}")


class WriterAgent(Agent):
    def receive(self, message: str, from_name: str) -> None:
        print(f"  [Writer] received from [{from_name}]: {message[:60]}")


class CriticAgent(Agent):
    def receive(self, message: str, from_name: str) -> None:
        print(f"  [Critic] received from [{from_name}]: {message[:60]}")


# ── Concrete mediator ──────────────────────────────────────────────────────────

class PipelineCoordinator(AgentMediator):
    def __init__(self):
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> "PipelineCoordinator":
        self._agents[agent.name] = agent
        return self

    def send(self, message: str, sender: Agent, recipient_name: str) -> None:
        recipient = self._agents.get(recipient_name)
        if recipient and recipient is not sender:
            recipient.receive(message, sender.name)
        elif not recipient:
            print(f"  [Coordinator] Unknown agent: {recipient_name}")


if __name__ == "__main__":
    coordinator = PipelineCoordinator()

    researcher = ResearcherAgent("Researcher", coordinator)
    writer = WriterAgent("Writer", coordinator)
    critic = CriticAgent("Critic", coordinator)

    coordinator.register(researcher).register(writer).register(critic)

    print("=== Multi-agent pipeline ===")
    researcher.send("Here are the key findings on RAG systems.", to="Writer")
    writer.send("Draft complete. Please review.", to="Critic")
    critic.send("Add more detail on retrieval step.", to="Writer")
    writer.send("Revised draft ready.", to="Researcher")
