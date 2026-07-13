<template>
  <section>
    <div class="ipo-toolbar">
      <div>
        <div class="section-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent)" stroke-width="2">
            <path d="M3 3v18h18"></path>
            <path d="m19 9-5 5-4-4-3 3"></path>
          </svg>
          <h4>Company listings and performance</h4>
        </div>
        <p class="text-muted ipo-disclaimer">{{ disclaimer }}</p>
      </div>
      <input v-model="query" class="input" placeholder="Filter companies" @input="resetPages" />
    </div>

    <p v-if="loading" class="text-muted">Loading listings...</p>
    <p v-else-if="error" class="text-muted">Couldn't load IPO data. {{ error }}</p>
    <p v-else-if="filtered.length === 0" class="text-muted">No companies match this filter.</p>

    <template v-else>
      <div class="ipo-grid">
        <article v-for="ipo in ipoPageRows" :key="ipo.symbol" class="ipo-card">
          <div class="ipo-card-head">
            <StockLogo
              :symbol="ipo.symbol"
              :name="ipo.company_name"
              :logo-url="logoUrlFor(ipo)"
              :size="42"
            />
            <div class="ipo-name-block">
              <div class="ipo-name-line">
                <strong>{{ ipo.company_name }}</strong>
                <button
                  class="btn btn-icon btn-secondary ipo-info-btn"
                  type="button"
                  :aria-label="`Show ${ipo.symbol} info`"
                  @click="selectedIpo = ipo"
                >
                  i
                </button>
              </div>
              <span class="text-muted">{{ ipo.symbol }} | {{ ipo.sector }}</span>
            </div>
            <span class="tag ipo-status">{{ ipo.status }}</span>
          </div>

          <div class="ipo-metrics">
            <div>
              <span class="text-muted">Current price</span>
              <strong>{{ currentPriceLabel(ipo.symbol) }}</strong>
            </div>
            <div>
              <span class="text-muted">Period return</span>
              <strong :style="{ color: returnColor(ipo.symbol) }">{{ returnLabel(ipo.symbol) }}</strong>
            </div>
            <div>
              <span class="text-muted">Avg volume</span>
              <strong>{{ avgVolumeLabel(ipo.symbol) }}</strong>
            </div>
            <div>
              <span class="text-muted">Listing</span>
              <strong>{{ ipo.listing_year ?? "N/A" }}</strong>
            </div>
          </div>

          <div class="ipo-spark-wrap">
            <svg
              v-if="historyFor(ipo.symbol).length >= 2"
              viewBox="0 0 160 54"
              preserveAspectRatio="none"
              class="ipo-spark"
              aria-hidden="true"
            >
              <polyline
                :points="sparkPoints(ipo.symbol)"
                fill="none"
                :stroke="returnColor(ipo.symbol)"
                stroke-width="2"
              />
            </svg>
            <p v-else class="text-muted">{{ fallbackTrendText(ipo.symbol) }}</p>
          </div>

          <dl class="ipo-decision-list">
            <div>
              <dt>Volatility signal</dt>
              <dd>{{ volatilityLabel(ipo.symbol) }}</dd>
            </div>
            <div>
              <dt>Liquidity signal</dt>
              <dd>{{ liquidityLabel(ipo.symbol) }}</dd>
            </div>
            <div>
              <dt>Offer price</dt>
              <dd>{{ ipo.offer_price_ghs ? `GHS ${ipo.offer_price_ghs.toFixed(2)}` : "N/A" }}</dd>
            </div>
          </dl>
        </article>
      </div>

      <div class="pager">
        <span class="text-muted">{{ ipoPageSummary }}</span>
        <button class="btn btn-secondary" :disabled="ipoPage === 1" @click="ipoPage -= 1">Prev</button>
        <button class="btn btn-secondary" :disabled="ipoPage === ipoTotalPages" @click="ipoPage += 1">Next</button>
      </div>

      <div class="hr"></div>

      <div class="section-title" style="margin-bottom: var(--space-3)">
        <h4>Pros and cons</h4>
      </div>
      <div class="ipo-proscons-grid">
        <article v-for="ipo in prosPageRows" :key="`pros-${ipo.symbol}`" class="ipo-card">
          <div class="ipo-mini-head">
            <StockLogo :symbol="ipo.symbol" :name="ipo.company_name" :logo-url="logoUrlFor(ipo)" :size="32" />
            <strong>{{ ipo.symbol }}</strong>
            <span class="text-muted">{{ ipo.company_name }}</span>
          </div>
          <div class="ipo-proscons">
            <div>
              <h6 style="margin: 0 0 8px; color: var(--color-positive)">Pros</h6>
              <ul class="ipo-list ipo-pros">
                <li v-for="(p, i) in ipo.pros" :key="i">{{ p }}</li>
              </ul>
            </div>
            <div>
              <h6 style="margin: 0 0 8px; color: var(--color-negative)">Cons</h6>
              <ul class="ipo-list ipo-cons">
                <li v-for="(c, i) in ipo.cons" :key="i">{{ c }}</li>
              </ul>
            </div>
          </div>
        </article>
      </div>

      <div class="pager">
        <span class="text-muted">{{ prosPageSummary }}</span>
        <button class="btn btn-secondary" :disabled="prosPage === 1" @click="prosPage -= 1">Prev</button>
        <button class="btn btn-secondary" :disabled="prosPage === prosTotalPages" @click="prosPage += 1">Next</button>
      </div>
    </template>

    <div v-if="selectedIpo" class="dialog-backdrop" @click.self="selectedIpo = null">
      <div class="dialog ipo-dialog">
        <div class="ipo-card-head">
          <StockLogo
            :symbol="selectedIpo.symbol"
            :name="selectedIpo.company_name"
            :logo-url="logoUrlFor(selectedIpo)"
            :size="44"
          />
          <div>
            <div class="dialog-title">{{ selectedIpo.company_name }}</div>
            <p class="text-muted" style="margin: 2px 0 0">{{ selectedIpo.symbol }} | {{ selectedIpo.sector }}</p>
          </div>
        </div>
        <div class="ipo-modal-metrics">
          <div>
            <span class="text-muted">Latest price</span>
            <strong>{{ currentPriceLabel(selectedIpo.symbol) }}</strong>
          </div>
          <div>
            <span class="text-muted">Return signal</span>
            <strong :style="{ color: returnColor(selectedIpo.symbol) }">{{ returnLabel(selectedIpo.symbol) }}</strong>
          </div>
          <div>
            <span class="text-muted">Liquidity</span>
            <strong>{{ liquidityLabel(selectedIpo.symbol) }}</strong>
          </div>
          <div>
            <span class="text-muted">Volatility</span>
            <strong>{{ volatilityLabel(selectedIpo.symbol) }}</strong>
          </div>
        </div>
        <p class="dialog-body">{{ selectedIpo.summary }}</p>
        <dl class="ipo-decision-list">
          <div>
            <dt>Status</dt>
            <dd>{{ selectedIpo.status }}</dd>
          </div>
          <div>
            <dt>Listed</dt>
            <dd>{{ selectedIpo.listing_year ?? "N/A" }}</dd>
          </div>
          <div>
            <dt>Latest price</dt>
            <dd>{{ currentPriceLabel(selectedIpo.symbol) }}</dd>
          </div>
        </dl>
        <div class="dialog-actions">
          <button class="btn btn-primary" type="button" @click="selectedIpo = null">Close</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import StockLogo from "./StockLogo.vue";
