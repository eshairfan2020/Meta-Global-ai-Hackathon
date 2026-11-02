import json

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import ConfigError, settings_from_env
from app.main import create_app
from app.providers.ollama import OllamaAnalysisProvider
from app.rules import apply_rules, detect_code_request
from app.schemas import Assessment, Language, RiskBand
from evaluation.cases import CASES
from evaluation.run_eval import evaluate, summarize, to_markdown
from tests.conftest import make_settings, ollama_client, ollama_ok, valid_assessment

pytestmark_async = pytest.mark.anyio


# ---------- deterministic safety rule ----------
@pytest.mark.parametrize("c", CASES, ids=lambda c: c["id"])
def test_rule_matches_eval_labels(c):
    assert (detect_code_request(c["text"]) is not None) == c["code"], c["text"]


@pytest.mark.parametrize("text", [
    "Never share your OTP with anyone.",
    "Please do not send me your PIN, we never ask for it.",
    "Code kisi ko share na karein.",
    "Apna OTP kisi ko mat batana.",
    "Your OTP is [REDACTED_CODE], valid for 5 minutes.",
    "Dress code for the event is formal.",
])
def test_rule_ignores_warnings_and_non_requests(text):
    assert detect_code_request(text) is None


def test_rule_still_fires_after_unrelated_secrecy_phrase():
    assert detect_code_request("Kisi ko mat batana. Apna OTP bata dein.") is not None


def _low_assessment() -> Assessment:
    d = valid_assessment()
    d.update(risk_band="insufficient_evidence", scam_category="unclear", warning_signals=[],
             recommended_actions=["Wait and see."])
    d["observed_facts"]["verification_code_requested"] = False
    return Assessment.model_validate(d)


def test_rule_raises_a_missed_code_request():
    text = "Main bank se hoon. Apna OTP bata dein."
    a, trig, adj = apply_rules(_low_assessment(), text, Language.en)
    assert adj and trig == ["code_request"]
    assert a.risk_band == RiskBand.high_concern and a.scam_category.value == "otp_theft"
    assert a.observed_facts.verification_code_requested is True
    assert a.warning_signals[0].source_quote in text  # quote is real text from the message
    assert a.recommended_actions[0] == "Do not share the code with anyone." and len(a.recommended_actions) <= 3
    Assessment.model_validate(a.model_dump())  # still schema-valid


def test_rule_is_localized():
    a, _, _ = apply_rules(_low_assessment(), "Apna OTP bata dein.", Language.ur)
    assert "Login code" in a.warning_signals[0].label and "zaroorat" in a.warning_signals[0].explanation


def test_rule_noop_when_model_already_correct():
    good = Assessment.model_validate({**valid_assessment(), "scam_category": "otp_theft"})
    good = good.model_copy(update={"observed_facts": good.observed_facts.model_copy(update={"verification_code_requested": True})})
    a, trig, adj = apply_rules(good, "Apna OTP bata dein.", Language.en)
    assert a == good and trig == ["code_request"] and adj is False


def test_rule_not_applied_to_benign():
    a, trig, adj = apply_rules(_low_assessment(), "Kal meeting 3 baje hai.", Language.en)
    assert trig == [] and adj is False and a.risk_band == RiskBand.insufficient_evidence


def test_api_enforces_floor_over_a_model_that_misses_it():
    low = _low_assessment().model_dump(mode="json")
    c, _ = ollama_client(lambda r: ollama_ok(low))
    j = c.post("/api/analyze", json={"text": "Main bank se hoon. Apna OTP bata dein.", "language": "en"}).json()
    assert j["assessment"]["risk_band"] == "high_concern"
    assert j["rule_adjusted"] is True and j["rules_triggered"] == ["code_request"]
    cid = j["case_id"]
    assert "built-in rule" in c.get(f"/api/cases/{cid}/export").text


def test_api_does_not_touch_benign_low_result():
    low = _low_assessment().model_dump(mode="json")
    c, _ = ollama_client(lambda r: ollama_ok(low))
    j = c.post("/api/analyze", json={"text": "Kal meeting 3 baje hai.", "language": "en"}).json()
    assert j["assessment"]["risk_band"] == "insufficient_evidence" and j["rule_adjusted"] is False and j["rules_triggered"] == []


