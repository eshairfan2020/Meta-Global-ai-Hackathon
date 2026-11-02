# Rasta — Pause. Verify. Proceed.

A mobile-first, bilingual English / Roman Urdu decision-support prototype
for Pakistani WhatsApp users facing suspicious requests for money or
login verification codes.

Built for the Meta Global AI Developer Hackathon, Indie Track.
Submission platform: Cerebral Valley.

> Rasta turns a suspicious message into a clearer next step:
> pause, verify independently, and document what you confirmed.

---

## Overview

An urgent message arrives:

> “Ammi, mera phone kharab ho gaya hai. Main naye number se baat kar
> raha hoon. Emergency hai, Rs 50000 bhej dein. Kisi ko mat batana.”

Should the recipient send money, ignore the request, or verify it first?

Rasta helps the user examine the message without presenting a model’s
judgment as certainty. It highlights quoted warning signals, explains
what remains unknown, suggests a calm reply, and guides independent
verification.

The application is a structured workflow, not a chatbot.

### Advisory only

Rasta cannot:

- Block payments.
- Recover compromised accounts.
- Prove a sender’s identity.
- Determine whether a voice is genuine.
- Read WhatsApp conversations automatically.
- Guarantee that a request is safe or fraudulent.

It does not automatically contact, accuse, or report anyone.

---

## Why This Project Exists

Suspicious messages can create pressure before a person has time to
verify the request.

A supposed relative may claim to be using a new number. A supposed bank
representative may ask for a login code. Urgency, secrecy, and authority
claims can make the next decision difficult.

Rasta focuses on that decision point.

Its proposed contribution is not simply another warning label. It
connects message analysis to practical actions:

1. Examine the evidence.
2. Understand uncertainty.
3. Avoid responding under pressure.
4. Verify through a previously known, independent channel.
5. Record what the user actually confirmed.

This project does not claim that WhatsApp has more account compromises
than other platforms, and it does not present unverified national fraud
statistics.

---

## Current Implementation Status

| Component | Status |
|---|---|
| Text-input and synthetic-example workflow | Implemented; see testing notes |
| Local Ollama provider | Implemented; live inference not yet verified |
| Mock provider | Implemented for predefined synthetic examples |
| Structured-output validation | Implemented |
| Manual family-verification workflow | Implemented; manual browser testing pending |
| User-recorded verification timeline | Implemented |
| Print-friendly incident export | Implemented |
| English / Roman Urdu interface | Implemented; language review pending |
| Persistent database and authentication | Not implemented |
| Firebase integration | Deferred |
| Screenshot and voice analysis | Deferred |

These implementation statements should be checked against the repository
before submission.

A provider adapter being implemented is not proof that a model has
successfully run. The live-test section below records that distinction.

---

## How It Works

1. Paste a suspicious message or select a synthetic example.
2. In Ollama mode, the backend submits the message to the configured
   local Meta Llama model.
3. The model returns a structured assessment containing:
   - Observed facts.
   - A concern band.
   - Quoted warning signals.
   - Uncertainty and missing context.
   - Recommended actions.
   - A suggested safe reply.
4. The backend validates the result before displaying it.
5. For possible family impersonation, the user can open Family
   Verification.
6. The user records the outcome of their independent check.
7. The user can export an advisory incident record.

A technical failure is displayed as “Processing failed,” not disguised
as a successful assessment.

---

## Meta Model Statement

This project is configured to use Meta Llama through Ollama on the
developer’s local Windows machine.

- Default configured tag: `llama3.2:3b`
- Explicit smaller-model option: `llama3.2:1b`
- Runtime: Ollama
- Inference endpoint: local `/api/chat`
- Hosted model APIs: none
- Non-Meta model calls: none
- Automatic fallback inference: none

**Exact model tag successfully tested: none yet.**

See [docs/live-test-log.md](docs/live-test-log.md). Update the tested
model statement only after completing a real inference run.

### Why Local Open-Weight Inference?

