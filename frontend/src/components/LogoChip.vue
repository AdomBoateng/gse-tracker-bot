<template>
  <img
    v-if="stock.logo_url"
    :src="stock.logo_url"
    alt=""
    class="shrink-0 object-contain bg-bg"
    :style="{ width: `${size}px`, height: `${size}px` }"
  />
  <div
    v-else
    class="shrink-0 flex items-center justify-center font-heading font-extrabold"
    :style="{ width: `${size}px`, height: `${size}px`, background: chip.bg, color: chip.fg, fontSize: `${Math.max(9, size * 0.3)}px` }"
  >
    {{ chip.initials }}
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { MarketData } from "../services/api";
import { getLogoChip } from "../utils/logoChip";

const props = defineProps<{ stock: MarketData; size?: number | string }>();
const size = computed(() => Number(props.size ?? 36));
const chip = computed(() => getLogoChip(props.stock.symbol, props.stock.name));
</script>
