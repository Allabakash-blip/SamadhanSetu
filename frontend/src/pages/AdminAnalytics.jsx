import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const palette = ["#2563eb", "#14b8a6", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#84cc16", "#f97316"];

function niceLabel(value) {
  return String(value ?? "Unknown").replaceAll("_", " ").toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
}

function DonutChart({ data, centerLabel = "Total" }) {
  const entries = Object.entries(data || {}).filter(([, v]) => Number(v) > 0);
  const total = entries.reduce((sum, [, v]) => sum + Number(v), 0);
  if (!entries.length) return <div className="chart-empty">No data available yet.</div>;

  let cumulative = 0;
  const radius = 72;
  const circumference = 2 * Math.PI * radius;
  return (
    <div className="donut-wrap">
      <div className="donut-visual">
        <svg viewBox="0 0 180 180" role="img" aria-label={centerLabel}>
          <circle cx="90" cy="90" r={radius} fill="none" stroke="#e8edf5" strokeWidth="26" />
          {entries.map(([label, value], index) => {
            const fraction = Number(value) / total;
            const dash = fraction * circumference;
            const offset = -cumulative * circumference;
            cumulative += fraction;
            return (
              <circle key={label} cx="90" cy="90" r={radius} fill="none" stroke={palette[index % palette.length]} strokeWidth="26"
                strokeDasharray={`${dash} ${circumference - dash}`} strokeDashoffset={offset} transform="rotate(-90 90 90)" />
            );
          })}
          <text x="90" y="84" textAnchor="middle" className="donut-total">{total}</text>
          <text x="90" y="105" textAnchor="middle" className="donut-label">{centerLabel}</text>
        </svg>
      </div>
      <div className="chart-legend">
        {entries.map(([label, value], index) => (
          <div className="legend-row" key={label}>
            <span className="legend-name"><i style={{ background: palette[index % palette.length] }} />{niceLabel(label)}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}

function BarChart({ data }) {
  const entries = Object.entries(data || {}).map(([label, value]) => [label, Number(value)]).filter(([, v]) => v >= 0);
  const max = Math.max(...entries.map(([, v]) => v), 1);
  if (!entries.length) return <div className="chart-empty">No data available yet.</div>;
  return (
    <div className="bar-chart">
      {entries.map(([label, value], index) => (
        <div className="bar-item" key={label}>
          <div className="bar-value">{value}</div>
          <div className="bar-track"><div className="bar-fill" style={{ height: `${Math.max((value / max) * 100, value ? 8 : 2)}%`, background: palette[index % palette.length] }} /></div>
          <div className="bar-label">{niceLabel(label)}</div>
        </div>
      ))}
    </div>
  );
}

function TrendChart({ data }) {
  const points = data || [];
  const width = 760, height = 280, pad = { left: 42, right: 18, top: 22, bottom: 48 };
  const max = Math.max(...points.map(p => Number(p.count) || 0), 1);
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const coords = points.map((p, i) => ({
    x: points.length === 1 ? pad.left + innerW / 2 : pad.left + (i * innerW) / (points.length - 1),
    y: pad.top + innerH - ((Number(p.count) || 0) / max) * innerH,
    count: Number(p.count) || 0,
    month: p.month,
  }));
  const line = coords.map((p, i) => `${i ? "L" : "M"}${p.x},${p.y}`).join(" ");
  const area = coords.length ? `${line} L${coords.at(-1).x},${pad.top + innerH} L${coords[0].x},${pad.top + innerH} Z` : "";
  return (
    <div className="trend-svg-wrap">
      <svg viewBox={`0 0 ${width} ${height}`} className="trend-svg" role="img" aria-label="Problems reported over the last six months">
        {[0, .25, .5, .75, 1].map((fraction) => {
          const y = pad.top + innerH - fraction * innerH;
          const value = Math.round(max * fraction);
          return <g key={fraction}><line x1={pad.left} x2={width - pad.right} y1={y} y2={y} className="grid-line" /><text x={pad.left - 9} y={y + 4} textAnchor="end" className="axis-label">{value}</text></g>;
        })}
        {area && <path d={area} className="trend-area" />}
        {line && <path d={line} className="trend-line" />}
        {coords.map((p) => <g key={p.month}><circle cx={p.x} cy={p.y} r="5" className="trend-dot" /><text x={p.x} y={height - 18} textAnchor="middle" className="axis-label">{String(p.month).slice(0, 3)}</text><title>{p.month}: {p.count} problem{p.count === 1 ? "" : "s"}</title></g>)}
      </svg>
    </div>
  );
}

function Kpi({ label, value, icon, tone }) {
  return <div className={`analytics-kpi ${tone}`}><div className="kpi-icon">{icon}</div><div><span>{label}</span><strong>{value}</strong></div></div>;
}

export default function AdminAnalytics() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    try { setLoading(true); setError(""); const response = await api.get("/analytics/overview"); setData(response.data); }
    catch (err) { setError(err.response?.data?.detail || "Unable to load analytics."); }
    finally { setLoading(false); }
  }
  useEffect(() => { load(); }, []);

  const t = data?.totals || {};
  const categoryCount = useMemo(() => Object.keys(data?.category_counts || {}).length, [data]);
  const locationNote = categoryCount === 1 ? "One category currently has reported problems." : `${categoryCount} categories currently have reported problems.`;

  if (loading) return <main className="page"><div className="panel"><h2>Loading impact analytics...</h2></div></main>;

  return (
    <main className="page analytics-page">
      <div className="analytics-topbar"><button className="btn secondary" onClick={() => navigate("/admin")}>← Admin Dashboard</button><button className="btn secondary" onClick={load}>↻ Refresh</button></div>
      <div className="analytics-hero"><div><div className="eyebrow">MILESTONE 6 · PLATFORM INTELLIGENCE</div><h1>Impact & Analytics</h1><p className="muted">A live view of citizen problems, collaboration progress, solution outcomes and measurable social impact.</p></div><div className="live-badge"><span /> Live data</div></div>
      {error && <div className="error">{error}</div>}

      <div className="analytics-kpi-grid">
        <Kpi label="Total Problems" value={t.problems ?? 0} icon="◉" tone="blue" />
        <Kpi label="Open Problems" value={t.open_problems ?? 0} icon="↗" tone="orange" />
        <Kpi label="Resolved" value={t.resolved_problems ?? 0} icon="✓" tone="green" />
        <Kpi label="Solutions" value={t.solutions ?? 0} icon="◆" tone="purple" />
        <Kpi label="Verified Solutions" value={t.verified_solutions ?? 0} icon="✓" tone="teal" />
        <Kpi label="People Affected" value={t.affected_people_reported ?? 0} icon="♟" tone="indigo" />
      </div>

      <section className="analytics-panel analytics-wide"><div className="panel-heading"><div><h2>Problems Reported</h2><p>Monthly reporting trend · last 6 months</p></div><span className="panel-chip">{t.problems ?? 0} total</span></div><TrendChart data={data?.monthly_problem_trend} /></section>

      <div className="analytics-chart-grid">
        <section className="analytics-panel"><div className="panel-heading"><div><h2>Problems by Category</h2><p>Distribution across problem domains</p></div></div><DonutChart data={data?.category_counts} centerLabel="Problems" /><p className="chart-footnote">{locationNote}</p></section>
        <section className="analytics-panel"><div className="panel-heading"><div><h2>Problems by Status</h2><p>Current lifecycle distribution</p></div></div><DonutChart data={data?.status_counts} centerLabel="Problems" /></section>
        <section className="analytics-panel"><div className="panel-heading"><div><h2>Priority Distribution</h2><p>Reported urgency levels</p></div></div><BarChart data={data?.priority_counts} /></section>
        <section className="analytics-panel"><div className="panel-heading"><div><h2>Solution Outcomes</h2><p>Progress of proposed solutions</p></div></div><BarChart data={data?.solution_status_counts} /></section>
      </div>

      <section className="analytics-panel analytics-wide"><div className="panel-heading"><div><h2>Industry Engagement</h2><p>Participation and practical support across active projects</p></div><span className="panel-chip">{t.industry_partners ?? 0} partners</span></div><div className="impact-metrics industry-metrics"><div><strong>{t.industry_offers ?? 0}</strong><span>Support offers</span></div><div><strong>{t.active_industry_partnerships ?? 0}</strong><span>Active partnerships</span></div><div><strong>{t.completed_industry_partnerships ?? 0}</strong><span>Completed partnerships</span></div><div><strong>{t.industry_partners ?? 0}</strong><span>Industry partners</span></div></div></section>

      <section className="analytics-panel analytics-wide"><div className="panel-heading"><div><h2>Industry Support Types</h2><p>What industry partners are offering to projects</p></div></div><BarChart data={data?.industry_support_type_counts} /></section>

      <section className="analytics-panel impact-panel"><div className="panel-heading"><div><h2>Social Impact Summary</h2><p>Outcome indicators calculated from platform activity</p></div></div><div className="impact-metrics"><div><strong>{t.problems_with_implemented_solution ?? 0}</strong><span>Problems with implemented solution</span></div><div><strong>{t.approved_solutions ?? 0}</strong><span>Approved solutions</span></div><div><strong>{t.verified_solutions ?? 0}</strong><span>Verified solutions</span></div><div><strong>{t.affected_people_reported ?? 0}</strong><span>Reported people affected</span></div><div><strong>{t.rejected_problems ?? 0}</strong><span>Rejected problems</span></div></div><p className="analytics-note">“Affected people” is the sum supplied by citizens in their reports. It is an indicative reported-impact measure, not an independently verified population count.</p></section>
    </main>
  );
}
