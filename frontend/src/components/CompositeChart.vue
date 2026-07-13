<template>
  <div>
    <div
      v-if="points.length < 2"
      class="flex flex-col items-center justify-center py-8 text-center text-white/80"
    >
      <span class="text-3xl mb-2">📊</span>
      <p class="font-medium">Composite trend is building</p>
      <p class="text-sm opacity-75 mt-1 max-w-xs">
        One trading day recorded so far - the trend line fills in day by day.
      </p>
    </div>
    <div v-else class="relative h-40">
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

const trendColor = computed(() => {
  if (props.points.length === 0) return "#93c5fd";
  const last = props.points[props.points.length - 1].composite_change_percent;
  return last >= 0 ? "#34d399" : "#fb7185";
});

const chartData = computed(() => ({
  labels: props.points.map((p) => p.date),
  datasets: [
    {
      data: props.points.map((p) => p.composite_change_percent),
      borderColor: trendColor.value,
      backgroundColor: `${trendColor.value}26`,
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
        label: (ctx: TooltipItem<"line">) => {
          const value = ctx.parsed.y ?? 0;
          return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
        },
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { color: "rgba(255,255,255,0.6)", maxTicksLimit: 6 },
    },
    y: {
      grid: { color: "rgba(255,255,255,0.15)" },
      ticks: {
        color: "rgba(255,255,255,0.6)",
        callback: (value: string | number) => `${value}%`,
      },
    },
  },
}));
</script>
