Here is the updated README, with the conflicting safety-rule and `keep_alive` claims removed. It preserves the distinction between implemented code, mock demonstrations, and unverified live inference.

Copy it into `README.md`. Update the **verification** section only after running the actual local model.

````markdown
# Rasta — Pause. Verify. Proceed.

A mobile-first, bilingual English / Roman Urdu decision-support prototype
for Pakistani WhatsApp users receiving suspicious requests for money or
login verification codes.

Built for the Meta Global AI Developer Hackathon — Indie Track.
Submission platform: Cerebral Valley.

> Rasta helps families pause, verify independently, and document what
> they confirmed—before they decide to pay.

---

## The Problem

A message arrives from a supposed relative using a new number:

>“Mom, my phone broke. I’m calling from a new number. It’s an emergency, send Rs 50,000. Don’t tell anyone.”

The example is fictional, but the decision it creates is important:
respond immediately, or pause to verify?

Suspicious requests can combine urgency, secrecy, family relationships,
or claims of authority. The recipient needs more than a warning label;
they need a clear next step.

Rasta focuses on that moment of decision.

It does not claim that WhatsApp has more account compromises than other
platforms or present unverified national fraud statistics.

---

## What Rasta Does

Rasta is a structured workflow, not a chatbot.

Users paste a message or select a clearly labeled synthetic example.
In Ollama mode, a locally running Meta Llama model generates an assessment
containing:

- Observed facts.
- A concern band.
- Warning signals supported by quoted message text.
- Uncertainty and missing context.
- Recommended actions.
- A polite reply to copy.

For possible family impersonation, Rasta offers a manual independent
verification workflow. Users can record their own verification outcome
and export an advisory incident record.

### Advisory Only

Rasta cannot:

- Block payments.
- Recover compromised accounts.
- Prove the sender’s identity.
- Determine whether a voice is genuine.
- Read WhatsApp conversations automatically.
- Guarantee that a request is safe or fraudulent.

It does not automatically contact, accuse, or report anyone.

---

## Current Status

This repository contains an implemented prototype with separate Ollama
and mock providers.

**Live model inference has been tested locally on Windows. Earlier automated test results below were recorded separately in a Linux sandbox**

| Component | Current status |
|---|---|
| Text input and synthetic examples | Implemented |
| Local Ollama provider | Implemented;  live inference tested locally on Windows|
| Mock provider | Implemented for predefined synthetic cases |
| Structured-output validation | Implemented |
| Evidence-quote checks | Implemented |
| Manual family-verification workflow | Implemented |
| User-recorded verification timeline | Implemented |
| Print-friendly incident export | Implemented |
| English / Roman Urdu interface | Implemented; language review pending |
| Manual browser smoke testing | Pending |
| Authentication and persistent database | Not implemented |
| Firebase | Deferred |
| Screenshot and voice analysis | Deferred |

Implementation does not imply that every feature has been manually
verified on the target Windows machine.

---

## How It Works

1. Paste a suspicious message or load a synthetic example.
2. Choose the interface language.
3. In Ollama mode, click **Analyze with local Meta model**.
4. The backend validates and applies best-effort redaction to the input.
5. The configured local Meta Llama model returns a structured assessment.
6. The backend validates the result and checks its evidence quotes.
7. Review the warning signals, uncertainty, safe reply, and next actions.
8. If relevant, open Family Verification and perform an independent check.
9. Record what you personally confirmed.
10. Export an incident record or delete the temporary case.

A technical failure is shown as **Processing failed**, not disguised as
an assessment of insufficient evidence.

---

## Meta Model Usage

### Configuration

- Model family: Meta Llama.
- Default configured Ollama tag: `llama3.2:3b`.
- Explicit smaller-model option: `llama3.2:1b`.
- Runtime: Ollama.
- Execution location: developer’s local Windows PC.
- Model endpoint: local Ollama `/api/chat`.
- Hosted model APIs: none.
- Non-Meta model calls: none.
- Automatic fallback inference: none.

### Live Verification

**Exact model tag successfully tested: none recorded yet.**

See [docs/live-test-log.md](docs/live-test-log.md).

After a successful live run, update this section with:

- Exact model tag.
- Available model identifier or digest.
- Test date.
- Target-machine details.
- Observed latency.
- Cases tested.
- Known output or language failures.

Do not replace “not tested” with the configured default unless that model
has actually completed an inference request.

### Why Local Meta Models?

The developer is based in Pakistan and received guidance from the event
team to use eligible Meta open-weight models on locally provided compute
instead of the geographically restricted hosted Model API.

