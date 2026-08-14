export type RiskComponents = {
  cvss: number;
  vulnerabilities: number;
  assets: number;
  events: number;
};

export type DashboardSummary = {
  security_score: number;
  risk_level: "low" | "medium" | "high" | "critical";
  assets: number;
  vulnerabilities: number;
  critical_vulnerabilities: number;
  high_vulnerabilities: number;
  security_events: number;
  risk_components: RiskComponents;
};

export type Asset = {
  id: number;
  hostname: string;
  ip_address: string;
  operating_system?: string | null;
  environment: string;
  risk_score: number;
  created_at: string;
};

export type Vulnerability = {
  id: number;
  cve_id: string;
  title: string;
  description?: string | null;
  cvss_score?: number | null;
  severity: string;
  status: string;
  affected_asset?: string | null;
  published_at?: string | null;
};

const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const getSummary = () => request<DashboardSummary>("/api/v1/dashboard/summary");
export const getAssets = () => request<Asset[]>("/api/v1/assets");
export const getVulnerabilities = () => request<Vulnerability[]>("/api/v1/vulnerabilities");
