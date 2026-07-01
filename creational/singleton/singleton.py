"""
Singleton Pattern
-----------------
Ensures a class has only one instance and provides a global access point to it.

Use case: ModelConfigManager — one shared config object across your entire app.
"""


class ModelConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {
                "model": "claude-sonnet-4-6",
                "temperature": 0.7,
                "max_tokens": 2048,
                "api_key": "sk-...",
            }
        return cls._instance

    def get(self, key):
        return self._config.get(key)

    def set(self, key, value):
        self._config[key] = value

    def all(self):
        return dict(self._config)


if __name__ == "__main__":
    config1 = ModelConfigManager()
    config2 = ModelConfigManager()

    print("Same instance?", config1 is config2)  # True

    config1.set("temperature", 0.3)
    print("config2 sees the change:", config2.get("temperature"))  # 0.3

    print("Full config:", config1.all())