import {
  fetchIpos,
  fetchLiveData,
  fetchSymbolHistory,
  type HistoryPoint,
  type IpoEntry,
  type MarketData,
} from "../services/api";

const IPO_LOGOS: Record<string, string> = {
  ACCESS: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/access.png",
  ASG: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/asg.png",
  BOPP: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/bopp.jpg",
  CAL: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/cal.png",
  EGL: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/egl.png",
  EGH: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/egh.png",
  FML: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/fml.png",
  GCB: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/gcb.png",
  GGBL: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/ggbl.png",
  GOIL: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/goil.png",
  KASA: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/kasa.png",
  MTNGH: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/mtn.png",
  SCB: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/scb.png",
  SIC: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/sic.png",
  TLW: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/tlw.png",
  TOTAL: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/total.png",
  UNIL: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/unil.png",
};

const ipos = ref<IpoEntry[]>([]);
const disclaimer = ref("");
const loading = ref(true);
const error = ref("");
const query = ref("");
const selectedIpo = ref<IpoEntry | null>(null);
const histories = ref<Record<string, HistoryPoint[]>>({});
const liveBySymbol = ref<Record<string, MarketData>>({});

const ipoPage = ref(1);
const prosPage = ref(1);
const pageSize = 6;
const prosPageSize = 4;

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase();
  if (!q) return ipos.value;
  return ipos.value.filter(
    (i) =>
      i.company_name.toLowerCase().includes(q) ||
      i.symbol.toLowerCase().includes(q) ||
      i.sector.toLowerCase().includes(q),
  );
});

const ipoTotalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize)));
const prosTotalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / prosPageSize)));
const ipoPageRows = computed(() =>
  filtered.value.slice((ipoPage.value - 1) * pageSize, ipoPage.value * pageSize),
);
const prosPageRows = computed(() =>
  filtered.value.slice((prosPage.value - 1) * prosPageSize, prosPage.value * prosPageSize),
);
const ipoPageSummary = computed(() => pageSummary(ipoPage.value, pageSize));
const prosPageSummary = computed(() => pageSummary(prosPage.value, prosPageSize));

