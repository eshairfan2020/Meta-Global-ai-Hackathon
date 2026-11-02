from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Language(str, Enum):
    en = "en"
    ur = "ur"  # Roman Urdu


class RiskBand(str, Enum):
    high_concern = "high_concern"
    some_concern = "some_concern"
    insufficient_evidence = "insufficient_evidence"


class ScamCategory(str, Enum):
    family_impersonation = "family_impersonation"
    otp_theft = "otp_theft"
    fake_agent = "fake_agent"
    payment_request = "payment_request"
    job_visa_prize = "job_visa_prize"
    unclear = "unclear"


class VerificationStatus(str, Enum):
    not_checked = "not_checked"
    attempting_independent_contact = "attempting_independent_contact"
    user_recorded_confirmation = "user_recorded_confirmation"
    user_recorded_denial = "user_recorded_denial"
    inconclusive = "inconclusive"


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ObservedFacts(_Strict):
    claimed_identity: str | None = Field(max_length=200)
    requested_action: str | None = Field(max_length=250)
    amount: str | None = Field(max_length=100)
    urgency_present: bool
    secrecy_present: bool
    verification_code_requested: bool


class WarningSignal(_Strict):
    label: str = Field(max_length=100)
    source_quote: str = Field(max_length=300)
    explanation: str = Field(max_length=350)


class Assessment(_Strict):
    risk_band: RiskBand
    scam_category: ScamCategory
    observed_facts: ObservedFacts
    warning_signals: list[WarningSignal] = Field(max_length=3)
    uncertainty: str = Field(max_length=500)
    recommended_actions: list[str] = Field(max_length=3)
    safe_reply: str = Field(max_length=500)
    family_verification_suggested: bool


class AnalyzeRequest(_Strict):
    text: str = Field(max_length=20000)  # hard bound; the 3000-char limit is enforced after normalization
    language: Language = Language.en


class VerificationRequest(_Strict):
    status: VerificationStatus


class VerificationEvent(BaseModel):
    status: VerificationStatus
    timestamp: str


class VerificationState(BaseModel):
    status: VerificationStatus = VerificationStatus.not_checked
    events: list[VerificationEvent] = []


class CaseView(BaseModel):
    case_id: str
    created_at: str
    language: Language
    is_synthetic: bool
    example_id: str | None
    provider: Literal["ollama", "mock"]
    model: str | None  # exact Ollama tag for real inference; None for mock
    inference: Literal["real", "simulated"]
    latency_ms: int | None
    redactions: int
    quotes_removed: int
    amount_cleared: bool
    rules_triggered: list[str] = []
    rule_adjusted: bool = False
    assessment: Assessment
    verification: VerificationState


class ModelStatus(BaseModel):
    provider: Literal["ollama", "mock"]
    model: str | None
    state: Literal["ready", "unreachable", "model_not_installed", "mock"]
    detail: str
