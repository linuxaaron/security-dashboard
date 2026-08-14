"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Asset, DashboardSummary, Vulnerability, getAssets, getSummary, getVulnerabilities } from "../lib/api";

const riskLabel: Record<DashboardSummary["risk_level"], string> = {
  low: "Low risk",
  medium: "Medium risk",
  high: "High risk",
  critical: "Critical risk",
};

function ScoreRing({ score }: { score: number }) {
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="score-ring" aria-label={`Security score ${score} out of 100`}>
      <svg viewBox="0 0 128 128" role="img">
        <circle className="ring-track" cx="64" cy="64" r={radius} />
        <circle
          className="ring-value"
          cx="64"
          cy="64"
          r={radius}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="score-value">
        <strong>{score.toFixed(1)}</strong>
        <span>/ 100</span>
      </div>
    </div>
  );
}

function RiskBars({ summary }: { summary: DashboardSummary }) {
  const items = [
    ["CVSS exposure", summary.risk_components.cvss],
    ["Vulnerability posture", summary.risk_components.vulnerabilities],
    ["Asset posture", summary.risk_components.assets],
    ["Event posture", summary.risk_components.events],
  ] as const;

  return (
    <div className="risk-bars">
      {items.map(([label, value]) => (
        <div className="bar-row" key={label}>
          <div className="bar-meta"><span>{label}</span><strong>{value.toFixed(0)}</strong></div>
          <div className="bar-track"><div className="bar-value" style={{ width: `${value}%` }} /></div>
        </div>
      ))}
    </div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState("Overview");

  const refresh = useCallback(async () => {
    try {
      setError(null);
      const [nextSummary, nextAssets, nextVulnerabilities] = await Promise.all([
        getSummary(),
        getAssets(),
        getVulnerabilities(),
      ]);
      setSummary(nextSummary);
      setAssets(nextAssets);
      setVulnerabilities(nextVulnerabilities);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to reach the API");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
    const interval = window.setInterval(() => void refresh(), 30000);
    return () => window.clearInterval(interval);
  }, [refresh]);

  const critical = useMemo(() => vulnerabilities.filter((v) => v.severity.toLowerCase() === "critical"), [vulnerabilities]);
  const high = useMemo(() => vulnerabilities.filter((v) => v.severity.toLowerCase() === "high"), [vulnerabilities]);

  if (loading) return <div className="loading-screen"><div className="loader" /><span>Loading security telemetry</span></div>;

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand"><div className="brand-mark">S</div><div><strong>SECURITY</strong><span>CONTROL CENTER</span></div></div>
        <nav>
          {["Overview", "Assets", "Vulnerabilities", "Risk Analysis"].map((item) => (
            <button className={activeView === item ? "nav-item active" : "nav-item"} key={item} onClick={() => setActiveView(item)}>
              <span className="nav-dot" />{item}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer"><span className="online-dot" />API connected<div className="api-version">FastAPI 0.2.0</div></div>
      </aside>

      <section className="content">
        <header className="topbar">
          <div><p className="eyebrow">SECURITY OPERATIONS</p><h1>{activeView}</h1></div>
          <button className="refresh" onClick={() => void refresh()} disabled={loading}>Refresh data</button>
        </header>

        {error && <div className="error-banner">API unavailable: {error}. Start the FastAPI backend on port 8000.</div>}

        {summary && activeView === "Overview" && (
          <>
            <section className="hero-grid">
              <div className="card score-card"><div><p className="card-label">SECURITY SCORE</p><h2>{riskLabel[summary.risk_level]}</h2><p className="muted">Calculated from current assets, CVEs and security events.</p></div><ScoreRing score={summary.security_score} /></div>
              <div className="stat-card"><span>Assets</span><strong>{summary.assets}</strong><small>Monitored endpoints</small></div>
              <div className="stat-card"><span>Vulnerabilities</span><strong>{summary.vulnerabilities}</strong><small>{summary.critical_vulnerabilities} critical · {summary.high_vulnerabilities} high</small></div>
              <div className="stat-card"><span>Security events</span><strong>{summary.security_events}</strong><small>Events currently tracked</small></div>
            </section>

            <section className="two-column">
              <div className="card panel"><div className="panel-head"><div><p className="card-label">RISK BREAKDOWN</p><h3>Security posture</h3></div><span className={`pill ${summary.risk_level}`}>{summary.risk_level}</span></div><RiskBars summary={summary} /></div>
              <div className="card panel"><div className="panel-head"><div><p className="card-label">VULNERABILITY SIGNAL</p><h3>Current exposure</h3></div></div><div className="signal-grid"><div><span>Critical</span><strong className="critical-text">{summary.critical_vulnerabilities}</strong></div><div><span>High</span><strong className="high-text">{summary.high_vulnerabilities}</strong></div><div><span>Other</span><strong>{Math.max(summary.vulnerabilities - critical.length - high.length, 0)}</strong></div></div><p className="muted note">Risk scores are deterministic and derived from the backend risk engine.</p></div>
            </section>
          </>
        )}

        {summary && activeView === "Assets" && <section className="card table-panel"><div className="panel-head"><div><p className="card-label">INVENTORY</p><h3>Monitored assets</h3></div><span className="count-badge">{assets.length}</span></div><AssetTable assets={assets} /></section>}
        {summary && activeView === "Vulnerabilities" && <section className="card table-panel"><div className="panel-head"><div><p className="card-label">VULNERABILITY INTELLIGENCE</p><h3>Imported CVEs</h3></div><span className="count-badge">{vulnerabilities.length}</span></div><VulnerabilityTable vulnerabilities={vulnerabilities} /></section>}
        {summary && activeView === "Risk Analysis" && <section className="two-column"><div className="card panel"><div className="panel-head"><div><p className="card-label">RISK ENGINE</p><h3>Score composition</h3></div></div><RiskBars summary={summary} /></div><div className="card panel analysis-copy"><p className="card-label">METHOD</p><h3>Transparent by design</h3><p>The score is calculated from CVSS exposure, vulnerability severity, asset risk and security events. Every component is bounded to 0–100 and weighted by the backend risk engine.</p><div className="formula">40% CVSS · 25% vulnerabilities · 20% assets · 15% events</div></div></section>}
      </section>
    </main>
  );
}

function AssetTable({ assets }: { assets: Asset[] }) {
  if (!assets.length) return <div className="empty">No assets registered.</div>;
  return <div className="table-wrap"><table><thead><tr><th>Hostname</th><th>IP address</th><th>OS</th><th>Environment</th><th>Risk</th></tr></thead><tbody>{assets.map((asset) => <tr key={asset.id}><td><strong>{asset.hostname}</strong></td><td>{asset.ip_address}</td><td>{asset.operating_system || "Unknown"}</td><td><span className="env">{asset.environment}</span></td><td><span className={asset.risk_score >= 70 ? "risk high" : asset.risk_score >= 40 ? "risk medium" : "risk low"}>{asset.risk_score.toFixed(0)}</span></td></tr>)}</tbody></table></div>;
}

function VulnerabilityTable({ vulnerabilities }: { vulnerabilities: Vulnerability[] }) {
  if (!vulnerabilities.length) return <div className="empty">No vulnerabilities imported.</div>;
  return <div className="table-wrap"><table><thead><tr><th>CVE</th><th>Severity</th><th>CVSS</th><th>Status</th><th>Published</th></tr></thead><tbody>{vulnerabilities.map((vulnerability) => <tr key={vulnerability.id}><td><strong>{vulnerability.cve_id}</strong></td><td><span className={`severity ${vulnerability.severity.toLowerCase()}`}>{vulnerability.severity}</span></td><td>{vulnerability.cvss_score?.toFixed(1) ?? "—"}</td><td>{vulnerability.status}</td><td>{vulnerability.published_at ? new Date(vulnerability.published_at).toLocaleDateString() : "—"}</td></tr>)}</tbody></table></div>;
}
