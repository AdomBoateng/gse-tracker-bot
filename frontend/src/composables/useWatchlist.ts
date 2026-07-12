import { ref, watch } from "vue";

const STORAGE_KEY = "gse-watchlist";

const loadInitial = (): Set<string> => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? new Set(JSON.parse(raw)) : new Set();
  } catch {
    return new Set();
  }
};

// Module-level so the watchlist is shared/reactive across every component that uses it
const watchlist = ref<Set<string>>(loadInitial());

watch(
  watchlist,
  (value) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...value]));
  },
  { deep: true },
);

export function useWatchlist() {
  const isWatched = (symbol: string | null | undefined): boolean =>
    !!symbol && watchlist.value.has(symbol);

  const toggle = (symbol: string | null | undefined) => {
    if (!symbol) return;
    const next = new Set(watchlist.value);
    if (next.has(symbol)) {
      next.delete(symbol);
    } else {
      next.add(symbol);
    }
    watchlist.value = next;
  };

  return { watchlist, isWatched, toggle };
}
