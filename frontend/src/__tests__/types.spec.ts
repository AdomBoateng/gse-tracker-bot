import { describe, it, expect } from "vitest";
import { logoFor, decorate } from "../types";
import type { MarketData } from "../services/api";

const fmt = (p: number) => `₵${p.toFixed(2)}`;

describe("logoFor", () => {
  it("is deterministic for the same symbol", () => {
    expect(logoFor("VBK")).toEqual(logoFor("VBK"));
  });

  it("returns a bg/fg palette entry", () => {
    const chip = logoFor("GCM");
    expect(chip).toHaveProperty("bg");
    expect(chip).toHaveProperty("fg");
  });

  it("never throws for null/empty symbols", () => {
    expect(() => logoFor(null)).not.toThrow();
    expect(() => logoFor(undefined)).not.toThrow();
    expect(() => logoFor("")).not.toThrow();
  });
});

describe("decorate", () => {
  const base: MarketData = {
    symbol: "VBK",
    name: "Volta Bank",
    company_name: "Volta Bank Plc",
    price: 12.45,
    change: 0.35,
    volume: 152000,
    sector: "Financials",
  };

  it("marks a positive change as up with a signed label and positive color", () => {
    const d = decorate(base, fmt);
    expect(d.changeUp).toBe(true);
    expect(d.priceLabel).toBe("₵12.45");
    expect(d.changeSignLabel).toContain("+0.35");
    expect(d.changeColor).toBe("var(--color-positive)");
    expect(d.volumeLabel).toBe("152,000");
  });

  it("marks a negative change with the negative color", () => {
    const d = decorate({ ...base, change: -1.85 }, fmt);
    expect(d.changeUp).toBe(false);
    expect(d.changeColor).toBe("var(--color-negative)");
  });
});
