"""
Flyweight Pattern
-----------------
Shares common state across many objects to reduce memory usage.
Splits object state into:
  - Intrinsic state: shared, immutable (stored in the flyweight)
  - Extrinsic state: unique per instance (passed in by the caller)

Use case: many agent workers share the same model config and tokenizer
(intrinsic) but each has its own session id and conversation history (extrinsic).
"""

import sys


# ── Flyweight — holds intrinsic (shared, immutable) state ─────────────────────

class ModelFlyweight:
    def __init__(self, model: str, tokenizer: str, max_tokens: int):
        self.model = model
        self.tokenizer = tokenizer      # in reality: a loaded tokenizer object
        self.max_tokens = max_tokens
        print(f"  [Flyweight] Created shared config for '{model}'")

    def run(self, system: str, user: str, session_id: str) -> str:
        """Extrinsic state (session_id, prompts) passed in — not stored here."""
        return f"[{self.model}] session={session_id} | {user[:30]}"


# ── Flyweight factory — ensures shared instances ───────────────────────────────

class ModelFlyweightFactory:
    _pool: dict[str, ModelFlyweight] = {}

    @classmethod
    def get(cls, model: str, tokenizer: str, max_tokens: int) -> ModelFlyweight:
        if model not in cls._pool:
            cls._pool[model] = ModelFlyweight(model, tokenizer, max_tokens)
        else:
            print(f"  [Factory] Reusing shared config for '{model}'")
        return cls._pool[model]

    @classmethod
    def pool_size(cls) -> int:
        return len(cls._pool)


# ── Agent worker — holds extrinsic (unique) state, shares intrinsic ───────────

class AgentWorker:
    def __init__(self, session_id: str, model_flyweight: ModelFlyweight):
        self.session_id = session_id
        self.history: list[str] = []        # extrinsic — unique per worker
        self._model = model_flyweight        # intrinsic — shared reference

    def chat(self, system: str, user: str) -> str:
        response = self._model.run(system, user, self.session_id)
        self.history.append(user)
        return response


if __name__ == "__main__":
    factory = ModelFlyweightFactory()

    # Spawn 5 workers — all using claude-sonnet-4-6
    # Without Flyweight: 5 separate model configs in memory
    # With Flyweight: 1 shared config, 5 workers
    workers = []
    for i in range(5):
        flyweight = factory.get("claude-sonnet-4-6", "cl100k", 4096)
        worker = AgentWorker(session_id=f"session-{i}", model_flyweight=flyweight)
        workers.append(worker)

    print(f"\nFlyweight pool size: {factory.pool_size()} (not 5)")
    print(f"All workers share same flyweight: "
          f"{len(set(id(w._model) for w in workers)) == 1}")

    # Add a second model — new flyweight created
    print()
    gpt_flyweight = factory.get("gpt-4o", "cl100k", 8192)
    gpt_worker = AgentWorker("session-gpt", gpt_flyweight)

    print(f"\nFlyweight pool size after adding GPT-4o: {factory.pool_size()}")

    # Run some chats
    print()
    print(workers[0].chat("You are helpful.", "What is RAG?"))
    print(workers[1].chat("You are helpful.", "Explain embeddings."))
    print(gpt_worker.chat("You are helpful.", "What is a transformer?"))

    # Memory comparison (approximate)
    print(f"\nWorkers in memory: {len(workers) + 1}")
    print(f"Shared flyweights in memory: {factory.pool_size()}")
    print(f"Flyweight object size: ~{sys.getsizeof(flyweight)} bytes (shared across all workers)")
