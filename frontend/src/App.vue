<template>
  <div
    class="flex flex-col min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50"
  >
    <!-- Navigation -->
    <nav
      class="bg-white/90 backdrop-blur-2xl shadow-2xl sticky top-0 z-50 border-b border-gray-200/50 transition-all duration-300"
      :class="isMarketOpen ? 'border-emerald-200/50' : 'border-rose-200/50'"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-22">
          <div class="flex items-center gap-5">
            <div
              class="relative group cursor-pointer"
              style="padding: 10px; border-radius: 16px"
            >
              <div
                class="absolute inset-0 bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 rounded-2xl opacity-20 transition-all duration-300"
                :class="
                  isMarketOpen
                    ? 'shadow-[0_0_40px_rgba(16,185,129,0.4)]'
                    : 'opacity-0'
                "
              ></div>
              <div
                class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-600 via-indigo-600 to-violet-600 flex items-center justify-center text-white shadow-xl relative z-10 transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3"
                :class="
                  isMarketOpen ? 'shadow-emerald-500/40' : 'shadow-blue-500/30'
                "
              >
                <span class="text-2xl">📊</span>
                <div
                  class="absolute top-0 right-0 w-4 h-4 rounded-full border-2 border-white"
                  :class="
                    isMarketOpen ? 'bg-emerald-500 animate-ping' : 'bg-rose-500'
                  "
                ></div>
              </div>
            </div>
            <div class="leading-tight">
              <h1
                class="text-3xl font-black bg-gradient-to-r from-blue-700 via-indigo-700 to-violet-700 bg-clip-text text-transparent tracking-tight"
              >
                GSE Tracker
              </h1>
              <div class="flex items-center gap-2 mt-1">
                <div
                  class="w-3 h-3 rounded-full"
                  :class="
                    isMarketOpen
                      ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.6)]'
                      : 'bg-rose-500 shadow-[0_0_10px_rgba(244,63,94,0.6)]'
                  "
                ></div>
                <div class="flex flex-col">
                  <p
                    class="text-xs font-bold tracking-wide uppercase"
                    :class="isMarketOpen ? 'text-emerald-600' : 'text-rose-600'"
                  >
                    {{ isMarketOpen ? "Market Open" : "Market Closed" }}
                  </p>
                  <p class="text-xs text-gray-600 font-medium">
                    {{ timeDisplay }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <router-link
              to="/"
              class="group relative px-7 py-3 rounded-2xl text-blue-600 hover:bg-blue-50/50 transition-all duration-300 font-semibold text-sm"
              :class="
                isMarketOpen
                  ? 'ring-2 ring-emerald-500/20'
                  : 'ring-2 ring-rose-500/20'
              "
            >
              <span
                class="absolute inset-0 bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 rounded-2xl transform scale-0 group-hover:scale-100 transition-transform duration-300 origin-left shadow-lg shadow-blue-500/30"
                :class="isMarketOpen ? 'shadow-emerald-500/20' : ''"
              ></span>
              <span
                class="relative z-10 flex items-center gap-2 transition-colors group-hover:text-white"
                :class="
                  isMarketOpen
                    ? 'text-emerald-600 hover:text-white'
                    : 'text-rose-600 hover:text-white'
                "
                >Dashboard</span
              >
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-1">
      <router-view />
    </main>

    <!-- Footer -->
    <footer
      class="bg-white border-t border-gray-200 py-4 text-center text-gray-600 text-sm"
    >
      <p>© 2026 GSE Tracker | Powered by afx.kwayisi.org</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { RouterLink, RouterView } from "vue-router";

const isMarketOpen = ref(false);
const timeDisplay = ref("");
let marketStatusInterval: number | null = null;

const updateMarketStatus = () => {
  const now = new Date();
  const currentHour = now.getUTCHours();
  const currentMinute = now.getUTCMinutes();
  const currentTimeInMinutes = currentHour * 60 + currentMinute;
  const marketOpenTime = 10 * 60;
  const marketCloseTime = 15 * 60;

  if (
    currentTimeInMinutes >= marketOpenTime &&
    currentTimeInMinutes < marketCloseTime
  ) {
    isMarketOpen.value = true;
    const closeTime = new Date();
    closeTime.setUTCHours(15, 0, 0, 0);
    const diff = closeTime.getTime() - now.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    timeDisplay.value = `Closes in: ${hours}h ${minutes}m`;
  } else {
    isMarketOpen.value = false;
    const openTimeToday = new Date();
    openTimeToday.setUTCHours(10, 0, 0, 0);
    const openTimeTomorrow = new Date();
    openTimeTomorrow.setDate(openTimeTomorrow.getDate() + 1);
    openTimeTomorrow.setUTCHours(10, 0, 0, 0);
    const timeToOpen =
      now.getTime() < openTimeToday.getTime()
        ? openTimeToday.getTime() - now.getTime()
        : openTimeTomorrow.getTime() - now.getTime();
    const hours = Math.floor(timeToOpen / (1000 * 60 * 60));
    const minutes = Math.floor((timeToOpen % (1000 * 60 * 60)) / (1000 * 60));
    timeDisplay.value = `Opens in: ${hours}h ${minutes}m`;
  }
};

onMounted(() => {
  updateMarketStatus();
  marketStatusInterval = window.setInterval(() => {
    updateMarketStatus();
  }, 60000);
});

onUnmounted(() => {
  if (marketStatusInterval) {
    clearInterval(marketStatusInterval);
  }
});
</script>
