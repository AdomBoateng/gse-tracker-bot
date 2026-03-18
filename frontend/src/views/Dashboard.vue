<template>
  <div class="container mx-auto px-4 py-8">
    <h1
      class="text-4xl md:text-5xl font-bold text-center mb-2 bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-600 bg-clip-text text-transparent"
    >
      GHANA STOCK EXCHANGE
    </h1>
    <p class="text-center text-gray-600 mb-8">
      Real-time market data, top performers, and comprehensive stock information
    </p>

    <div v-if="loading" class="space-y-6 animate-fadeIn">
      <div
        class="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl p-8 h-64 animate-pulse"
      >
        <div class="h-6 bg-gray-200 rounded w-1/3 mb-6"></div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="h-32 bg-gray-200 rounded-xl"></div>
          <div class="h-32 bg-gray-200 rounded-xl"></div>
        </div>
      </div>
      <div
        class="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl p-8 h-64 animate-pulse"
      ></div>
      <div
        class="max-w-6xl mx-auto bg-white rounded-2xl shadow-xl p-8 h-96 animate-pulse"
      ></div>
    </div>

    <div v-else>
      <!-- Market Status Section -->
      <div class="max-w-6xl mx-auto mb-8">
        <div
          class="bg-gradient-to-br rounded-2xl p-8 text-white shadow-2xl overflow-hidden relative"
          :class="
            marketOpen
              ? 'from-emerald-500 via-green-600 to-teal-600'
              : 'from-slate-800 via-gray-900 to-black'
          "
        >
          <div class="absolute top-0 right-0 p-8 opacity-10">
            <svg class="w-64 h-64" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 8.5l-2.5 1.25L12 11zm0 2.5l-5-2.5-5 2.5 10 5 10-5-5-2.5-5 2.5z"
              />
            </svg>
          </div>
          <div
            class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6"
          >
            <div>
              <div class="flex items-center gap-3 mb-2">
                <span class="text-3xl">{{ marketOpen ? "☀️" : "🌙" }}</span>
                <h2 class="text-3xl font-bold">
                  {{ marketOpen ? "MARKET IS OPEN" : "MARKET IS CLOSED" }}
                </h2>
              </div>
              <p class="text-lg opacity-90">
                {{
                  marketOpen
                    ? `Trading ends in ${timeRemaining}`
                    : `Opens in ${timeToOpen}`
                }}
              </p>
              <p class="text-sm opacity-75 mt-2">
                Market Hours: 10:00 AM - 3:00 PM GMT
                <br />
                <span class="text-xs opacity-60"
                  >Current Mode:
                  {{
                    isNextDayMode
                      ? "Previous Day Data (12:00 AM - 10:00 AM GMT)"
                      : "Today's Live Data (10:00 AM - 11:59 PM GMT)"
                  }}</span
                >
              </p>
            </div>
            <!-- <div class="flex gap-4">
              <div
                v-if="gseIndex"
                class="text-center px-6 py-4 bg-white/20 backdrop-blur-sm rounded-xl"
              >
                <p class="text-sm opacity-75">GSE Index</p>
                <p class="text-2xl font-bold">
                  {{ gseIndex.index.toFixed(2) }}
                </p>
                <p
                  class="text-sm"
                  :class="
                    gseIndex.change === 0
                      ? 'text-gray-300'
                      : gseIndex.change > 0
                        ? 'text-emerald-300'
                        : 'text-rose-300'
                  "
                >
                  {{
                    gseIndex.change === 0 ? "" : gseIndex.change > 0 ? "+" : ""
                  }}{{ gseIndex.change.toFixed(2) }} ({{
                    gseIndex.percentChange.toFixed(2)
                  }}%)
                </p>
              </div>
              <div
                class="text-center px-6 py-4 bg-white/20 backdrop-blur-sm rounded-xl min-w-[120px]"
              >
                <p class="text-sm opacity-75">Total Companies</p>
                <p class="text-2xl font-bold">{{ liveData.length }}</p>
              </div>
              <div
                class="text-center px-6 py-4 bg-white/20 backdrop-blur-sm rounded-xl min-w-[120px]"
              >
                <p class="text-sm opacity-75">Total Volume</p>
                <p class="text-2xl font-bold">
                  {{ totalVolume.toLocaleString() }}
                </p>
              </div>
            </div> -->
          </div>
        </div>
      </div>

      <!-- Today's Market Stats (Active Day Only) -->
      <div v-if="marketOpen" class="max-w-6xl mx-auto mb-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Total Stocks -->
          <div
            class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 shadow-xl text-white"
          >
            <div class="flex items-center gap-3 mb-2">
              <div
                class="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center"
              >
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M4 4h16v2H4V4zm0 6h16v2H4v-2zm0 6h16v2H4v-2z" />
                </svg>
              </div>
              <h3 class="text-lg font-bold">Total Stocks</h3>
            </div>
            <p class="text-4xl font-bold">{{ liveData.length }}</p>
            <p class="text-sm opacity-75 mt-1">Active listed companies</p>
          </div>
          <!-- Total Volume -->
          <div
            class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 shadow-xl text-white"
          >
            <div class="flex items-center gap-3 mb-2">
              <div
                class="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center"
              >
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M13 13h8V7h-8v6zm-2 6h2v-6h-2v6zm-6-6h2v-6H5v6zm6 0h2v-6h-2v6zm6 0h2v-6h-2v6zM1 17h2v-6H1v6zm6 0h2v-6H7v6z"
                  />
                </svg>
              </div>
              <h3 class="text-lg font-bold">Current Total Volume Traded</h3>
            </div>
            <p class="text-4xl font-bold">{{ totalVolume.toLocaleString() }}</p>
            <p class="text-sm opacity-75 mt-1">Shares</p>
          </div>
          <!-- GSE Index -->
          <div
            v-if="gseIndex"
            class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 shadow-xl text-white"
          >
            <div class="flex items-center gap-3 mb-2">
              <div
                class="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center"
              >
                <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"
                  />
                </svg>
              </div>
              <h3 class="text-lg font-bold">Current GSE Index</h3>
            </div>
            <p class="text-4xl font-bold">{{ gseIndex.index.toFixed(2) }}</p>
            <p
              class="text-sm mt-1"
              :class="
                gseIndex.change === 0
                  ? 'opacity-75'
                  : gseIndex.change > 0
                    ? 'text-emerald-300'
                    : 'text-rose-300'
              "
            >
              {{ gseIndex.change === 0 ? "" : gseIndex.change > 0 ? "+" : ""
              }}{{ gseIndex.change.toFixed(2) }} ({{
                gseIndex.percentChange.toFixed(2)
              }}%)
            </p>
          </div>
        </div>
      </div>

      <!-- Today's Top Gainers Section -->
      <div class="max-w-6xl mx-auto mb-8">
        <div
          class="bg-white/90 backdrop-blur-lg rounded-2xl shadow-xl overflow-hidden border border-white/20"
        >
          <div
            class="bg-gradient-to-r from-emerald-500 via-green-500 to-emerald-600 px-6 py-4"
          >
            <h2 class="text-2xl font-bold text-white flex items-center gap-3">
              <span>📈</span>
              {{ isNextDayMode ? "Previous Day's" : "Today's" }} Top Gainers
              <span class="text-sm font-normal opacity-75 ml-2"
                >({{ dateDisplay }})</span
              >
            </h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div
                v-for="stock in gainers"
                :key="stock.name"
                class="group relative bg-gradient-to-br from-white via-emerald-50/30 to-white rounded-xl p-5 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border border-emerald-100 hover:border-emerald-400 cursor-pointer"
              >
                <div class="absolute top-4 right-4">
                  <img
                    v-if="stock.logo_url"
                    :src="stock.logo_url"
                    alt="Logo"
                    class="w-16 h-16 rounded-xl object-contain shadow-inner bg-white p-1"
                  />
                  <div
                    v-else
                    class="w-16 h-16 rounded-xl bg-gradient-to-br from-emerald-100 to-emerald-200 flex items-center justify-center text-3xl font-bold text-emerald-700 shadow-inner"
                  >
                    {{ stock.name.charAt(0) }}
                  </div>
                </div>
                <div class="mt-14 space-y-3">
                  <div class="flex items-center justify-between">
                    <h3
                      class="font-bold text-xl text-gray-800 group-hover:text-emerald-600 transition-colors"
                    >
                      {{ stock.name }}
                    </h3>
                    <span
                      class="px-3 py-1 bg-gradient-to-r from-emerald-100 to-emerald-200 text-emerald-700 text-xs rounded-full font-bold shadow-sm"
                      >{{ stock.symbol }}</span
                    >
                  </div>
                  <p
                    class="text-3xl font-bold bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-transparent"
                  >
                    ₵{{ stock.price.toFixed(2) }}
                  </p>
                  <div class="flex items-center gap-3">
                    <span
                      class="font-bold text-lg"
                      :class="
                        stock.change === 0
                          ? 'text-gray-500'
                          : stock.change > 0
                            ? 'text-emerald-600'
                            : 'text-rose-600'
                      "
                      >{{
                        stock.change > 0 ? "⬆️" : stock.change < 0 ? "⬇️" : "➖"
                      }}
                      {{ stock.change.toFixed(2) }}</span
                    >
                    <span
                      class="opacity-75 text-sm"
                      :class="
                        stock.change === 0
                          ? 'text-gray-500'
                          : stock.change > 0
                            ? 'text-emerald-600'
                            : 'text-rose-600'
                      "
                      >({{
                        ((stock.change / stock.price) * 100).toFixed(2)
                      }}%)</span
                    >
                  </div>
                  <div class="pt-4 border-t-2 border-emerald-100">
                    <p
                      class="text-xs text-gray-500 uppercase tracking-wider mb-2 font-semibold"
                    >
                      Volume Traded
                    </p>
                    <p class="font-bold text-gray-700 text-lg">
                      {{ stock.volume.toLocaleString() }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Today's Top Losers Section -->
      <div class="max-w-6xl mx-auto mb-8">
        <div
          class="bg-white/90 backdrop-blur-lg rounded-2xl shadow-xl overflow-hidden border border-white/20"
        >
          <div
            class="bg-gradient-to-r from-rose-500 via-red-500 to-rose-600 px-6 py-4"
          >
            <h2 class="text-2xl font-bold text-white flex items-center gap-3">
              <span>📉</span>
              {{ isNextDayMode ? "Previous Day's" : "Today's" }} Top Losers
              <span class="text-sm font-normal opacity-75 ml-2"
                >({{ dateDisplay }})</span
              >
            </h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div
                v-for="stock in losers"
                :key="stock.name"
                class="group relative bg-gradient-to-br from-white via-rose-50/30 to-white rounded-xl p-5 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border border-rose-100 hover:border-rose-400 cursor-pointer"
              >
                <div class="absolute top-4 right-4">
                  <img
                    v-if="stock.logo_url"
                    :src="stock.logo_url"
                    alt="Logo"
                    class="w-16 h-16 rounded-xl object-contain shadow-inner bg-white p-1"
                  />
                  <div
                    v-else
                    class="w-16 h-16 rounded-xl bg-gradient-to-br from-rose-100 to-rose-200 flex items-center justify-center text-3xl font-bold text-rose-700 shadow-inner"
                  >
                    {{ stock.name.charAt(0) }}
                  </div>
                </div>
                <div class="mt-14 space-y-3">
                  <div class="flex items-center justify-between">
                    <h3
                      class="font-bold text-xl text-gray-800 group-hover:text-rose-600 transition-colors"
                    >
                      {{ stock.name }}
                    </h3>
                    <span
                      class="px-3 py-1 bg-gradient-to-r from-rose-100 to-rose-200 text-rose-700 text-xs rounded-full font-bold shadow-sm"
                      >{{ stock.symbol }}</span
                    >
                  </div>
                  <p
                    class="text-3xl font-bold bg-gradient-to-r from-rose-600 to-red-600 bg-clip-text text-transparent"
                  >
                    ₵{{ stock.price.toFixed(2) }}
                  </p>
                  <div class="flex items-center gap-3">
                    <span
                      class="font-bold text-lg"
                      :class="
                        stock.change === 0
                          ? 'text-gray-500'
                          : stock.change > 0
                            ? 'text-rose-600'
                            : 'text-rose-600'
                      "
                      >{{
                        stock.change > 0 ? "⬆️" : stock.change < 0 ? "⬇️" : "➖"
                      }}
                      {{ stock.change.toFixed(2) }}</span
                    >
                    <span
                      class="opacity-75 text-sm"
                      :class="
                        stock.change === 0
                          ? 'text-gray-500'
                          : stock.change > 0
                            ? 'text-rose-600'
                            : 'text-rose-600'
                      "
                      >({{
                        ((Math.abs(stock.change) / stock.price) * 100).toFixed(
                          2,
                        )
                      }}%)</span
                    >
                  </div>
                  <div class="pt-4 border-t-2 border-rose-100">
                    <p
                      class="text-xs text-gray-500 uppercase tracking-wider mb-2 font-semibold"
                    >
                      Volume Traded
                    </p>
                    <p class="font-bold text-gray-700 text-lg">
                      {{ stock.volume.toLocaleString() }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- All Companies Section -->
      <div class="max-w-6xl mx-auto mb-8">
        <div
          class="bg-white/90 backdrop-blur-lg rounded-2xl shadow-xl overflow-hidden border border-white/20"
        >
          <div
            class="bg-gradient-to-r from-blue-600 via-indigo-600 to-violet-700 px-6 py-5"
          >
            <div class="flex items-center justify-between flex-wrap gap-4">
              <h2 class="text-2xl font-bold text-white flex items-center gap-3">
                <span>📋</span> All Companies
              </h2>
              <div class="flex gap-2 items-center">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search stocks..."
                  class="px-4 py-2 rounded-lg border border-white/30 bg-white/20 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/40"
                />
                <button
                  @click="sortBy = sortBy === 'name' ? '-name' : 'name'"
                  class="px-3 py-2 rounded-lg bg-white/20 hover:bg-white/30 transition-colors text-white"
                >
                  Sort: {{ sortBy.startsWith("-") ? "↓" : "↑" }}
                </button>
              </div>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gradient-to-r from-gray-50 to-gray-100">
                <tr>
                  <th
                    class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider"
                  >
                    Company
                  </th>
                  <th
                    class="px-6 py-4 text-center text-xs font-bold text-gray-600 uppercase tracking-wider"
                  >
                    Logo
                  </th>
                  <th
                    class="px-6 py-4 text-right text-xs font-bold text-gray-600 uppercase tracking-wider"
                  >
                    Volume
                  </th>
                  <th
                    class="px-6 py-4 text-right text-xs font-bold text-gray-600 uppercase tracking-wider"
                  >
                    Price
                  </th>
                  <th
                    class="px-6 py-4 text-right text-xs font-bold text-gray-600 uppercase tracking-wider"
                  >
                    Change
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr
                  v-for="stock in paginatedStocks"
                  :key="stock.symbol ?? stock.name"
                  class="hover:bg-blue-50/30 transition-colors duration-200"
                >
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center gap-4">
                      <div
                        class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-100 to-violet-100 flex items-center justify-center text-2xl font-bold text-blue-600 shadow-sm"
                      >
                        {{ stock.name.charAt(0) }}
                      </div>
                      <div>
                        <p class="font-semibold text-gray-900">
                          {{ stock.name }}
                        </p>
                        <p class="text-xs text-gray-500">
                          {{ stock.company_name }}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-center">
                    <img
                      v-if="stock.logo_url"
                      :src="stock.logo_url"
                      alt="Logo"
                      class="w-12 h-12 mx-auto rounded-lg object-contain shadow-sm bg-white p-1"
                    />
                    <div
                      v-else
                      class="w-12 h-12 mx-auto rounded-lg bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center text-sm font-bold text-gray-600 shadow-sm"
                    >
                      {{ stock.symbol ? stock.symbol.charAt(0) : "?" }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right">
                    <p class="font-medium text-gray-600">
                      {{ stock.volume.toLocaleString() }}
                    </p>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right">
                    <p class="font-bold text-gray-900">
                      ₵{{ stock.price.toFixed(2) }}
                    </p>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right">
                    <span
                      class="font-bold px-4 py-1.5 rounded-lg"
                      :class="getChangeColorClass(stock.change)"
                    >
                      {{ stock.change > 0 ? "+" : ""
                      }}{{ stock.change.toFixed(2) }} ({{
                        Math.abs((stock.change / stock.price) * 100).toFixed(2)
                      }}%)
                    </span>
                  </td>
                </tr>
                <tr v-if="paginatedStocks.length === 0">
                  <td colspan="5" class="px-6 py-12 text-center text-gray-500">
                    No stocks found matching your search
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div
            class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-t border-gray-200 flex flex-col md:flex-row items-center justify-between gap-4"
          >
            <p class="text-sm text-gray-600">
              Showing
              {{
                paginatedStocks.length > 0
                  ? (currentPage - 1) * itemsPerPage + 1
                  : 0
              }}
              -
              {{ Math.min(currentPage * itemsPerPage, sortedStocks.length) }} of
              {{ sortedStocks.length }} companies
            </p>
            <div class="flex gap-2">
              <button
                @click="currentPage = Math.max(1, currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-3 py-1 rounded-lg bg-white border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 font-medium transition-colors"
              >
                Previous
              </button>
              <span class="px-3 py-1 text-gray-700 font-medium"
                >Page {{ currentPage }} of {{ totalPages }}</span
              >
              <button
                @click="currentPage = Math.min(totalPages, currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 rounded-lg bg-white border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 font-medium transition-colors"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Market Summary Section -->
      <div v-if="!marketOpen" class="max-w-6xl mx-auto mb-8">
        <div
          class="bg-gradient-to-br rounded-2xl p-8 text-white shadow-2xl overflow-hidden relative"
          :class="'from-slate-800 via-gray-900 to-black'"
        >
          <div class="absolute top-0 right-0 p-8 opacity-10">
            <svg class="w-64 h-64" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 2L2 7l10 5 10-5-10-5zm0 9l2.5-1.25L12 8.5l-2.5 1.25L12 11zm0 2.5l-5-2.5-5 2.5 10 5 10-5-5-2.5-5 2.5z"
              />
            </svg>
          </div>
          <div class="relative z-10">
            <h2 class="text-3xl font-bold mb-6 flex items-center gap-3">
              <span>📊</span> Market Summary - {{ dateDisplay }}
            </h2>

            <!-- Summary Statistics Table -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div
                v-if="gainers.length > 0"
                class="bg-emerald-500/20 backdrop-blur-sm rounded-xl p-4 border border-emerald-500/30"
              >
                <h4 class="font-semibold text-emerald-300 mb-3">Top Gainers</h4>
                <div class="space-y-2">
                  <div
                    v-for="stock in gainers.slice(0, 5)"
                    :key="stock.name"
                    class="flex justify-between items-center py-2 border-b border-emerald-600/30 last:border-0"
                  >
                    <div class="flex items-center gap-2">
                      <span
                        class="w-5 h-5 rounded-full bg-emerald-600/50 text-emerald-100 flex items-center justify-center text-xs font-bold"
                        >{{ gainers.indexOf(stock) + 1 }}</span
                      >
                      <span class="font-medium text-emerald-100 text-sm">{{
                        stock.name
                      }}</span>
                    </div>
                    <div class="text-right">
                      <span class="block text-emerald-50 text-sm"
                        >₵{{ stock.price.toFixed(2) }}</span
                      >
                      <span class="block text-xs text-emerald-300 font-medium"
                        >{{ stock.change > 0 ? "+" : ""
                        }}{{ stock.change.toFixed(2) }} ({{
                          ((stock.change / stock.price) * 100).toFixed(2)
                        }}%)</span
                      >
                    </div>
                  </div>
                </div>
              </div>
              <div
                v-if="losers.length > 0"
                class="bg-rose-500/20 backdrop-blur-sm rounded-xl p-4 border border-rose-500/30"
              >
                <h4 class="font-semibold text-rose-300 mb-3">Top Losers</h4>
                <div class="space-y-2">
                  <div
                    v-for="stock in losers.slice(0, 5)"
                    :key="stock.name"
                    class="flex justify-between items-center py-2 border-b border-rose-600/30 last:border-0"
                  >
                    <div class="flex items-center gap-2">
                      <span
                        class="w-5 h-5 rounded-full bg-rose-600/50 text-rose-100 flex items-center justify-center text-xs font-bold"
                        >{{ losers.indexOf(stock) + 1 }}</span
                      >
                      <span class="font-medium text-rose-100 text-sm">{{
                        stock.name
                      }}</span>
                    </div>
                    <div class="text-right">
                      <span class="block text-rose-50 text-sm"
                        >₵{{ stock.price.toFixed(2) }}</span
                      >
                      <span class="block text-xs text-rose-300 font-medium"
                        >{{ stock.change.toFixed(2) }} ({{
                          (
                            (Math.abs(stock.change) / stock.price) *
                            100
                          ).toFixed(2)
                        }}%)</span
                      >
                    </div>
                  </div>
                </div>
              </div>
              <div
                class="bg-blue-500/20 backdrop-blur-sm rounded-xl p-4 border border-blue-500/30"
              >
                <h4 class="font-semibold text-blue-300 mb-3">Market Stats</h4>
                <div class="space-y-2">
                  <div
                    class="flex justify-between items-center py-2 border-b border-blue-600/30 last:border-0"
                  >
                    <span class="font-medium text-blue-100 text-sm"
                      >Total Listed Companies</span
                    >
                    <span class="font-semibold text-blue-50">{{
                      liveData.length
                    }}</span>
                  </div>
                  <div
                    class="flex justify-between items-center py-2 border-b border-blue-600/30 last:border-0"
                  >
                    <span class="font-medium text-blue-100 text-sm"
                      >{{ marketOpen ? 'Current' : 'Previous' }} Total Volume Traded</span
                    >
                    <span class="font-semibold text-blue-50">{{
                      totalVolume.toLocaleString()
                    }}</span>
                  </div>
                  <div
                    v-if="gseIndex"
                    class="flex justify-between items-center py-2 border-b border-blue-600/30 last:border-0"
                  >
                    <span class="font-medium text-blue-100 text-sm"
                      >{{ marketOpen ? 'Current' : 'Previous' }} GSE Index</span
                    >
                    <span class="font-semibold text-blue-50"
                      >{{ gseIndex.index.toFixed(2) }} ({{
                        gseIndex.change === 0
                          ? ""
                          : gseIndex.change > 0
                            ? "+"
                            : ""
                      }}{{ gseIndex.change.toFixed(2) }} ({{
                        gseIndex.percentChange.toFixed(2)
                      }}%))</span
                    >
                  </div>
                </div>
              </div>
            </div>

            <!-- Market Summary Explanation -->
            <div
              class="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/10 shadow-lg"
            >
              <h3
                class="text-lg font-bold text-white mb-3 flex items-center gap-2"
              >
                <span>🔍</span> Market Analysis
              </h3>
              <div
                class="space-y-4 text-gray-300 leading-relaxed"
                v-html="marketAnalysisText"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Disclaimer -->
      <div
        class="max-w-6xl mx-auto mt-8 p-6 bg-gradient-to-r from-yellow-50 to-amber-50 border-2 border-yellow-200 rounded-2xl shadow-sm"
      >
        <p class="text-sm text-yellow-900 leading-relaxed">
          <strong>Disclaimer:</strong> This data is provided for informational
          purposes only. Real-time market data may have slight delays. Always
          verify with official Ghana Stock Exchange sources before making
          investment decisions.
        </p>
      </div>

      <!-- Toast Notifications -->
      <div class="fixed bottom-6 right-6 z-50 space-y-2">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="flex items-center p-4 rounded-xl shadow-lg border-l-4 animate-slideInRight bg-white backdrop-blur-sm"
          :class="
            toast.type === 'error' ? 'border-red-500' : 'border-emerald-500'
          "
          role="alert"
        >
          <span class="mr-3 text-xl">{{
            toast.type === "error" ? "⚠️" : "✅"
          }}</span>
          <div>
            <h4 class="font-semibold text-gray-800">
              {{ toast.type === "error" ? "Error" : "Success" }}
            </h4>
            <p class="text-sm text-gray-600">{{ toast.message }}</p>
          </div>
          <button
            @click="removeToast(toast.id)"
            class="ml-4 text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import axios from "axios";

interface MarketData {
  symbol: string | null;
  name: string;
  company_name: string;
  price: number;
  change: number;
  volume: number;
  logo_url?: string;
  sector?: string;
}

interface StockIndex {
  index: number;
  change: number;
  percentChange: number;
}

interface Toast {
  id: number;
  message: string;
  type: "success" | "error";
}

const liveData = ref<MarketData[]>([]);
const gainers = ref<MarketData[]>([]);
const losers = ref<MarketData[]>([]);
const gseIndex = ref<StockIndex | null>(null);
const loading = ref(true);
const searchQuery = ref("");
const sortBy = ref("name");
const toasts = ref<Toast[]>([]);
const stockLogos = ref<Record<string, string>>({});
const currentPage = ref(1);
const itemsPerPage = 10;

const API_BASE = "/api/v1";

const isNextDayMode = computed(() => {
  const now = new Date();
  console.log('Current Hour:', now.getHours(), 'Current Minute:', now.getMinutes());
  const currentHour = now.getHours();
  const currentMinute = now.getMinutes();
  const currentTimeInMinutes = currentHour * 60 + currentMinute;
  const marketOpenTime = 10 * 60;
  const midnightMinutes = 0;
  const inNextDayMode = (
    currentTimeInMinutes >= midnightMinutes &&
    currentTimeInMinutes < marketOpenTime
  );
  console.log('isNextDayMode:', inNextDayMode, 'currentTimeInMinutes:', currentTimeInMinutes, 'marketOpenTime:', marketOpenTime);
  return inNextDayMode;
});

const marketOpen = computed(() => {
  const now = new Date();
  console.log('Market Check - Hour:', now.getHours(), 'Minute:', now.getMinutes());
  const currentHour = now.getHours();
  const currentMinute = now.getMinutes();
  const currentTimeInMinutes = currentHour * 60 + currentMinute;
  const marketOpenTime = 10 * 60;
  const marketCloseTime = 15 * 60;
  if (isNextDayMode.value) {
    console.log('Market Closed - Next Day Mode');
    return false;
  }
  const isOpen = (
    currentTimeInMinutes >= marketOpenTime &&
    currentTimeInMinutes < marketCloseTime
  );
  console.log('Market Open:', isOpen, 'currentTimeInMinutes:', currentTimeInMinutes, 'openTime:', marketOpenTime, 'closeTime:', marketCloseTime);
  return isOpen;
});

const timeRemaining = computed(() => {
  if (!marketOpen.value) return "N/A";
  const now = new Date();
  const closeTime = new Date();
  closeTime.setUTCHours(15, 0, 0, 0);
  const diff = closeTime.getTime() - now.getTime();
  const hours = Math.floor(diff / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  return `${hours}h ${minutes}m`;
});

const timeToOpen = computed(() => {
  if (marketOpen.value) return "N/A";
  const now = new Date();
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
  return `${hours}h ${minutes}m`;
});

const getCurrentDateDisplay = (isPreviousDay: boolean = false) => {
  const now = new Date();
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const dateObj = isPreviousDay ? new Date(now.getTime() - 86400000) : now;
  const day = dateObj.getDate();
  const month = monthNames[dateObj.getMonth()];
  const year = dateObj.getFullYear();
  return `${month} ${day}, ${year}`;
};

const dateDisplay = computed(() => {
  const display = getCurrentDateDisplay(isNextDayMode.value);
  console.log('dateDisplay:', display, 'isNextDayMode:', isNextDayMode.value);
  return display;
});

const totalVolume = computed(() =>
  liveData.value.reduce((sum, stock) => sum + stock.volume, 0),
);

const sortedStocks = computed(() => {
  let stocks = [...liveData.value];
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    stocks = stocks.filter(
      (stock) =>
        stock.name.toLowerCase().includes(query) ||
        (stock.symbol && stock.symbol.toLowerCase().includes(query)),
    );
  }
  const direction = sortBy.value.startsWith("-") ? -1 : 1;
  const field = sortBy.value.replace("-", "") as keyof MarketData;
  stocks.sort((a, b) => {
    const valueA = a[field];
    const valueB = b[field];
    if (typeof valueA === "string" && typeof valueB === "string")
      return direction * valueA.localeCompare(valueB);
    return direction * (Number(valueA) - Number(valueB));
  });
  return stocks;
});

const marketAnalysisText = computed(() => {
  const gainersList = gainers.value
    .map((s) => {
      const change = s.change;
      const percent = ((change / s.price) * 100).toFixed(2);
      const colorClass =
        change > 0
          ? "text-emerald-300 font-bold"
          : change < 0
            ? "text-rose-300 font-bold"
            : "text-gray-300 font-bold";
      const changeStr =
        change > 0 ? `+${change.toFixed(2)}` : `${change.toFixed(2)}`;
      return `<span class="${colorClass}">${s.name} (${changeStr} (${percent}%))</span>`;
    })
    .join(", ");

  const losersList = losers.value
    .map((s) => {
      const change = s.change;
      const percent = ((change / s.price) * 100).toFixed(2);
      const colorClass =
        change > 0
          ? "text-emerald-300 font-bold"
          : change < 0
            ? "text-rose-300 font-bold"
            : "text-gray-300 font-bold";
      const changeStr =
        change > 0 ? `+${change.toFixed(2)}` : `${change.toFixed(2)}`;
      return `<span class="${colorClass}">${s.name} (${changeStr} (${percent}%))</span>`;
    })
    .join(", ");

  const trend = gseIndex.value
    ? gseIndex.value.change > 0
      ? "positive"
      : gseIndex.value.change < 0
        ? "negative"
        : "flat"
    : "flat";

  return `
    <p>As of ${dateDisplay.value}, the market recorded notable movements across several listed equities.</p>
    <p>The Top Gainers were led by ${gainersList}, with strong upward price movements reflecting increased buying interest and positive market sentiment.</p>
    <p>On the other hand, the Top Losers included ${losersList}, indicating selling pressure or reduced investor confidence in these stocks during the trading session.</p>
    <p>Overall, the market activity saw a total of ${liveData.value.length} stocks traded, with a cumulative volume of ${totalVolume.value.toLocaleString()} shares exchanged. The broader market direction, as reflected by the index, shows a ${trend} trend.</p>
  `;
});

const totalPages = computed(() =>
  Math.ceil(sortedStocks.value.length / itemsPerPage),
);

const paginatedStocks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return sortedStocks.value.slice(start, start + itemsPerPage);
});

const getChangeColorClass = (change: number): string => {
  if (change === 0 || change === 0.0) {
    return "bg-gray-100 text-gray-600";
  } else if (change > 0) {
    return "bg-gradient-to-r from-emerald-100 to-emerald-200 text-emerald-700 shadow-sm";
  } else {
    return "bg-gradient-to-r from-rose-100 to-rose-200 text-rose-700 shadow-sm";
  }
};

const loadStockLogos = async () => {
  try {
    const response = await fetch("/stocks.txt");
    if (response.ok) {
      const data: { stocks: Array<{ symbol: string; logo_url: string }> } =
        await response.json();
      data.stocks.forEach((stock) => {
        stockLogos.value[stock.symbol] = stock.logo_url;
      });
    }
  } catch (error) {
    console.error("Error loading stock logos:", error);
  }
};

const fetchLiveMarketData = async () => {
  loading.value = true;
  console.log('Fetching live market data...');
  try {
    const response = await axios.get(`${API_BASE}/gse/live`);
    console.log('API Response:', response.data);
    const liveDataList = response.data as Array<
      { symbol: string; logo_url?: string } & MarketData
    >;
    liveData.value = liveDataList.map((stock) => ({
      ...stock,
      logo_url: stockLogos.value[stock.symbol] || stock.logo_url,
    }));
    console.log('Live Data:', liveData.value);
    gainers.value = liveData.value
      .filter((s) => s.change > 0)
      .sort((a, b) => b.change - a.change)
      .slice(0, 8);
    console.log('Total stocks:', liveData.value.length);
    console.log('Stocks with positive change:', gainers.value.length);
    gainers.value.forEach((s, i) => console.log(`Gainer ${i+1}:`, s.name, 'change:', s.change));
    losers.value = liveData.value
      .filter((s) => s.change < 0)
      .sort((a, b) => a.change - b.change)
      .slice(0, 8);
    console.log('Stocks with negative change:', losers.value.length);
    losers.value.forEach((s, i) => console.log(`Loser ${i+1}:`, s.name, 'change:', s.change));
    if (liveData.value.length > 0) {
      const totalValue = liveData.value.reduce(
        (sum, stock) => sum + stock.price,
        0,
      );
      const prevTotalValue =
        totalValue -
        liveData.value.reduce((sum, stock) => sum + stock.change, 0);
      const indexChange = liveData.value.reduce(
        (sum, stock) => sum + stock.change,
        0,
      );
      gseIndex.value = {
        index: (totalValue / liveData.value.length) * 1000,
        change: indexChange,
        percentChange: (indexChange / prevTotalValue) * 100,
      };
      console.log('GSE Index:', gseIndex.value);
    }
  } catch (error) {
    console.error("Error fetching live market data:", error);
    addToast("Failed to load market data", "error");
  } finally {
    loading.value = false;
  }
};

const addToast = (message: string, type: "success" | "error" = "success") => {
  const id = Date.now();
  toasts.value.push({ id, message, type });
  setTimeout(() => removeToast(id), 3000);
};

const removeToast = (id: number) => {
  toasts.value = toasts.value.filter((t) => t.id !== id);
};

onMounted(() => {
  loadStockLogos();
  fetchLiveMarketData();

  // Real-time updates for market status and stock data
  // Update stock data every 60 seconds
  const marketDataInterval = window.setInterval(() => {
    fetchLiveMarketData();
  }, 60000);

  onUnmounted(() => {
    if (marketDataInterval) clearInterval(marketDataInterval);
  });
});

const calculateTimeToNextSwitch = () => {
  const now = new Date();
  const currentHour = now.getUTCHours();

  if (currentHour < 10) {
    const nextSwitch = new Date();
    nextSwitch.setUTCHours(10, 0, 0, 0);
    return nextSwitch.getTime() - now.getTime();
  } else {
    const nextSwitch = new Date();
    nextSwitch.setUTCHours(0, 0, 0, 0);
    nextSwitch.setDate(nextSwitch.getDate() + 1);
    return nextSwitch.getTime() - now.getTime();
  }
};

const setupDateRefresh = () => {
  const timeToSwitch = calculateTimeToNextSwitch();
  setTimeout(() => {
    fetchLiveMarketData();
    setupDateRefresh();
  }, timeToSwitch);
};

const currentInterval = ref<number | null>(null);

onUnmounted(() => {
  if (currentInterval.value) clearInterval(currentInterval.value);
});
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
.animate-slideInRight {
  animation: slideInRight 0.3s ease-out forwards;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
