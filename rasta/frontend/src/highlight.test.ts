import { expect, test } from "vitest";
import { splitHighlights } from "./highlight";

const msg = "Ammi, mera phone kharab hai. Emergency hai, Rs 50000 bhej dein. Kisi ko mat batana.";

test("marks quoted phrases and keeps all text", () => {
  const segs = splitHighlights(msg, ["emergency hai, rs 50000 bhej dein", "Kisi ko mat batana"]);
  expect(segs.map((s) => s.text).join("")).toBe(msg);
  expect(segs.filter((s) => s.hit).map((s) => s.text)).toEqual(["Emergency hai, Rs 50000 bhej dein", "Kisi ko mat batana"]);
});

test("merges overlapping quotes", () => {
  const segs = splitHighlights(msg, ["Emergency hai, Rs 50000", "Rs 50000 bhej dein"]);
  expect(segs.filter((s) => s.hit).map((s) => s.text)).toEqual(["Emergency hai, Rs 50000 bhej dein"]);
});

test("ignores quotes that are not found or too short", () => {
  const segs = splitHighlights(msg, ["not in the message", "ab"]);
  expect(segs).toEqual([{ text: msg, hit: false }]);
});

test("empty message", () => {
  expect(splitHighlights("", ["abc"])).toEqual([{ text: "", hit: false }]);
});
