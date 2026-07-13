<template>
  <div>
    <div style="overflow-x: auto">
      <table class="table">
        <thead>
          <tr>
            <th>Company</th>
            <th>Sector</th>
            <th style="text-align: right">Volume</th>
            <th style="text-align: right">Price</th>
            <th style="text-align: right">Change</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="s in rows"
            :key="s.symbol || s.name"
            style="cursor: pointer"
            @click="$emit('open', s)"
          >
            <td>
              <div style="display: flex; align-items: center; gap: var(--space-3)">
                <StockLogo :symbol="s.symbol" :name="s.name" :logo-url="s.logo_url" :bg="s.logoBg" :fg="s.logoFg" :size="34" />
                <div>
                  <div style="font-weight: 600">{{ s.name }}</div>
                  <div class="text-muted" style="font-size: 11px">{{ s.company_name }}</div>
                </div>
              </div>
            </td>
            <td class="text-muted">{{ s.sector }}</td>
            <td class="tabnum" style="text-align: right">{{ s.volumeLabel }}</td>
            <td class="tabnum" style="text-align: right; font-weight: 600">{{ s.priceLabel }}</td>
            <td class="tabnum" style="text-align: right; font-weight: 600" :style="{ color: s.changeColor }">
              {{ s.changeSignLabel }}
            </td>
            <td style="text-align: right">
              <button
                class="btn-ghost"
                style="background: none; border: none; padding: 4px; cursor: pointer; color: var(--color-text)"
                aria-label="Toggle watchlist"
                @click.stop="$emit('toggle-watch', s.symbol)"
              >
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  :fill="isWatched(s.symbol) ? 'var(--color-accent)' : 'none'"
                  stroke="var(--color-text)"
                  stroke-width="2"
                >
                  <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 20.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
                </svg>
              </button>
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td colspan="6" class="text-muted" style="text-align: center; padding: var(--space-8)">
              No companies match this filter.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="display: flex; align-items: center; justify-content: space-between; padding-top: var(--space-3)">
      <p class="text-muted" style="font-size: 12px; margin: 0">{{ pageSummary }}</p>
      <div style="display: flex; gap: 6px">
        <button class="btn btn-secondary btn-icon" aria-label="Previous page" :disabled="page <= 1" @click="$emit('prev')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"></path></svg>
        </button>
        <button class="btn btn-secondary btn-icon" aria-label="Next page" :disabled="page >= totalPages" @click="$emit('next')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"></path></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StockLogo from "./StockLogo.vue";
import { useWatchlist } from "../composables/useWatchlist";
import type { DecoratedStock } from "../types";

defineProps<{
  rows: DecoratedStock[];
  pageSummary: string;
  page: number;
  totalPages: number;
}>();

defineEmits<{
  open: [stock: DecoratedStock];
  "toggle-watch": [symbol: string | null];
  prev: [];
  next: [];
}>();

const { isWatched } = useWatchlist();
</script>