# ---------- keep_alive, warmup, attempts ----------
def test_config_keep_alive():
    assert settings_from_env({}).ollama_keep_alive == "30m"
    assert settings_from_env({"OLLAMA_KEEP_ALIVE": "-1"}).ollama_keep_alive == "-1"
    with pytest.raises(ConfigError):
        settings_from_env({"OLLAMA_KEEP_ALIVE": "forever"})


def test_chat_payload_includes_keep_alive():
    c, seen = ollama_client(lambda r: ollama_ok(valid_assessment()), ollama_keep_alive="10m")
    c.post("/api/analyze", json={"text": "abc def ghi", "language": "en"})
    assert json.loads(seen[0].content)["keep_alive"] == "10m"


def test_warmup_endpoint_ollama_and_errors():
    c, seen = ollama_client(lambda r: httpx.Response(200, json={"done": True}))
    j = c.post("/api/warmup").json()
    assert j["warmed"] is True and j["model"] == "llama3.2:3b" and seen[0].url.path == "/api/generate"
    body = json.loads(seen[0].content)
    assert "prompt" not in body and body["keep_alive"] == "30m"
    c2, _ = ollama_client(lambda r: httpx.Response(404, json={"error": "nf"}))
    assert c2.post("/api/warmup").json()["error"]["code"] == "model_not_installed"

    def down(r):
        raise httpx.ConnectError("x")

    c3, _ = ollama_client(down)
    assert c3.post("/api/warmup").status_code == 503


def test_warmup_in_mock_mode_is_a_noop(mock_client):
    j = mock_client.post("/api/warmup").json()
    assert j["warmed"] is False


@pytest.mark.anyio
async def test_attempts_reported():
    n = []

    def h(req):
        n.append(1)
        return ollama_ok("{bad") if len(n) == 1 else ollama_ok(valid_assessment())

    p = OllamaAnalysisProvider(make_settings(), transport=httpx.MockTransport(h))
    assert (await p.analyze("abc def", Language.en)).attempts == 2
    p2 = OllamaAnalysisProvider(make_settings(), transport=httpx.MockTransport(lambda r: ollama_ok(valid_assessment())))
    assert (await p2.analyze("abc def", Language.en)).attempts == 1


# ---------- evaluation kit (mocked provider: tests the harness only) ----------
def test_eval_cases_are_well_formed():
    ids = [c["id"] for c in CASES]
    assert len(ids) == len(set(ids)) == 27
    assert {c["expected"] for c in CASES} == {"scam", "benign", "ambiguous"}
    assert all(len(c["text"]) < 3000 for c in CASES)


@pytest.mark.anyio
async def test_eval_harness_runs_and_summarizes():
    low = _low_assessment().model_dump(mode="json")  # a "bad model" that always says insufficient_evidence
    p = OllamaAnalysisProvider(make_settings(), transport=httpx.MockTransport(lambda r: ollama_ok(low)))
    rows = await evaluate(p, CASES, Language.en)
    s = summarize(rows)
    assert s["n"] == 27 and s["ok"] == 27 and s["first_try_valid"] == "27/27"
    n_scam = sum(c["expected"] == "scam" for c in CASES)
    n_code = sum(c["code"] for c in CASES)
    assert s["scam_missed_model"] == f"{n_scam}/{n_scam}"           # the fake model misses everything...
    assert s["code_high_model"] == f"0/{n_code}"
    assert s["code_high_final"] == f"{n_code}/{n_code}"              # ...but the safety rule catches every code request
    assert s["benign_false_alarm_final"] == "0/6"                    # and does not flag benign messages (incl. the bank OTP notice)
    md = to_markdown(s, rows, "TEST-MODEL", "en")
    assert "not** an accuracy claim" in md or "not an accuracy claim" in md.replace("**", "")


@pytest.mark.anyio
async def test_eval_records_technical_errors():
    def down(r):
        raise httpx.ConnectError("x")

    p = OllamaAnalysisProvider(make_settings(), transport=httpx.MockTransport(down))
    rows = await evaluate(p, CASES[:3], Language.en)
    s = summarize(rows)
    assert s["ok"] == 0 and s["errors"] == {"model_unavailable": 3}
