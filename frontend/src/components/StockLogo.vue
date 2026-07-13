<template>
  <div
    class="gse-logo"
    :style="{
      width: size + 'px',
      height: size + 'px',
      background: bg,
      color: fg,
      fontSize: fontSize + 'px',
    }"
  >
    <img v-if="logoUrl" :src="logoUrl" :alt="symbol || name" />
    <template v-else>{{ monogram }}</template>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { logoFor } from "../types";

const props = withDefaults(
  defineProps<{
    symbol?: string | null;
    name?: string;
    logoUrl?: string | null;
    size?: number;
    bg?: string;
    fg?: string;
  }>(),
  { size: 34 },
);

const palette = computed(() => logoFor(props.symbol));
const bg = computed(() => props.bg ?? palette.value.bg);
const fg = computed(() => props.fg ?? palette.value.fg);
const fontSize = computed(() => Math.max(8, Math.round(props.size * 0.3)));

const monogram = computed(() => {
  const base = props.symbol || props.name || "?";
  return base.slice(0, 4).toUpperCase();
});
</script>
