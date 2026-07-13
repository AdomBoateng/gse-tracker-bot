import type { MarketData } from "./services/api";

/** A MarketData row decorated with presentation fields for the modernist UI. */
export interface DecoratedStock extends MarketData {
  rank?: number;
  logoBg: string;
  logoFg: string;
  priceLabel: string;
  changeAbsLabel: string; // absolute change, 2dp, no sign
  changeSignLabel: string; // e.g. "+0.35 (2.8%)"
  changeColor: string; // css variable
  volumeLabel: string;
  changeUp: boolean;
}

const STOCK_METADATA: Record<string, { company_name: string; sector: string; logo_url: string }> = {
  KASA: {
    company_name: "Kasapreko Plc",
    sector: "Consumer Goods",
    logo_url: "https://fdqilmfldmzqynpvyiql.supabase.co/storage/v1/object/public/GSE-logos/kasa.png",
  },
};

const LOGO_PALETTE = [
  { bg: "var(--color-accent-100)", fg: "var(--color-accent-800)" },
  { bg: "var(--color-neutral-200)", fg: "var(--color-neutral-800)" },
  { bg: "var(--color-accent-200)", fg: "var(--color-accent-800)" },
  { bg: "var(--color-neutral-300)", fg: "var(--color-neutral-900)" },
];

export function logoFor(symbol: string | null | undefined): { bg: string; fg: string } {
  const key = symbol && symbol.length ? symbol.charCodeAt(0) : 0;
  return LOGO_PALETTE[key % LOGO_PALETTE.length];
}

/** Decorate a raw MarketData row for display, using a currency formatter. */
export function decorate(
  stock: MarketData,
  formatPrice: (priceInGHS: number) => string,
): DecoratedStock {
  const metadata = stock.symbol ? STOCK_METADATA[stock.symbol] : undefined;
  const enriched = {
    ...stock,
    company_name: stock.company_name || metadata?.company_name || stock.name,
    sector: stock.sector || metadata?.sector || "Unclassified",
    logo_url: stock.logo_url || metadata?.logo_url,
  };
  const changeUp = enriched.change > 0;
  const percent =
    enriched.price !== 0 ? (enriched.change / enriched.price) * 100 : 0;
  const logo = logoFor(enriched.symbol);
  const changeColor =
    enriched.change > 0
      ? "var(--color-positive)"
      : enriched.change < 0
        ? "var(--color-negative)"
        : "var(--color-text)";
  return {
    ...enriched,
    logoBg: logo.bg,
    logoFg: logo.fg,
    priceLabel: formatPrice(enriched.price),
    changeAbsLabel: Math.abs(enriched.change).toFixed(2),
    changeSignLabel: `${enriched.change > 0 ? "+" : ""}${enriched.change.toFixed(2)} (${percent.toFixed(1)}%)`,
    changeColor,
    volumeLabel: enriched.volume.toLocaleString(),
    changeUp,
  };
}
