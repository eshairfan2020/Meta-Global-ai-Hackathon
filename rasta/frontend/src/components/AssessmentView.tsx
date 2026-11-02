import { useEffect, useRef, useState, type ReactElement } from "react";
import type { CaseView, RiskBand } from "../types";
import type { Strings } from "../i18n";
import { splitHighlights } from "../highlight";
import { Btn, Card, IconSearch, IconUnclear, IconWarning, Pill } from "./ui";

const BANNER: Record<RiskBand, { box: string; iconWrap: string; icon: ReactElement }> = {
  high_concern: { box: "border-red-800 bg-red-700 text-white", iconWrap: "bg-white/20", icon: <IconWarning /> },
  some_concern: { box: "border-amber-500 bg-amber-100 text-amber-950", iconWrap: "bg-amber-300/60", icon: <IconSearch /> },
  // deliberately calm and neutral — never green, never a check mark
  insufficient_evidence: { box: "border-slate-300 bg-slate-100 text-slate-900", iconWrap: "bg-slate-200", icon: <IconUnclear /> },
};

async function copyText(s: string) {
  try { await navigator.clipboard.writeText(s); return; } catch { /* fall back */ }
  const ta = document.createElement("textarea");
  ta.value = s; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove();
}

interface Props {
  t: Strings; c: CaseView; message: string; uiLang: string; onVerify: () => void; onExport: () => void; onDelete: () => void; onEdit: () => void;
}

export default function AssessmentView({ t, c, message, uiLang, onVerify, onExport, onDelete, onEdit }: Props) {
  const [copied, setCopied] = useState(false);
  const bannerRef = useRef<HTMLDivElement>(null);
  // Bring the result banner into view (and to screen readers) as soon as the screen appears.
  useEffect(() => { bannerRef.current?.focus(); }, []);
  const a = c.assessment, f = a.observed_facts;
  const yn = (b: boolean) => (b ? t.yes : t.no);
  const bandLabel = t[`risk_${a.risk_band}` as keyof Strings] as string;
  const note = a.risk_band === "insufficient_evidence" ? t.riskNote_insufficient_evidence : t.riskNote_other;
  const b = BANNER[a.risk_band];
  const rows: [string, string][] = [
    [t.claimed, f.claimed_identity ?? t.none], [t.action, f.requested_action ?? t.none], [t.amount, f.amount ?? t.none],
    [t.urgency, yn(f.urgency_present)], [t.secrecy, yn(f.secrecy_present)], [t.codeReq, yn(f.verification_code_requested)],
  ];
  return (
    <div className="space-y-5">
      <div ref={bannerRef} tabIndex={-1} className={`rounded-2xl border-2 p-5 shadow-sm focus:outline-none sm:p-6 ${b.box}`}>
        <div className="flex items-center gap-4">
          <span className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-full ${b.iconWrap}`} aria-hidden="true">{b.icon}</span>
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider opacity-80">{t.riskResult}</p>
            <h2 className="text-3xl font-extrabold leading-tight">{bandLabel}</h2>
          </div>
        </div>
        <p className="mt-3 text-base">{note}</p>
        <div className="mt-4 flex flex-wrap items-center gap-2 border-t border-current/20 pt-4">
          <Pill tone={c.inference === "real" ? "ok" : "warn"}>{c.inference === "real" ? t.liveBadge : t.sampleBadge}</Pill>
          {c.model && <Pill tone="info">{c.model}</Pill>}
          {c.latency_ms !== null && <Pill tone="info">{(c.latency_ms / 1000).toFixed(1)} s</Pill>}
          {c.is_synthetic && <Pill tone="info">{t.syntheticLabel}</Pill>}
        </div>
        {c.language !== uiLang && <div className="mt-2 text-xs">Assessment language: {c.language === "en" ? "English" : "Roman Urdu"}</div>}
      </div>

      {(c.quotes_removed > 0 || c.amount_cleared || c.redactions > 0 || c.rule_adjusted) && (
        <Card className="text-xs text-slate-700">
          <ul className="list-disc space-y-1 pl-4">
            {c.rule_adjusted && <li>{t.note_rule}</li>}
            {c.redactions > 0 && <li>{c.redactions} {t.note_redact}</li>}
            {c.quotes_removed > 0 && <li>{c.quotes_removed} {t.note_quotes}</li>}
            {c.amount_cleared && <li>{t.note_amount}</li>}
          </ul>
        </Card>
      )}

      {message && (
        <Card title={t.yourMessage}>
          <p className="whitespace-pre-wrap wrap-break-words text-base leading-relaxed text-slate-800">
            {splitHighlights(message, a.warning_signals.map((x) => x.source_quote)).map((seg, i) =>
              seg.hit ? <mark key={i} className="rounded bg-amber-200 px-0.5 text-amber-950">{seg.text}</mark> : <span key={i}>{seg.text}</span>)}
          </p>
        </Card>
      )}

      <Card title={t.signals}>
        {a.warning_signals.length === 0 ? <p className="text-sm text-slate-600">{t.noSignals}</p> : (
          <ul className="space-y-5">
            {a.warning_signals.map((s, i) => (
              <li key={i} className="text-sm">
                <div className="font-semibold text-slate-900">{s.label}</div>
                <figure className="my-2 ml-2 border-l-4 border-teal-600 bg-slate-50 py-2 pl-3 pr-2">
                  <figcaption className="text-[11px] font-semibold uppercase tracking-wide text-teal-800">{t.fromYourMessage}</figcaption>
                  <blockquote className="mt-0.5 font-mono text-[13px] leading-snug text-slate-800">“{s.source_quote}”</blockquote>
                </figure>
                <div className="text-slate-700">{s.explanation}</div>
              </li>
            ))}
          </ul>
        )}\\
      </Card>

      <Card title={t.facts}>
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2 text-sm">
          {rows.map(([k, v]) => (<div key={k} className="contents"><dt className="text-slate-600">{k}</dt><dd className="font-medium">{v}</dd></div>))}
        </dl>
      </Card>

      <Card title={t.uncertainty}><p className="text-sm">{a.uncertainty}</p></Card>

      <Card title={t.actions}>
        <ol className="list-decimal space-y-2 pl-5 text-sm">{a.recommended_actions.map((x, i) => <li key={i}>{x}</li>)}</ol>
      </Card>

      <Card title={t.safeReply}>
        <p className="rounded-lg bg-slate-50 p-3 text-sm">{a.safe_reply}</p>
        <Btn className="mt-3" onClick={async () => { await copyText(a.safe_reply); setCopied(true); setTimeout(() => setCopied(false), 2000); }}>
          {copied ? t.copied : t.copy}
        </Btn>
        <span className="sr-only" aria-live="polite">{copied ? t.copied : ""}</span>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Btn variant="primary" onClick={onVerify}>{t.openVerify}{a.family_verification_suggested ? " ★" : ""}</Btn>
        <Btn onClick={onExport}>{t.export}</Btn>
        <Btn onClick={onEdit}>{t.edit}</Btn>
        <Btn variant="danger" onClick={onDelete}>{t.del}</Btn>
      </div>
    </div>
  );
}
