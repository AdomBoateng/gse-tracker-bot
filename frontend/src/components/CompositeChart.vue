<template>
  <div>
    <div v-if="points.length < 2" class="flex flex-col items-center justify-center py-4 text-center text-muted">
      <p class="text-sm !m-0">Composite trend is building &mdash; check back after another trading day.</p>
    </div>
    <div v-else class="relative h-14">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { Line } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
  type TooltipItem,
} from "chart.js";
import type { CompositeHistoryPoint } from "../services/api";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler);

const props = defineProps<{ points: CompositeHistoryPoint[] }>();

const POSITIVE = "#157a45";
const NEGATIVE = "#ae1800";

const trendColor = computed(() => {
  if (props.points.length === 0) return POSITIVE;
  const last = props.points[props.points.length - 1].composite_change_percent;
  return last >= 0 ? POSITIVE : NEGATIVE;
});

const chartData = computed(() => ({
  labels: props.points.map((p) => p.date),
  datasets: [
    {
      data: props.points.map((p) => p.composite_change_percent),
      borderColor: trendColor.value,
      backgroundColor: `${trendColor.value}26`,
      borderWidth: 1.75,
      fill: true,
      tension: 0.15,
      pointRadius: (ctx: { dataIndex: number }) =>
        ctx.dataIndex === props.points.length - 1 ? 2.5 : 0,
      pointHoverRadius: 4,
      pointBackgroundColor: trendColor.value,
      pointBorderColor: trendColor.value,
      pointBorderWidth: 0,
    },
  ],
}));

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: "index" as const, intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#201e1d",
      titleFont: { family: "Archivo, system-ui, sans-serif" },
      bodyFont: { family: "Archivo, system-ui, sans-serif" },
      titleColor: "#f3f2f2",
      bodyColor: "#f3f2f2",
      displayColors: false,
      callbacks: {
        label: (ctx: TooltipItem<"line">) => {
          const value = ctx.parsed.y ?? 0;
          return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
        },
      },
    },
  },
  scales: {
    x: { display: false },
    y: { display: false },
  },
}));
</script>
