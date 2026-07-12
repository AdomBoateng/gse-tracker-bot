import { computed, ref } from "vue";
import { fetchFxRates } from "../services/api";

export type CurrencyCode = "GHS" | "USD" | "GBP" | "EUR";

const CURRENCY_SYMBOLS: Record<string, string> = {
  GHS: "₵",
  USD: "$",
  GBP: "£",
  EUR: "€",
};

// Module-level so every component shares the same selection and cached rates
const selectedCurrency = ref<CurrencyCode>("GHS");
const rates = ref<Record<string, number>>({});

let fetchPromise: Promise<void> | null = null;

const loadRates = (): Promise<void> => {
  if (!fetchPromise) {
    fetchPromise = fetchFxRates("GHS")
      .then((data) => {
        rates.value = data.rates;
      })
      .catch(() => {
        // Leave rates empty - formatPrice() falls back to GHS-only when a rate is missing
      });
  }
  return fetchPromise;
};

export function useCurrency() {
  loadRates();

  const availableCurrencies = computed<CurrencyCode[]>(() => [
    "GHS",
    ...(Object.keys(rates.value) as CurrencyCode[]),
  ]);

  const convert = (priceInGHS: number): number => {
    if (selectedCurrency.value === "GHS") return priceInGHS;
    const rate = rates.value[selectedCurrency.value];
    return rate ? priceInGHS * rate : priceInGHS;
  };

  const formatPrice = (priceInGHS: number): string => {
    const symbol = CURRENCY_SYMBOLS[selectedCurrency.value] ?? "₵";
    return `${symbol}${convert(priceInGHS).toFixed(2)}`;
  };

  return { selectedCurrency, availableCurrencies, formatPrice };
}
