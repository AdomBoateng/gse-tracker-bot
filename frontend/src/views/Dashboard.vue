<template>
  <!-- Loading skeleton -->
  <div v-if="loading" style="max-width: 1360px; margin: var(--space-6) auto; padding: 0 var(--space-4)">
    <div class="gse-card" style="padding: var(--space-8)">
      <div style="height: 24px; width: 30%; background: var(--color-neutral-300); margin-bottom: var(--space-6)"></div>
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: var(--space-4)">
        <div style="height: 140px; background: var(--color-neutral-200)"></div>
        <div style="height: 140px; background: var(--color-neutral-200)"></div>
      </div>
    </div>
  </div>

  <div v-else>
    <!-- ══════════════════ Layout 1a — Ledger ══════════════════ -->
    <div v-if="layout === '1a'" class="gse-card" style="max-width: 1360px; margin: var(--space-6) auto">
      <nav class="nav" style="padding: var(--space-3) var(--space-6)">
        <span class="nav-brand">GSE <span style="color: var(--color-accent)">·</span> TRACKER</span>
        <a :aria-current="!watchlistFilter ? 'page' : undefined" @click="watchlistFilter = false">Dashboard</a>
        <a :aria-current="watchlistFilter ? 'page' : undefined" @click="watchlistFilter = true; page = 1">
          Watchlist ({{ watchlistCount }})
        </a>
        <div style="margin-left: auto; display: flex; align-items: center; gap: var(--space-3)">
          <LayoutToggle v-model="layout" />
          <span class="tag" :style="statusTagStyle">{{ statusLabel }}</span>
          <select v-model="selectedCurrency" class="input" style="min-height: 32px; width: auto; padding: 4px 8px">
            <option v-for="c in availableCurrencies" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
      </nav>

      <div style="padding: var(--space-6)">
        <!-- Market status band -->
        <div :style="`display:grid;grid-template-columns:2fr 1fr;border:2px solid var(--color-divider);border-top:4px solid ${heroBarColor}`">
          <div style="padding: var(--space-6); border-right: 2px solid var(--color-divider)">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px">
              <span :class="statusDotClass" style="width: 9px; height: 9px; border-radius: 50%" :style="{ background: statusDotColor }"></span>
              <h6 style="margin: 0; color: var(--color-text)">{{ statusHeading }}</h6>
            </div>
            <h2 style="margin: 0 0 var(--space-2)">{{ marketHeadline }}</h2>
            <p class="text-muted" style="margin: 0">{{ marketSubline }}</p>
            <p class="text-muted" style="margin-top: var(--space-2); font-size: 12px">Market hours 10:00–15:00 GMT</p>
          </div>
          <div style="padding: var(--space-6); display: flex; flex-direction: column; justify-content: center; gap: 8px">
            <div style="display: flex; justify-content: space-between; align-items: baseline">
              <h6 style="margin: 0">Composite change</h6>
              <span class="text-muted" style="font-size: 11px" title="Unofficial market-cap-weighted proxy, not the official GSE-CI">GSE-CI ⓘ</span>
            </div>
            <h3 style="margin: 0" :style="{ color: compositeColor }">{{ compositeChangeLabel }}</h3>
            <Sparkline :series="compositeHistory" :color="compositeColor" :height="52" />
          </div>
        </div>

        <!-- Market summary (closed) -->
        <div v-if="!marketOpen" style="margin-top: var(--space-6); border: 2px solid var(--color-divider); border-top: none; padding: var(--space-6)">
          <MarketSummary
            :top-gainer="gainers[0] ?? null"
            :top-loser="losers[0] ?? null"
            :best-performer="bestPerformer"
            :worst-performer="worstPerformer"
            :date-label="dateDisplay"
            :analysis="analysisText"
          />
        </div>

        <!-- Stats -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); border: 2px solid var(--color-divider); border-top: none; margin-top: var(--space-6)">
          <div style="padding: var(--space-4) var(--space-6); border-right: 1px solid var(--color-divider)">
            <h6 class="text-muted" style="margin: 0 0 6px">Listed companies</h6>
            <h3 style="margin: 0">{{ liveData.length }}</h3>
          </div>
          <div style="padding: var(--space-4) var(--space-6); border-right: 1px solid var(--color-divider)">
            <h6 class="text-muted" style="margin: 0 0 6px">Volume traded</h6>
            <h3 style="margin: 0">{{ totalVolume.toLocaleString() }}</h3>
          </div>
          <div style="padding: var(--space-4) var(--space-6)">
            <h6 class="text-muted" style="margin: 0 0 6px">Advancing / declining</h6>
            <h3 style="margin: 0">
              <span style="color: var(--color-positive)">{{ advancing }}</span>
              <span class="text-muted" style="font-size: 16px">/</span>
              <span style="color: var(--color-negative)">{{ declining }}</span>
            </h3>
          </div>
        </div>

        <!-- Gainers / losers -->
        <div style="margin-top: var(--space-8)">
          <GainersLosers :gainers="gainers" :losers="losers" @open="openStockDetail" />
        </div>

        <div class="hr" style="margin-top: var(--space-8)"></div>

        <!-- All companies -->
        <div>
          <div style="display: flex; align-items: center; gap: var(--space-3); flex-wrap: wrap; margin-bottom: var(--space-4)">
            <h4 style="margin: 0; margin-right: auto">All companies</h4>
            <input v-model="searchQuery" class="input" placeholder="Search name or symbol" style="width: 220px" @input="page = 1" />
            <div class="seg">
              <label class="seg-opt" :class="{ 'is-active': sortDir === 'asc' }" @click="sortDir = 'asc'">A → Z</label>
              <label class="seg-opt" :class="{ 'is-active': sortDir === 'desc' }" @click="sortDir = 'desc'">Z → A</label>
            </div>
            <button class="btn btn-secondary" :style="watchlistBtnStyle" @click="watchlistFilter = !watchlistFilter; page = 1">
              <svg width="14" height="14" viewBox="0 0 24 24" :fill="watchlistFilter ? 'var(--color-accent)' : 'none'" stroke="currentColor" stroke-width="2"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 20.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
              Watchlist
            </button>
            <a class="btn btn-secondary" :href="csvExportUrl" download="gse-companies.csv">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path></svg>
              Export CSV
            </a>
          </div>
          <CompaniesTable
            :rows="pageRows"
            :page-summary="pageSummary"
            :page="page"
            :total-pages="totalPages"
            @open="openStockDetail"
            @toggle-watch="toggleWatchlist"
            @prev="page = Math.max(1, page - 1)"
            @next="page = Math.min(totalPages, page + 1)"
          />
        </div>

        <!-- IPO section -->
        <div class="hr" style="margin-top: var(--space-8)"></div>
        <IpoSection />

        <div class="hr" style="margin-top: var(--space-8)"></div>
        <NewsSection />

        <div class="hr" style="margin-top: var(--space-8)"></div>
        <p class="text-muted" style="font-size: 12px; max-width: 640px">
          Disclaimer — this data is illustrative and may be delayed. Verify with the official Ghana Stock Exchange before making investment decisions.
        </p>
      </div>
    </div>

    <!-- ══════════════════ Layout 1b — Split terminal ══════════════════ -->
    <div v-else class="gse-card" style="max-width: 1360px; margin: var(--space-6) auto; display: grid; grid-template-columns: 260px 1fr">
      <aside style="border-right: 2px solid var(--color-divider); padding: var(--space-6) var(--space-4); display: flex; flex-direction: column; gap: var(--space-6)">
        <div>
          <span class="nav-brand" style="display: block">GSE <span style="color: var(--color-accent)">·</span> TRACKER</span>
          <p class="text-muted" style="font-size: 12px; margin-top: 6px">{{ dateDisplay }}</p>
        </div>
        <LayoutToggle v-model="layout" block />
        <div style="border: 2px solid var(--color-divider); padding: var(--space-3)">
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px">
            <span :class="statusDotClass" style="width: 9px; height: 9px; border-radius: 50%" :style="{ background: statusDotColor }"></span>
            <h6 style="margin: 0">{{ statusHeading }}</h6>
          </div>
          <p style="margin: 0; font-weight: 600; font-size: 15px">{{ marketHeadline }}</p>
          <p class="text-muted" style="margin: 4px 0 0; font-size: 12px">{{ marketSubline }}</p>
        </div>
        <nav style="display: flex; flex-direction: column; gap: 2px">
          <a class="nav" style="padding: 8px 0; border: none; border-bottom: 1px solid var(--color-divider); cursor: pointer" :aria-current="!watchlistFilter ? 'page' : undefined" @click="watchlistFilter = false">Dashboard</a>
          <a class="nav" style="padding: 8px 0; border: none; border-bottom: 1px solid var(--color-divider); cursor: pointer" :aria-current="watchlistFilter ? 'page' : undefined" @click="watchlistFilter = true; page = 1">Watchlist ({{ watchlistCount }})</a>
        </nav>
        <div class="field">
          <label>Search</label>
          <input v-model="searchQuery" class="input" placeholder="Name or symbol" @input="page = 1" />
        </div>
        <div class="field">
          <label>Currency</label>
          <select v-model="selectedCurrency" class="input">
            <option v-for="c in availableCurrencies" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <button class="btn btn-secondary btn-block" :style="watchlistBtnStyle" @click="watchlistFilter = !watchlistFilter; page = 1">Watchlist only</button>
        <a class="btn btn-secondary btn-block" :href="csvExportUrl" download="gse-companies.csv">Export CSV</a>
      </aside>

      <div style="padding: var(--space-6)">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: var(--space-4); border-bottom: 2px solid var(--color-divider); padding-bottom: var(--space-4); margin-bottom: var(--space-6)">
          <div>
            <h6 class="text-muted" style="margin: 0 0 4px">Composite change</h6>
            <h3 style="margin: 0" :style="{ color: compositeColor }">{{ compositeChangeLabel }}</h3>
          </div>
          <div style="width: 220px">
            <Sparkline :series="compositeHistory" :color="compositeColor" width="220" :height="52" />
          </div>
          <div style="text-align: right">
            <h6 class="text-muted" style="margin: 0 0 4px">Volume traded</h6>
            <h3 style="margin: 0">{{ totalVolume.toLocaleString() }}</h3>
          </div>
          <div style="text-align: right">
            <h6 class="text-muted" style="margin: 0 0 4px">Advancing / declining</h6>
            <h3 style="margin: 0">
              <span style="color: var(--color-positive)">{{ advancing }}</span>
              <span class="text-muted" style="font-size: 16px">/</span>
              <span style="color: var(--color-negative)">{{ declining }}</span>
            </h3>
          </div>
        </div>

        <div v-if="!marketOpen" style="border: 2px solid var(--color-divider); padding: var(--space-5); margin-bottom: var(--space-6)">
          <MarketSummary
            dense
            :top-gainer="gainers[0] ?? null"
            :top-loser="losers[0] ?? null"
            :best-performer="bestPerformer"
            :worst-performer="worstPerformer"
            :date-label="dateDisplay"
            :analysis="analysisText"
          />
        </div>

        <div style="margin-bottom: var(--space-6)">
          <GainersLosers dense :gainers="gainers" :losers="losers" @open="openStockDetail" />
        </div>

        <CompaniesTable
          :rows="pageRows"
          :page-summary="pageSummary"
          :page="page"
          :total-pages="totalPages"
          @open="openStockDetail"
          @toggle-watch="toggleWatchlist"
          @prev="page = Math.max(1, page - 1)"
          @next="page = Math.min(totalPages, page + 1)"
        />

        <div class="hr" style="margin-top: var(--space-8)"></div>
        <IpoSection />

        <div class="hr" style="margin-top: var(--space-8)"></div>
        <NewsSection />

        <div class="hr" style="margin-top: var(--space-8)"></div>
        <p class="text-muted" style="font-size: 11px; max-width: 560px">
          Disclaimer — illustrative data only; verify with the official Ghana Stock Exchange before making investment decisions.
        </p>
      </div>
    </div>

    <!-- Toasts -->
    <div style="position: fixed; bottom: var(--space-6); right: var(--space-6); display: flex; flex-direction: column; gap: 8px; width: 280px; z-index: 50">
      <div
        v-for="t in toasts"
        :key="t.id"
        style="background: var(--color-bg); border: 1px solid var(--color-divider); box-shadow: var(--shadow-md); padding: var(--space-3); display: flex; justify-content: space-between; gap: 8px; align-items: flex-start"
        :style="{ borderLeft: `3px solid ${t.type === 'error' ? 'var(--color-accent)' : 'var(--color-text)'}` }"
        role="alert"
      >
        <p style="margin: 0; font-size: 13px">{{ t.message }}</p>
        <button style="background: none; border: none; padding: 0; cursor: pointer; color: var(--color-text)" @click="removeToast(t.id)">✕</button>
      </div>
    </div>
  </div>

  <StockDetailModal :stock="selectedStock" @close="closeStockDetail" />
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import Sparkline from "../components/Sparkline.vue";
import GainersLosers from "../components/GainersLosers.vue";
import MarketSummary from "../components/MarketSummary.vue";
import CompaniesTable from "../components/CompaniesTable.vue";
import IpoSection from "../components/IpoSection.vue";
import LayoutToggle from "../components/LayoutToggle.vue";
import NewsSection from "../components/NewsSection.vue";
import StockDetailModal from "../components/StockDetailModal.vue";
import {
  fetchLiveData,
  fetchComposite,
  fetchCompositeHistory,
  csvExportUrl,
  type MarketData,
  type CompositeSummary,
  type CompositeHistoryPoint,
} from "../services/api";
import { useWatchlist } from "../composables/useWatchlist";
import { useCurrency } from "../composables/useCurrency";
import { decorate, type DecoratedStock } from "../types";

