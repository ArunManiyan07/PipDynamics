import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AppContext } from "../context/AppContext";

export default function Markets() {
  const { pair, setPair, timeframe, setTimeframe } =
    useContext(AppContext);

  const navigate = useNavigate();

  return (
    <div className="page">
      <h1>Select Market</h1>

      <select value={pair} onChange={(e) => setPair(e.target.value)}>
  <option>EUR/USD</option>
  <option>GBP/USD</option>
  <option>USD/JPY</option>
  <option>USD/CHF</option>
  <option>AUD/USD</option>
  <option>NZD/USD</option>
  <option>USD/CAD</option>
  <option>EUR/GBP</option>
  <option>EUR/JPY</option>
  <option>GBP/JPY</option>
  <option>AUD/JPY</option>
  <option>EUR/AUD</option>
  <option>XAU/USD</option>
  <option>GBP/AUD</option>
  <option>NZD/JPY</option>
</select>


      <select
        value={timeframe}
        onChange={(e) => setTimeframe(e.target.value)}
      >
        <option>M5</option>
        <option>M15</option>
        <option>H1</option>
      </select>

      <button
        className="primary-btn"
        onClick={() => navigate("/dashboard")}
      >
        View Dashboard →
      </button>
    </div>
  );
}
