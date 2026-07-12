<template>
  <div class="px-4 sm:px-6 py-6 max-w-[1360px] mx-auto">
    <div v-if="loading" class="space-y-6 animate-fadeIn">
      <div class="border-2 border-divider h-48"></div>
      <div class="border-2 border-divider h-32"></div>
      <div class="border-2 border-divider h-96"></div>
    </div>

    <div v-else>
      <!-- Market status band -->
      <div
        class="grid grid-cols-1 md:grid-cols-[2fr_1fr] border-2 border-divider border-t-4"
        :style="{ borderTopColor: marketOpen ? 'var(--color-positive)' : 'var(--color-accent)' }"
      >
        <div class="p-6 border-b-2 md:border-b-0 md:border-r-2 border-divider">
          <div class="flex items-center gap-2.5 mb-1.5">
            <span
              class="w-2.5 h-2.5 rounded-full"
              :class="marketOpen ? 'gse-live-dot' : ''"
              :style="{ background: marketOpen ? 'var(--color-positive)' : 'var(--color-negative)' }"
            ></span>
            <h6 class="!m-0">{{ marketOpen ? "Live" : "Closed" }}</h6>
          </div>
          <h2 class="!mb-2">{{ marketOpen ? "Market is open" : "Market is closed" }}</h2>
          <p class="text-muted !mb-0">
            {{ marketOpen ? `Closes in ${timeRemaining}` : `Opens in ${timeToOpen}` }}
          </p>
          <p class="text-muted mt-2 text-xs">Market hours 10:00&ndash;15:00 GMT</p>
        </div>
        <div class="p-6 flex flex-col justify-center gap-2">
          <div class="flex justify-between items-baseline">
            <h6 class="!m-0">Composite change</h6>
            <span class="text-muted text-[11px]">GSE-CI</span>
          </div>
          <h3 class="!m-0" :style="{ color: compositeColor }">{{ compositeChangeLabel }}</h3>
          <CompositeChart :points="compositeHistory" />
          <div v-if="compositeHistory.length >= 2" class="flex justify-between">
            <span class="text-muted text-[10px]">{{ compositeHistory[0].date }}</span>
            <span class="text-muted text-[10px]">{{ compositeHistory[compositeHistory.length - 1].date }}</span>
          </div>
        </div>
      </div>

      <!-- Market summary (closed only) -->
      <div v-if="!marketOpen" class="mt-6 border-2 border-t-0 border-divider p-6">
        <div class="flex items-center gap-1.5 mb-3">
          <span class="w-2 h-2 rounded-full bg-ink shrink-0"></span>
          <h5 class="!m-0">Today's market summary</h5>
          <span class="text-muted text-xs">{{ dateDisplay }}</span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div
            v-for="card in summaryCards"
            :key="card.title"
            class="gse-sum-card border-2 border-divider p-4 relative overflow-hidden"
            :style="{ '--gse-accent': card.accent }"
          >
            <h6 class="text-muted !mb-2.5">{{ card.title }}</h6>
            <div v-if="card.stock" class="flex items-center gap-2 mb-3">
              <LogoChip :stock="card.stock" size="32" />
              <div class="min-w-0">
                <div class="font-semibold text-sm truncate">{{ card.stock.name }}</div>
                <span class="text-muted text-[11px]">{{ card.stock.sector }}</span>
              </div>
            </div>
            <div v-else class="text-muted text-sm mb-3">&mdash;</div>
            <h3 class="!m-0" :style="{ color: card.color }">{{ card.label }}</h3>
          </div>
        </div>
        <p class="text-muted mt-4 leading-relaxed">{{ marketAnalysisText }}</p>
      </div>

      <!-- Stats row -->
      <div class="grid grid-cols-1 sm:grid-cols-3 border-2 border-divider border-t-0 mt-6">
        <div class="p-4 sm:px-6 border-b sm:border-b-0 sm:border-r border-divider">
          <h6 class="text-muted !mb-1.5">Listed companies</h6>
          <h3 class="!m-0">{{ liveData.length }}</h3>
        </div>
        <div class="p-4 sm:px-6 border-b sm:border-b-0 sm:border-r border-divider">
          <h6 class="text-muted !mb-1.5">Volume traded</h6>
          <h3 class="!m-0 tabular-nums">{{ totalVolume.toLocaleString() }}</h3>
        </div>
        <div class="p-4 sm:px-6">
          <h6 class="text-muted !mb-1.5">Advancing / declining</h6>
          <h3 class="!m-0">
            <span style="color: var(--color-positive)">{{ gainersCount }}</span>
            <span class="text-muted text-base"> / </span>
            <span style="color: var(--color-negative)">{{ losersCount }}</span>
          </h3>
        </div>
      </div>

      <!-- Gainers / Losers -->
      <div class="grid grid-cols-1 md:grid-cols-2 mt-8 gap-6 md:gap-0">
        <div class="md:pr-6 md:border-r-2 border-divider">
          <div class="flex items-center gap-2 mb-3">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-text)" stroke-width="2"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline><polyline points="16 7 22 7 22 13"></polyline></svg>
            <h4 class="!m-0">Top gainers</h4>
          </div>
          <div
            v-for="(s, i) in gainers"
            :key="s.symbol ?? s.name"
            class="gse-row grid items-center gap-3 py-2 border-b border-divider last:border-0 cursor-pointer"
            style="grid-template-columns: 20px 36px 1fr auto auto"
            @click="openStockDetail(s)"
          >
            <span class="text-muted text-[11px]">{{ i + 1 }}</span>
            <LogoChip :stock="s" size="36" />
            <div class="min-w-0">
              <div class="font-semibold truncate">{{ s.name }}</div>
              <span class="text-muted text-[11px]">{{ s.sector }}</span>
            </div>
            <span class="font-semibold tabular-nums">{{ formatPrice(s.price) }}</span>
            <span class="font-semibold tabular-nums" style="color: var(--color-positive)">&#9650; {{ s.change.toFixed(2) }}</span>
          </div>
        </div>
        <div class="md:pl-6">
          <div class="flex items-center gap-2 mb-3">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-negative)" stroke-width="2"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"></polyline><polyline points="16 17 22 17 22 11"></polyline></svg>
            <h4 class="!m-0">Top losers</h4>
          </div>
          <div
            v-for="(s, i) in losers"
            :key="s.symbol ?? s.name"
            class="gse-row grid items-center gap-3 py-2 border-b border-divider last:border-0 cursor-pointer"
            style="grid-template-columns: 20px 36px 1fr auto auto"
            @click="openStockDetail(s)"
          >
            <span class="text-muted text-[11px]">{{ i + 1 }}</span>
            <LogoChip :stock="s" size="36" />
            <div class="min-w-0">
              <div class="font-semibold truncate">{{ s.name }}</div>
              <span class="text-muted text-[11px]">{{ s.sector }}</span>
            </div>
            <span class="font-semibold tabular-nums">{{ formatPrice(s.price) }}</span>
            <span class="font-semibold tabular-nums" style="color: var(--color-negative)">&#9660; {{ Math.abs(s.change).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <div class="hr"></div>

      <!-- All companies -->
      <div>
        <div class="flex items-center gap-3 flex-wrap mb-4">
          <h4 class="!m-0 mr-auto">All companies</h4>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search name or symbol"
            class="bg-surface border border-divider px-2.5 py-1.5 text-sm w-[220px] min-h-[36px]"
          />
          <div class="inline-flex overflow-hidden border border-divider">
            <label
              class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[13px] cursor-pointer"
              :class="sortDir === 'asc' ? 'bg-accent text-bg' : 'hover:bg-black/5'"
            >
              <input type="radio" name="sort-dir" class="sr-only" :checked="sortDir === 'asc'" @change="sortDir = 'asc'" />
              A &rarr; Z
            </label>
            <label
              class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[13px] cursor-pointer border-l border-divider"
              :class="sortDir === 'desc' ? 'bg-accent text-bg' : 'hover:bg-black/5'"
            >
              <input type="radio" name="sort-dir" class="sr-only" :checked="sortDir === 'desc'" @change="sortDir = 'desc'" />
              Z &rarr; A
            </label>
          </div>
          <button
            class="inline-flex items-center gap-1.5 border px-3 py-1.5 text-[13px] font-heading font-extrabold"
            :class="showWatchlistOnly ? 'bg-accent-100 border-accent' : 'border-divider'"
            @click="showWatchlistOnly = !showWatchlistOnly"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" :fill="showWatchlistOnly ? 'var(--color-accent)' : 'none'" stroke="currentColor" stroke-width="2"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 20.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
            Watchlist
          </button>
          <a
            :href="csvExportUrl"
            download
            class="inline-flex items-center gap-1.5 border border-divider px-3 py-1.5 text-[13px] font-heading font-extrabold"
          >
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path></svg>
            Export CSV
          </a>
        </div>

        <table class="w-full border-collapse text-sm">
          <thead>
            <tr>
              <th class="text-left text-[11px] tracking-wide uppercase text-muted p-2 border-b-2 border-divider">Company</th>
              <th class="text-left text-[11px] tracking-wide uppercase text-muted p-2 border-b-2 border-divider">Sector</th>
              <th class="text-right text-[11px] tracking-wide uppercase text-muted p-2 border-b-2 border-divider">Volume</th>
              <th class="text-right text-[11px] tracking-wide uppercase text-muted p-2 border-b-2 border-divider">Price</th>
              <th class="text-right text-[11px] tracking-wide uppercase text-muted p-2 border-b-2 border-divider">Change</th>
              <th class="p-2 border-b-2 border-divider"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="s in paginatedStocks"
              :key="s.symbol ?? s.name"
              class="cursor-pointer hover:bg-black/[0.04]"
              @click="openStockDetail(s)"
            >
              <td class="p-2 border-b border-divider">
                <div class="flex items-center gap-3">
                  <LogoChip :stock="s" size="34" />
                  <div class="font-semibold">{{ s.name }}</div>
                </div>
              </td>
              <td class="p-2 border-b border-divider text-muted">{{ s.sector }}</td>
              <td class="p-2 border-b border-divider text-right tabular-nums">{{ s.volume.toLocaleString() }}</td>
              <td class="p-2 border-b border-divider text-right font-semibold tabular-nums">{{ formatPrice(s.price) }}</td>
              <td
                class="p-2 border-b border-divider text-right font-semibold tabular-nums"
                :style="{ color: s.change > 0 ? 'var(--color-positive)' : s.change < 0 ? 'var(--color-negative)' : 'var(--color-text)' }"
              >
                {{ s.change > 0 ? "+" : "" }}{{ s.change.toFixed(2) }} ({{ (Math.abs(s.change) / s.price * 100).toFixed(1) }}%)
              </td>
              <td class="p-2 border-b border-divider text-right">
                <button
                  class="w-8 h-8 inline-flex items-center justify-center"
                  :aria-label="isWatched(s.symbol) ? 'Remove from watchlist' : 'Add to watchlist'"
                  @click.stop="toggleWatchlist(s.symbol)"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" :fill="isWatched(s.symbol) ? 'var(--color-accent)' : 'none'" stroke="var(--color-text)" stroke-width="2"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 20.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path></svg>
                </button>
              </td>
            </tr>
            <tr v-if="paginatedStocks.length === 0">
              <td colspan="6" class="text-center p-8 text-muted">No companies match this filter.</td>
            </tr>
          </tbody>
        </table>
        <div class="flex items-center justify-between pt-3">
          <p class="text-muted text-xs !m-0">{{ pageSummary }}</p>
          <div class="flex gap-1.5">
            <button
              class="border border-divider w-9 h-9 inline-flex items-center justify-center disabled:opacity-45 disabled:cursor-not-allowed"
              :disabled="page === 0"
              aria-label="Previous page"
              @click="page = Math.max(0, page - 1)"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"></path></svg>
            </button>
            <button
              class="border border-divider w-9 h-9 inline-flex items-center justify-center disabled:opacity-45 disabled:cursor-not-allowed"
              :disabled="page >= totalPages - 1"
              aria-label="Next page"
              @click="page = Math.min(totalPages - 1, page + 1)"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"></path></svg>
            </button>
          </div>
        </div>
      </div>

      <div class="hr mt-8"></div>
      <p class="text-muted text-xs max-w-[640px]">
        Disclaimer &mdash; this data is illustrative only. Real-time market data may be delayed; verify with the official Ghana Stock Exchange before making investment decisions.
      </p>
    </div>

    <!-- Toasts -->
    <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2 w-[280px]">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="bg-bg border border-divider border-l-[3px] shadow-md p-3 flex justify-between gap-2 items-start animate-slideInRight"
        :style="{ borderLeftColor: toast.type === 'error' ? 'var(--color-accent)' : 'var(--color-text)' }"
        role="alert"
      >
        <p class="!m-0 text-sm">{{ toast.message }}</p>
        <button class="bg-transparent border-0 cursor-pointer text-ink" @click="removeToast(toast.id)">&times;</button>
      </div>
    </div>

    <StockDetailModal :stock="selectedStock" @close="closeStockDetail" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRoute } from "vue-router";
