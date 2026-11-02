import json

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from app.providers.fixtures import FIXTURES
from app.providers.ollama import OllamaAnalysisProvider

EX_FAMILY = "Ammi, mera phone kharab ho gaya hai. Main naye number se baat kar raha hoon. Emergency hai, Rs 50000 bhej dein. Kisi ko mat batana."


@pytest.fixture
def anyio_backend():
    return "asyncio"


def valid_assessment() -> dict:
    return json.loads(json.dumps(FIXTURES["family_emergency"]["en"]))


def ollama_ok(content) -> httpx.Response:
    body = content if isinstance(content, str) else json.dumps(content)
    return httpx.Response(200, json={"message": {"role": "assistant", "content": body}})


def make_settings(**kw) -> Settings:
    return Settings(**{"ai_provider": "ollama", **kw})


def ollama_client(handler, **kw) -> tuple[TestClient, list]:
    seen: list[httpx.Request] = []

    def wrapped(req: httpx.Request):
        seen.append(req)
        return handler(req)

    s = make_settings(**kw)
    provider = OllamaAnalysisProvider(s, transport=httpx.MockTransport(wrapped))
    return TestClient(create_app(s, provider)), seen


@pytest.fixture
def mock_client():
    return TestClient(create_app(make_settings(ai_provider="mock")))
