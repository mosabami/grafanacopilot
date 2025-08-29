import './App.css'
import { CopilotSidebar } from './components/CopilotSidebar'

function App() {
  return (
    <div className="app-shell">
      <header className="header">
        <div className="brand">
          <div className="logo">MG</div>
          <div>
            <div style={{ fontWeight: 700 }}>Managed Grafana</div>
            <div className="muted">on Azure</div>
          </div>
        </div>

        <nav className="nav-links" aria-label="Main navigation">
          <a href="#">Overview</a>
          <a href="#">Pricing</a>
          <a href="#">Docs</a>
          <a href="#" className="primary">Get started</a>
        </nav>
      </header>

      <div className="main">
        <main>
          <section className="hero">
            <div className="left">
              <h1 className="hero-title">Managed Grafana on Azure</h1>
              <p className="hero-sub">Visualize application and infrastructure telemetry with a fully managed Grafana service that's secure, scalable, and integrated with Azure Monitor, Log Analytics, and more.</p>

              <div className="hero-cta">
                <button className="cta-primary">Try Managed Grafana</button>
                <button className="cta-secondary">Learn about managed Grafana</button>
              </div>

              <div className="features" aria-hidden>
                <div className="feature">
                  <h4>Secure & compliant</h4>
                  <p className="muted">Azure AD integration and RBAC out of the box.</p>
                </div>
                <div className="feature">
                  <h4>Fully managed</h4>
                  <p className="muted">We handle upgrades, scaling, and high availability.</p>
                </div>
                <div className="feature">
                  <h4>Built-in integrations</h4>
                  <p className="muted">Native connectors to Azure Monitor and Prometheus.</p>
                </div>
              </div>
            </div>

            <div className="right-preview" aria-hidden>
              <div className="preview-surface">
                <div className="preview-text">Grafana preview</div>
              </div>
            </div>
          </section>
        </main>

        <CopilotSidebar />
      </div>
    </div>
  )
}

export default App