import CompositeChart from "../components/CompositeChart.vue";
import StockDetailModal from "../components/StockDetailModal.vue";
import LogoChip from "../components/LogoChip.vue";
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

interface Toast {
  id: number;
  message: string;
  type: "success" | "error";
}

const route = useRoute();

const liveData = ref<MarketData[]>([]);
const gainers = ref<MarketData[]>([]);
const losers = ref<MarketData[]>([]);
const compositeData = ref<CompositeSummary | null>(null);
const compositeHistory = ref<CompositeHistoryPoint[]>([]);
const loading = ref(true);
const searchQuery = ref("");
const sortDir = ref<"asc" | "desc">("asc");
const toasts = ref<Toast[]>([]);
const page = ref(0);
const pageSize = 6;
const showWatchlistOnly = ref(route.query.watchlist === "1");
const selectedStock = ref<MarketData | null>(null);

const { isWatched, toggle: toggleWatchlist } = useWatchlist();
const { formatPrice } = useCurrency();

watch(
  () => route.query.watchlist,
  (v) => {
    if (v === "1") showWatchlistOnly.value = true;
  },
);

const isNextDayMode = computed(() => {
  const now = new Date();
  const currentTimeInMinutes = now.getHours() * 60 + now.getMinutes();
  return currentTimeInMinutes >= 0 && currentTimeInMinutes < 10 * 60;
});

