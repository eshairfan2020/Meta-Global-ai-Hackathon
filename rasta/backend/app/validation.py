from .schemas import Assessment
from .textproc import amount_supported, find_quote


def postprocess(a: Assessment, text: str) -> tuple[Assessment, int, bool]:
    """Backend checks on model output against the analyzed (redacted, normalized) input.
    - Warning signals whose quote is not present in the input are removed.
    - An amount that does not appear in the input is cleared.
    The model's risk band is never changed here."""
    kept, removed = [], 0
    for sig in a.warning_signals:
        real = find_quote(sig.source_quote, text)
        if real is None:
            removed += 1
        else:
            kept.append(sig.model_copy(update={"source_quote": real}))
    facts = a.observed_facts
    cleared = False
    if facts.amount is not None and not amount_supported(facts.amount, text):
        facts = facts.model_copy(update={"amount": None})
        cleared = True
    return a.model_copy(update={"warning_signals": kept, "observed_facts": facts}), removed, cleared
