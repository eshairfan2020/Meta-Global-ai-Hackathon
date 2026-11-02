"""Shared analysis pipeline used by the API and the evaluation script, so both do exactly the same steps."""
from dataclasses import dataclass

from .errors import BadInput
from .examples import match_example
from .providers.base import AnalysisProvider, ProviderOutput
from .rules import apply_rules
from .schemas import Assessment, Language, RiskBand
from .textproc import MAX_CHARS, normalize, redact
from .validation import postprocess


@dataclass
class PipelineResult:
    example: dict | None
    redactions: int
    out: ProviderOutput
    raw_band: RiskBand  # what the model said, before backend checks and rules
    assessment: Assessment
    quotes_removed: int
    amount_cleared: bool
    rules_triggered: list[str]
    rule_adjusted: bool


async def run_pipeline(provider: AnalysisProvider, raw_text: str, language: Language) -> PipelineResult:
    text = normalize(raw_text)
    if not text:
        raise BadInput("Please paste a message to analyze.")
    if len(text) > MAX_CHARS:
        raise BadInput(f"The message is too long (maximum {MAX_CHARS} characters).")
    text, redactions = redact(text)
    example = match_example(text)
    out = await provider.analyze(text, language)  # technical failures propagate as errors
    raw_band = out.assessment.risk_band
    assessment, removed, cleared = postprocess(out.assessment, text)
    assessment, triggered, adjusted = apply_rules(assessment, text, language)
    return PipelineResult(example, redactions, out, raw_band, assessment, removed, cleared, triggered, adjusted)
