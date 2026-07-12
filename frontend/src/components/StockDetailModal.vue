<template>
  <Teleport to="body">
    <div
      v-if="stock"
      class="fixed inset-0 z-[60] grid place-items-center p-4"
      style="background: color-mix(in srgb, var(--color-neutral-900) 50%, transparent)"
      @click.self="$emit('close')"
    >
      <div class="w-full max-w-[440px] flex flex-col gap-3 p-4 bg-surface shadow-lg animate-fadeIn">
        <div class="flex justify-between items-start">
          <div class="flex items-center gap-3">
            <LogoChip :stock="stock" size="40" />
            <div>
              <div class="font-heading font-extrabold text-xl leading-tight">{{ stock.name }}</div>
              <span class="text-muted text-xs">{{ stock.sector }}</span>
            </div>
          </div>
          <button
            class="bg-transparent border-0 text-lg cursor-pointer text-accent"
            aria-label="Close"
            @click="$emit('close')"
          >
            &times;
          </button>
        </div>

        <div class="flex justify-between items-baseline">
          <h2 class="!m-0">{{ formatPrice(stock.price) }}</h2>
          <span
            class="font-semibold"
            :style="{ color: stock.change > 0 ? 'var(--color-positive)' : stock.change < 0 ? 'var(--color-negative)' : 'var(--color-text)' }"
          >
            {{ stock.change > 0 ? "+" : "" }}{{ stock.change.toFixed(2) }}
            ({{ Math.abs((stock.change / stock.price) * 100).toFixed(2) }}%)
          </span>
        </div>

        <StockChart :points="history" />
        <div class="text-muted text-xs">30-day price history &middot; {{ stock.sector }}</div>

        <div class="flex justify-end gap-2 mt-2">
          <button
            class="inline-flex items-center gap-1.5 border px-3 py-1.5 text-[13px] font-heading font-extrabold"
            :class="isWatched(stock.symbol) ? 'bg-accent-100 border-accent' : 'border-divider'"
            @click="toggle(stock.symbol)"
          >
            {{ isWatched(stock.symbol) ? "★ Watching" : "☆ Watch" }}
          </button>
          <button
            class="inline-flex items-center justify-center px-3 py-1.5 text-[13px] font-heading font-extrabold bg-accent text-bg"
            @click="$emit('close')"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import StockChart from "./StockChart.vue";
import LogoChip from "./LogoChip.vue";
import { fetchSymbolHistory, type HistoryPoint, type MarketData } from "../services/api";
import { useWatchlist } from "../composables/useWatchlist";
import { useCurrency } from "../composables/useCurrency";

const props = defineProps<{ stock: MarketData | null }>();
defineEmits<{ close: [] }>();

const { isWatched, toggle } = useWatchlist();
const { formatPrice } = useCurrency();

const history = ref<HistoryPoint[]>([]);

watch(
  () => props.stock?.symbol,
  async (symbol) => {
    history.value = [];
    if (!symbol) return;
    try {
      history.value = await fetchSymbolHistory(symbol);
    } catch {
      history.value = [];
    }
  },
  { immediate: true },
);
</script>
