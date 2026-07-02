"""
Decorator Pattern
-----------------
Attaches additional behavior to an object dynamically by wrapping it.
Decorators implement the same interface as the object they wrap.

Use case: wrap an LLM client with logging, caching, and retry
without modifying the original client code.
"""

import time
import hashlib
from abc import ABC, abstractmethod


# ── Component interface ────────────────────────────────────────────────────────

class LLMClient(ABC):
    @abstractmethod
    def chat(self, system: str, user: str) -> str:
        pass


# ── Concrete component ─────────────────────────────────────────────────────────

class ClaudeClient(LLMClient):
    def chat(self, system: str, user: str) -> str:
        time.sleep(0.1)  # simulate network call
        return f"[Claude] answer to: '{user[:30]}'"


# ── Base decorator — implements same interface, wraps another LLMClient ────────

class LLMDecorator(LLMClient):
    def __init__(self, client: LLMClient):
        self._client = client

    def chat(self, system: str, user: str) -> str:
        return self._client.chat(system, user)  # delegate by default


# ── Concrete decorators ────────────────────────────────────────────────────────

class LoggingDecorator(LLMDecorator):
    def chat(self, system: str, user: str) -> str:
        print(f"[LOG] Request: '{user[:40]}'")
        start = time.time()
        response = self._client.chat(system, user)
        elapsed = time.time() - start
        print(f"[LOG] Response in {elapsed:.2f}s: '{response[:40]}'")
        return response


class CachingDecorator(LLMDecorator):
    def __init__(self, client: LLMClient):
        super().__init__(client)
        self._cache: dict[str, str] = {}

    def chat(self, system: str, user: str) -> str:
        key = hashlib.md5(f"{system}{user}".encode()).hexdigest()
        if key in self._cache:
            print(f"[CACHE] Hit for: '{user[:30]}'")
            return self._cache[key]
        response = self._client.chat(system, user)
        self._cache[key] = response
        print(f"[CACHE] Stored for: '{user[:30]}'")
        return response


class RetryDecorator(LLMDecorator):
    def __init__(self, client: LLMClient, retries: int = 3):
        super().__init__(client)
        self._retries = retries

    def chat(self, system: str, user: str) -> str:
        for attempt in range(1, self._retries + 1):
            try:
                return self._client.chat(system, user)
            except Exception as e:
                print(f"[RETRY] Attempt {attempt} failed: {e}")
                if attempt == self._retries:
                    raise
        return ""


if __name__ == "__main__":
    system = "You are a helpful assistant."
    user = "What is the capital of France?"

    # Stack decorators — each wraps the previous
    client = ClaudeClient()
    client = CachingDecorator(client)
    client = LoggingDecorator(client)
    client = RetryDecorator(client)

    print("=== First call (cache miss) ===")
    client.chat(system, user)

    print()
    print("=== Second call (cache hit) ===")
    client.chat(system, user)
