<template>
  <div>
    <div
      v-if="points.length < 2"
      class="flex flex-col items-center justify-center py-8 text-center"
    >
      <p class="font-semibold !m-0">Building price history</p>
      <p class="text-sm text-muted mt-1 max-w-xs">
        History starts accumulating from today, one trading day at a time &mdash; check
        back soon.
      </p>
      <p v-if="points.length === 1" class="text-sm text-muted mt-3">
        Latest recorded close:
        <span class="font-semibold text-ink">₵{{ points[0].price.toFixed(2) }}</span>
        on {{ points[0].date }}
      </p>
    </div>
    <div v-else class="relative h-48">
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
import type { HistoryPoint } from "../services/api";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler);

const props = defineProps<{ points: HistoryPoint[] }>();

// Single-series line: color follows the period's direction, matching the
// gainers(emerald)/losers(rose) convention used throughout the rest of the app.
const trendColor = computed(() => {
  if (props.points.length < 2) return "#157a45";
  const first = props.points[0].price;
  const last = props.points[props.points.length - 1].price;
  return last >= first ? "#157a45" : "#ae1800";
});

const chartData = computed(() => ({
  labels: props.points.map((p) => p.date),
  datasets: [
    {
      data: props.points.map((p) => p.price),
      borderColor: trendColor.value,
      backgroundColor: `${trendColor.value}1a`,
      borderWidth: 2,
      fill: true,
      tension: 0.25,
      pointRadius: (ctx: { dataIndex: number }) =>
        ctx.dataIndex === props.points.length - 1 ? 5 : 0,
      pointHoverRadius: 5,
      pointBackgroundColor: trendColor.value,
      pointBorderColor: "#ffffff",
      pointBorderWidth: 2,
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
        label: (ctx: TooltipItem<"line">) => `₵${(ctx.parsed.y ?? 0).toFixed(2)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: "#7d7979", maxTicksLimit: 6, font: { family: "Archivo, system-ui, sans-serif" } },
    },
    y: {
      grid: { color: "#d7d3d3" },
      ticks: { color: "#7d7979", font: { family: "Archivo, system-ui, sans-serif" } },
    },
  },
}));
</script>
