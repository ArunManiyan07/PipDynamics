import { useEffect, useState } from "react";
import "./styles.css";
import { getRecommendation, getPrice } from "./api";

const PAIRS = [
  "EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","AUDUSD","NZDUSD",
  "EURGBP","EURJPY","EURCHF","EURCAD","EURAUD","EURNZD",
  "GBPJPY","GBPCAD","GBPAUD","AUDJPY","AUDNZD"
];

function isMarketOpen() {
  const now = new Date();
  const wd = now.getUTCDay();
  const hr = now.getUTCHours();
  if (wd === 6) return false;
  if (wd === 0 && hr < 21) return false;
  return true;
}

export default function App() {
  const [pair, setPair] = useState("EURUSD");
  const [timeframe, setTimeframe] = useState("M15");
  const [result, setResult] = useState({});
  const [price, setPrice] = useState({});
  const [error, setError] = useState("");

  const MARKET_OPEN = isMarketOpen();

  useEffect(() => {
    async function loadData() {
      try {
        const rec = await getRecommendation(pair, timeframe);
        const pr = await getPrice(pair);
        setResult(rec);
        setPrice(pr);
      } catch {
        setError("⚠️ Backend not responding (FastAPI)");
      }
    }
    loadData();
  }, [pair, timeframe]);

  const signal = result.signal || "WAIT";
  const confidence = Number(result.confidence || 0);
  const reason = result.reason || "Based on structure, momentum & volatility";

  const live = price.live_price;
  const last = price.last_close;

  let change = null;
  if (live && last) change = ((live - last) / last) * 100;

  const nowIST = new Date().toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    weekday: "long",
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true
  });

  function strengthLabel() {
    if (["BUY","SELL"].includes(signal) && confidence >= 80) return "Strong";
    if (signal === "WAIT") return "Forming";
    if (signal === "NO TRADE") return "Unclear";
    return "Weak";
  }

  return (
    <div>
      <div className="header">
        <h1>📈 PipDynamics</h1>
        <p>AI-powered Forex Market Recommendations</p>
      </div>

      <div className="market-open">
        <b>{MARKET_OPEN ? "🟢 Market Open • Live data enabled" : "⚪ Market Closed • Last known price"}</b>
      </div>

      <div className="controls">
        <select value={pair} onChange={e => setPair(e.target.value)}>
          {PAIRS.map(p => <option key={p}>{p}</option>)}
        </select>

        <select value={timeframe} onChange={e => setTimeframe(e.target.value)}>
          <option>M15</option>
          <option>H1</option>
        </select>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="main-grid">

        <div className="signal-card">
          <div className={`signal-text ${signal.toLowerCase()}`}>{signal}</div>

          <div className="signal-meta">
            Status: <b>{strengthLabel()}</b>
          </div>

          <div className="confidence-bar">
            <div className="confidence-fill" style={{ width: `${confidence}%` }} />
          </div>

          <div className="confidence-text">
            Model Conviction: <b>{confidence}%</b>
          </div>

          <div className="signal-reason">{reason}</div>
        </div>

        <div className={`price-card ${!MARKET_OPEN ? "closed" : ""}`}>
          <div className="price-pair">{pair}</div>
          <div className="price-value">
            {live ? live.toFixed(5) : "--.--"}
          </div>
          <div
            className="price-change"
            style={{ color: change >= 0 ? "#22c55e" : "#ef4444" }}
          >
            {change !== null ? `${change >= 0 ? "▲" : "▼"} ${Math.abs(change).toFixed(2)}%` : "--"}
          </div>
          <div className="price-status">
            {MARKET_OPEN ? "🟢 Live Price" : "⚪ Market Closed"}
          </div>
        </div>

      </div>

      <div className="timestamp">{nowIST}</div>
    </div>
  );
}
