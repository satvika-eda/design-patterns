"""
Thread-Safe Singleton
---------------------
Same idea but safe when multiple threads try to create the instance simultaneously.
Relevant when your AI app uses async workers or parallel inference calls.
"""

import threading


class ModelConfigManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # double-checked locking
                    cls._instance = super().__new__(cls)
                    cls._instance._config = {
                        "model": "claude-sonnet-4-6",
                        "temperature": 0.7,
                        "max_tokens": 2048,
                    }
        return cls._instance

    def get(self, key):
        return self._config.get(key)

    def set(self, key, value):
        self._config[key] = value


if __name__ == "__main__":
    instances = []

    def create():
        instances.append(ModelConfigManager())

    threads = [threading.Thread(target=create) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("All same instance?", len(set(id(i) for i in instances)) == 1)  # True
