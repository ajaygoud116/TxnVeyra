import { useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Bell,
  ChevronDown,
  CircleDot,
  Command,
  Database,
  Fingerprint,
  GitBranch,
  LayoutDashboard,
  MapPinned,
  Search,
  ShieldCheck,
  Shield,
  SlidersHorizontal,
  Workflow,
} from "lucide-react";
import { getHealth, type HealthResponse } from "./lib/api";

const navigation = [
  { label: "Command Center", icon: LayoutDashboard, active: true },
  { label: "Transaction Intelligence", icon: Activity },
  { label: "Risk Engine", icon: ShieldCheck },
  { label: "Network Explorer", icon: GitBranch },
  { label: "Investigation Centre", icon: Workflow },
  { label: "Geo & Temporal", icon: MapPinned },
  { label: "Data Management", icon: Database },
];

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [apiError, setApiError] = useState(false);

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setApiError(true));
  }, []);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Shield size={21} /></div>
          <div>
            <div className="brand-name">TxnVeyra</div>
            <div className="brand-caption">RISK INTELLIGENCE</div>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>
        <div className="workspace-switch">
          <div className="workspace-icon"><Command size={16} /></div>
          <div className="workspace-copy">
            <strong>Analyst workspace</strong>
            <span>Development environment</span>
          </div>
          <ChevronDown size={15} />
        </div>

        <div className="nav-label">INTELLIGENCE</div>
        <nav aria-label="Main navigation">
          {navigation.map(({ label, icon: Icon, active }) => (
            <button className={`nav-item ${active ? "active" : ""}`} key={label} type="button">
              <Icon size={17} strokeWidth={1.8} />
              <span>{label}</span>
              {label === "Investigation Centre" && <span className="nav-count">—</span>}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="environment-pill"><span /> LOCAL DEVELOPMENT</div>
          <div className="profile">
            <div className="avatar">SP</div>
            <div><strong>Platform Admin</strong><span>Prototype account</span></div>
            <SlidersHorizontal size={16} />
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumbs">Workspace <span>/</span> <strong>Command Center</strong></div>
          <div className="top-actions">
            <div className="system-status">
              <span className={`status-dot ${health ? "online" : ""}`} />
              {health ? "API connected" : apiError ? "API unavailable" : "Checking API"}
            </div>
            <button className="icon-button" aria-label="Notifications" type="button"><Bell size={18} /></button>
            <div className="top-avatar">SP</div>
          </div>
        </header>

        <section className="page">
          <div className="page-heading">
            <div>
              <div className="eyebrow"><CircleDot size={13} /> PAYMENT RISK OPERATIONS</div>
              <h1>Command Center</h1>
              <p>Monitor transaction risk, explore emerging patterns, and coordinate investigations.</p>
            </div>
            <button className="date-button" type="button"><Search size={15} /> Search workspace</button>
          </div>

          <div className="notice">
            <AlertTriangle size={17} />
            <div><strong>Development environment</strong><span>Historical data only. No live UPI or banking connection is configured.</span></div>
            <span className="notice-tag">PROTOTYPE</span>
          </div>

          <div className="section-heading">
            <div><h2>Operational overview</h2><p>Platform metrics will appear here after the data ingestion stage.</p></div>
            <span className="muted-label">NO DATA CONNECTED</span>
          </div>

          <div className="metric-grid">
            {[
              { label: "Transactions monitored", value: "—", note: "Awaiting data import", icon: Activity },
              { label: "High-risk alerts", value: "—", note: "Risk engine not configured", icon: AlertTriangle },
              { label: "Open investigations", value: "—", note: "Case management pending", icon: Fingerprint },
              { label: "Network entities", value: "—", note: "Graph layer pending", icon: GitBranch },
            ].map(({ label, value, note, icon: Icon }) => (
              <article className="metric-card" key={label}>
                <div className="metric-top"><span>{label}</span><Icon size={17} /></div>
                <div className="metric-value">{value}</div>
                <div className="metric-note">{note}</div>
              </article>
            ))}
          </div>

          <div className="content-grid">
            <section className="panel activity-panel">
              <div className="panel-heading"><div><h2>Risk activity</h2><p>Transaction risk signals over time</p></div><button className="subtle-button" type="button">Last 30 days <ChevronDown size={14} /></button></div>
              <div className="empty-chart">
                <div className="empty-icon"><Activity size={22} /></div>
                <strong>No activity to display</strong>
                <span>Import a supported historical dataset to begin exploring risk patterns.</span>
              </div>
            </section>
            <section className="panel feed-panel">
              <div className="panel-heading"><div><h2>Investigation queue</h2><p>Prioritized analyst work</p></div><ArrowUpRight size={17} /></div>
              <div className="empty-feed">
                <div className="empty-icon"><Workflow size={21} /></div>
                <strong>No investigations yet</strong>
                <span>Alerts and cases will appear here when those modules are implemented.</span>
              </div>
            </section>
          </div>

          <section className="panel platform-panel">
            <div className="panel-heading"><div><h2>Platform services</h2><p>Development service connectivity</p></div><span className="live-label">SERVICE CHECK</span></div>
            <div className="service-row">
              <div className="service-icon"><ShieldCheck size={17} /></div>
              <div className="service-copy"><strong> TxnVeyra API</strong><span>FastAPI application</span></div>
              <span className={`service-state ${health ? "good" : apiError ? "bad" : ""}`}>{health ? "Connected" : apiError ? "Unavailable" : "Checking"}</span>
            </div>
            <div className="service-row">
              <div className="service-icon"><Database size={17} /></div>
              <div className="service-copy"><strong>PostgreSQL</strong><span>Primary application database</span></div>
              <span className="service-state pending">Check via API</span>
            </div>
            <div className="service-row">
              <div className="service-icon"><Workflow size={17} /></div>
              <div className="service-copy"><strong>Fraud intelligence modules</strong><span>Rules, ML and graph analytics</span></div>
              <span className="service-state pending">Not configured</span>
            </div>
          </section>

          <footer className="footer"><span>TxnVeyra · Intelligent Payment Fraud & Risk Intelligence</span><span>Build 0.1.0 · Development</span></footer>
        </section>
      </main>
    </div>
  );
}

export default App;
