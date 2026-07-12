import { test, expect } from "@playwright/test";
import { mockApi } from "./fixtures";

test("shows the market summary section and CLOSED status outside trading hours", async ({ page }) => {
  // 20:00 GMT is outside the 10:00-15:00 GMT trading window.
  await page.clock.setFixedTime(new Date("2026-07-13T20:00:00Z"));
  await mockApi(page);

  await page.goto("/");

  await expect(page.getByText("CLOSED", { exact: true })).toBeVisible();
  await expect(page.getByText("Market is closed")).toBeVisible();
  await expect(page.getByText("Today's market summary")).toBeVisible();
  await expect(page.getByText("Top gainer", { exact: true })).toBeVisible();
  await expect(page.getByText("Top loser", { exact: true })).toBeVisible();
  await expect(page.getByText("Best performer", { exact: true })).toBeVisible();
  await expect(page.getByText("Worst performer", { exact: true })).toBeVisible();
});