interface Toast {
  id: number;
  message: string;
  type: "success" | "error";
}

const LAYOUT_KEY = "gse-layout";
const layout = ref<"1a" | "1b">(
  (localStorage.getItem(LAYOUT_KEY) as "1a" | "1b") || "1a",
);
watch(layout, (v) => localStorage.setItem(LAYOUT_KEY, v));

const liveData = ref<MarketData[]>([]);
const compositeData = ref<CompositeSummary | null>(null);
const compositeHistory = ref<CompositeHistoryPoint[]>([]);
const loading = ref(true);

const searchQuery = ref("");
const sortDir = ref<"asc" | "desc">("asc");
const watchlistFilter = ref(false);
const page = ref(1);
const pageSize = 8;

const toasts = ref<Toast[]>([]);
const selectedStock = ref<MarketData | null>(null);

const { isWatched, toggle } = useWatchlist();
const { selectedCurrency, availableCurrencies, formatPrice } = useCurrency();

const watchlistCount = computed(
  () => liveData.value.filter((s) => isWatched(s.symbol)).length,
);

// ── Market status (local time; Ghana runs on GMT/UTC) ──
const now = ref(new Date());
let clock: number | null = null;

const isNextDayMode = computed(() => {
  const minutes = now.value.getHours() * 60 + now.value.getMinutes();
  return minutes >= 0 && minutes < 10 * 60;
});
const marketOpen = computed(() => {
  if (isNextDayMode.value) return false;
  const minutes = now.value.getHours() * 60 + now.value.getMinutes();
  return minutes >= 10 * 60 && minutes < 15 * 60;
});

