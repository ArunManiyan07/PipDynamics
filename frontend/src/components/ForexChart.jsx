import TradingViewWidget from "react-tradingview-widget";

export default function ForexChart({ pair, timeframe }) {
  const tfMap = {
    M15: "15",
    H1: "60",
  };

  return (
    <div
      style={{
        height: "420px",
        borderRadius: "16px",
        overflow: "hidden",
        background: "#020617",
        boxShadow: "0 0 25px rgba(34,211,238,0.15)",
      }}
    >
      <TradingViewWidget
        symbol={`FX:${pair}`}
        interval={tfMap[timeframe] || "15"}
        theme="dark"
        autosize
      />
    </div>
  );
}
