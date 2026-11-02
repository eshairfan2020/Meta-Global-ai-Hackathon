import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { Strings } from "../i18n";
import { Btn, Card } from "./ui";

// The report HTML is built and escaped by the backend and shown in an iframe with NO scripts
// allowed (sandbox without allow-scripts); allow-same-origin only lets us call print() on it.
export default function Report({ t, caseId, onBack }: { t: Strings; caseId: string; onBack: () => void }) {
  const [html, setHtml] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const ref = useRef<HTMLIFrameElement>(null);
  useEffect(() => { api.exportHtml(caseId).then(setHtml).catch((e) => setErr(e.message)); }, [caseId]);
  return (
    <div className="space-y-5">
      <Card title={t.reportTitle}>
        {err && <p role="alert" className="text-sm text-red-800">{err}</p>}
        {!html && !err && <p className="text-sm text-slate-600">{t.loadingReport}</p>}
        {html && <iframe ref={ref} title={t.reportTitle} srcDoc={html} sandbox="allow-same-origin" className="h-[70vh] w-full rounded border border-slate-200 bg-white" />}
      </Card>
      <div className="flex gap-2">
        <Btn onClick={onBack}>{t.back}</Btn>
        <Btn variant="primary" disabled={!html} onClick={() => ref.current?.contentWindow?.print()}>{t.print}</Btn>
      </div>
    </div>
  );
}