const dateDisplay = computed(() => {
  const d = isNextDayMode.value ? new Date(now.value.getTime() - 86400000) : now.value;
  return d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
});

const statusHeading = computed(() => (marketOpen.value ? "Live" : "Closed"));
const statusLabel = computed(() => (marketOpen.value ? "OPEN" : "CLOSED"));
const marketHeadline = computed(() => (marketOpen.value ? "Market is open" : "Market is closed"));
const marketSubline = computed(() =>
  marketOpen.value ? "Trading closes at 15:00 GMT" : "Opens next session at 10:00 GMT",
);
const statusDotColor = computed(() => (marketOpen.value ? "var(--color-positive)" : "var(--color-negative)"));
const statusDotClass = computed(() => (marketOpen.value ? "gse-live-dot" : ""));
const heroBarColor = computed(() => (marketOpen.value ? "var(--color-positive)" : "var(--color-accent)"));
const statusTagStyle = computed(() =>
  marketOpen.value
    ? { background: "var(--color-neutral-200)", color: "var(--color-neutral-800)" }
    : { background: "var(--color-accent-100)", color: "var(--color-accent-800)" },
);

// ── Decorated data ──
const decorated = computed<DecoratedStock[]>(() =>
  liveData.value.map((s) => decorate(s, formatPrice)),
);

