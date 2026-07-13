import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("../../services/api", () => ({
  fetchFxRates: vi.fn().mockResolvedValue({
    base: "GHS",
    date: "2026-07-12",
    rates: { USD: 0.08, GBP: 0.06, EUR: 0.07 },
  }),
}));

import { useCurrency } from "../useCurrency";

describe("useCurrency", () => {
  beforeEach(() => {
    const { selectedCurrency } = useCurrency();
    selectedCurrency.value = "GHS";
  });

  it("formats GHS prices with the cedi symbol by default", () => {
    const { formatPrice } = useCurrency();
    expect(formatPrice(12.4)).toBe("₵12.40");
  });

  it("converts to the selected currency once rates load", async () => {
    const { selectedCurrency, formatPrice } = useCurrency();
    // allow the module-level fetchFxRates() promise to resolve
    await new Promise((r) => setTimeout(r, 0));
    selectedCurrency.value = "USD";
    expect(formatPrice(100)).toBe("$8.00");
  });

  it("falls back to GHS price when a rate is missing", () => {
    const { selectedCurrency, formatPrice } = useCurrency();
    // @ts-expect-error deliberately invalid currency for the fallback path
    selectedCurrency.value = "XYZ";
    expect(formatPrice(10)).toBe("₵10.00");
  });
});
