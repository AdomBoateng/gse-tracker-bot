<template>
  <div>
    <svg
      v-if="values.length >= 2"
      :width="width"
      :height="height"
      :viewBox="`0 0 120 ${vbHeight}`"
      preserveAspectRatio="none"
      class="gse-icon"
    >
      <defs>
        <linearGradient :id="gradId" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" :stop-color="color" stop-opacity="0.28" />
          <stop offset="100%" :stop-color="color" stop-opacity="0" />
        </linearGradient>
      </defs>
      <line
        x1="0"
        :y1="zeroY"
        x2="120"
        :y2="zeroY"
        stroke="var(--color-divider)"
        stroke-width="1"
        stroke-dasharray="2 3"
      />
      <path :d="areaPath" :fill="`url(#${gradId})`" stroke="none" />
      <polyline :points="points" fill="none" :stroke="color" stroke-width="1.75" />
      <circle :cx="endX" :cy="endY" r="2.5" :fill="color" />
    </svg>
    <p v-else class="text-muted" style="font-size: 12px; margin: 0">
      Composite trend is building — the line fills in day by day.
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { CompositeHistoryPoint } from "../services/api";

const props = withDefaults(
  defineProps<{
    series: CompositeHistoryPoint[];
    color?: string;
    width?: string | number;
    height?: number;
  }>(),
  { color: "var(--color-text)", width: "100%", height: 52 },
);

const vbHeight = 52;
const gradId = `spark-${Math.random().toString(36).slice(2, 8)}`;

const values = computed(() =>
  props.series.map((p) => p.composite_change_percent),
);

const scaled = computed(() => {
  const vals = values.value;
  if (vals.length < 2) return { coords: [], zeroY: vbHeight / 2 };
  const min = Math.min(...vals, 0);
  const max = Math.max(...vals, 0);
  const range = max - min || 1;
  const pad = 6;
  const usable = vbHeight - pad * 2;
  const yFor = (v: number) => pad + (max - v) * (usable / range);
  const coords = vals.map((v, i) => ({
    x: (i / (vals.length - 1)) * 120,
    y: yFor(v),
  }));
  return { coords, zeroY: yFor(0) };
});

const points = computed(() =>
  scaled.value.coords.map((c) => `${c.x.toFixed(1)},${c.y.toFixed(1)}`).join(" "),
);
const areaPath = computed(() => {
  const c = scaled.value.coords;
  if (!c.length) return "";
  return (
    `M${c[0].x.toFixed(1)},${vbHeight} ` +
    c.map((p) => `L${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ") +
    ` L${c[c.length - 1].x.toFixed(1)},${vbHeight} Z`
  );
});
const zeroY = computed(() => scaled.value.zeroY.toFixed(1));
const endX = computed(() => {
  const c = scaled.value.coords;
  return c.length ? c[c.length - 1].x.toFixed(1) : "0";
});
const endY = computed(() => {
  const c = scaled.value.coords;
  return c.length ? c[c.length - 1].y.toFixed(1) : "0";
});
</script>
