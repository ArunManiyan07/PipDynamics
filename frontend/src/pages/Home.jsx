import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="hero">
      <div className="hero-container">
        
        {/* LEFT SIDE CONTENT */}
        <div className="hero-content">
          
          <h1 className="hero-title">
            Welcome to PipDynamics
          </h1>

          <p className="hero-tagline">
            AI-powered Forex signal system that analyzes 
            market structure and momentum.
          </p>

          <p className="hero-description">
            Built for modern traders, PipDynamics leverages 
            AI-driven market structure detection and momentum 
            analysis to identify high-probability opportunities. 
            It filters market noise, reduces emotional 
            decision-making, and provides structured insights 
            you can trust in fast-moving Forex environments.
          </p>

          <div className="hero-actions">
            <Link to="/markets" className="primary-btn">
              Start Analysis →
            </Link>
          </div>

        </div>

      </div>
    </section>
  );
}