const pageSummary = (page: number, size: number): string => {
  const total = filtered.value.length;
  if (!total) return "No companies";
  const start = (page - 1) * size + 1;
  const end = Math.min(page * size, total);
  return `Showing ${start}-${end} of ${total}`;
};

const resetPages = () => {
  ipoPage.value = 1;
  prosPage.value = 1;
};

const historyFor = (symbol: string): HistoryPoint[] => histories.value[symbol] ?? [];
const liveFor = (symbol: string): MarketData | undefined => liveBySymbol.value[symbol];

const logoUrlFor = (ipo: IpoEntry): string | null => ipo.logo_url ?? IPO_LOGOS[ipo.symbol] ?? null;

const currentPriceLabel = (symbol: string): string => {
  const live = liveFor(symbol);
  if (live) return `GHS ${live.price.toFixed(2)}`;
  const points = historyFor(symbol);
  if (!points.length) return "Building";
  return `GHS ${points[points.length - 1].price.toFixed(2)}`;
};

const returnValue = (symbol: string): number | null => {
  const points = historyFor(symbol);
  const live = liveFor(symbol);
  if (points.length < 2 || points[0].price === 0) {
    if (!live) return null;
    const previous = live.price - live.change;
    return previous ? (live.change / previous) * 100 : null;
  }
  const first = points[0].price;
  const last = points[points.length - 1].price;
  return ((last - first) / first) * 100;
};

const returnLabel = (symbol: string): string => {
  const value = returnValue(symbol);
  if (value === null) return "Building";
  return `${value >= 0 ? "+" : ""}${value.toFixed(1)}%`;
};

const returnColor = (symbol: string): string => {
  const value = returnValue(symbol);
  if (value === null) return "var(--color-text)";
  return value >= 0 ? "var(--color-positive)" : "var(--color-negative)";
};

const avgVolumeLabel = (symbol: string): string => {
  const points = historyFor(symbol);
  const live = liveFor(symbol);
  if (!points.length) return live ? live.volume.toLocaleString() : "Building";
  const avg = points.reduce((sum, p) => sum + p.volume, 0) / points.length;
  return Math.round(avg).toLocaleString();
};

const volatilityLabel = (symbol: string): string => {
  const points = historyFor(symbol);
  const live = liveFor(symbol);
  if (points.length < 3) {
    if (!live || !live.price) return "Needs more history";
    const liveScore = (Math.abs(live.change) / live.price) * 100;
    if (liveScore < 1) return "Low intraday movement";
    if (liveScore < 4) return "Moderate intraday movement";
    return "High intraday movement";
  }
  const changes = points.map((p) => Math.abs(p.change));
  const avg = changes.reduce((sum, change) => sum + change, 0) / changes.length;
  const latest = points[points.length - 1].price || 1;
  const score = (avg / latest) * 100;
  if (score < 1) return "Low recent price movement";
  if (score < 4) return "Moderate recent movement";
  return "High recent movement";
};

const liquidityLabel = (symbol: string): string => {
  const points = historyFor(symbol);
  const live = liveFor(symbol);
  if (!points.length && !live) return "Needs more history";
  const avg = points.length
    ? points.reduce((sum, p) => sum + p.volume, 0) / points.length
    : live?.volume ?? 0;
  if (avg >= 100000) return "High trading activity";
  if (avg >= 10000) return "Moderate trading activity";
  return "Thin trading activity";
};

const fallbackTrendText = (symbol: string): string => {
  const live = liveFor(symbol);
  if (!live) return "Price history will build as daily snapshots are captured.";
  return `Today's move: ${live.change >= 0 ? "+" : ""}${live.change.toFixed(2)} on ${live.volume.toLocaleString()} shares.`;
};

const sparkPoints = (symbol: string): string => {
  const points = historyFor(symbol);
  if (points.length < 2) return "";
  const prices = points.map((p) => p.price);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const range = max - min || 1;
  return prices
    .map((price, index) => {
      const x = (index / (prices.length - 1)) * 160;
      const y = 48 - ((price - min) / range) * 42;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
};

const loadHistoriesForPage = async () => {
  const symbols = ipoPageRows.value.map((ipo) => ipo.symbol);
  await Promise.all(
    symbols
      .filter((symbol) => !histories.value[symbol])
      .map(async (symbol) => {
        histories.value = {
          ...histories.value,
          [symbol]: await fetchSymbolHistory(symbol, 3650),
        };
      }),
  );
};

watch(ipoPageRows, loadHistoriesForPage);

onMounted(async () => {
  try {
    const [data, liveRows] = await Promise.all([fetchIpos(), fetchLiveData()]);
    liveBySymbol.value = Object.fromEntries(
      liveRows.filter((row) => row.symbol).map((row) => [row.symbol as string, row]),
    );
    ipos.value = data.ipos;
    disclaimer.value = data.disclaimer;
    await loadHistoriesForPage();
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
});
</script>
