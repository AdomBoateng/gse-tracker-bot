import { describe, it, expect } from "vitest";
import { getLogoChip } from "../logoChip";

describe("getLogoChip", () => {
  it("is deterministic for the same symbol", () => {
    expect(getLogoChip("VBK")).toEqual(getLogoChip("VBK"));
  });

  it("derives initials from the symbol, uppercased", () => {
    expect(getLogoChip("vbk").initials).toBe("VBK");
  });

  it("falls back to the company name when symbol is missing", () => {
    const chip = getLogoChip(null, "Gold Coast Mining");
    expect(chip.initials).toBe("GOL");
  });

  it("never throws for missing symbol and name", () => {
    expect(() => getLogoChip(null, "")).not.toThrow();
  });
});
