<template>
  <div
    style="display: grid; grid-template-columns: 1fr 1fr"
    :style="dense ? 'gap:var(--space-6)' : ''"
  >
    <!-- Gainers -->
    <div :style="dense ? '' : 'padding-right:var(--space-6);border-right:2px solid var(--color-divider)'">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: var(--space-3)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-positive)" stroke-width="2">
          <polyline points="22 7 13.5 15.5 8.5 10.5 2 17"></polyline>
          <polyline points="16 7 22 7 22 13"></polyline>
        </svg>
        <component :is="dense ? 'h5' : 'h4'" style="margin: 0">Top gainers</component>
      </div>
      <p v-if="!gainers.length" class="text-muted" style="font-size: 13px">No advancers right now.</p>
      <div
        v-for="s in gainers"
        :key="s.symbol || s.name"
        class="gse-row"
        :style="dense ? 'grid-template-columns:28px 1fr auto auto' : 'grid-template-columns:20px 36px 1fr auto auto'"
        style="cursor: pointer"
        @click="$emit('open', s)"
      >
        <span v-if="!dense" class="text-muted" style="font-size: 11px">{{ s.rank }}</span>
        <StockLogo :symbol="s.symbol" :name="s.name" :logo-url="s.logo_url" :bg="s.logoBg" :fg="s.logoFg" :size="dense ? 28 : 36" />
        <div>
          <div style="font-weight: 600">{{ s.name }}</div>
          <span v-if="!dense" class="text-muted" style="font-size: 11px">{{ s.sector }}</span>
        </div>
        <span class="tabnum" style="font-weight: 600">{{ s.priceLabel }}</span>
        <span class="tabnum" style="font-weight: 600; color: var(--color-positive)">▲ {{ s.changeAbsLabel }}</span>
      </div>
    </div>

    <!-- Losers -->
    <div :style="dense ? '' : 'padding-left:var(--space-6)'">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: var(--space-3)">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-negative)" stroke-width="2">
          <polyline points="22 17 13.5 8.5 8.5 13.5 2 7"></polyline>
          <polyline points="16 17 22 17 22 11"></polyline>
        </svg>
        <component :is="dense ? 'h5' : 'h4'" style="margin: 0">Top losers</component>
      </div>
      <p v-if="!losers.length" class="text-muted" style="font-size: 13px">No decliners right now.</p>
      <div
        v-for="s in losers"
        :key="s.symbol || s.name"
        class="gse-row"
        :style="dense ? 'grid-template-columns:28px 1fr auto auto' : 'grid-template-columns:20px 36px 1fr auto auto'"
        style="cursor: pointer"
        @click="$emit('open', s)"
      >
        <span v-if="!dense" class="text-muted" style="font-size: 11px">{{ s.rank }}</span>
        <StockLogo :symbol="s.symbol" :name="s.name" :logo-url="s.logo_url" :bg="s.logoBg" :fg="s.logoFg" :size="dense ? 28 : 36" />
        <div>
          <div style="font-weight: 600">{{ s.name }}</div>
          <span v-if="!dense" class="text-muted" style="font-size: 11px">{{ s.sector }}</span>
        </div>
        <span class="tabnum" style="font-weight: 600">{{ s.priceLabel }}</span>
        <span class="tabnum" style="font-weight: 600; color: var(--color-negative)">▼ {{ s.changeAbsLabel }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StockLogo from "./StockLogo.vue";
import type { DecoratedStock } from "../types";

withDefaults(
  defineProps<{
    gainers: DecoratedStock[];
    losers: DecoratedStock[];
    dense?: boolean;
  }>(),
  { dense: false },
);

defineEmits<{ open: [stock: DecoratedStock] }>();
</script>