const gainers = computed<DecoratedStock[]>(() =>
  decorated.value
    .filter((s) => s.change > 0)
    .sort((a, b) => b.change - a.change)
    .slice(0, 5)
    .map((s, i) => ({ ...s, rank: i + 1 })),
);
const losers = computed<DecoratedStock[]>(() =>
  decorated.value
    .filter((s) => s.change < 0)
    .sort((a, b) => a.change - b.change)
    .slice(0, 5)
    .map((s, i) => ({ ...s, rank: i + 1 })),
);

const byPercent = computed(() =>
  [...decorated.value].sort(
    (a, b) => b.change / (b.price || 1) - a.change / (a.price || 1),
  ),
);
const bestPerformer = computed(() => byPercent.value[0] ?? null);
const worstPerformer = computed(() =>
  byPercent.value.length ? byPercent.value[byPercent.value.length - 1] : null,
);

const totalVolume = computed(() => liveData.value.reduce((sum, s) => sum + s.volume, 0));
const advancing = computed(() => liveData.value.filter((s) => s.change > 0).length);
const declining = computed(() => liveData.value.filter((s) => s.change < 0).length);

const compositeChangePercent = computed(
  () => compositeData.value?.composite_change_percent ?? 0,
);
const compositeUp = computed(() => compositeChangePercent.value >= 0);
const compositeColor = computed(() =>
  compositeUp.value ? "var(--color-positive)" : "var(--color-negative)",
);
const compositeChangeLabel = computed(
  () => `${compositeUp.value ? "+" : ""}${compositeChangePercent.value.toFixed(2)}%`,
);