The developer is based in Pakistan. Following guidance received from
the event team regarding access restrictions on Meta’s hosted Model
API, this project uses the local open-weight route instead.

Ollama is the runtime. Meta Llama is the model intended to perform the
analysis.

The configured application does not require a paid cloud-model API or
Meta Model API credits.

### Model Configuration Controls

The backend:

- Requires a loopback `OLLAMA_BASE_URL`.
- Rejects model configuration that does not match its allowed
  `llama*` tag pattern.
- Selects the provider from server configuration, not client input.

The tag-prefix check is a configuration guard, not cryptographic proof
of model provenance. Before submission, verify the installed model and
record the exact tag and available model identifier in the live-test log.

Meeting a model-use requirement does not guarantee final acceptance,
judging scores, or a prize.

---

## Synthetic Inputs vs. Real Inference

The demonstration messages are fictional and clearly labeled.

### Ollama Mode

Selecting an example loads its input text only.

Clicking “Analyze with local Meta model” requests actual inference from
the configured local model. The application displays the validated
response, not a predefined assessment.

Custom messages are also supported in this mode.

This describes the implemented execution path; successful live execution
still needs to be verified.

### Mock Mode

Mock mode returns predefined assessments for the four synthetic examples.

It is intended for interface development and workflow testing without
a running model.

- Results are labeled simulated.
- Edited or custom messages are rejected with an explanation.
- The application does not silently replace failed inference with a
  mock result.

Synthetic evidence and simulated analysis are different:

- Synthetic input + actual model response demonstrates live inference.
- Synthetic input + predefined response demonstrates the product workflow.

---

## Demonstration Cases

The fixtures cover:

1. Family emergency impersonation.
2. A fake bank request for a login verification code.
3. A legitimate-looking request requiring context.
4. An ambiguous urgent message.

Fixtures must not contain actual passwords, verification codes, private
conversations, or real payment details.

Mock assessments are examples, not accuracy measurements or ground
truth for evaluating the live model.

---

## Family Verification

Family Verification is a manual safety workflow, not an automated
identity check.

It guides the user to:

1. Pause before sending money.
2. Contact the person using a number known before the suspicious message.
3. Avoid relying solely on the same WhatsApp conversation if compromise
   may be possible.
4. Check with another trusted relative or independent channel.
5. Use the family’s agreed offline verification method, if one exists.
6. Record what they personally confirmed.

Rasta does not collect or store family code words.

It does not treat a familiar voice, delivered message, or completed
checklist as proof of identity.

### User-Recorded Outcomes

The workflow records statuses such as:

- Not checked.
- Attempting independent contact.
- User-recorded confirmation.
- User-recorded denial.
- Inconclusive.

These are user reports, not independent findings by Rasta.

Completing the workflow does not automatically clear the model’s
assessment.

If a genuine emergency may exist, users should seek independent help
rather than dismiss the situation solely because a message appears
suspicious.

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
        | Input validation and best-effort redaction
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

Backend result checks
        |
        +-- Pydantic schema validation
        +-- Quote-in-input checks
        +-- Amount-in-input checks
        |
        v
Temporary in-memory case store
        |
        +-- Assessment view
        +-- Verification timeline
        +-- HTML incident export / Print to PDF
