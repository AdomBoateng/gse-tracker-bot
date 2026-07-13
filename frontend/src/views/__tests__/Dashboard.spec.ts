import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import type { MarketData } from "../../services/api";

const { mockStocks } = vi.hoisted(() => ({
  mockStocks: [
    { symbol: "VBK", name: "Volta Bank", company_name: "Volta Bank Plc", price: 12.45, change: 0.35, volume: 152000, sector: "Financials" },
    { symbol: "GCM", name: "Gold Coast Mining", company_name: "Gold Coast Mining Plc", price: 45.10, change: -1.85, volume: 61000, sector: "Materials" },
    { symbol: "AKF", name: "Akwaaba Foods", company_name: "Akwaaba Foods Plc", price: 3.82, change: 0.21, volume: 98000, sector: "Consumer" },
  ] as MarketData[],
}));

vi.mock("../../services/api", () => ({
  fetchLiveData: vi.fn().mockResolvedValue(mockStocks),
  fetchComposite: vi.fn().mockResolvedValue({
    composite_change_percent: 1.2,
    total_market_cap: 1000,
    total_volume: 311000,
    stock_count: 3,
  }),
  fetchCompositeHistory: vi.fn().mockResolvedValue([]),
  fetchSymbolHistory: vi.fn().mockResolvedValue([]),
  fetchFxRates: vi.fn().mockResolvedValue({ base: "GHS", date: "2026-07-12", rates: { USD: 0.08 } }),
  fetchIpos: vi.fn().mockResolvedValue({ disclaimer: "", ipos: [] }),
  fetchMarketNews: vi.fn().mockResolvedValue({ disclaimer: "", articles: [] }),
  csvExportUrl: "/api/v1/gse/export/csv",
}));

import Dashboard from "../Dashboard.vue";

// Stub the fetch-on-mount / chart-only children so the smoke test stays focused
// on the dashboard's own layout, data wiring, and table interactions.
const mountDashboard = () =>
  mount(Dashboard, {
    global: {
      stubs: {
        Sparkline: true,
        IpoSection: true,
        NewsSection: true,
        StockChart: true,
      },
    },
  });

// Click the "Watchlist" filter button in the table toolbar (a <button>, distinct
// from the "Watchlist (n)" nav link and the per-row "Toggle watchlist" buttons).
const clickWatchlistToolbar = (wrapper: ReturnType<typeof mountDashboard>) => {
  const btn = wrapper.findAll("button").find((b) => b.text().trim() === "Watchlist");
  if (!btn) throw new Error("Watchlist toolbar button not found");
  return btn.trigger("click");
};

describe("Dashboard smoke test", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-07-13T11:00:00Z")); // inside 10:00-15:00 GMT market hours
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("renders the dashboard without throwing and shows fetched companies", async () => {
    const wrapper = mountDashboard();
    await flushPromises();

    expect(wrapper.text()).toContain("All companies");
    expect(wrapper.text()).toContain("Volta Bank");
    expect(wrapper.text()).toContain("Gold Coast Mining");
    expect(wrapper.text()).toContain("Listed companies");
  });

  it("shows the open-market hero copy during market hours", async () => {
    const wrapper = mountDashboard();
    await flushPromises();
    expect(wrapper.text()).toContain("Market is open");
    expect(wrapper.text()).not.toContain("Today's market summary");
  });

  it("shows the closed-market summary outside trading hours", async () => {
    vi.setSystemTime(new Date("2026-07-13T20:00:00Z"));
    const wrapper = mountDashboard();
    await flushPromises();
    expect(wrapper.text()).toContain("Market is closed");
    expect(wrapper.text()).toContain("Today's market summary");
  });

  it("filters the table via search", async () => {
    const wrapper = mountDashboard();
    await flushPromises();

    const search = wrapper.find('input[placeholder="Search name or symbol"]');
    await search.setValue("gold");
    await flushPromises();

    const tableText = wrapper.find("table").text();
    expect(tableText).toContain("Gold Coast Mining");
    expect(tableText).not.toContain("Volta Bank");
  });

  it("toggles a row into the watchlist and filters to it", async () => {
    const wrapper = mountDashboard();
    await flushPromises();

    await wrapper.find('button[aria-label="Toggle watchlist"]').trigger("click");
    await clickWatchlistToolbar(wrapper);
    await flushPromises();

    const rows = wrapper.findAll("tbody tr");
    expect(rows.length).toBe(1);
  });

  it("opens the stock detail modal on row click", async () => {
    const wrapper = mountDashboard();
    await flushPromises();

    await wrapper.find("tbody tr").trigger("click");
    await flushPromises();

    // StockDetailModal renders via <Teleport to="body">, outside the wrapper's own subtree
    expect(document.body.textContent).toContain("Price history");
  });
});
