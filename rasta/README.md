# Rasta — Pause. Verify. Proceed.

Mobile-first, bilingual (English / Roman Urdu), **non-chat** decision-support app for Pakistani WhatsApp users who
receive a suspicious request for money or a login code. Built for the Meta Global AI Developer Hackathon (Indie track,
submission via Cerebral Valley).

> Rasta helps families pause, verify independently, and preserve the evidence—before they decide to pay.

**Advisory only.** Rasta cannot block payments, recover accounts, prove identity, detect genuine voices, read WhatsApp
automatically, or guarantee that a request is safe. It never reports or accuses anyone.

## Model statement

This project uses **Meta Llama through Ollama on the developer's local Windows machine** (default tag `llama3.2:3b`;
`llama3.2:1b` can be selected explicitly). Demonstration inputs are synthetic. In Ollama mode, assessments are generated
by the running model. Mock mode uses predefined results and is labeled separately.

- Every model call at runtime goes to the local Ollama instance (`/api/chat`, loopback only). There is no other model:
  no hosted API, no non-Meta analysis/translation/transcription/embedding, and no fallback inference.
- The backend refuses to start if `OLLAMA_MODEL` is not a `llama*` tag or if `OLLAMA_BASE_URL` is not loopback.
- **Exact model tag tested: none yet** — see [docs/live-test-log.md](docs/live-test-log.md). Update this line only after a real run.
- This note does not claim that meeting the model requirement guarantees acceptance, scores, or a prize.

## Problem and target user

A relative “on a new number” asks for urgent money, or a fake bank agent asks for a login code. The problem is decision
pressure. Rasta slows that moment down: quoted warning signals, honest uncertainty, a safe reply to copy, a manual
independent family-verification checklist, a user-recorded outcome timeline, and a printable incident record.

## Architecture

```
React + Vite + TS + Tailwind (127.0.0.1:5173)
        │  fetch /api/*  (Vite dev proxy → backend)
        ▼
FastAPI (127.0.0.1:8000)  ── validates input (≤3000 chars), masks code-like values, rate-limits to 1 inference
        │
        ├── AnalysisProvider (chosen by server env AI_PROVIDER, never by the client)
        │     ├── OllamaAnalysisProvider ──HTTP──▶ Ollama (127.0.0.1:11434) ──▶ Meta Llama (local, CPU)
        │     └── MockAnalysisProvider   ──▶ predefined fixtures for the 4 synthetic examples only
        │
        ├── Backend checks: Pydantic schema, quote-in-input verification, amount-in-input check
        ├── In-memory case store (cleared on restart; no raw message stored)
        └── Incident export: server-built, HTML-escaped, print-friendly HTML (Print / Save as PDF)
```

Model output is data only: it is never executed or rendered as HTML and cannot trigger external actions.

## Prerequisites (Windows 10/11, PowerShell)

