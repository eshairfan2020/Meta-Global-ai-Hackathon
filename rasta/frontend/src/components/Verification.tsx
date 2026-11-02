import type { CaseView, VStatus } from "../types";
import type { Strings } from "../i18n";
import { Btn, Card, Pill } from "./ui";

const OUTCOMES: VStatus[] = ["attempting_independent_contact", "user_recorded_confirmation", "user_recorded_denial", "inconclusive"];
const TONE = { not_checked: "info", attempting_independent_contact: "busy", user_recorded_confirmation: "warn", user_recorded_denial: "bad", inconclusive: "info" } as const;

interface Props { t: Strings; c: CaseView; busy: boolean; error: string | null; onRecord: (s: VStatus) => void; onBack: () => void; onExport: () => void }

export default function Verification({ t, c, busy, error, onRecord, onBack, onExport }: Props) {
  const label = (s: VStatus) => t[`s_${s}` as keyof Strings] as string;
  const v = c.verification;
  return (
    <div className="space-y-5">
      <Card title={t.vTitle}>
        <p className="mb-3 text-sm text-slate-700">{t.vIntro}</p>
        <ol className="list-decimal space-y-2 pl-5 text-sm">{t.vSteps.map((s, i) => <li key={i}>{s}</li>)}</ol>
        <p className="mt-3 rounded-lg border border-amber-300 bg-amber-50 p-2 text-sm text-amber-900">{t.vEmergency}</p>
      </Card>

      <Card title={t.vRecord}>
        <div className="mb-3 flex items-center gap-2 text-sm">{t.vCurrent}: <Pill tone={TONE[v.status]}>{label(v.status)}</Pill></div>
        <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">
          {OUTCOMES.map((s) => <Btn key={s} disabled={busy} onClick={() => onRecord(s)}>{label(s)}</Btn>)}
        </div>
        <p className="mt-3 text-xs text-slate-600">{t.userRecorded}</p>
        <p className="mt-1 text-xs text-slate-600">{t.noClear}</p>
        {error && <p role="alert" className="mt-2 text-sm text-red-800">{error}</p>}
      </Card>

      <Card title={t.timeline}>
        {v.events.length === 0 ? <p className="text-sm text-slate-600">{t.noEvents}</p> : (
          <ol className="space-y-2 border-l-2 border-teal-600 pl-3 text-sm">
            {v.events.map((e, i) => (
              <li key={i}><div className="font-medium">{label(e.status)}</div>
                <div className="text-xs text-slate-600">{new Date(e.timestamp).toLocaleString()} · {t.userRecorded}</div></li>
            ))}
          </ol>
        )}
      </Card>

      <div className="flex flex-wrap gap-2">
        <Btn onClick={onBack}>{t.back}</Btn>
        <Btn variant="primary" onClick={onExport}>{t.export}</Btn>
      </div>
    </div>
  );
}
