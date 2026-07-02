"""
Bridge Pattern
--------------
Decouples an abstraction from its implementation so the two can vary independently.

The problem without Bridge:
  SummarizationWithClaude, SummarizationWithGPT,
  ClassificationWithClaude, ClassificationWithGPT,
  QAWithClaude, QAWithGPT ...
  → M tasks × N providers = M×N subclasses

With Bridge:
  M tasks + N providers = M+N classes, any combination works.

Use case: AI tasks (summarizer, classifier, QA) × providers (Anthropic, OpenAI).
"""

from abc import ABC, abstractmethod


# ── Implementation interface (the "back end") ──────────────────────────────────

class LLMBackend(ABC):
    @abstractmethod
    def generate(self, system: str, user: str) -> str:
        pass


# ── Concrete implementations ───────────────────────────────────────────────────

class AnthropicBackend(LLMBackend):
    def generate(self, system: str, user: str) -> str:
        return f"[Claude] {user}"  # placeholder for real SDK call


class OpenAIBackend(LLMBackend):
    def generate(self, system: str, user: str) -> str:
        return f"[GPT-4o] {user}"  # placeholder for real SDK call


# ── Abstraction (the "front end") ─────────────────────────────────────────────

class AITask(ABC):
    def __init__(self, backend: LLMBackend):
        self._backend = backend  # the bridge

    @abstractmethod
    def run(self, input_text: str) -> str:
        pass


# ── Refined abstractions ───────────────────────────────────────────────────────

class Summarizer(AITask):
    def run(self, input_text: str) -> str:
        return self._backend.generate(
            system="You are a summarization assistant. Be concise.",
            user=f"Summarize: {input_text}",
        )


class Classifier(AITask):
    def __init__(self, backend: LLMBackend, labels: list[str]):
        super().__init__(backend)
        self._labels = labels

    def run(self, input_text: str) -> str:
        return self._backend.generate(
            system=f"Classify the input into one of: {self._labels}. Reply with the label only.",
            user=input_text,
        )


class QATask(AITask):
    def __init__(self, backend: LLMBackend, context: str):
        super().__init__(backend)
        self._context = context

    def run(self, question: str) -> str:
        return self._backend.generate(
            system=f"Answer based only on this context: {self._context}",
            user=question,
        )


if __name__ == "__main__":
    anthropic = AnthropicBackend()
    openai = OpenAIBackend()

    text = "The transformer architecture uses self-attention to process sequences in parallel."

    # Any task × any backend — no new subclasses needed
    print("Summarizer + Anthropic:", Summarizer(anthropic).run(text))
    print("Summarizer + OpenAI:   ", Summarizer(openai).run(text))

    print("Classifier + Anthropic:", Classifier(anthropic, ["ML", "Finance", "Health"]).run(text))
    print("Classifier + OpenAI:   ", Classifier(openai, ["ML", "Finance", "Health"]).run(text))

    print("QA + Anthropic:", QATask(anthropic, text).run("What does self-attention do?"))
    print("QA + OpenAI:   ", QATask(openai, text).run("What does self-attention do?"))
