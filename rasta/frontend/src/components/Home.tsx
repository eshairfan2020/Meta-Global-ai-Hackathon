import type { Example, Lang, ModelStatus } from "../types";
import type { Strings } from "../i18n";
import { Btn, Card } from "./ui";

export const MAX_CHARS = 3000;
export const norm = (s: string) => s.replace(/\s+/g, " ").trim();

interface Props {
  t: Strings; lang: Lang; text: string; examples: Example[]; status: ModelStatus | null;
  busy: boolean; hasResult: boolean; onText: (s: string) => void; onAnalyze: () => void; onBack: () => void;
}

export default function Home({ t, lang, text, examples, status, busy, hasResult, onText, onAnalyze, onBack }: Props) {
  const isMock = status?.provider === "mock";
  const len = norm(text).length;
  const over = len > MAX_CHARS;
  const matched = examples.find((e) => norm(e.text) === norm(text));
  return (
    <div className="space-y-8">
      <section className="space-y-2 pt-2">
        <h2 className="text-2xl font-bold leading-tight text-slate-900 sm:text-3xl">{t.homeHeadline}</h2>
        <p className="text-base text-slate-700">{t.homeSub}</p>
      </section>

      <Card>
        <label htmlFor="msg" className="mb-2 block text-sm font-semibold text-slate-800">{t.textLabel}</label>
        {matched && <p className="mb-2 text-xs font-medium text-teal-800">{t.syntheticLabel}</p>}
        <textarea id="msg" value={text} onChange={(e) => onText(e.target.value)} rows={7} placeholder={t.placeholder}
          disabled={busy} className="w-full rounded-lg border border-slate-300 p-3 text-base disabled:bg-slate-50" />
        <div className={`mt-1 text-right text-xs ${over ? "font-semibold text-red-700" : "text-slate-500"}`}>
          {len} / {MAX_CHARS} {t.chars}
        </div>
        <p className="mt-3 rounded-lg border border-amber-300 bg-amber-50 p-3 text-xs text-amber-900">{t.warnCodes}</p>
        {isMock && <p className="mt-3 rounded-lg border border-slate-300 bg-slate-50 p-3 text-xs text-slate-700">{t.mockExplain}</p>}
        <div className="mt-5 flex flex-wrap gap-3">
          <Btn variant="primary" size="lg" onClick={onAnalyze} disabled={busy || len === 0 || over} className="w-full sm:w-auto sm:min-w-64">
            {isMock ? t.analyzeMock : t.analyzeOllama}
          </Btn>
          {hasResult && <Btn size="lg" className="font-medium" onClick={onBack} disabled={busy}>{t.back}</Btn>}
        </div>
        <p className="mt-3 text-xs text-slate-600">{t.notChat}</p>
      </Card>

      <section aria-label={t.orTryExample} className="space-y-3">
        <div className="flex items-center gap-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
          <span className="h-px flex-1 bg-slate-200" aria-hidden="true" />
          <span>{t.orTryExample}</span>
          <span className="h-px flex-1 bg-slate-200" aria-hidden="true" />
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {examples.map((e) => (
            <button key={e.id} onClick={() => onText(e.text)} disabled={busy}
              className={`min-h-11 rounded-full border px-4 py-2 text-sm font-medium transition-colors disabled:opacity-50 ${
                matched?.id === e.id ? "border-teal-700 bg-teal-700 text-white" : "border-teal-300 bg-white text-teal-900 hover:bg-teal-50"}`}>
              {lang === "en" ? e.title_en : e.title_ur}
              <span className="sr-only">{t.loadExample}</span>
            </button>
          ))}
        </div>
        <p className="text-center text-xs text-slate-600">{t.syntheticLabel}</p>
      </section>

      <p className="px-1 text-xs text-slate-600">{t.privacy}</p>
    </div>
  );
}
