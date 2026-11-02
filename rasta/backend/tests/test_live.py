"""Opt-in live inference test. Requires Ollama running with the configured Meta Llama model:
    pytest -m live -s
It records latency and prints results; it does not assert accuracy."""
import asyncio

import pytest

from app.config import load_settings
from app.examples import EXAMPLES
from app.providers.ollama import OllamaAnalysisProvider
from app.schemas import Language
from app.textproc import normalize
from app.validation import postprocess

pytestmark = pytest.mark.live


@pytest.mark.parametrize("lang", [Language.en, Language.ur])
def test_live_examples(lang):
    s = load_settings()
    p = OllamaAnalysisProvider(s)

    async def run():
        st = await p.status()
        assert st.state == "ready", st.detail
        for ex in EXAMPLES:
            out = await p.analyze(normalize(ex["text"]), lang)
            a, removed, cleared = postprocess(out.assessment, normalize(ex["text"]))
            print(f"[{s.ollama_model}] {ex['id']} {lang.value}: band={a.risk_band.value} cat={a.scam_category.value} "
                  f"signals={len(a.warning_signals)} quotes_removed={removed} latency_ms={out.latency_ms}")

    asyncio.run(run())
