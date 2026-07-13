import { describe, it, expect, vi } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import type { MarketData } from "../../services/api";

vi.mock("../../services/api", () => ({
  fetchSymbolHistory: vi.fn().mockResolvedValue([
    { date: "2026-07-10", price: 12.0, change: 0.1, volume: 1000 },
    { date: "2026-07-11", price: 12.45, change: 0.35, volume: 1200 },
  ]),
  fetchFxRates: vi.fn().mockResolvedValue({ base: "GHS", date: "2026-07-12", rates: {} }),
}));

import StockDetailModal from "../StockDetailModal.vue";

const stock: MarketData = {
  symbol: "VBK",
  name: "Volta Bank",
  company_name: "Volta Bank Plc",
  price: 12.45,
  change: 0.35,
  volume: 152000,
  sector: "Financials",
};

describe("StockDetailModal", () => {
  it("renders nothing when no stock is selected", () => {
    const wrapper = mount(StockDetailModal, {
      props: { stock: null },
      global: { stubs: { StockChart: true, teleport: true } },
    });
    expect(wrapper.find(".dialog-backdrop").exists()).toBe(false);
  });

  it("shows stock details and price history once a stock is selected", async () => {
    const wrapper = mount(StockDetailModal, {
      props: { stock },
      global: { stubs: { StockChart: true, teleport: true } },
    });
    await flushPromises();

    expect(wrapper.text()).toContain("Volta Bank");
    expect(wrapper.text()).toContain("Financials");
    expect(wrapper.text()).toContain("₵12.45");
  });

  it("emits close when the close button is clicked", async () => {
    const wrapper = mount(StockDetailModal, {
      props: { stock },
      global: { stubs: { StockChart: true, teleport: true } },
    });
    await flushPromises();

    await wrapper.find('button[aria-label="Close"]').trigger("click");
    expect(wrapper.emitted("close")).toBeTruthy();
  });
});