Local execution also fits the sensitivity of the evidence. Users may be
examining private family messages, so the prototype is configured to
perform analysis without a cloud-model request.

The trade-off is limited compute. Rasta therefore focuses on short text
inputs, bounded output, and one active inference at a time.

Ollama is the runtime; Meta Llama is the model performing analysis.

### Configuration Guards

The backend:

- Requires `OLLAMA_BASE_URL` to be loopback.
- Requires `OLLAMA_MODEL` to match its allowed `llama*` tag pattern.
- Selects the provider from server configuration, not a client request.

A tag-prefix check is not proof of model provenance. Verify the installed
model and record its exact identity before submission.

Using the specified model route does not guarantee final acceptance,
judging scores, or a prize.

---

## Synthetic Inputs and Mock Assessments

Synthetic input and simulated inference are different.

### Ollama Mode

Selecting an example loads its fictional input text only.

Clicking Analyze sends the text to the configured local model. The
assessment must come from the actual returned response.

Custom text is supported in this mode.

If the model is unavailable, times out, or returns invalid output after
one correction retry, the application shows an error.

It does not silently substitute a predefined assessment.

### Mock Mode

Mock mode returns predefined sample assessments for the four synthetic
examples.

It is intended for UI development and workflow demonstrations without a
running model.

- Results are labeled simulated.
- Edited or custom input is rejected with an explanation.
- Mock results are not presented as live model inference.

### Demonstration Cases

The fixtures cover:

1. Family emergency impersonation.
2. A fake bank request for a login verification code.
3. A legitimate-looking request requiring context.
4. An ambiguous urgent message.

The examples are fictional and must not contain real passwords,
verification codes, private chats, or payment credentials.

Mock assessments are not measured accuracy results.

---

## Family Verification

Family Verification is a manual independent-checking workflow—not an
automated identity-verification system.

It guides the user to:

1. Pause before sending money.
2. Contact the person through a number known before the message arrived.
3. Avoid relying only on the same WhatsApp conversation if account
   compromise may be possible.
4. Check through another trusted relative or independent channel.
5. Use an agreed offline family-verification method, if one exists.
6. Record the outcome of the check.

Rasta does not collect, store, or transmit family code words.

It does not treat a familiar voice, message delivery, or a completed
checklist as proof of identity.

### User-Recorded Statuses

- `not_checked`
- `attempting_independent_contact`
- `user_recorded_confirmation`
- `user_recorded_denial`
- `inconclusive`

These statuses reflect what the user reported. Rasta does not
independently verify them.

Recording a confirmation does not automatically clear the assessment.

If a genuine emergency may exist, seek independent help rather than
dismissing it solely because a message appears suspicious.

---

## Architecture

```text
React + Vite + TypeScript + Tailwind
http://127.0.0.1:5173
        |
        | fetch /api/*
        | Vite development proxy
        v
FastAPI
http://127.0.0.1:8000
        |
        | Input validation
        | Best-effort redaction
        | One active inference at a time
        v
AnalysisProvider
        |
        +-- OllamaAnalysisProvider
        |       |
        |       v
        |   Local Ollama /api/chat
        |   http://127.0.0.1:11434
        |       |
        |       v
        |   Configured Meta Llama model
        |
        +-- MockAnalysisProvider
                |
                v
            Predefined synthetic assessments

Backend output validation
        |
        +-- Pydantic schema checks
        +-- Quote-in-input verification
        +-- Amount-in-input verification
        |
        v
Temporary in-memory case store
        |
        +-- Assessment screen
        +-- Manual verification timeline
        +-- Print-friendly incident export
```

Model output is data only. It cannot execute code, send notifications,
or trigger external actions.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, Pydantic |
| Local inference | Ollama with Meta Llama |
| Current storage | Backend memory |
| Incident export | Server-built, HTML-escaped, print-friendly HTML |
| Planned persistence | Firebase Authentication and Cloud Firestore |

The current workflow does not require Docker, WSL, a vector database,
or a multi-agent orchestration framework.

---

## Prerequisites

Target environment: Windows 10/11 with PowerShell.

- Python 3.10+; development tests used Python 3.12.
- Node.js compatible with the installed Vite version.
  The project specifies Node 20.19+ or 22.12+ and was developed with
  Node 22.
