import pytest
from pydantic import ValidationError

from app.config import ConfigError, settings_from_env
from app.schemas import Assessment
from app.textproc import amount_supported, find_quote, normalize, redact
from tests.conftest import valid_assessment


def test_normalize_whitespace():
    assert normalize("  a \n\n b\t c ") == "a b c"


def test_redact_codes_ids_numbers():
    t, n = redact("Your verification code is 482913. Also pin: 1234 and CNIC 35202-1234567-1 and 03001234567890")
    assert "482913" not in t and "1234 " not in t.replace("[REDACTED_CODE]", "")
    assert "35202" not in t and "03001234567890" not in t
    assert n >= 4
    t2, _ = redact("482913 is your OTP")
    assert "482913" not in t2


def test_redact_leaves_amounts():
    t, n = redact("Rs 50000 bhej dein")
    assert t == "Rs 50000 bhej dein" and n == 0


def test_find_quote():
    text = "Kisi ko mat batana. Emergency hai"
    assert find_quote("“kisi ko mat batana”", text) == "Kisi ko mat batana"
    assert find_quote("Send money now", text) is None
    assert find_quote("ab", text) is None


def test_amount_supported():
    assert amount_supported("Rs 50,000", "bhej dein Rs 50000")
    assert not amount_supported("Rs 99999", "bhej dein Rs 50000")


def test_schema_valid_and_enums():
    Assessment.model_validate(valid_assessment())
    schema = Assessment.model_json_schema()
    assert set(schema["$defs"]["RiskBand"]["enum"]) == {"high_concern", "some_concern", "insufficient_evidence"}
    assert "unclear" in schema["$defs"]["ScamCategory"]["enum"]


@pytest.mark.parametrize("mutate", [
    lambda d: d.update(risk_band="definitely_scam"),
    lambda d: d.update(scam_category="high_concern | some_concern"),
    lambda d: d.update(warning_signals=d["warning_signals"] * 2),
    lambda d: d.update(recommended_actions=["a", "b", "c", "d"]),
    lambda d: d.update(extra_field=1),
    lambda d: d.update(safe_reply="x" * 501),
    lambda d: d.pop("uncertainty"),
])
def test_schema_rejects_bad(mutate):
    d = valid_assessment()
    mutate(d)
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)


def test_config_rejects_non_meta_model():
    with pytest.raises(ConfigError):
        settings_from_env({"OLLAMA_MODEL": "mistral:7b"})


def test_config_rejects_remote_ollama_and_bad_provider():
    with pytest.raises(ConfigError):
        settings_from_env({"OLLAMA_BASE_URL": "http://example.com:11434"})
    with pytest.raises(ConfigError):
        settings_from_env({"AI_PROVIDER": "openai"})


def test_config_defaults():
    s = settings_from_env({})
    assert (s.ai_provider, s.ollama_model, s.ollama_context_size, s.ollama_max_output_tokens) == ("ollama", "llama3.2:3b", 2048, 600)
    assert settings_from_env({"OLLAMA_MODEL": "llama3.2:1b"}).ollama_model == "llama3.2:1b"
