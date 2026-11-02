import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

LOOPBACK = {"127.0.0.1", "localhost", "::1"}


class ConfigError(ValueError):
    pass


def _load_dotenv(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


@dataclass(frozen=True)
class Settings:
    ai_provider: str = "ollama"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2:3b"
    ollama_context_size: int = 2048
    ollama_max_output_tokens: int = 600
    ollama_timeout_seconds: float = 180.0
    ollama_keep_alive: str = "30m"
    persistence_mode: str = "memory"
    frontend_origin: str = "http://localhost:5173"


def _int(env: dict, key: str, default: int) -> int:
    try:
        return int(env.get(key, default))
    except ValueError as e:
        raise ConfigError(f"{key} must be an integer") from e


def settings_from_env(env: dict | None = None) -> Settings:
    env = dict(os.environ if env is None else env)
    try:
        timeout = float(env.get("OLLAMA_TIMEOUT_SECONDS", 180))
    except ValueError as e:
        raise ConfigError("OLLAMA_TIMEOUT_SECONDS must be a number") from e
    s = Settings(
        ai_provider=env.get("AI_PROVIDER", "ollama").strip().lower(),
        ollama_base_url=env.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/"),
        ollama_model=env.get("OLLAMA_MODEL", "llama3.2:3b").strip(),
        ollama_context_size=_int(env, "OLLAMA_CONTEXT_SIZE", 2048),
        ollama_max_output_tokens=_int(env, "OLLAMA_MAX_OUTPUT_TOKENS", 600),
        ollama_timeout_seconds=timeout,
        ollama_keep_alive=env.get("OLLAMA_KEEP_ALIVE", "30m").strip(),
        persistence_mode=env.get("PERSISTENCE_MODE", "memory").strip().lower(),
        frontend_origin=env.get("FRONTEND_ORIGIN", "http://localhost:5173").rstrip("/"),
    )
    if s.ai_provider not in {"ollama", "mock"}:
        raise ConfigError("AI_PROVIDER must be 'ollama' or 'mock'")
    if not re.fullmatch(r"-?\d+[smh]?", s.ollama_keep_alive):
        raise ConfigError("OLLAMA_KEEP_ALIVE must look like 30m, 1h, 300s or -1")
    if s.persistence_mode != "memory":
        raise ConfigError("Only PERSISTENCE_MODE=memory is implemented (Firebase is not).")
    if not s.ollama_model.lower().startswith("llama"):
        raise ConfigError("OLLAMA_MODEL must be a Meta Llama tag (e.g. llama3.2:3b). Non-Meta models are not allowed.")
    if (urlparse(s.ollama_base_url).hostname or "") not in LOOPBACK:
        raise ConfigError("OLLAMA_BASE_URL must point to a loopback address (local Ollama only).")
    return s


def load_settings() -> Settings:
    _load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    return settings_from_env()
