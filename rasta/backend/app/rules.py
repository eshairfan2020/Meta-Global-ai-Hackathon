"""Deterministic safety rule (plain code, NOT a model call).

If a message clearly asks the reader to share/send/read out a login or verification code, the final
result can never be below high_concern. A small local model can miss this, so the floor is enforced here.
The rule is transparent: the case reports `rules_triggered` and `rule_adjusted`."""
import re

from .schemas import Assessment, Language, RiskBand, ScamCategory, WarningSignal

_CODE = r"\b(?:otp|pin|passcode|password|code)\b"
_VERB_LONG = (r"\b(?:send|share|give|tell|read|forward|provide|text|dictate|reply|"
              r"bata\w*|btao|bhej\w*|dein|dijiye|dena|likh\w*|suna\w*)\b")
_VERB_SHORT = r"\b(?:de|do)\b"

# verb ... code   |   code ... verb   |   code ... de/do (short gap only)
_PATTERNS = [
    re.compile(rf"{_VERB_LONG}[^.!?\n]{{0,50}}?{_CODE}", re.I),
    re.compile(rf"{_CODE}[^.!?\n]{{0,80}}?{_VERB_LONG}", re.I),
    re.compile(rf"{_CODE}[^.!?\n]{{0,25}}?{_VERB_SHORT}", re.I),
]

_NEG = r"(?:not|never|dont|don't|don’t|without|avoid|nahi|nahin|mat|na)"
_PRE = re.compile(rf"\b{_NEG}\s+(?:\w+\s+)?$", re.I)
_POST = re.compile(rf"^\W*(?:\w+\W+)?{_NEG}\b", re.I)
_INSIDE = re.compile(rf"\b{_NEG}\b", re.I)


def _negated(text: str, s: int, e: int) -> bool:
    """e.g. 'Never share your OTP', 'code kisi ko share na karein' are warnings, not requests."""
    return bool(_PRE.search(text[max(0, s - 30):s]) or _POST.match(text[e:e + 16]) or _INSIDE.search(text[s:e]))


def detect_code_request(text: str) -> str | None:
    """Return the exact matching span of `text`, or None."""
    for pat in _PATTERNS:
        for m in pat.finditer(text):
            if not _negated(text, m.start(), m.end()):
                return m.group(0).strip()
    return None


_L = {
    Language.en: dict(
        label="Login code requested (built-in rule)",
        expl="The message asks you to share a code. Genuine banks and apps never need you to read out or send a login code.",
        uncertainty="Rasta cannot verify who sent this, but a request for a login code is a serious warning sign.",
        action="Do not share the code with anyone.",
    ),
    Language.ur: dict(
        label="Login code manga ja raha hai (built-in rule)",
        expl="Message mein code batane ya bhejne ko kaha gaya hai. Asli bank ya app ko aapse login code poochne ki zaroorat nahi hoti.",
        uncertainty="Rasta bhejne wale ki tasdeeq nahi kar sakta, lekin login code ki darkhwast ek sanjeeda warning nishani hai.",
        action="Code kisi ko na dein.",
    ),
}


def apply_rules(a: Assessment, text: str, language: Language) -> tuple[Assessment, list[str], bool]:
    """Returns (assessment, rules_triggered, adjusted). `adjusted` is True only if the rule changed the result."""
    span = detect_code_request(text)
    if span is None:
        return a, [], False
    s = _L[language]
    upd: dict = {}
    facts = a.observed_facts
    raised = a.risk_band != RiskBand.high_concern
    if not facts.verification_code_requested:
        facts = facts.model_copy(update={"verification_code_requested": True})
        upd["observed_facts"] = facts
    if raised:
        upd["risk_band"] = RiskBand.high_concern
        upd["uncertainty"] = s["uncertainty"]
    if a.scam_category == ScamCategory.unclear:
        upd["scam_category"] = ScamCategory.otp_theft
    if not upd:
        return a, ["code_request"], False  # the model already got it right; nothing changed

    sigs = list(a.warning_signals)
    low = span.lower()
    if not any(low in x.source_quote.lower() or x.source_quote.lower() in low for x in sigs):
        sigs = [WarningSignal(label=s["label"], source_quote=span[:300], explanation=s["expl"])] + sigs[:2]
    upd["warning_signals"] = sigs
    if raised:
        upd["recommended_actions"] = ([s["action"]] + [x for x in a.recommended_actions if x != s["action"]])[:3]
    return a.model_copy(update=upd), ["code_request"], True
