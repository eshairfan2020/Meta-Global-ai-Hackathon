import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from "./api";
import { STRINGS } from "./i18n";
import type { CaseView, Example, Lang, ModelStatus, VStatus } from "./types";
import AssessmentView from "./components/AssessmentView";
import Home from "./components/Home";
import Report from "./components/Report";
import Verification from "./components/Verification";
import { Btn, Pill } from "./components/ui";

type Screen = "home" | "assessment" | "verification" | "report";

export default function App() {
  const [lang, setLang] = useState<Lang>("en");
  const [screen, setScreen] = useState<Screen>("home");
  const [text, setText] = useState("");
  const [examples, setExamples] = useState<Example[]>([]);
  const [status, setStatus] = useState<ModelStatus | null>(null);
  const [statusErr, setStatusErr] = useState(false);
  const [checking, setChecking] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [result, setResult] = useState<CaseView | null>(null);
  const t = STRINGS[lang];

  const refreshStatus = useCallback(async () => {
    setChecking(true);
    try { setStatus(await api.modelStatus()); setStatusErr(false); } catch { setStatus(null); setStatusErr(true); }
    setChecking(false);
  }, []);

  useEffect(() => {
    refreshStatus();
    api.examples().then(setExamples).catch(() => setExamples([]));
  }, [refreshStatus]);

  const discard = (msg: string | null) => {
    if (result) { api.remove(result.case_id).catch(() => {}); setResult(null); }
    setNotice(msg);
  };

  const onText = (s: string) => {
    if (result && s !== text) discard(t.edited);
    setText(s);
    setError(null);
  };

  const analyze = async () => {
    setBusy(true); setError(null); setNotice(null);
    try {
      if (result) api.remove(result.case_id).catch(() => {});
      setResult(null);
      setResult(await api.analyze(text, lang));
      setScreen("assessment");
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Processing failed.");
    } finally {
      setBusy(false);
      refreshStatus();
    }
  };

  const record = async (s: VStatus) => {
    if (!result) return;
    setBusy(true); setError(null);
    try { setResult(await api.record(result.case_id, s)); }
    catch (e) { setError(e instanceof ApiError ? e.message : "Could not record."); }
    finally { setBusy(false); }
  };

  const reset = () => { discard(null); setText(""); setError(null); setScreen("home"); };

  // status pills
  const provPill = checking ? <Pill tone="info">{t.st_checking}</Pill>
    : statusErr || !status ? <Pill tone="bad">{t.st_unreachable}</Pill>
    : status.state === "ready" ? <Pill tone="ok">{t.st_ready}: {status.model}</Pill>
    : status.state === "mock" ? <Pill tone="warn">{t.st_mock}</Pill>
    : <Pill tone="bad">{t.st_unreachable}</Pill>;
  const opPill = busy ? <Pill tone="busy">{t.st_processing}</Pill>
    : error && screen === "home" ? <Pill tone="bad">{t.st_failed}</Pill>
    : result ? <Pill tone="ok">{t.st_done}</Pill> : null;

  return (
    <div className="mx-auto min-h-screen max-w-2xl px-4 pb-12 pt-6 sm:px-6">
      <header className="mb-6">
        <div className="flex items-start justify-between gap-2">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-teal-800">Rasta</h1>
            <p className="text-sm font-medium text-slate-600">{t.tagline}</p>
          </div>
          <div role="group" aria-label={t.language} className="flex overflow-hidden rounded-lg border border-slate-300 text-sm">
            {(["en", "ur"] as Lang[]).map((l) => (
              <button key={l} onClick={() => setLang(l)} aria-pressed={lang === l}
                className={`min-h-11 px-3 ${lang === l ? "bg-teal-700 text-white" : "bg-white"}`}>
                {l === "en" ? "English" : "Roman Urdu"}
              </button>
            ))}
          </div>
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-2" aria-live="polite">
          {provPill}{opPill}
          {status && status.state !== "ready" && status.state !== "mock" && <span className="text-xs text-slate-600">{status.detail}</span>}
          {statusErr && <span className="text-xs text-slate-600">Backend not reachable.</span>}
          <Btn className="min-h-8! px-2! py-0.5! text-xs" onClick={refreshStatus} disabled={checking}>{t.retry}</Btn>
        </div>
      </header>

      <main className="space-y-5">
        {busy && screen === "home" && <p role="status" className="rounded-lg border border-sky-300 bg-sky-50 p-3 text-sm text-sky-900">{t.processing}</p>}
        {error && screen === "home" && (
          <div role="alert" className="rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-900">
            <div className="font-semibold">{t.failedTitle}</div><div>{error}</div>
          </div>
        )}
        {notice && screen === "home" && <p role="status" className="rounded-lg border border-slate-300 bg-slate-100 p-3 text-sm">{notice}</p>}

        {screen === "home" && (
          <Home t={t} lang={lang} text={text} examples={examples} status={status} busy={busy} hasResult={!!result}
            onText={onText} onAnalyze={analyze} onBack={() => setScreen("assessment")} />
        )}
        {screen === "assessment" && result && (
          <AssessmentView t={t} c={result} uiLang={lang} message={error ?? ""} onVerify={() => setScreen("verification")}
            onExport={() => setScreen("report")} onDelete={reset} onEdit={() => setScreen("home")} />
        )}
        {screen === "verification" && result && (
          <Verification t={t} c={result} busy={busy} error={error} onRecord={record}
            onBack={() => setScreen("assessment")} onExport={() => setScreen("report")} />
        )}
        {screen === "report" && result && <Report t={t} caseId={result.case_id} onBack={() => setScreen("assessment")} />}
      </main>

      <footer className="mt-10 border-t border-slate-200 pt-3 text-xs text-slate-600">{t.footer}</footer>
    </div>
  );
}
