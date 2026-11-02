import re

MAX_CHARS = 3000
_WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    return _WS.sub(" ", text).strip()


_CODE_AFTER = re.compile(r"(?i)\b(code|otp|pin|cvv|password|passcode|verification)\b([^\d\n]{0,25})(\d{3,8})\b")
_CODE_BEFORE = re.compile(r"(?i)\b(\d{4,8})\b([^\d\n]{0,20}\b(?:code|otp|pin)\b)")
_CNIC = re.compile(r"\b\d{5}-?\d{7}-?\d\b")
_LONG_NUM = re.compile(r"\b\d{10,16}\b")


def redact(text: str) -> tuple[str, int]:
    """Best-effort masking of code-like values. Not a guarantee."""
    n = 0

    def sub(pattern, repl, s):
        nonlocal n
        s, c = pattern.subn(repl, s)
        n += c
        return s

    text = sub(_CODE_AFTER, r"\1\2[REDACTED_CODE]", text)
    text = sub(_CODE_BEFORE, r"[REDACTED_CODE]\2", text)
    text = sub(_CNIC, "[REDACTED_ID]", text)
    text = sub(_LONG_NUM, "[REDACTED_NUMBER]", text)
    return text, n


_QUOTE_CHARS = " \"'“”‘’"


def find_quote(quote: str, text: str) -> str | None:
    """Return the matching substring of `text` (original casing) or None if unsupported."""
    nq = normalize(quote).strip(_QUOTE_CHARS)
    if len(nq) < 3:
        return None
    low = text.lower()
    idx = low.find(nq.lower())
    if idx < 0:
        return None
    return text[idx : idx + len(nq)] if len(low) == len(text) else nq


_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def amount_supported(amount: str, text: str) -> bool:
    nums = [n.replace(",", "") for n in _NUM.findall(amount)]
    if nums:
        in_text = {n.replace(",", "") for n in _NUM.findall(text)}
        return all(n in in_text for n in nums)
    return normalize(amount).lower() in text.lower()
