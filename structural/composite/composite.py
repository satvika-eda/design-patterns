"""
Composite Pattern
-----------------
Composes objects into tree structures to represent part-whole hierarchies.
Lets clients treat individual objects and compositions uniformly.

Use case: agent pipeline tree — a pipeline can be a single task or a group
of tasks (including nested pipelines). Run them all with the same interface.
"""

from abc import ABC, abstractmethod


# ── Component interface ────────────────────────────────────────────────────────

class PipelineComponent(ABC):
    @abstractmethod
    def run(self, input_text: str) -> str:
        pass

    @abstractmethod
    def describe(self, indent: int = 0) -> str:
        pass


# ── Leaf — a single atomic task ────────────────────────────────────────────────

class Task(PipelineComponent):
    def __init__(self, name: str, system_prompt: str):
        self._name = name
        self._system_prompt = system_prompt

    def run(self, input_text: str) -> str:
        return f"[{self._name}] processed: {input_text[:40]}..."

    def describe(self, indent: int = 0) -> str:
        return " " * indent + f"- Task: {self._name}"


# ── Composite — a group of components (can contain tasks or other pipelines) ───

class Pipeline(PipelineComponent):
    def __init__(self, name: str, sequential: bool = True):
        self._name = name
        self._sequential = sequential
        self._components: list[PipelineComponent] = []

    def add(self, component: PipelineComponent) -> "Pipeline":
        self._components.append(component)
        return self

    def run(self, input_text: str) -> str:
        results = []
        current = input_text
        for component in self._components:
            result = component.run(current)
            results.append(result)
            if self._sequential:
                current = result  # output of one feeds into the next
        return "\n".join(results)

    def describe(self, indent: int = 0) -> str:
        mode = "sequential" if self._sequential else "parallel"
        lines = [" " * indent + f"+ Pipeline: {self._name} ({mode})"]
        for component in self._components:
            lines.append(component.describe(indent + 2))
        return "\n".join(lines)


if __name__ == "__main__":
    # Individual tasks (leaves)
    chunker    = Task("Chunker",    "Split text into chunks.")
    embedder   = Task("Embedder",   "Embed each chunk.")
    retriever  = Task("Retriever",  "Retrieve top-k chunks.")
    reranker   = Task("Reranker",   "Rerank retrieved chunks.")
    llm        = Task("LLM",        "Generate answer from context.")
    guardrails = Task("Guardrails", "Check output for safety.")

    # Sub-pipeline: ingestion (sequential)
    ingestion = Pipeline("Ingestion").add(chunker).add(embedder)

    # Sub-pipeline: retrieval (sequential)
    retrieval = Pipeline("Retrieval").add(retriever).add(reranker)

    # Top-level RAG pipeline — contains sub-pipelines and tasks
    rag = Pipeline("RAG Pipeline").add(ingestion).add(retrieval).add(llm).add(guardrails)

    # Treat the whole tree as one component — same interface as a single Task
    print("=== Pipeline structure ===")
    print(rag.describe())
    print()

    print("=== Running pipeline ===")
    output = rag.run("What is retrieval augmented generation?")
    print(output)
