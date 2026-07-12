// Deterministic fallback "logo" for companies without a logo_url: a colored
// initials chip, palette rotation selected by the first character of the symbol.
const PALETTE = [
  { bg: "var(--color-accent-100)", fg: "var(--color-accent-800)" },
  { bg: "var(--color-neutral-200)", fg: "var(--color-neutral-800)" },
  { bg: "var(--color-accent-200)", fg: "var(--color-accent-800)" },
  { bg: "var(--color-neutral-300)", fg: "var(--color-neutral-900)" },
];

export interface LogoChip {
  bg: string;
  fg: string;
  initials: string;
}

export function getLogoChip(symbol: string | null | undefined, fallbackName = ""): LogoChip {
  const label = symbol || fallbackName || "?";
  const idx = label.charCodeAt(0) % PALETTE.length;
  return { ...PALETTE[idx], initials: label.slice(0, 3).toUpperCase() };
}
