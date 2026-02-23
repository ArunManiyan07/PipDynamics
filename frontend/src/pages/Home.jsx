import { Link } from "react-router-dom";

export default function Home() {
  return (
    <>
      {/* ================= HERO SECTION ================= */}
      <section className="hero">
        <div className="hero-container">

          {/* LEFT SIDE */}
          <div className="hero-content">
            <h1 className="hero-title">
              Smarter Forex Decisions.
              <br />
              <span>Powered by AI Intelligence.</span>
            </h1>

            <p className="hero-description">
              PipDynamics combines market structure detection,
              momentum filtering, and AI-driven probability scoring
              to generate high-quality Forex trading signals.
            </p>

            <div className="hero-actions">
              <Link to="/Markets" className="primary-btn">
                View Market →
              </Link>
            </div>
          </div>

          {/* RIGHT SIDE – LIVE PREVIEW */}
          <div className="hero-preview">
            <div className="preview-card">
              <h3>Live AI Signal</h3>

              <div className="preview-row">
                <span>Pair</span>
                <strong>EUR/USD</strong>
              </div>

              <div className="preview-row">
                <span>Direction</span>
                <strong className="bullish">BUY</strong>
              </div>

              <div className="preview-row">
                <span>Entry</span>
                <strong>1.0845</strong>
              </div>

              <div className="preview-row">
                <span>Confidence</span>
                <strong>82%</strong>
              </div>

              <div className="preview-bar">
                <div style={{ width: "82%" }}></div>
              </div>
            </div>
          </div>

        </div>
      </section>


      {/* ================= FEATURES SECTION ================= */}
      <section className="features">
        <h2 className="section-title">Why PipDynamics?</h2>

        <div className="features-grid">

          <div className="feature-card">
            <h3>AI Market Structure Detection</h3>
            <p>
              Detects trend shifts, breakouts, and consolidation
              phases using structured algorithmic logic.
            </p>
          </div>

          <div className="feature-card">
            <h3>Momentum-Based Filtering</h3>
            <p>
              Filters out weak setups and identifies strong,
              directional moves backed by data.
            </p>
          </div>

          <div className="feature-card">
            <h3>Probability Confidence Scoring</h3>
            <p>
              Every signal includes a structured confidence
              percentage to support disciplined trading.
            </p>
          </div>

        </div>
      </section>


      {/* ================= LIVE SIGNALS PREVIEW ================= */}
      <section className="signals-preview">
        <h2 className="section-title">Live Market Signals</h2>

        <div className="signals-grid">

          <div className="signal-card">
            <div className="signal-header">
              <h3>EUR/USD</h3>
              <span className="badge buy">BUY</span>
            </div>
            <p>Confidence: 76%</p>
          </div>

          <div className="signal-card">
            <div className="signal-header">
              <h3>GBP/JPY</h3>
              <span className="badge sell">SELL</span>
            </div>
            <p>Confidence: 64%</p>
          </div>

          <div className="signal-card">
            <div className="signal-header">
              <h3>XAU/USD</h3>
              <span className="badge breakout">BREAKOUT</span>
            </div>
            <p>Confidence: 81%</p>
          </div>

        </div>

      </section>


      {/* ================= HOW IT WORKS ================= */}
      <section className="how-it-works">
        <h2 className="section-title">How It Works</h2>

        <div className="steps-grid">

          <div className="step-card">
            <h3>1. Select Market</h3>
            <p>Choose your preferred Forex pair.</p>
          </div>

          <div className="step-card">
            <h3>2. AI Evaluation</h3>
            <p>Structure and momentum are analyzed in real time.</p>
          </div>

          <div className="step-card">
            <h3>3. Receive Signal</h3>
            <p>Get entry levels, bias direction, and confidence score.</p>
          </div>

        </div>
      </section>


      {/* ================= FOOTER ================= */}
      <footer className="footer">
        <p>© 2026 PipDynamics. All rights reserved.</p>
        <p className="disclaimer">
          Trading involves risk. Past performance does not guarantee future results.
        </p>
      </footer>
    </>
  );
}