const marketOpen = computed(() => {
  if (isNextDayMode.value) return false;
  const now = new Date();
  const currentTimeInMinutes = now.getHours() * 60 + now.getMinutes();
  return currentTimeInMinutes >= 10 * 60 && currentTimeInMinutes < 15 * 60;
});

const timeRemaining = computed(() => {
  if (!marketOpen.value) return "N/A";
  const now = new Date();
  const closeTime = new Date();
  closeTime.setUTCHours(15, 0, 0, 0);
  const diff = closeTime.getTime() - now.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
});

const timeToOpen = computed(() => {
  if (marketOpen.value) return "N/A";
  const now = new Date();
  const openTimeToday = new Date();
  openTimeToday.setUTCHours(10, 0, 0, 0);
  const openTimeTomorrow = new Date();
  openTimeTomorrow.setDate(openTimeTomorrow.getDate() + 1);
  openTimeTomorrow.setUTCHours(10, 0, 0, 0);
  const diff =
    now.getTime() < openTimeToday.getTime()
      ? openTimeToday.getTime() - now.getTime()
      : openTimeTomorrow.getTime() - now.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
});

const dateDisplay = computed(() => {
  const now = new Date();
  const dateObj = isNextDayMode.value ? new Date(now.getTime() - 86400000) : now;
  return dateObj.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
});

