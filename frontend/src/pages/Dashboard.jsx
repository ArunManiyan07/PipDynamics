import { useContext, useEffect, useState, useRef } from "react";
import { AppContext } from "../context/AppContext";
import { getRecommendation, getPrice } from "../api";
import CustomChart from "../components/CustomChart";

export default function Dashboard() {
  const { pair, timeframe } = useContext(AppContext);

  const [data, setData] = useState(null);
  const [livePrice, setLivePrice] = useState(null);
  const [prevPrice, setPrevPrice] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const priceIntervalRef = useRef(null);

  // ==============================
  // FETCH SIGNAL DATA
  // ==============================
  useEffect(() => {
    async function fetchSignal() {
      setLoading(true);
      setError(null);

      try {
        const result = await getRecommendation(pair, timeframe);
        if (!result) throw new Error("Empty response");
        setData(result);
      } catch (err) {
        console.error("Signal fetch error:", err);
        setError("Failed to load signal data.");
      } finally {
        setLoading(false);
      }
    }

    fetchSignal();
  }, [pair, timeframe]);

  // ==============================
  // FETCH LIVE PRICE (STABLE POLLING)
  // ==============================
  useEffect(() => {
    async function fetchLivePrice() {
      try {
        const result = await getPrice(pair);

        if (result?.live_price != null) {
          setPrevPrice(livePrice);
          setLivePrice(result.live_price);
        }
      } catch (err) {
        console.error("Live price error:", err);
      }
    }

    fetchLivePrice();

    priceIntervalRef.current = setInterval(fetchLivePrice, 3000);

    return () => {
      clearInterval(priceIntervalRef.current);
    };
  }, [pair]); // ❌ removed livePrice dependency

  // ==============================
  // UI STATES
  // ==============================
  if (loading) {
    return (
      <div style={{ padding: "100px", textAlign: "center" }}>
        Loading Market Data...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "100px", textAlign: "center", color: "red" }}>
        {error}
      </div>
    );
  }

  if (!data) {
    return (
      <div style={{ padding: "100px", textAlign: "center" }}>
        No Data Available
      </div>
    );
  }

  // ==============================
  // SAFE VALUES
  // ==============================
  const confidence = Number(data?.confidence ?? 0);
  const bias = data?.bias || "No Bias";
  const trend = data?.trend || "Neutral";

  const entry = data?.entry ?? "-";
  const sl = data?.sl ?? "-";
  const tp = data?.tp ?? "-";
  const rr = data?.rr ?? "-";
  const reasons = data?.reasons || [];

  const trendClass =
    trend.toLowerCase() === "bullish"
      ? "bullish"
      : trend.toLowerCase() === "bearish"
      ? "bearish"
      : "";

  const biasClass =
    bias.toLowerCase() === "buy"
      ? "bullish"
      : bias.toLowerCase() === "sell"
      ? "bearish"
      : "";

  const getConfidenceColor = (value) => {
    if (value >= 70) return "#00ff88";
    if (value >= 55) return "#4fd1ff";
    if (value >= 40) return "#ffaa00";
    return "#888";
  };

  const getConfidenceLabel = (value) => {
    if (value >= 70) return "High Conviction";
    if (value >= 55) return "Strong";
    if (value >= 40) return "Moderate";
    return "Weak";
  };

  const priceColor =
    livePrice > prevPrice
      ? "#00ff88"
      : livePrice < prevPrice
      ? "#ff4d4d"
      : "#ffffff";

  // ==============================
  // UI
  // ==============================
  return (
    <div className="dashboard-container">
      {/* TOP SUMMARY */}
      <div className="dashboard-top">
        <div className="top-item">
          <span>Pair</span>
          <h2>{pair}</h2>
        </div>

        <div className="top-item">
          <span>Live Price</span>
          <h2 style={{ color: priceColor, transition: "0.3s ease" }}>
            {livePrice ?? "-"}
          </h2>
        </div>

        <div className="top-item">
          <span>Timeframe</span>
          <h2>{timeframe}</h2>
        </div>

        <div className="top-item">
          <span>Trend</span>
          <h2 className={trendClass}>{trend}</h2>
        </div>

        <div className="top-item">
          <span>AI Confidence</span>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{
                width: `${confidence}%`,
                background: getConfidenceColor(confidence),
              }}
            ></div>
          </div>
          <p>
            {confidence}% – {getConfidenceLabel(confidence)}
          </p>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="dashboard-content">
        <div className="dashboard-chart">
          <CustomChart pair={pair} timeframe={timeframe} />
        </div>

        <div className="dashboard-right">
          <div className="dashboard-card">
            <h3>Trade Setup</h3>

            <p>
              <strong>Bias:</strong>{" "}
              <span className={biasClass} style={{ fontWeight: "bold" }}>
                {bias}
              </span>
            </p>

            {bias === "No Bias" ? (
              <p style={{ opacity: 0.7 }}>
                ⚠ Waiting for high-probability setup...
              </p>
            ) : (
              <>
                <p><strong>Entry:</strong> {entry}</p>
                <p><strong>Stop Loss:</strong> {sl}</p>
                <p><strong>Take Profit:</strong> {tp}</p>
                <p><strong>Risk Reward:</strong> {rr}</p>
              </>
            )}
          </div>

          <div className="dashboard-card">
            <h3>Why {bias}?</h3>

            {reasons.length > 0 ? (
              <ul>
                {reasons.map((reason, index) => (
                  <li key={index}>✔ {reason}</li>
                ))}
              </ul>
            ) : (
              <p>No explanation available.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}