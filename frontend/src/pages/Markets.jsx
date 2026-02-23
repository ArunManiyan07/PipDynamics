import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AppContext } from "../context/AppContext";
import CustomChart from "../components/CustomChart";

export default function Markets() {
  const { pair, setPair, timeframe, setTimeframe } =
    useContext(AppContext);

  const navigate = useNavigate();

  const pairs = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF",
    "AUD/USD", "NZD/USD", "USD/CAD", "EUR/GBP",
    "EUR/JPY", "GBP/JPY", "AUD/JPY", "EUR/AUD",
    "XAU/USD", "GBP/AUD", "NZD/JPY"
  ];

  const timeframes = ["15M", "1H", "1D"];

  return (
    <div className="market-container">

      {/* Page Header */}
      <header className="market-header">
        <h1>Market Analysis</h1>
        <p>Select currency pair and timeframe</p>
      </header>

      {/* Control Bar */}
      <div className="market-controls">

        <div className="control-inline">

          {/* Left Control Group */}
          <div className="left-controls">

            {/* Pair Dropdown */}
            <div className="control-group">
              <label>Pair</label>
              <select
                value={pair}
                onChange={(e) => setPair(e.target.value)}
              >
                {pairs.map((p) => (
                  <option key={p} value={p}>
                    {p}
                  </option>
                ))}
              </select>
            </div>

            {/* Timeframe Buttons */}
            <div className="timeframe-inline">
              {timeframes.map((tf) => (
                <button
                  key={tf}
                  type="button"
                  className={`tf-btn ${timeframe === tf ? "active" : ""}`}
                  onClick={() => setTimeframe(tf)}
                >
                  {tf}
                </button>
              ))}
            </div>

            {/* Analyze Button (Grouped Left) */}
            <button
              type="button"
              className="analyze-btn"
              onClick={() => navigate("/dashboard")}
            >
              Analyze →
            </button>

          </div>

        </div>

      </div>

      {/* Content Section */}
      <div className="market-content">

        {/* Chart */}
        <div className="chart-area">
          <CustomChart pair={pair} timeframe={timeframe} />
        </div>

        {/* AI Signal Panel */}
        <aside className="signal-panel">
          <h3>AI Signal</h3>

          <div className="signal-box">
            <p><strong>Signal:</strong> BUY</p>
            <p><strong>Confidence:</strong> 82%</p>
            <p><strong>Entry:</strong> 1.0845</p>
            <p><strong>SL:</strong> 1.0800</p>
            <p><strong>TP:</strong> 1.0920</p>
          </div>
        </aside>

      </div>

    </div>
  );
}