const compositeChangeLabel = computed(() => {
  if (!compositeData.value) return "--";
  const v = compositeData.value.composite_change_percent;
  return `${v > 0 ? "+" : ""}${v.toFixed(2)}%`;
});
const compositeColor = computed(() => {
  const v = compositeData.value?.composite_change_percent ?? 0;
  return v >= 0 ? "var(--color-positive)" : "var(--color-negative)";
});

const totalVolume = computed(() => liveData.value.reduce((sum, s) => sum + s.volume, 0));
const gainersCount = computed(() => liveData.value.filter((s) => s.change > 0).length);
const losersCount = computed(() => liveData.value.filter((s) => s.change < 0).length);

const byPercent = computed(() =>
  [...liveData.value].sort((a, b) => b.change / b.price - a.change / a.price),
);

interface SummaryCard {
  title: string;
  stock: MarketData | null;
  label: string;
  color: string;
  accent: string;
}

const changeSignLabel = (s: MarketData) =>
  `${s.change > 0 ? "+" : ""}${s.change.toFixed(2)} (${((s.change / s.price) * 100).toFixed(1)}%)`;

const summaryCards = computed<SummaryCard[]>(() => {
  const topGainer = gainers.value[0] ?? null;
  const topLoser = losers.value[0] ?? null;
  const bestPerformer = byPercent.value[0] ?? null;
  const worstPerformer = byPercent.value[byPercent.value.length - 1] ?? null;
  return [
    { title: "Top gainer", stock: topGainer, label: topGainer ? changeSignLabel(topGainer) : "--", color: "var(--color-positive)", accent: "var(--color-positive)" },
    { title: "Top loser", stock: topLoser, label: topLoser ? changeSignLabel(topLoser) : "--", color: "var(--color-negative)", accent: "var(--color-negative)" },
    { title: "Best performer", stock: bestPerformer, label: bestPerformer ? changeSignLabel(bestPerformer) : "--", color: bestPerformer && bestPerformer.change >= 0 ? "var(--color-positive)" : "var(--color-negative)", accent: "var(--color-accent)" },
    { title: "Worst performer", stock: worstPerformer, label: worstPerformer ? changeSignLabel(worstPerformer) : "--", color: worstPerformer && worstPerformer.change >= 0 ? "var(--color-positive)" : "var(--color-negative)", accent: "var(--color-accent-700)" },
  ];
});

