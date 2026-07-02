"""
Proxy Pattern
-------------
Provides a surrogate that controls access to another object.
The proxy implements the same interface as the real object.

Three common proxy types:
  - Virtual proxy: delays expensive initialization until needed
  - Protection proxy: controls access based on permissions
  - Rate limiting proxy: throttles calls to the real object

Use case: sit a proxy in front of an LLM client to handle
lazy loading, access control, and rate limiting.
"""

import time
from abc import ABC, abstractmethod
from collections import deque


# ── Subject interface ──────────────────────────────────────────────────────────

class LLMClient(ABC):
    @abstractmethod
    def chat(self, system: str, user: str) -> str:
        pass


# ── Real subject — expensive to initialize ─────────────────────────────────────

class ClaudeClient(LLMClient):
    def __init__(self):
        print("  [ClaudeClient] Initializing... (loading SDK, validating API key)")
        time.sleep(0.2)  # simulate expensive startup

    def chat(self, system: str, user: str) -> str:
        return f"[Claude] {user[:40]}"


# ── Virtual proxy — delays initialization until first use ─────────────────────

class LazyLLMProxy(LLMClient):
    def __init__(self):
        self._client: ClaudeClient | None = None  # not created yet

    def chat(self, system: str, user: str) -> str:
        if self._client is None:
            print("  [LazyProxy] First call — initializing real client now")
            self._client = ClaudeClient()
        return self._client.chat(system, user)


# ── Protection proxy — checks permissions before forwarding ───────────────────

class ProtectedLLMProxy(LLMClient):
    def __init__(self, client: LLMClient, allowed_roles: set[str]):
        self._client = client
        self._allowed_roles = allowed_roles

    def chat(self, system: str, user: str, role: str = "guest") -> str:
        if role not in self._allowed_roles:
            raise PermissionError(f"Role '{role}' is not allowed to call the LLM.")
        print(f"  [ProtectionProxy] Access granted for role='{role}'")
        return self._client.chat(system, user)


# ── Rate limiting proxy — throttles calls per second ──────────────────────────

class RateLimitedLLMProxy(LLMClient):
    def __init__(self, client: LLMClient, max_calls: int, window_seconds: float):
        self._client = client
        self._max_calls = max_calls
        self._window = window_seconds
        self._timestamps: deque = deque()

    def chat(self, system: str, user: str) -> str:
        now = time.time()
        # drop timestamps outside the window
        while self._timestamps and now - self._timestamps[0] > self._window:
            self._timestamps.popleft()

        if len(self._timestamps) >= self._max_calls:
            raise RuntimeError(
                f"Rate limit exceeded: {self._max_calls} calls per {self._window}s"
            )

        self._timestamps.append(now)
        print(f"  [RateLimitProxy] Call {len(self._timestamps)}/{self._max_calls}")
        return self._client.chat(system, user)


if __name__ == "__main__":
    system = "You are a helpful assistant."

    # 1. Virtual proxy — real client created only on first chat()
    print("=== Virtual Proxy ===")
    proxy = LazyLLMProxy()
    print("Proxy created — no client yet")
    print(proxy.chat(system, "What is RAG?"))       # client created here
    print(proxy.chat(system, "What is a vector DB?"))  # reused
    print()

    # 2. Protection proxy
    print("=== Protection Proxy ===")
    real = ClaudeClient()
    protected = ProtectedLLMProxy(real, allowed_roles={"admin", "engineer"})
    print(protected.chat(system, "Summarize this.", role="admin"))
    try:
        protected.chat(system, "Summarize this.", role="guest")
    except PermissionError as e:
        print(f"  Blocked: {e}")
    print()

    # 3. Rate limiting proxy
    print("=== Rate Limiting Proxy ===")
    rate_limited = RateLimitedLLMProxy(ClaudeClient(), max_calls=3, window_seconds=5)
    for i in range(4):
        try:
            print(rate_limited.chat(system, f"Question {i+1}"))
        except RuntimeError as e:
            print(f"  Blocked: {e}")
