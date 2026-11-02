import type { CaseView, Example, Lang, ModelStatus, VStatus } from "./types";

const BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? "";

export class ApiError extends Error {
  constructor(public code: string, message: string, public status: number) { super(message); }
}

async function call<T>(path: string, init?: RequestInit, as: "json" | "text" = "json"): Promise<T> {
  let r: Response;
  try {
    r = await fetch(BASE + path, init);
  } catch {
    throw new ApiError("network", "Cannot reach the Rasta backend. Is it running on 127.0.0.1:8000?", 0);
  }
  if (!r.ok) {
    let code = "http_" + r.status, msg = "Request failed.";
    try { const j = await r.json(); code = j.error?.code ?? code; msg = j.error?.message ?? msg; } catch { /* ignore */ }
    throw new ApiError(code, msg, r.status);
  }
  return (as === "text" ? r.text() : r.json()) as Promise<T>;
}

const json = (method: string, body?: unknown): RequestInit => ({
  method, headers: { "Content-Type": "application/json" }, body: body === undefined ? undefined : JSON.stringify(body),
});

export const api = {
  examples: () => call<Example[]>("/api/examples"),
  modelStatus: () => call<ModelStatus>("/api/model-status"),
  analyze: (text: string, language: Lang) => call<CaseView>("/api/analyze", json("POST", { text, language })),
  record: (id: string, status: VStatus) => call<CaseView>(`/api/cases/${id}/verification`, json("POST", { status })),
  exportHtml: (id: string) => call<string>(`/api/cases/${id}/export`, undefined, "text"),
  remove: (id: string) => call<{ deleted: boolean }>(`/api/cases/${id}`, { method: "DELETE" }),
};