const marketAnalysisText = computed(() => {
  const topGainer = gainers.value[0];
  const topLoser = losers.value[0];
  const trend = (compositeData.value?.composite_change_percent ?? 0) >= 0 ? "up" : "down";
  const change = Math.abs(compositeData.value?.composite_change_percent ?? 0).toFixed(2);
  return `As of ${dateDisplay.value}, ${liveData.value.length} listed companies traded a combined ${totalVolume.value.toLocaleString()} shares. ${topGainer ? topGainer.name : "The market"} led advancers while ${topLoser ? topLoser.name : "declines were broad"}${topLoser ? " led decliners" : ""}, leaving the composite ${trend} ${change}% on the session.`;
});

const sortedStocks = computed(() => {
  let stocks = [...liveData.value];
  if (showWatchlistOnly.value) {
    stocks = stocks.filter((s) => isWatched(s.symbol));
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    stocks = stocks.filter(
      (s) => s.name.toLowerCase().includes(q) || (s.symbol && s.symbol.toLowerCase().includes(q)),
    );
  }
  const dir = sortDir.value === "asc" ? 1 : -1;
  stocks.sort((a, b) => dir * a.name.localeCompare(b.name));
  return stocks;
});

const totalPages = computed(() => Math.max(1, Math.ceil(sortedStocks.value.length / pageSize)));

const paginatedStocks = computed(() => {
  const clampedPage = Math.min(page.value, totalPages.value - 1);
  const start = clampedPage * pageSize;
  return sortedStocks.value.slice(start, start + pageSize);
});

const pageSummary = computed(() => {
  const total = sortedStocks.value.length;
  if (total === 0) return "No companies";
  const clampedPage = Math.min(page.value, totalPages.value - 1);
  const start = clampedPage * pageSize + 1;
  const end = Math.min((clampedPage + 1) * pageSize, total);
  return `Showing ${start}–${end} of ${total}`;
});

watch([searchQuery, showWatchlistOnly], () => {
  page.value = 0;
});

const fetchLiveMarketData = async () => {
  loading.value = true;
  try {
    liveData.value = await fetchLiveData();
    gainers.value = liveData.value.filter((s) => s.change > 0).sort((a, b) => b.change - a.change).slice(0, 5);
    losers.value = liveData.value.filter((s) => s.change < 0).sort((a, b) => a.change - b.change).slice(0, 5);
  } catch (error) {
    console.error("Error fetching live market data:", error);
    addToast("Failed to load market data", "error");
  } finally {
    loading.value = false;
  }
};

const fetchCompositeData = async () => {
  try {
    compositeData.value = await fetchComposite();
    compositeHistory.value = await fetchCompositeHistory();
  } catch (error) {
    console.error("Error fetching composite data:", error);
  }
};

const openStockDetail = (stock: MarketData) => {
  selectedStock.value = stock;
};
const closeStockDetail = () => {
  selectedStock.value = null;
};

const addToast = (message: string, type: "success" | "error" = "success") => {
  const id = Date.now();
  toasts.value.push({ id, message, type });
  setTimeout(() => removeToast(id), 3000);
};
const removeToast = (id: number) => {
  toasts.value = toasts.value.filter((t) => t.id !== id);
};

let marketDataInterval: number | null = null;

onMounted(() => {
  fetchLiveMarketData();
  fetchCompositeData();
  marketDataInterval = window.setInterval(() => {
    fetchLiveMarketData();
    fetchCompositeData();
  }, 60000);
});

onUnmounted(() => {
  if (marketDataInterval) clearInterval(marketDataInterval);
});
</script>