- Python 3.10+ (developed with 3.12)
- Node.js 20.19+ or 22.12+ (needed by Vite 8; developed with Node 22)
- [Ollama for Windows](https://ollama.com/download/windows)
- Roughly 2–3 GB free RAM for `llama3.2:3b` on CPU (1B uses less). No Docker, WSL or GPU required.

## Setup

**1. Install the model (you run this; the app never downloads weights):**
```powershell
ollama pull llama3.2:3b      # or: ollama pull llama3.2:1b
ollama list                  # confirm the tag is installed
```

**2. Backend**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # if blocked: Set-ExecutionPolicy -Scope Process Bypass
pip install -r requirements.txt
Copy-Item .env.example .env      # edit OLLAMA_MODEL / AI_PROVIDER if needed
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**3. Frontend** (second terminal)
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev                      # http://127.0.0.1:5173
```

Check `http://127.0.0.1:8000/api/model-status` — it reports `ready`, `model_not_installed`, `unreachable` or `mock`.

## Configuration (`backend/.env`)

| Variable | Default | Notes |
|---|---|---|
| `AI_PROVIDER` | `ollama` | `ollama` or `mock`. Server-controlled. No silent fallback between them. |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Must be loopback. |
| `OLLAMA_MODEL` | `llama3.2:3b` | Must be a Llama tag; `llama3.2:1b` allowed explicitly. |
| `OLLAMA_CONTEXT_SIZE` | `2048` | `num_ctx` |
| `OLLAMA_MAX_OUTPUT_TOKENS` | `600` | `num_predict` |
| `OLLAMA_TIMEOUT_SECONDS` | `180` | Per request; the single retry has its own timeout. |
| `PERSISTENCE_MODE` | `memory` | Only `memory` is implemented. |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | CORS allow-list. |

## Mock vs real inference

- **Ollama mode:** selecting an example loads *input only*. “Analyze with local Meta model” sends it to the model and you
  see the validated model output (also for your own text). Timeouts, an unreachable/uninstalled model, or invalid JSON
  (after one correction retry) show **“Processing failed”** — never a fake “insufficient evidence”.
- **Mock mode** (`AI_PROVIDER=mock`): returns *predefined sample assessments* for the four synthetic examples only,
  badged “simulated”. Edited or custom text is rejected with an explanation. Use it for UI development without the model.

## What the backend verifies on model output

Schema and enum validation (`extra` fields rejected), max 3 warning signals / 3 actions, field lengths; every
`source_quote` must appear in the analyzed text (unsupported ones are removed and counted); an `amount` not present in the
input is cleared. The model's risk band is never altered by these checks. Code-like values, CNIC-like and long numbers
are masked before inference (best effort, not perfect).

## Tests

```powershell
# backend (mocked HTTP for Ollama; no model needed)
cd backend ; pytest -q
# opt-in live inference against your local Ollama (records latency; asserts no accuracy)
pytest -m live -s
# frontend: UI smoke tests against a stubbed backend + type-check/build
cd ..\frontend ; npm test ; npm run build
```

**Actual results so far** (run in a Linux sandbox, Python 3.12 / Node 22 — not on the target Windows machine, and with no Ollama installed):
- `pytest -q`: 44 passed, 2 live tests deselected.
- `npm test`: 4 passed (jsdom, stubbed fetch). `npm run build`: succeeded.
- Manual HTTP check of the running backend: mock mode returned simulated results and rejected edited text; Ollama mode
  with no Ollama running returned HTTP 503 `model_unavailable`.
- **Live inference: not run.** Latency and Roman Urdu quality are unknown until you run it.

### Frontend smoke checklist (manual, in a browser)
Load each synthetic example · analyze in mock mode · edit a sample (assessment disappears) · stop Ollama and analyze in
Ollama mode (see “Processing failed”) · copy safe reply · record each verification status · export / print · delete/reset ·
narrow the window to ~375 px · toggle English / Roman Urdu. *(Not yet performed by hand; automated jsdom coverage exists
for most of these.)*

## Privacy and limitations

- “Analysis runs through the configured local Ollama instance.” The backend and Ollama must stay on loopback.
- Cases live in backend memory only and vanish on restart; no raw message is stored or exported; no `localStorage`.
- Backend logs contain request lines only, never message text or model output.
- Single-user local demo: **no authentication** on case endpoints.
- Small local models can be wrong, including false reassurance. The UI never says “safe”; “insufficient evidence” means exactly that.
- Roman Urdu output quality from a 1B/3B model is unverified and may be poor. The Roman Urdu UI strings and mock
  fixtures were hand-written and have not been reviewed by a native speaker.
- Warning signals are not proof of fraud; a verification outcome recorded by the user does not clear the assessment.

## Optional Firebase

**Not implemented.** Planned only after the core flow is stable (Firebase Auth + Firestore, backend ID-token verification,
ownership checks, restrictive rules, redacted results only). `PERSISTENCE_MODE` accepts only `memory`.

## Deferred

Screenshots/OCR, voice transcription, deepfake detection, automatic WhatsApp/SMS alerts, trusted-contact enrollment,
bank integrations, link fetching, automatic complaints, SAM/V-JEPA and other models.

See [SUBMISSION_NOTES.md](SUBMISSION_NOTES.md) for a plain account of what is real, synthetic, mocked, and untested.
