import axios from "axios";

const API_BASE = "/api/v1";

export interface MarketData {
  symbol: string | null;
  name: string;
  company_name: string;
  price: number;
  change: number;
  volume: number;
  logo_url?: string;
  sector?: string;
}

export interface CompositeSummary {
  composite_change_percent: number;
  total_market_cap: number;
  total_volume: number;
  stock_count: number;
}

export interface HistoryPoint {
  date: string;
  price: number;
  change: number;
  volume: number;
}

export interface CompositeHistoryPoint {
  date: string;
  composite_change_percent: number;
}

export interface FxRates {
  base: string;
  date: string;
  rates: Record<string, number>;
}

export const fetchLiveData = async (): Promise<MarketData[]> => {
  const response = await axios.get(`${API_BASE}/gse/live`);
  return response.data;
};

export const fetchComposite = async (): Promise<CompositeSummary> => {
  const response = await axios.get(`${API_BASE}/gse/composite`);
  return response.data;
};

export const fetchCompositeHistory = async (days = 30): Promise<CompositeHistoryPoint[]> => {
  const response = await axios.get(`${API_BASE}/gse/history/composite`, { params: { days } });
  return response.data;
};

export const fetchSymbolHistory = async (symbol: string, days = 30): Promise<HistoryPoint[]> => {
  const response = await axios.get(`${API_BASE}/gse/history/${symbol}`, { params: { days } });
  return response.data;
};

export const fetchFxRates = async (base = "GHS"): Promise<FxRates> => {
  const response = await axios.get(`${API_BASE}/fx/rates`, { params: { base } });
  return response.data;
};

export const csvExportUrl = `${API_BASE}/gse/export/csv`;
