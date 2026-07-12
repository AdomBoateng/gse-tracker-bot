import type { Page } from "@playwright/test";

export const mockStocks = [
  { symbol: "VBK", name: "Volta Bank", company_name: "Volta Bank Plc", price: 12.45, change: 0.35, volume: 152000, sector: "Financials", logo_url: "" },
  { symbol: "AKF", name: "Akwaaba Foods", company_name: "Akwaaba Foods Plc", price: 3.82, change: 0.21, volume: 98000, sector: "Consumer", logo_url: "" },
  { symbol: "GCM", name: "Gold Coast Mining", company_name: "Gold Coast Mining Plc", price: 45.10, change: -1.85, volume: 61000, sector: "Materials", logo_url: "" },
  { symbol: "SVT", name: "Savannah Telecom", company_name: "Savannah Telecom Plc", price: 8.90, change: 0.12, volume: 210500, sector: "Telecom", logo_url: "" },
  { symbol: "KTX", name: "Kente Textiles", company_name: "Kente Textiles Plc", price: 2.15, change: -0.08, volume: 47000, sector: "Consumer", logo_url: "" },
  { symbol: "HMI", name: "Harmattan Insurance", company_name: "Harmattan Insurance Plc", price: 6.60, change: 0.44, volume: 33000, sector: "Financials", logo_url: "" },
  { symbol: "CDC", name: "Cedi Capital", company_name: "Cedi Capital Plc", price: 15.75, change: -0.63, volume: 72500, sector: "Financials", logo_url: "" },
  { symbol: "ABG", name: "Atlantic Breweries GH", company_name: "Atlantic Breweries GH Plc", price: 22.30, change: 0.95, volume: 88000, sector: "Consumer", logo_url: "" },
];

export const mockComposite = {
  composite_change_percent: 1.24,
  total_market_cap: 5_000_000,
  total_volume: mockStocks.reduce((s, x) => s + x.volume, 0),
  stock_count: mockStocks.length,
};

export const mockCompositeHistory = Array.from({ length: 10 }, (_, i) => ({
  date: `2026-07-0${i + 1}`,
  composite_change_percent: Math.sin(i) * 2,
}));

export const mockHistory = Array.from({ length: 10 }, (_, i) => ({
  date: `2026-07-0${i + 1}`,
  price: 12 + i * 0.1,
  change: 0.1,
  volume: 1000 + i * 10,
}));

export const mockFxRates = {
  base: "GHS",
  date: "2026-07-12",
  rates: { USD: 0.081, GBP: 0.064, EUR: 0.075 },
};

export async function mockApi(page: Page) {
  await page.route("**/api/v1/gse/live", (route) => route.fulfill({ json: mockStocks }));
  await page.route("**/api/v1/gse/composite", (route) => route.fulfill({ json: mockComposite }));
  await page.route("**/api/v1/gse/history/composite**", (route) => route.fulfill({ json: mockCompositeHistory }));
  await page.route(/\/api\/v1\/gse\/history\/[A-Z]+/, (route) => route.fulfill({ json: mockHistory }));
  await page.route("**/api/v1/fx/rates**", (route) => route.fulfill({ json: mockFxRates }));
  await page.route("**/api/v1/gse/export/csv", (route) =>
    route.fulfill({
      contentType: "text/csv",
      headers: { "content-disposition": "attachment; filename=gse_live.csv" },
      body: "Symbol,Company,Sector,Price (GHS),Change,% Change,Volume\nVBK,Volta Bank Plc,Financials,12.45,0.35,2.9,152000\n",
    }),
  );
}
