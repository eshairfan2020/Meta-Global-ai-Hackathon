import type { ReactNode } from "react";

type Tone = "ok" | "warn" | "bad" | "info" | "busy";
const TONES: Record<Tone, string> = {
  ok: "bg-teal-50 text-teal-900 border-teal-300",
  warn: "bg-amber-50 text-amber-900 border-amber-300",
  bad: "bg-red-50 text-red-900 border-red-300",
  info: "bg-slate-100 text-slate-800 border-slate-300",
  busy: "bg-sky-50 text-sky-900 border-sky-300",
};

export function Pill({ tone, children }: { tone: Tone; children: ReactNode }) {
  return <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${TONES[tone]}`}>{children}</span>;
}

export function Card({ title, children, className = "" }: { title?: string; children: ReactNode; className?: string }) {
  return (
    <section className={`rounded-xl border border-slate-200 bg-white p-5 shadow-sm ${className}`}>
      {title && <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-teal-800">{title}</h2>}
      {children}
    </section>
  );
}

export function Btn({ variant = "secondary", size = "md", className = "", ...p }:
  React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "danger"; size?: "md" | "lg" }) {
  const v = {
    primary: "bg-teal-700 text-white hover:bg-teal-800 disabled:bg-slate-300 disabled:text-slate-600",
    secondary: "bg-white text-slate-900 border border-slate-300 hover:border-teal-500 hover:bg-teal-50 disabled:opacity-50",
    danger: "bg-white text-red-800 border border-red-300 hover:bg-red-50",
  }[variant];
  const s = size === "lg" ? "min-h-14 px-6 py-3 text-base font-semibold" : "min-h-11 px-4 py-2 text-sm font-medium";
  return <button {...p} className={`rounded-lg transition-colors ${s} ${v} ${className}`} />;
}

// Simple inline SVG icons (no dependency). Decorative: always aria-hidden.
const svgProps = {
  viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 2,
  strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true, className: "h-8 w-8",
};
export const IconWarning = () => (
  <svg {...svgProps}><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" /><path d="M12 9v4M12 17h.01" /></svg>
);
export const IconSearch = () => (
  <svg {...svgProps}><circle cx="11" cy="11" r="7" /><path d="m21 21-4.3-4.3" /></svg>
);
// Deliberately a question mark, not a check: "insufficient evidence" must never read as "safe".
export const IconUnclear = () => (
  <svg {...svgProps}><circle cx="12" cy="12" r="10" /><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 2.5-3 4.5M12 17.5h.01" /></svg>
);
