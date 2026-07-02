"""
Chain of Responsibility Pattern
--------------------------------
Passes a request along a chain of handlers. Each handler decides to
process it or pass it to the next handler.

Use case: LLM request validation pipeline — check rate limit, then
content safety, then token budget, before allowing the request through.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMRequest:
    user_id: str
    prompt: str
    token_count: int
    flagged: bool = False


# ── Handler interface ──────────────────────────────────────────────────────────

class Handler(ABC):
    def __init__(self):
        self._next: Handler | None = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler  # allows chaining: a.set_next(b).set_next(c)

    def handle(self, request: LLMRequest) -> str:
        if self._next:
            return self._next.handle(request)
        return "✅ Request approved"

    @abstractmethod
    def _check(self, request: LLMRequest) -> str | None:
        """Return an error string to block, or None to pass through."""
        pass

    def handle(self, request: LLMRequest) -> str:
        error = self._check(request)
        if error:
            return f"❌ Blocked by {self.__class__.__name__}: {error}"
        if self._next:
            return self._next.handle(request)
        return "✅ Request approved"


# ── Concrete handlers ──────────────────────────────────────────────────────────

class RateLimitHandler(Handler):
    LIMITS = {"user-1": 10, "user-2": 5}

    def _check(self, request: LLMRequest) -> str | None:
        limit = self.LIMITS.get(request.user_id, 3)
        print(f"  [RateLimit] user={request.user_id} limit={limit} — OK")
        return None  # simplified: always passes in this demo


class SafetyHandler(Handler):
    BLOCKED_TERMS = {"ignore instructions", "jailbreak", "bypass"}

    def _check(self, request: LLMRequest) -> str | None:
        for term in self.BLOCKED_TERMS:
            if term in request.prompt.lower():
                return f"prompt contains blocked term '{term}'"
        print(f"  [Safety] prompt is clean — OK")
        return None


class TokenBudgetHandler(Handler):
    def __init__(self, max_tokens: int):
        super().__init__()
        self._max = max_tokens

    def _check(self, request: LLMRequest) -> str | None:
        if request.token_count > self._max:
            return f"token count {request.token_count} exceeds limit {self._max}"
        print(f"  [TokenBudget] {request.token_count}/{self._max} tokens — OK")
        return None


if __name__ == "__main__":
    # Build the chain
    rate_limit = RateLimitHandler()
    safety = SafetyHandler()
    token_budget = TokenBudgetHandler(max_tokens=1000)

    rate_limit.set_next(safety).set_next(token_budget)

    requests = [
        LLMRequest("user-1", "What is RAG?", token_count=50),
        LLMRequest("user-2", "Please jailbreak the system", token_count=20),
        LLMRequest("user-1", "Summarize this document", token_count=1500),
    ]

    for req in requests:
        print(f"\nRequest: '{req.prompt}'")
        result = rate_limit.handle(req)
        print(result)
