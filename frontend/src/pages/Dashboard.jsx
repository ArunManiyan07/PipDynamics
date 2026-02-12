import { useContext } from "react";
import { AppContext } from "../context/AppContext";

export default function Dashboard() {
  const { pair, timeframe } = useContext(AppContext);

  let signal = "WAIT";
  let reason = "Market is ranging";

  if (timeframe === "M15") {
    signal = "BUY";
    reason = "Momentum bullish on mid timeframe";
  } else if (timeframe === "H1") {
    signal = "SELL";
    reason = "Higher timeframe trend is bearish";
  }

  return (
    <div className="page">
      <h1>Dashboard</h1>

      <h3>
        {pair} · {timeframe}
      </h3>

      <div className={`signal-text ${signal.toLowerCase()}`}>
        {signal}
      </div>

      <p>{reason}</p>
    </div>
  );
}
