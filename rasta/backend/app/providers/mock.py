from ..errors import MockNoFixture
from ..examples import match_example
from ..schemas import Assessment, Language, ModelStatus
from .base import AnalysisProvider, ProviderOutput
from .fixtures import FIXTURES


class MockAnalysisProvider(AnalysisProvider):
    """Development provider. Returns predefined sample assessments for the four synthetic
    examples only. It never analyzes arbitrary text and never reuses an unrelated fixture."""

    name = "mock"

    async def analyze(self, text: str, language: Language) -> ProviderOutput:
        ex = match_example(text)
        if ex is None:
            raise MockNoFixture()
        data = FIXTURES[ex["id"]][language.value]
        return ProviderOutput(Assessment.model_validate(data), model=None, inference="simulated", latency_ms=None)

    async def status(self) -> ModelStatus:
        return ModelStatus(
            provider="mock", model=None, state="mock",
            detail="Mock mode: predefined sample assessments for the four synthetic examples. No model is running.",
        )
