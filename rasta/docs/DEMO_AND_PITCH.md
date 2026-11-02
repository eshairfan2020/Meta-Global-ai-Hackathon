# Demo video and pitch guide

Confirm the real video length limit and required form fields in your Cerebral Valley dashboard first.
Target ≈ 2:50. English narration + captions; Roman Urdu messages stay in Roman Urdu on screen.

## Before you record
1. `.\run.ps1` (loads the model). Check the pill says **Live local inference: llama3.2:3b** (or the tag you actually use).
2. Do one throw-away analysis so the model is warm. Recording a cold first request wastes 60+ s.
3. Run `python -m evaluation.run_eval` first so you can quote real numbers. Use only results you actually have.
4. Browser at phone width (~390 px) or a phone-sized window. Hide bookmarks and notifications.

## Script
| Time | On screen | Say |
|---|---|---|
| 0:00–0:20 | Synthetic “Ammi, naye number se… Rs 50000 bhej dein… Kisi ko mat batana” | “Someone you love seems to be in trouble. The message is urgent and secret. You have seconds to decide. This is a *fictional* example. Rasta helps you pause.” |
| 0:20–1:20 | Load example → **Check this message** → banner → highlighted message → quoted signals → uncertainty → copy safe reply | “A local Meta Llama model reads the message on this laptop. Rasta shows exactly which phrases worried it, says what it can’t know, and gives a calm reply you can send instead of paying.” (Say “waiting time shortened” if you cut the wait.) |
| 1:20–1:50 | Family verification → record “attempting independent contact” → “I confirmed it is them/NOT them” → timeline → Export | “The key step is outside the chat: call a number you already had, or another relative. Rasta records only what *you* confirm. It never clears the warning for you.” |
| 1:50–2:15 | Verification-code example | “Asking for a login code is a serious sign. A small model can miss it, so a plain-code safety rule enforces a floor — and the result says when the rule, not the model, raised it.” |
| 2:15–2:40 | Optional: stop Ollama → analyze → **Processing failed** | “If the model is down you get an honest error — never a fake ‘looks fine’, never a hidden cloud fallback.” |
| 2:40–2:50 | Footer / report disclaimer | “Rasta gives safety guidance, not guaranteed fraud detection. Pause. Verify. Proceed.” |

Show real screens only. Label staged data (“synthetic example”) and any edited waiting time.

## Claims you can make / must not make
Safe: local Meta Llama via Ollama; synthetic demo inputs; quotes are verified against the message; no actions are
triggered by model output; user-recorded verification; “proposed difference: a practical verification workflow, not just a label.”

Do **not** say: “world’s first”, “only tool that…”, “protects users”, any accuracy % you did not measure, “all data stays on
your device”, or anything about real users/loss prevented unless you ran and documented a pilot.

## Likely judge questions
- **Why not paste it into a chatbot?** Sensitive family chats are analyzed by a local model with no cloud API; the app adds a structured, verified result and an independent-verification workflow instead of a chat.
- **Is a 3B model accurate enough?** Show `docs/eval-results-*.md` (27 synthetic messages, small, not an accuracy claim). Explain the safety rule for code requests and that results are advisory.
- **What if the model is wrong or injected?** Output is schema-validated, quotes are checked against the message, model output can’t trigger actions, injection cases are in the evaluation set.
- **Roman Urdu quality?** State what you saw. If you had a native reader rate outputs, give that number; otherwise call it an open limitation.
- **What would you do next?** Pilot with consented families (see `docs/pilot-protocol.md`), expand the evaluation set, native-speaker review, then screenshot input.