- [Ollama for Windows](https://ollama.com/download/windows).
- Sufficient free disk space for dependencies and model weights.
- Available memory for the operating system, browser, backend, model,
  and runtime context.

### Hardware Expectations

The intended target machine has:

- AMD Ryzen 5 PRO 3400G.
- Four CPU cores / eight threads.
- Approximately 9.9 GB usable system RAM.
- No verified GPU acceleration.

There is no validated minimum-RAM or latency claim for this machine.

Model download size is not the same as runtime memory usage. Close
unnecessary applications before testing.

If the 3B model is not practical, explicitly configure the 1B model and
document that choice. Do not assume equivalent assessment quality.

---

## Setup

Run these commands from the repository root unless directed otherwise.

### 1. Install the Model

Install Ollama, then download the selected model:

```powershell
ollama pull llama3.2:3b
ollama list
```

Smaller alternative:

```powershell
ollama pull llama3.2:1b
```

The application does not download model weights automatically.

Ensure Ollama is running before live analysis.

### 2. Start the Backend

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If PowerShell blocks virtual-environment activation and local policy
permits it:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

Edit `backend/.env` before starting the backend if selecting another
provider or installed model.

### 3. Start the Frontend

In a second terminal:

```powershell
cd frontend

npm install

Copy-Item .env.example .env

npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

### 4. Check Provider Status

Open:

```text
http://127.0.0.1:8000/api/model-status
```

Expected states include:

- `ready`
- `model_not_installed`
- `unreachable`
- `mock`

A ready status does not replace an end-to-end inference test.

---

## Configuration

Backend configuration: `backend/.env`.

| Variable | Default | Purpose |
|---|---|---|
| `AI_PROVIDER` | `ollama` | `ollama` or `mock`; server-controlled |
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Loopback Ollama endpoint |
| `OLLAMA_MODEL` | `llama3.2:3b` | Explicitly selected model tag |
| `OLLAMA_CONTEXT_SIZE` | `2048` | Ollama `num_ctx` |
| `OLLAMA_MAX_OUTPUT_TOKENS` | `600` | Ollama `num_predict` |
| `OLLAMA_TIMEOUT_SECONDS` | `180` | Timeout per request |
| `PERSISTENCE_MODE` | `memory` | Only implemented persistence mode |
| `FRONTEND_ORIGIN` | `http://localhost:5173` | Configured CORS origin |

The correction retry has its own timeout. A failed request followed by
a retry may therefore take longer than one timeout period.

Keep the configured origin consistent with the frontend address when
making cross-origin requests. The development setup uses the Vite proxy.

Restart the backend after changing environment variables.

### Local Inference

```dotenv
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b
PERSISTENCE_MODE=memory
```

### Mock Mode

```dotenv
AI_PROVIDER=mock
PERSISTENCE_MODE=memory
```

There is no silent provider fallback.

---

## Assessment Validation

The backend checks:

- Schema and allowed enum values.
- Unexpected fields.
- Field-length limits.
- A maximum of three warning signals.
- A maximum of three recommended actions.
- Whether each source quote appears in the analyzed text.
- Whether an extracted amount appears in the input.

Unsupported quotes are removed and counted. Unsupported amounts are
cleared.

The backend applies best-effort masking of code-like values, CNIC-like
patterns, and long numbers before inference.

### What These Checks Do Not Prove

Structural validation is not semantic validation.

A valid JSON response can still contain incorrect reasoning, misleading
advice, or an inappropriate concern band.

The current checks do not alter the model’s concern band. This
implementation does not claim a tested deterministic rule that forces
all login-code requests into a particular concern band.

If evidence quotes are removed, the remaining assessment should not be
treated as independently validated.

Redaction may miss sensitive information or remove useful context.
Do not paste actual passwords, PINs, or login verification codes.

---

## Testing

### Backend

From `backend/`:

```powershell
pytest -q
```

These tests use mocked Ollama HTTP responses and do not require a model.

Opt-in live tests:

```powershell
pytest -m live -s
```

Live tests record latency. They do not establish fraud-detection accuracy.

### Frontend

From `frontend/`:

```powershell
npm test
npm run build
```

### Recorded Results

The recorded results below were obtained in a Linux sandbox with
Python 3.12 and Node 22—not on the target Windows machine.

- Backend: `44 passed`, with `2 live tests deselected`.
- Frontend: `4 passed` using jsdom and stubbed fetch.
- Frontend production build: succeeded.
- Manual backend HTTP checks:
  - Mock mode returned simulated assessments.
  - Edited fixture text was rejected in mock mode.
  - Ollama mode without a running Ollama instance returned HTTP 503
    `model_unavailable`.


A subsequent manual test confirmed live inference on Windows using llama3.2:3b through Ollama.

Windows performance, actual latency, and Roman Urdu model quality remain
unverified.

### Manual Browser Checklist

Before recording or submitting:

- [ ] Load all four synthetic examples.
- [ ] Check clearly labeled mock assessments.
- [ ] Edit a sample and confirm the old assessment disappears.
- [ ] Complete actual inference with the installed Meta model.
- [ ] Test a custom message.
- [ ] Stop Ollama and confirm a processing error is shown.
- [ ] Copy a safe reply.
- [ ] Record verification outcomes.
- [ ] Export and print an incident record.
- [ ] Delete/reset a case.
- [ ] Test a narrow mobile layout.
- [ ] Toggle English / Roman Urdu.
- [ ] Review language quality.
- [ ] Record the exact tested model and observed limitations.

These checks have not yet been completed manually.

---

## Privacy and Security

- Analysis is configured to use a loopback Ollama instance.
- Cases are stored in backend memory and disappear on restart.
- The original raw message is not persisted.
- No `localStorage` persistence is used.
- Logs are intended to contain request metadata, not message bodies
  or model output.
- Links from messages are not automatically fetched.
- Model output is not executed.
- Exported HTML is escaped.

Derived fields and evidence excerpts can still contain sensitive
information. Review an incident record before sharing it.

Local inference does not by itself eliminate every privacy or security
risk.

### Local Demonstration Only

The current application is a single-user local demo.

Case endpoints do not have authentication. Loopback binding is not a
replacement for authorization.

Do not expose the backend or Ollama directly to the internet.

Public deployment requires authentication, ownership enforcement,
deployment review, and an appropriate inference-hosting plan.

---

## Incident Export

The incident record is advisory. It is not:

- A forensic report.
- An official complaint.
- A verified identity record.
- Proof that fraud occurred.
- A certification that payment is safe.

The export should identify:

- Case ID and timestamp.
- Whether the input was synthetic.
- Whether the assessment was mocked or model-generated.
- Provider and configured model.
- Observed facts.
- Warning signals and uncertainty.
- Recommended actions.
- User-recorded verification events.

Review the export for sensitive content before sharing it.

---

## Proposed Differentiation

Rasta focuses on the transition from a warning to an independent check.

Its proposed contribution combines:

- English / Roman Urdu presentation.
- Evidence-grounded explanations.
- Explicit uncertainty.
- A calm reply to copy.
- A manual family-verification workflow.
- A record of the user’s own confirmation process.

It does not claim that no competing product offers similar features.

Further user research and comparative evaluation are needed to determine
whether this workflow improves decisions over a concern label alone.

---

## Future Direction: User-Initiated WhatsApp Access

A future version could explore a WhatsApp Business Platform experience
where users deliberately send suspicious content to Rasta.

The aim would be to bring verification closer to where the suspicious
request arrives.

This is not implemented in the current prototype.

It would require review of platform policies, consent, privacy,
deployment, inference hosting, and operational requirements.

It would not provide background access to private conversations or
guarantee native integration into WhatsApp.

Rasta is not an official Meta or WhatsApp safety feature.

---

## Optional Firebase

Firebase is not implemented.

A future persistence layer may use:

- Firebase Authentication.
- Cloud Firestore.
- Backend ID-token verification.
- Per-user ownership checks.
- Restrictive client security rules.
- Minimal redacted saved results.

Currently, only this persistence mode is supported:

```dotenv
PERSISTENCE_MODE=memory
```

If cloud persistence is added, update the privacy statement to explain
exactly what leaves the local machine.

---

## Deferred Features

- Screenshot understanding and OCR.
- Voice transcription.
- Deepfake detection.
- Automated WhatsApp or SMS alerts.
- Trusted-contact enrollment.
- Bank integrations.
- Link reputation checks.
- Automatic complaints or reports.
- Additional model families.

These are not current capabilities.

---

## Submission Checklist

- [ ] Run successful local inference.
- [ ] Record the exact tested model tag and identifier.
- [ ] Update `docs/live-test-log.md`.
- [ ] Record observed latency and language limitations.
- [ ] Complete manual browser testing.
- [ ] Ensure the video distinguishes synthetic inputs from mock output.
- [ ] Remove any unverified feature or performance claims.
- [ ] Confirm the README, video, and form describe the same build.
- [ ] Review the public repository for secrets.
- [ ] Confirm the repository and video are accessible to judges.
- [ ] Check current Cerebral Valley submission requirements.
- [ ] Update `SUBMISSION_NOTES.md`.

See [SUBMISSION_NOTES.md](SUBMISSION_NOTES.md) for an account of what is
implemented, synthetic, mocked, deferred, and untested.

---

Rasta provides safety guidance, not guaranteed detection.

Pause. Verify. Proceed.
````