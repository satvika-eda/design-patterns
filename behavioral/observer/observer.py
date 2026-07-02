"""
Observer Pattern
----------------
Defines a one-to-many dependency: when one object changes state,
all its dependents are notified automatically.

Use case: LLM agent events — when a response is generated, multiple
observers (logger, cost tracker, UI streamer) are notified automatically.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Event ──────────────────────────────────────────────────────────────────────

@dataclass
class LLMEvent:
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int


# ── Observer interface ─────────────────────────────────────────────────────────

class Observer(ABC):
    @abstractmethod
    def on_event(self, event: LLMEvent) -> None:
        pass


# ── Concrete observers ─────────────────────────────────────────────────────────

class Logger(Observer):
    def on_event(self, event: LLMEvent) -> None:
        print(f"  [Logger] model={event.model} | prompt='{event.prompt[:30]}' | response='{event.response[:30]}'")


class CostTracker(Observer):
    PRICE_PER_1K = {"claude-sonnet-4-6": (0.003, 0.015), "gpt-4o": (0.005, 0.015)}

    def __init__(self):
        self.total_cost = 0.0

    def on_event(self, event: LLMEvent) -> None:
        input_price, output_price = self.PRICE_PER_1K.get(event.model, (0.001, 0.002))
        cost = (event.input_tokens / 1000 * input_price) + (event.output_tokens / 1000 * output_price)
        self.total_cost += cost
        print(f"  [CostTracker] call cost=${cost:.4f} | total=${self.total_cost:.4f}")


class UIStreamer(Observer):
    def on_event(self, event: LLMEvent) -> None:
        print(f"  [UIStreamer] Streaming to client: '{event.response[:50]}'")


# ── Subject — the observable ───────────────────────────────────────────────────

class LLMAgent:
    def __init__(self, model: str):
        self._model = model
        self._observers: list[Observer] = []

    def subscribe(self, observer: Observer) -> "LLMAgent":
        self._observers.append(observer)
        return self

    def unsubscribe(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def _notify(self, event: LLMEvent) -> None:
        for observer in self._observers:
            observer.on_event(event)

    def chat(self, prompt: str) -> str:
        # Simulate LLM call
        response = f"[{self._model}] answer to: '{prompt[:30]}'"
        input_tokens = len(prompt.split())
        output_tokens = len(response.split())

        event = LLMEvent(self._model, prompt, response, input_tokens, output_tokens)
        self._notify(event)   # agent doesn't know who's listening
        return response


if __name__ == "__main__":
    cost_tracker = CostTracker()

    agent = (
        LLMAgent("claude-sonnet-4-6")
        .subscribe(Logger())
        .subscribe(cost_tracker)
        .subscribe(UIStreamer())
    )

    print("=== Call 1 ===")
    agent.chat("What is retrieval augmented generation?")

    print("\n=== Call 2 ===")
    agent.chat("Explain vector embeddings.")

    print(f"\nTotal session cost: ${cost_tracker.total_cost:.4f}")
