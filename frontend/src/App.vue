<template>
  <div class="flex flex-col min-h-screen bg-bg text-ink font-body">
    <nav class="flex items-center gap-4 px-4 sm:px-6 py-3 border-b-2 border-divider">
      <span class="font-heading font-extrabold text-lg mr-auto">
        GSE <span class="text-accent">&middot;</span> TRACKER
      </span>
      <RouterLink
        to="/"
        class="text-sm hover:text-accent"
        active-class="text-accent"
        exact-active-class="text-accent"
      >
        Dashboard
      </RouterLink>
      <RouterLink :to="{ path: '/', query: { watchlist: '1' } }" class="text-sm hover:text-accent">
        Watchlist
      </RouterLink>
      <div class="flex items-center gap-3 ml-2">
        <span
          class="inline-flex items-center text-[11px] tracking-wide px-2.5 py-0.5"
          :class="isMarketOpen ? 'bg-neutral-200 text-neutral-800' : 'bg-accent-100 text-accent-800'"
        >
          {{ isMarketOpen ? "OPEN" : "CLOSED" }}
        </span>
        <select
          v-model="selectedCurrency"
          aria-label="Currency"
          class="text-sm bg-surface border border-divider px-2 py-1 min-h-[32px]"
        >
          <option v-for="code in availableCurrencies" :key="code" :value="code">{{ code }}</option>
        </select>
      </div>
    </nav>

    <main class="flex-1">
      <router-view />
    </main>

    <footer class="border-t-2 border-divider py-3 text-center text-xs text-muted">
      <p>&copy; 2026 GSE Tracker | Powered by afx.kwayisi.org</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { useCurrency } from "./composables/useCurrency";

const { selectedCurrency, availableCurrencies } = useCurrency();

const isMarketOpen = ref(false);
let marketStatusInterval: number | null = null;

const updateMarketStatus = () => {
  const now = new Date();
  const currentTimeInMinutes = now.getUTCHours() * 60 + now.getUTCMinutes();
  isMarketOpen.value = currentTimeInMinutes >= 10 * 60 && currentTimeInMinutes < 15 * 60;
};

onMounted(() => {
  updateMarketStatus();
  marketStatusInterval = window.setInterval(updateMarketStatus, 60000);
});

onUnmounted(() => {
  if (marketStatusInterval) clearInterval(marketStatusInterval);
});
</script>
