"""
Adapter Pattern
---------------
Converts the interface of a class into another interface that clients expect.
Lets incompatible interfaces work together.

Use case: each LLM provider SDK has a completely different API.
The Adapter wraps each one behind a consistent interface your pipeline uses.
"""

from abc import ABC, abstractmethod


# ── Target interface — what your pipeline expects ──────────────────────────────

class LLMClient(ABC):
    @abstractmethod
    def chat(self, system: str, user: str) -> str:
        pass


# ── Adaptees — third-party SDKs with their own incompatible interfaces ─────────

class AnthropicSDK:
    """Simulates the real Anthropic SDK interface."""
    def messages_create(self, model: str, max_tokens: int, system: str, messages: list) -> dict:
        user_text = messages[0]["content"]
        return {
            "content": [{"text": f"[Anthropic] system='{system}' user='{user_text}'"}]
        }


class OpenAISDK:
    """Simulates the real OpenAI SDK interface."""
    def chat_completions_create(self, model: str, messages: list) -> dict:
        system_text = messages[0]["content"]
        user_text = messages[1]["content"]
        return {
            "choices": [{"message": {"content": f"[OpenAI] system='{system_text}' user='{user_text}'"}}]
        }


# ── Adapters — wrap each SDK behind the target interface ───────────────────────

class AnthropicAdapter(LLMClient):
    def __init__(self, model: str = "claude-sonnet-4-6", max_tokens: int = 1024):
        self._sdk = AnthropicSDK()
        self._model = model
        self._max_tokens = max_tokens

    def chat(self, system: str, user: str) -> str:
        response = self._sdk.messages_create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response["content"][0]["text"]


class OpenAIAdapter(LLMClient):
    def __init__(self, model: str = "gpt-4o"):
        self._sdk = OpenAISDK()
        self._model = model

    def chat(self, system: str, user: str) -> str:
        response = self._sdk.chat_completions_create(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response["choices"][0]["message"]["content"]


# ── Pipeline — only knows about LLMClient, never about the SDKs ───────────────

class SummarizationPipeline:
    def __init__(self, client: LLMClient):
        self._client = client

    def summarize(self, text: str) -> str:
        return self._client.chat(
            system="You are a summarization assistant. Be concise.",
            user=f"Summarize this: {text}",
        )


if __name__ == "__main__":
    text = "The transformer architecture revolutionized NLP by introducing self-attention..."

    for name, client in [
        ("Anthropic", AnthropicAdapter()),
        ("OpenAI", OpenAIAdapter()),
    ]:
        pipeline = SummarizationPipeline(client)
        print(f"[{name}]", pipeline.summarize(text))
