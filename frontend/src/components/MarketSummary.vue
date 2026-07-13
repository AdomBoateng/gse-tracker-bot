<template>
  <div>
    <div class="gse-sum-kicker">
      <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--color-text); flex: none"></span>
      <h5 style="margin: 0">Today's market summary</h5>
      <span class="text-muted" style="font-size: 12px">{{ dateLabel }}</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-3)">
      <div
        v-for="card in cards"
        :key="card.label"
        class="gse-sum-card"
        :style="{ '--gse-accent': card.accent, padding: dense ? 'var(--space-3)' : 'var(--space-4)' }"
      >
        <h6 class="text-muted" style="margin: 0 0 10px">{{ card.label }}</h6>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px">
          <StockLogo
            v-if="!dense"
            :symbol="card.stock.symbol"
            :name="card.stock.name"
            :logo-url="card.stock.logo_url"
            :bg="card.stock.logoBg"
            :fg="card.stock.logoFg"
            :size="32"
          />
          <div style="min-width: 0">
            <div style="font-weight: 600; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
              {{ card.stock.name }}
            </div>
            <span class="text-muted" style="font-size: 11px">{{ card.stock.sector }}</span>
          </div>
        </div>
        <component :is="dense ? 'h4' : 'h3'" style="margin: 0" :style="{ color: card.color }">
          {{ card.stock.changeSignLabel }}
        </component>
      </div>
    </div>
    <p class="text-muted" style="margin-top: var(--space-4); line-height: 1.6" :style="dense ? 'font-size:12.5px' : ''">
      {{ analysis }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import StockLogo from "./StockLogo.vue";
import type { DecoratedStock } from "../types";

const props = withDefaults(
  defineProps<{
    topGainer: DecoratedStock | null;
    topLoser: DecoratedStock | null;
    bestPerformer: DecoratedStock | null;
    worstPerformer: DecoratedStock | null;
    dateLabel: string;
    analysis: string;
    dense?: boolean;
  }>(),
  { dense: false },
);

const placeholder: DecoratedStock = {
  symbol: "—",
  name: "—",
  company_name: "—",
  sector: "—",
  price: 0,
  change: 0,
  volume: 0,
  logoBg: "var(--color-neutral-200)",
  logoFg: "var(--color-neutral-800)",
  priceLabel: "—",
  changeAbsLabel: "—",
  changeSignLabel: "—",
  changeColor: "var(--color-text)",
  volumeLabel: "—",
  changeUp: true,
};

const cards = computed(() => [
  {
    label: "Top gainer",
    stock: props.topGainer ?? placeholder,
    accent: "var(--color-positive)",
    color: "var(--color-positive)",
  },
  {
    label: "Top loser",
    stock: props.topLoser ?? placeholder,
    accent: "var(--color-negative)",
    color: "var(--color-negative)",
  },
  {
    label: "Best performer",
    stock: props.bestPerformer ?? placeholder,
    accent: "var(--color-accent)",
    color: (props.bestPerformer ?? placeholder).changeColor,
  },
  {
    label: "Worst performer",
    stock: props.worstPerformer ?? placeholder,
    accent: "var(--color-accent-700)",
    color: (props.worstPerformer ?? placeholder).changeColor,
  },
]);
</script>
