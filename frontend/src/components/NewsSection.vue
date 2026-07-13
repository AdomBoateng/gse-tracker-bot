<template>
  <section>
    <div class="ipo-toolbar">
      <div>
        <div class="section-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent)" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5z"></path>
          </svg>
          <h4>Market news</h4>
        </div>
        <p class="text-muted ipo-disclaimer">{{ disclaimer || fallbackDisclaimer }}</p>
      </div>
      <div class="news-actions">
        <input v-model="query" class="input" placeholder="Filter news" @input="page = 1" />
        <select v-model="sourceFilter" class="input" @change="page = 1">
          <option value="">All sources</option>
          <option value="official">Official</option>
          <option value="media">Media</option>
          <option value="search">Search links</option>
        </select>
        <select v-model="categoryFilter" class="input" @change="page = 1">
          <option value="">All categories</option>
          <option value="Company News">Company News</option>
          <option value="Official">Official</option>
          <option value="Dividends">Dividends</option>
          <option value="IPO">IPO</option>
          <option value="Financials">Financials</option>
        </select>
        <button class="btn btn-secondary" type="button" @click="loadNews">Refresh</button>
      </div>
    </div>

    <p v-if="loading" class="text-muted">Loading public news...</p>
    <p v-else-if="error" class="text-muted">Couldn't load news. {{ error }}</p>
    <p v-else-if="filtered.length === 0" class="text-muted">No news matches this filter.</p>

    <template v-else>
      <div class="news-list">
        <article v-for="article in pageRows" :key="article.url" class="news-item">
          <div>
            <h5>
              <a :href="article.url" target="_blank" rel="noopener noreferrer">{{ article.title }}</a>
            </h5>
            <div class="news-tags">
              <span v-if="article.symbol" class="tag">{{ article.symbol }}</span>
              <span class="tag">{{ article.category || "Company News" }}</span>
              <span class="tag">{{ sourceLabel(article.source_type) }}</span>
            </div>
            <p v-if="article.summary" class="text-muted news-summary">{{ article.summary }}</p>
            <p class="text-muted">{{ article.source }} | {{ article.published_at || "Recent" }} | {{ article.topic }}</p>
          </div>
        </article>
      </div>

      <div class="pager">
        <span class="text-muted">{{ pageSummary }}</span>
        <button class="btn btn-secondary" :disabled="page === 1" @click="page -= 1">Prev</button>
        <button class="btn btn-secondary" :disabled="page === totalPages" @click="page += 1">Next</button>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { fetchMarketNews, type NewsArticle } from "../services/api";

const articles = ref<NewsArticle[]>([]);
const disclaimer = ref("");
const loading = ref(true);
const error = ref("");
const query = ref("");
const sourceFilter = ref("");
const categoryFilter = ref("");
const page = ref(1);
const pageSize = 8;
let refreshTimer: number | null = null;

const fallbackDisclaimer =
  "Latest public news, IPO, dividend, and company updates. Verify market-sensitive items with official disclosures.";
