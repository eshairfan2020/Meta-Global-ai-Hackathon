import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from .config import Settings, load_settings
from .errors import AppError, BadInput
from .examples import EXAMPLES
from .providers.base import AnalysisProvider
from .providers.mock import MockAnalysisProvider
from .pipeline import run_pipeline
from .providers.ollama import OllamaAnalysisProvider
from .report import render_report
from .schemas import AnalyzeRequest, CaseView, ModelStatus, VerificationRequest, VerificationStatus
from .store import CaseStore

log = logging.getLogger("rasta")  # never log message text or model output


def build_provider(s: Settings) -> AnalysisProvider:
    return MockAnalysisProvider() if s.ai_provider == "mock" else OllamaAnalysisProvider(s)


def _err(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


def create_app(settings: Settings | None = None, provider: AnalysisProvider | None = None) -> FastAPI:
    settings = settings or load_settings()
    provider = provider or build_provider(settings)  # provider is chosen by server config only
    store = CaseStore()
    app = FastAPI(title="Rasta backend", version="0.1.0")

    origins = {settings.frontend_origin, "http://127.0.0.1:5173", "http://localhost:5173"}
    app.add_middleware(CORSMiddleware, allow_origins=sorted(origins), allow_methods=["GET", "POST", "DELETE"],
                       allow_headers=["Content-Type"])

    @app.exception_handler(AppError)
    async def _app_error(_: Request, exc: AppError):
        return _err(exc.status, exc.code, exc.message)

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError):  # do not echo input back
        return _err(422, "invalid_input", "The request was not valid.")

    @app.exception_handler(Exception)
    async def _unhandled(_: Request, exc: Exception):
        log.error("unhandled error: %s", type(exc).__name__)
        return _err(500, "internal_error", "Something went wrong.")

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/api/model-status", response_model=ModelStatus)
    async def model_status():
        return await provider.status()

    @app.get("/api/examples")
    async def examples():
        return EXAMPLES

    @app.post("/api/analyze", response_model=CaseView)
    async def analyze(req: AnalyzeRequest):
        r = await run_pipeline(provider, req.text, req.language)
        return store.create(
            language=req.language, is_synthetic=r.example is not None,
            example_id=r.example["id"] if r.example else None,
            provider=provider.name, model=r.out.model, inference=r.out.inference, latency_ms=r.out.latency_ms,
            redactions=r.redactions, quotes_removed=r.quotes_removed, amount_cleared=r.amount_cleared,
            rules_triggered=r.rules_triggered, rule_adjusted=r.rule_adjusted,
            assessment=r.assessment, verification={"status": VerificationStatus.not_checked, "events": []},
        )

    @app.post("/api/warmup")
    async def warmup():
        return await provider.warmup()

    @app.get("/api/cases/{case_id}", response_model=CaseView)
    async def get_case(case_id: str):
        return store.get(case_id)

    @app.post("/api/cases/{case_id}/verification", response_model=CaseView)
    async def record_verification(case_id: str, req: VerificationRequest):
        if req.status == VerificationStatus.not_checked:
            raise BadInput("Choose an outcome to record.")
        return store.record(case_id, req.status)

    @app.get("/api/cases/{case_id}/export", response_class=HTMLResponse)
    async def export(case_id: str):
        html = render_report(store.get(case_id))
        return HTMLResponse(html, headers={"Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'",
                                           "Cache-Control": "no-store"})

    @app.delete("/api/cases/{case_id}")
    async def delete_case(case_id: str):
        store.delete(case_id)
        return {"deleted": True}

    return app


app = create_app()
