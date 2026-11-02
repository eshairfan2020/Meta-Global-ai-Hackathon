from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

from ..schemas import Assessment, Language, ModelStatus


@dataclass
class ProviderOutput:
    assessment: Assessment
    model: str | None
    inference: Literal["real", "simulated"]
    latency_ms: int | None
    attempts: int = 1  # model requests used (2 = one correction retry)


class AnalysisProvider(ABC):
    name: Literal["ollama", "mock"]

    @abstractmethod
    async def analyze(self, text: str, language: Language) -> ProviderOutput: ...

    async def warmup(self) -> dict:
        return {"warmed": False, "model": None, "detail": "No model to warm up in this mode."}

    @abstractmethod
    async def status(self) -> ModelStatus: ...
