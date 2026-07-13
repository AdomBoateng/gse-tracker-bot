<template>
  <div>
    <div
      v-if="points.length < 2"
      class="flex flex-col items-center justify-center py-12 text-center"
    >
      <span class="text-4xl mb-3">📈</span>
      <p class="text-gray-600 font-medium">Building price history</p>
      <p class="text-sm text-gray-400 mt-1 max-w-xs">
        History starts accumulating from today, one trading day at a time — check
        back soon.
      </p>
      <p v-if="points.length === 1" class="text-sm text-gray-500 mt-3">
        Latest recorded close:
        <span class="font-semibold text-gray-700">₵{{ points[0].price.toFixed(2) }}</span>
        on {{ points[0].date }}
      </p>
    </div>
    <div v-else class="relative h-56">
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
  if (props.points.length < 2) return "#201e1d";
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
      backgroundColor: "rgba(11,11,11,0.85)",
      titleColor: "#ffffff",
      bodyColor: "#ffffff",
      displayColors: false,
      callbacks: {
        label: (ctx: TooltipItem<"line">) => `₵${(ctx.parsed.y ?? 0).toFixed(2)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: "#898781", maxTicksLimit: 6 },
    },
    y: {
      grid: { color: "#e1e0d9" },
      ticks: { color: "#898781" },
    },
  },
}));
</script>
