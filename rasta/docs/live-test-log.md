# Live inference test log

**Status: NOT YET RUN.** No live inference has been verified. Fill this in after running the steps in the README
(`pytest -m live -s` in `backend/`, plus manual runs through the UI). Do not enter results you did not observe.

| Date | Model tag | Example | Language | risk_band returned | Quotes removed | Latency (s) | Notes / failures |
|------|-----------|---------|----------|--------------------|----------------|-------------|------------------|
|      |           |         |          |                    |                |             |                  |

Things worth noting while testing:
- Does the model return valid JSON on the first try, or does the one retry trigger?
- Roman Urdu: are explanations understandable? Is meaning preserved?
- Any harmful false reassurance (e.g. the verification-code example not flagged)?
- Peak RAM and whether the 3B tag is usable on your machine; if not, try `llama3.2:1b`.

## Manual live-inference confirmation

- Date recorded: November 2, 2026
- Model: llama3.2:3b
- Runtime: Ollama
- Environment: Developer’s local Windows PC
- Result: The application successfully received and displayed an
  actual model-generated response.
- Latency: Not formally measured.
- Safety accuracy and Roman Urdu quality: Not formally evaluated.