import { describe, it, expect, beforeEach } from "vitest";
import { nextTick } from "vue";
import { useWatchlist } from "../useWatchlist";

describe("useWatchlist", () => {
  beforeEach(() => {
    localStorage.clear();
    const { watchlist } = useWatchlist();
    watchlist.value = new Set();
  });

  it("starts with nothing watched", () => {
    const { isWatched } = useWatchlist();
    expect(isWatched("VBK")).toBe(false);
  });

  it("toggling adds then removes a symbol", () => {
    const { isWatched, toggle } = useWatchlist();
    toggle("VBK");
    expect(isWatched("VBK")).toBe(true);
    toggle("VBK");
    expect(isWatched("VBK")).toBe(false);
  });

  it("is null/undefined safe", () => {
    const { isWatched, toggle } = useWatchlist();
    expect(isWatched(null)).toBe(false);
    expect(isWatched(undefined)).toBe(false);
    toggle(null); // should not throw
  });

  it("persists to localStorage", async () => {
    const { toggle } = useWatchlist();
    toggle("GCM");
    await nextTick();
    const stored = JSON.parse(localStorage.getItem("gse-watchlist") ?? "[]");
    expect(stored).toContain("GCM");
  });

  it("shares state across every call (module-level singleton)", () => {
    const a = useWatchlist();
    const b = useWatchlist();
    a.toggle("SVT");
    expect(b.isWatched("SVT")).toBe(true);
  });
});
