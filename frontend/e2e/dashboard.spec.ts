import { test, expect } from "@playwright/test";
import { mockApi, mockStocks } from "./fixtures";

test.beforeEach(async ({ page }) => {
  // Mid-session, well inside 10:00-15:00 GMT market hours.
  await page.clock.setFixedTime(new Date("2026-07-13T12:00:00Z"));
  await mockApi(page);
});

test("loads the dashboard with live data and no console errors", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (err) => errors.push(String(err)));
  page.on("console", (msg) => { if (msg.type() === "error") errors.push(msg.text()); });

  await page.goto("/");
  await expect(page.getByText("GSE").first()).toBeVisible();
  await expect(page.getByText("Market is open")).toBeVisible();
  await expect(page.getByText("All companies")).toBeVisible();
  await expect(page.locator("tbody tr").first()).toBeVisible();

  expect(errors).toEqual([]);
});

test("shows stats row and top gainers/losers derived from live data", async ({ page }) => {
  await page.goto("/");
  const listedCard = page.locator("h6", { hasText: "Listed companies" }).locator("..");
  await expect(listedCard.locator("h3")).toHaveText(String(mockStocks.length));
  await expect(page.getByText("Top gainers")).toBeVisible();
  await expect(page.getByText("Top losers")).toBeVisible();
});

test("search filters the company table", async ({ page }) => {
  await page.goto("/");
  await page.getByPlaceholder("Search name or symbol").fill("gold");
  await expect(page.locator("tbody tr")).toHaveCount(1);
  await expect(page.locator("tbody")).toContainText("Gold Coast Mining");
});

test("shows the empty state when no company matches the filter", async ({ page }) => {
  await page.goto("/");
  await page.getByPlaceholder("Search name or symbol").fill("nonexistent-co");
  await expect(page.getByText("No companies match this filter.")).toBeVisible();
});

test("A-Z / Z-A sort toggles table order", async ({ page }) => {
  await page.goto("/");
  await page.getByText("Z → A").click();
  await expect(page.locator("tbody tr").first()).toContainText("Volta Bank");

  await page.getByText("A → Z").click();
  await expect(page.locator("tbody tr").first()).toContainText("Akwaaba Foods");
});

test("watchlist toggle adds a row and filters the table to it", async ({ page }) => {
  await page.goto("/");
  await page.locator("tbody tr", { hasText: "Gold Coast Mining" }).getByLabel("Add to watchlist").click();

  await page.getByRole("button", { name: "Watchlist", exact: true }).click();
  await expect(page.locator("tbody tr")).toHaveCount(1);
  await expect(page.locator("tbody")).toContainText("Gold Coast Mining");

  // un-toggling restores the full list
  await page.getByRole("button", { name: "Watchlist", exact: true }).click();
  await expect(page.locator("tbody tr")).toHaveCount(6); // page size
});

test("pagination advances and rolls back pages", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText(/Showing 1.6 of 8/)).toBeVisible();

  await page.getByLabel("Next page").click();
  await expect(page.getByText(/Showing 7.8 of 8/)).toBeVisible();

  await page.getByLabel("Previous page").click();
  await expect(page.getByText(/Showing 1.6 of 8/)).toBeVisible();
});

test("currency selector converts displayed prices", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("tbody tr").first()).toContainText("₵");

  await page.getByLabel("Currency").selectOption("USD");
  await expect(page.locator("tbody tr").first()).toContainText("$");
});

test("clicking a row opens the stock detail modal with price history", async ({ page }) => {
  await page.goto("/");
  await page.getByPlaceholder("Search name or symbol").fill("Volta Bank");
  await page.locator("tbody tr", { hasText: "Volta Bank" }).click();

  const dialog = page.locator(".fixed.inset-0");
  await expect(dialog.getByText("30-day price history")).toBeVisible();
  await expect(dialog.getByRole("button", { name: "☆ Watch" })).toBeVisible();

  await dialog.getByRole("button", { name: "Close", exact: true }).last().click();
  await expect(page.getByText("30-day price history")).not.toBeVisible();
});

test("CSV export link points at the backend export endpoint", async ({ page }) => {
  await page.goto("/");
  const href = await page.getByRole("link", { name: "Export CSV" }).getAttribute("href");
  expect(href).toBe("/api/v1/gse/export/csv");
});

test("watchlist nav link pre-filters the table via query param", async ({ page }) => {
  await page.goto("/");
  await page.locator("tbody tr", { hasText: "Kente Textiles" }).getByLabel("Add to watchlist").click();

  await page.getByRole("link", { name: "Watchlist" }).click();
  await expect(page).toHaveURL(/watchlist=1/);
  await expect(page.locator("tbody tr")).toHaveCount(1);
  await expect(page.locator("tbody")).toContainText("Kente Textiles");
});
