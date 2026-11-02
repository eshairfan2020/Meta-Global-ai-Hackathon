export interface Seg { text: string; hit: boolean }

/** Split `message` into segments, marking the parts that equal one of the quoted warning phrases.
 *  Matching is case-insensitive and whitespace-normalized; quotes that are not found (e.g. because the
 *  backend masked a code-like value) are simply not highlighted. */
export function splitHighlights(message: string, quotes: string[]): Seg[] {
  const low = message.toLowerCase();
  if (low.length !== message.length) return [{ text: message, hit: false }];
  const ranges: [number, number][] = [];
  for (const q of quotes) {
    const nq = q.replace(/\s+/g, " ").trim().toLowerCase();
    if (nq.length < 3) continue;
    const i = low.indexOf(nq);
    if (i >= 0) ranges.push([i, i + nq.length]);
  }
  ranges.sort((a, b) => a[0] - b[0]);
  const merged: [number, number][] = [];
  for (const r of ranges) {
    const last = merged[merged.length - 1];
    if (last && r[0] <= last[1]) last[1] = Math.max(last[1], r[1]);
    else merged.push([r[0], r[1]]);
  }
  const out: Seg[] = [];
  let pos = 0;
  for (const [s, e] of merged) {
    if (s > pos) out.push({ text: message.slice(pos, s), hit: false });
    out.push({ text: message.slice(s, e), hit: true });
    pos = e;
  }
  if (pos < message.length) out.push({ text: message.slice(pos), hit: false });
  return out.length ? out : [{ text: message, hit: false }];
}