const marketFallbackArticles: NewsArticle[] = [
  {
    title: "Ghana Stock Exchange market announcements",
    url: "https://gse.com.gh/market-announcements/",
    published_at: "",
    source: "Ghana Stock Exchange",
    source_type: "official",
    category: "Official",
    topic: "Official market announcements",
  },
  {
    title: "Ghana Stock Exchange listed company disclosures",
    url: "https://gse.com.gh/listed-companies/",
    published_at: "",
    source: "Ghana Stock Exchange",
    source_type: "official",
    category: "Official",
    topic: "Listed company information",
  },
  {
    title: "Ghana Stock Exchange news and updates",
    url: "https://gse.com.gh/news/",
    published_at: "",
    source: "Ghana Stock Exchange",
    source_type: "official",
    category: "Company News",
    topic: "Exchange news",
  },
];
const stockNewsTargets = [
  ["ACCESS", "Access Bank Ghana Plc"],
  ["ADB", "Agricultural Development Bank Plc"],
  ["AADS", "AngloGold Ashanti Depository Shares"],
  ["AGA", "AngloGold Ashanti Ltd"],
  ["ASG", "Asante Gold Corporation"],
  ["ALLGH", "Atlantic Lithium"],
  ["BOPP", "Benso Oil Palm Plantation Plc"],
  ["CAL", "CalBank Plc"],
  ["CMLT", "Camelot Ghana Ltd"],
  ["CLYD", "Clydestone Ghana Ltd"],
  ["CPC", "Cocoa Processing Company Ltd"],
  ["DIGICUT", "Digicut Production & Advertising Ltd"],
  ["DASPHARMA", "Dannex Ayrton Starwin PLC"],
  ["EGL", "Enterprise Group Plc"],
  ["EGH", "Ecobank Ghana Plc"],
  ["ETI", "Ecobank Transnational Inc"],
  ["FML", "Fan Milk Ltd"],
  ["FAB", "First Atlantic Bank"],
  ["GLD", "NewGold Issuer Ltd."],
  ["GCB", "GCB Bank Plc"],
  ["KASA", "Kasapreko Plc"],
  ["GGBL", "Guinness Ghana Breweries Plc"],
  ["GOIL", "GOIL PLC"],
  ["MTNGH", "Scancom Plc MTN Ghana"],
  ["RBGH", "Republic Bank Ghana Plc"],
  ["SCB", "Standard Chartered Bank Ghana Plc"],
  ["SCBPREF", "Standard Chartered Bank Preferential Shares"],
  ["SIC", "SIC Insurance Company Ltd"],
  ["SOGEGH", "Societe Generale Ghana Plc"],
  ["TOTAL", "TotalEnergies Marketing Ghana Plc"],
  ["HORDS", "Hords Ltd"],
  ["IIL", "Intravenous Infusions Ltd"],
  ["MAC", "Mega African Capital Limited"],
  ["MMH", "Meridian-Marshalls Holdings Ltd"],
  ["SAMBA", "Samba Foods Ltd"],
  ["TBL", "Trust Bank Ltd The Gambia"],
  ["TLW", "Tullow Oil Plc"],
  ["UNIL", "Unilever Ghana Ltd"],
  ["ZEN", "ZEN Petroleum"],
] as const;

const stockFallbackArticles: NewsArticle[] = stockNewsTargets.map(([symbol, companyName]) => {
  const query = encodeURIComponent(`"${companyName}" OR ${symbol} Ghana stock dividend IPO`);
  return {
    symbol,
    company_name: companyName,
    title: `Latest ${symbol} news and filings`,
    url: `https://news.google.com/search?q=${query}&hl=en-GH&gl=GH&ceid=GH:en`,
    published_at: "",
    source: "Google News",
    source_type: "search",
    category: "Company News",
    topic: `${companyName} company news`,
    summary: `Search link for public news, dividends, IPO updates, and company filings related to ${companyName}.`,
  };
});
const fallbackArticles = [...marketFallbackArticles, ...stockFallbackArticles];

const filtered = computed(() => {
  const q = query.value.trim().toLowerCase();
  return articles.value.filter((article) => {
    const matchesText = !q ||
      article.title.toLowerCase().includes(q) ||
      article.source.toLowerCase().includes(q) ||
      article.topic.toLowerCase().includes(q) ||
      (article.symbol ? article.symbol.toLowerCase().includes(q) : false) ||
      (article.company_name ? article.company_name.toLowerCase().includes(q) : false);
    const matchesSource = !sourceFilter.value || article.source_type === sourceFilter.value;
    const matchesCategory = !categoryFilter.value || article.category === categoryFilter.value;
    return matchesText && matchesSource && matchesCategory;
  });
});

const sourceLabel = (sourceType?: string): string => {
  if (sourceType === "official") return "Official";
  if (sourceType === "media") return "Media";
  if (sourceType === "search") return "Search";
  return "Source";
};

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize)));
const pageRows = computed(() => filtered.value.slice((page.value - 1) * pageSize, page.value * pageSize));
const pageSummary = computed(() => {
  const total = filtered.value.length;
  if (!total) return "No articles";
  const start = (page.value - 1) * pageSize + 1;
  const end = Math.min(page.value * pageSize, total);
  return `Showing ${start}-${end} of ${total}`;
});

const loadNews = async () => {
  try {
    error.value = "";
    const data = await fetchMarketNews();
    articles.value = data.articles;
    disclaimer.value = data.disclaimer;
    page.value = Math.min(page.value, totalPages.value);
  } catch (e) {
    articles.value = fallbackArticles;
    disclaimer.value = fallbackDisclaimer;
    error.value = "";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadNews();
  refreshTimer = window.setInterval(loadNews, 300000);
});

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer);
});
</script>