const analysisText = computed(() => {
  const tg = gainers.value[0];
  const tl = losers.value[0];
  return (
    `As of ${dateDisplay.value}, ${liveData.value.length} listed companies traded a combined ` +
    `${totalVolume.value.toLocaleString()} shares. ` +
    `${tg ? tg.name : "The market"} led advancers` +
    `${tl ? ` while ${tl.name} led decliners` : ""}, ` +
    `leaving the composite ${compositeUp.value ? "up" : "down"} ` +
    `${Math.abs(compositeChangePercent.value).toFixed(2)}% on the session.`
  );
});

// ── Table filtering / sorting / pagination ──
const filteredStocks = computed<DecoratedStock[]>(() => {
  let list = decorated.value;
  if (watchlistFilter.value) list = list.filter((s) => isWatched(s.symbol));
  const q = searchQuery.value.trim().toLowerCase();
  if (q) {
    list = list.filter(
      (s) =>
        s.name.toLowerCase().includes(q) ||
        (s.symbol ? s.symbol.toLowerCase().includes(q) : false),
    );
  }
  return [...list].sort((a, b) =>
    sortDir.value === "asc" ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name),
  );
});

const totalPages = computed(() => Math.max(1, Math.ceil(filteredStocks.value.length / pageSize)));
const clampedPage = computed(() => Math.min(page.value, totalPages.value));
const pageRows = computed(() =>
  filteredStocks.value.slice((clampedPage.value - 1) * pageSize, clampedPage.value * pageSize),
);
const pageSummary = computed(() => {
  const total = filteredStocks.value.length;
  if (total === 0) return "No companies";
  const start = (clampedPage.value - 1) * pageSize + 1;
  const end = Math.min(clampedPage.value * pageSize, total);
  return `Showing ${start}–${end} of ${total}`;
});

const watchlistBtnStyle = computed(() =>
  watchlistFilter.value
    ? "background:var(--color-accent-100);border-color:var(--color-accent)"
    : "",
);

// ── Actions ──
const openStockDetail = (stock: MarketData) => {
  selectedStock.value = stock;
};
const closeStockDetail = () => {
  selectedStock.value = null;
};
const toggleWatchlist = (symbol: string | null) => {
  if (!symbol) return;
  const wasWatched = isWatched(symbol);
  toggle(symbol);
  addToast(wasWatched ? `Removed ${symbol} from watchlist` : `Added ${symbol} to watchlist`);
};

const addToast = (message: string, type: "success" | "error" = "success") => {
  const id = Date.now() + Math.random();
  toasts.value.push({ id, message, type });
  setTimeout(() => removeToast(id), 3000);
};
const removeToast = (id: number) => {
  toasts.value = toasts.value.filter((t) => t.id !== id);
};

// ── Data loading ──
const loadLive = async () => {
  try {
    liveData.value = await fetchLiveData();
  } catch (e) {
    console.error("Error fetching live market data:", e);
    addToast("Failed to load market data", "error");
  }
};
const loadComposite = async () => {
  try {
    compositeData.value = await fetchComposite();
    compositeHistory.value = await fetchCompositeHistory();
  } catch (e) {
    console.error("Error fetching composite data:", e);
  }
};

let dataInterval: number | null = null;

onMounted(async () => {
  // Show the page as soon as live prices arrive; the composite endpoint is
  // slower (it fetches shares outstanding per symbol) so it fills in after.
  await loadLive();
  loading.value = false;
  loadComposite();
  dataInterval = window.setInterval(() => {
    loadLive();
    loadComposite();
  }, 60000);
  clock = window.setInterval(() => {
    now.value = new Date();
  }, 30000);
});

onUnmounted(() => {
  if (dataInterval) clearInterval(dataInterval);
  if (clock) clearInterval(clock);
});
</script>
