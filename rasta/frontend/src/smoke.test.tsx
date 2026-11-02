// UI smoke test against a FAKE backend (fetch is stubbed). It verifies UI behaviour only;
// it says nothing about the real backend or any model.
import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, expect, test, vi } from "vitest";
import App from "./App";

const EX = { id: "ambiguous_urgency", title_en: "Ambiguous urgency", title_ur: "Mubham jaldi", text: "Mujhe abhi help chahiye. Please call me." };
const assessment = {
  risk_band: "insufficient_evidence", scam_category: "unclear",
  observed_facts: { claimed_identity: null, requested_action: "Call the sender", amount: null, urgency_present: true, secrecy_present: false, verification_code_requested: false },
  warning_signals: [{ label: "Urgency", source_quote: "Mujhe abhi help chahiye", explanation: "Urgency alone does not show fraud." }],
  uncertainty: "Too little information.", recommended_actions: ["Call a known number."], safe_reply: "I will call you on your usual number.",
  family_verification_suggested: true,
};
let events: { status: string; timestamp: string }[] = [];
let analyzeFails = false;
let calls: string[] = [];

const caseView = () => ({
  case_id: "abc", created_at: "2026-10-30T00:00:00+00:00", language: "en", is_synthetic: true, example_id: EX.id,
  provider: "mock", model: null, inference: "simulated", latency_ms: null, redactions: 0, quotes_removed: 0, amount_cleared: false,
  assessment, verification: { status: events.at(-1)?.status ?? "not_checked", events },
});
const ok = (b: unknown) => Promise.resolve(new Response(JSON.stringify(b), { status: 200 }));

beforeEach(() => {
  events = []; analyzeFails = false; calls = [];
  vi.stubGlobal("fetch", (url: string, init?: RequestInit) => {
    const m = init?.method ?? "GET"; calls.push(`${m} ${url}`);
    if (url === "/api/examples") return ok([EX]);
    if (url === "/api/model-status") return ok({ provider: "mock", model: null, state: "mock", detail: "Mock mode" });
    if (url === "/api/analyze") return analyzeFails
      ? Promise.resolve(new Response(JSON.stringify({ error: { code: "model_unavailable", message: "The local Ollama service could not be reached." } }), { status: 503 }))
      : ok(caseView());
    if (url.endsWith("/verification")) { events.push({ status: JSON.parse(init!.body as string).status, timestamp: new Date().toISOString() }); return ok(caseView()); }
    if (url.endsWith("/export")) return Promise.resolve(new Response("<html><body>REPORT</body></html>", { status: 200 }));
    if (m === "DELETE") return ok({ deleted: true });
    return Promise.reject(new Error("unexpected " + url));
  });
});
afterEach(cleanup);

test("load example → analyze → copy → record → export → delete", async () => {
  const u = userEvent.setup();
  const copySpy = vi.spyOn(navigator.clipboard, "writeText");
  render(<App />);
  await screen.findByText("Mock mode");
  expect(screen.getByText(/Synthetic example — not a real incident\./)).toBeTruthy();
  await u.click(await screen.findByText("Load example"));
  expect((screen.getByLabelText("Message to check") as HTMLTextAreaElement).value).toBe(EX.text);
  await u.click(screen.getByRole("button", { name: "Show predefined sample assessment" }));
  await screen.findByText("Insufficient evidence");
  expect(screen.getByText(/Predefined sample assessment \(simulated/)).toBeTruthy();
  expect(screen.getByText(/No clear warning found does not mean safe/)).toBeTruthy();
  await u.click(screen.getByRole("button", { name: "Copy safe reply" }));
  expect(copySpy).toHaveBeenCalledWith(assessment.safe_reply);
  await u.click(screen.getByRole("button", { name: /Open family verification/ }));
  await u.click(await screen.findByRole("button", { name: "I confirmed it is them" }));
  await waitFor(() => expect(screen.getAllByText("I confirmed it is them").length).toBeGreaterThan(1));
  expect(screen.getAllByText(/not independently verified by Rasta/).length).toBeGreaterThan(0);
  await u.click(screen.getByRole("button", { name: "Export incident record" }));
  await waitFor(() => expect(screen.getByTitle("Incident record")).toBeTruthy());
  await u.click(screen.getByRole("button", { name: "Back" }));
  await u.click(screen.getByRole("button", { name: "Delete case & reset" }));
  await screen.findByLabelText("Message to check");
  expect((screen.getByLabelText("Message to check") as HTMLTextAreaElement).value).toBe("");
  expect(calls).toContain("DELETE /api/cases/abc");
});

test("editing text discards the saved assessment", async () => {
  const u = userEvent.setup();
  render(<App />);
  await u.click(await screen.findByText("Load example"));
  await u.click(screen.getByRole("button", { name: "Show predefined sample assessment" }));
  await screen.findByText("Insufficient evidence");
  await u.click(screen.getByRole("button", { name: "Edit message" }));
  await u.type(screen.getByLabelText("Message to check"), " now");
  expect(screen.getByText(/previous assessment was discarded/)).toBeTruthy();
  expect(screen.queryByRole("button", { name: "Back" })).toBeNull();
  expect(calls).toContain("DELETE /api/cases/abc");
});

test("technical failure shows 'Processing failed', not an assessment", async () => {
  analyzeFails = true;
  const u = userEvent.setup();
  render(<App />);
  await u.click(await screen.findByText("Load example"));
  await u.click(screen.getByRole("button", { name: "Show predefined sample assessment" }));
  await screen.findByText(/Processing failed \(technical error/);
  expect(screen.getByText("The local Ollama service could not be reached.")).toBeTruthy();
  expect(screen.queryByText("Insufficient evidence")).toBeNull();
});

test("language toggle switches interface strings", async () => {
  const u = userEvent.setup();
  render(<App />);
  await u.click(await screen.findByRole("button", { name: "Roman Urdu" }));
  expect(screen.getByText("Ruko. Tasdeeq karo. Phir aage barho.")).toBeTruthy();
});