```

Model output is treated as data. It cannot execute code, select
notification recipients, or trigger external actions.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python, Pydantic |
| Local inference | Ollama with Meta Llama |
| Current storage | In-memory backend store |
| Export | Server-built, HTML-escaped, print-friendly HTML |
| Optional future persistence | Firebase Auth and Cloud Firestore |

No Docker, WSL, vector database, or multi-agent orchestration framework
is required for the current workflow.

---

## Prerequisites

Target environment: Windows 10/11 with PowerShell.

- Python 3.10 or newer; development tests used Python 3.12.
- Node.js compatible with the repository’s installed Vite version.
  The current project specifies Node 20.19+ or 22.12+ and was developed
  with Node 22.
- [Ollama for Windows](https://ollama.com/download/windows).
- Sufficient free disk space for dependencies and model weights.
- Available RAM for the model, its runtime context, operating system,
  browser, and development tools.

### Hardware Expectations

The application is intended to be tested with a small CPU-run model.

There is no validated minimum-RAM or latency claim for the target PC.
Model file size is not the same as runtime memory consumption.

Close unnecessary applications before testing. If 3B inference is not
practical, explicitly configure the 1B model and document which model
was actually tested.

The 1B and 3B configurations must be evaluated rather than assumed
equivalent in quality.

---

## Setup

Run commands from the repository root unless a step changes directory.

### 1. Install the Model

Install Ollama, then download the selected model:

```powershell
ollama pull llama3.2:3b
ollama list
```

For the smaller alternative:

```powershell
ollama pull llama3.2:1b
```

The application never downloads model weights automatically.

Make sure Ollama is running before attempting live analysis.

### 2. Start the Backend

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Copy-Item .env.example .env

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If PowerShell blocks virtual-environment activation, and local policy
permits it, a process-scoped setting can be used:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

Edit `backend/.env` before starting the backend if you want a different
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

The endpoint reports states such as:

- `ready`
- `model_not_installed`
- `unreachable`
- `mock`

A ready status indicates availability checks passed. It does not replace
an end-to-end inference test.

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

The correction retry has its own timeout. A failed first request followed
by a retry can therefore take longer than a single timeout period.

Keep the configured origin consistent with the frontend address when
making cross-origin requests. The development setup normally uses the
Vite proxy.

Restart the backend after changing environment variables.

### Enable Mock Mode

```dotenv
AI_PROVIDER=mock
PERSISTENCE_MODE=memory
```

### Enable Local Inference

```dotenv
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2:3b
PERSISTENCE_MODE=memory
```

There is no silent fallback between providers.

---

## Assessment Validation

The backend performs structural and evidence-consistency checks:

- Pydantic schema and enum validation.
- Rejection of unexpected fields.
- Field-length limits.
- Maximum three warning signals and three recommended actions.
- Verification that each source quote appears in the analyzed text.
- Removal and counting of unsupported quotes.
- Clearing an extracted amount that is not present in the input.

The backend also applies best-effort masking of code-like values,
CNIC-like patterns, and long numbers before inference.

### Important Limitations of These Checks

These checks do not establish that the model’s interpretation is correct.

The current checks do not alter the model’s concern band. If supporting
quotes are removed, the remaining concern band should not be interpreted
as independently validated.

Redaction can miss sensitive content or remove useful context, including
numbers relevant to a request. Users should not submit actual passwords,
PINs, or verification codes.

---

## Testing

### Backend Tests

From `backend/`:

```powershell
pytest -q
```

These tests use mocked Ollama HTTP responses and do not require a model.

Opt-in local inference tests:

```powershell
pytest -m live -s
```

Live tests record latency; they do not establish detection accuracy.

### Frontend Tests

From `frontend/`:

```powershell
npm test
npm run build
```

### Recorded Results

The following results were recorded in a Linux sandbox using Python 3.12
and Node 22, not on the target Windows machine:

- Backend: `44 passed`, with `2 live tests deselected`.
- Frontend: `4 passed` using jsdom and stubbed fetch.
- Frontend production build: succeeded.
- Manual backend HTTP check:
  - Mock mode returned simulated assessments.
  - Mock mode rejected edited fixture input.
  - Ollama mode without Ollama returned HTTP 503
    `model_unavailable`.

Live inference has not yet been run.

Observed latency, Windows performance, and Roman Urdu model quality
remain unknown.

### Manual Browser Checklist

Before recording or submitting:

- [ ] Load each synthetic example.
- [ ] Analyze in clearly labeled mock mode.
- [ ] Edit a sample and confirm its old assessment disappears.
- [ ] Run actual inference with the installed Meta model.
- [ ] Test a custom message.
- [ ] Stop Ollama and confirm “Processing failed” is shown.
- [ ] Copy a safe reply.
- [ ] Record verification outcomes.
- [ ] Export and print an incident record.
- [ ] Delete/reset a case.
- [ ] Test a narrow mobile layout.
- [ ] Toggle English / Roman Urdu.
- [ ] Record the exact tested model and observed limitations.

These browser checks have not yet been completed manually.

---

## Privacy and Security

- Inference is configured to use a loopback Ollama endpoint.
- Cases are held in backend memory and disappear on restart.
- The application does not persist the original raw message.
- Exported records may still contain sensitive information in derived
  fields or evidence excerpts; review before sharing.
- No `localStorage` persistence is used.
- Backend logs are intended to contain request metadata, not message
  bodies or model output.
- No links from messages are automatically fetched.
- Model-generated content is not executed.
- Incident HTML is escaped before rendering.

### Local Demo Only

The current application is a single-user local demonstration.

There is no authentication on case endpoints. Loopback binding is a
deployment boundary, not a replacement for authorization.

Do not expose the backend or Ollama directly to the internet.

A public deployment requires authentication, ownership enforcement,
deployment security review, and a suitable inference-hosting plan.

---

## Incident Export

The export is a print-friendly advisory record, not a forensic report or
an official complaint.

It should identify:

- The case and timestamp.
- Whether the input was synthetic.
- Whether the assessment was mocked or model-generated.
- The selected provider and model.
- Observed facts and warning signals.
- Uncertainty.
- Recommended actions.
- User-recorded verification events.

It does not certify that fraud occurred or that a sender’s identity was
verified.

---

## What Makes Rasta Different?

Rasta’s proposed focus is the connection between analysis and independent
verification for Pakistani users.

The workflow combines:

- English / Roman Urdu presentation.
- Evidence-grounded explanations.
- Explicit uncertainty.
- A calm reply to copy.
- Manual independent family verification.
- A record of the user’s own confirmation process.

This is a product hypothesis, not a claim that no existing product offers
similar capabilities.

Further user research and comparative testing are needed to establish
whether the workflow improves decisions over a warning label alone.

---

## Future Direction: User-Initiated WhatsApp Access

A future version could explore a WhatsApp Business Platform experience
where users deliberately send suspicious content to Rasta for guidance.

The goal would be to bring independent verification closer to the place
where the suspicious request arrives.

This is not implemented in the current prototype.

It would require review of platform policies, consent, privacy,
deployment, inference hosting, and operational requirements.

It would not provide background access to private conversations or
guarantee a native WhatsApp integration.

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
- Minimal, redacted saved results.

The current application accepts only:

```dotenv
PERSISTENCE_MODE=memory
```

If cloud persistence is introduced, the privacy statement must clearly
explain what leaves the local machine.

---

## Deferred Features

- Screenshot analysis and OCR.
- Voice transcription.
- Deepfake detection.
- Automated WhatsApp or SMS alerts.
- Trusted-contact enrollment.
- Bank integrations.
- Link fetching and reputation checks.
- Automatic complaints or reports.
- Additional model families.

These are not current capabilities.

---

## Submission Checklist

- [ ] Complete a successful local inference run.
- [ ] Update the exact tested model tag.
- [ ] Update `docs/live-test-log.md`.
- [ ] Record actual latency and language limitations.
- [ ] Complete the manual browser checklist.
- [ ] Ensure the video distinguishes synthetic inputs from mock outputs.
- [ ] Ensure README, demo, and submission claims match the code.
- [ ] Review exports for sensitive content.
- [ ] Check the current Cerebral Valley submission requirements.
- [ ] Update `SUBMISSION_NOTES.md`.

See [SUBMISSION_NOTES.md](SUBMISSION_NOTES.md) for a plain account of
what is implemented, synthetic, mocked, deferred, and untested.

---

Rasta provides safety guidance, not guaranteed detection.

Pause. Verify. Proceed.