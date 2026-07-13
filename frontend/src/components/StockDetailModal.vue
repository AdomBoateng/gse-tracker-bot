<template>
  <Teleport to="body">
    <div v-if="stock" class="dialog-backdrop" @click.self="$emit('close')">
      <div class="dialog" style="width: min(520px, 100%)">
        <div style="display: flex; justify-content: space-between; align-items: flex-start">
          <div style="display: flex; align-items: center; gap: var(--space-3)">
            <StockLogo :symbol="stock.symbol" :name="stock.name" :logo-url="stock.logo_url" :size="40" />
            <div>
              <div class="dialog-title">{{ stock.name }}</div>
              <span class="text-muted" style="font-size: 12px">{{ stock.company_name }}</span>
            </div>
          </div>
          <button
            class="btn-ghost"
            style="background: none; border: none; font-size: 18px; cursor: pointer; color: var(--color-text)"
            aria-label="Close"
            @click="$emit('close')"
          >
            ✕
          </button>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: baseline">
          <h2 style="margin: 0">{{ formatPrice(stock.price) }}</h2>
          <span style="font-weight: 600" :style="{ color: changeColor }">
            {{ stock.change > 0 ? "+" : "" }}{{ stock.change.toFixed(2) }}
            ({{ Math.abs((stock.change / stock.price) * 100).toFixed(2) }}%)
          </span>
        </div>

        <div class="text-muted" style="display: flex; justify-content: space-between; font-size: 12px">
          <span>Price history</span>
          <span>{{ stock.sector }}</span>
        </div>
        <StockChart :points="history" />

        <div class="dialog-actions">
          <button class="btn btn-secondary" @click="toggle(stock.symbol)">
            {{ isWatched(stock.symbol) ? "★ Watching" : "☆ Watch" }}
          </button>
          <button class="btn btn-primary" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import StockChart from "./StockChart.vue";
import StockLogo from "./StockLogo.vue";
import { fetchSymbolHistory, type HistoryPoint, type MarketData } from "../services/api";
import { useWatchlist } from "../composables/useWatchlist";
import { useCurrency } from "../composables/useCurrency";

const props = defineProps<{ stock: MarketData | null }>();
defineEmits<{ close: [] }>();

const { isWatched, toggle } = useWatchlist();
const { formatPrice } = useCurrency();

const history = ref<HistoryPoint[]>([]);

const changeColor = computed(() =>
  props.stock && props.stock.change >= 0
    ? "var(--color-positive)"
    : "var(--color-negative)",
);

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
