import "./LiveSignals.css";

export default function LiveSignals() {

  const signals = [
    {
      pair: "EUR/USD",
      type: "buy",
      entry: "1.0845",
      sl: "1.0812",
      tp: "1.0921",
      live: "1.0843",
      confidence: 82
    },
    {
      pair: "GBP/JPY",
      type: "sell",
      entry: "1.0845",
      sl: "1.0810",
      tp: "1.0921",
      live: "1.0810",
      confidence: 82
    },
    {
      pair: "XAU/USD",
      type: "breakout",
      entry: "1.0810",
      sl: "1.0920",
      tp: "1.0920",
      live: "1.0620",
      confidence: 82
    }
  ];

  return (
    <div className="live-wrapper">
      <h1 className="live-title">Live Market Signals</h1>

      <div className="live-grid">
        {signals.map((signal, index) => (
          <div className={`live-card ${signal.type}`} key={index}>

            <div className="card-top">
              <h2>{signal.pair}</h2>
              <span className={`tag ${signal.type}`}>
                {signal.type.toUpperCase()}
              </span>
            </div>

            <div className="price-row">
              <span>Entry:</span>
              <span className="value">{signal.entry}</span>
              <span className="live-price">{signal.live}</span>
            </div>

            <div className="price-row">
              <span>SL:</span>
              <span>{signal.sl}</span>
              <span>{signal.tp}</span>
            </div>

            <div className="confidence">
              <span>{signal.confidence}% confidence</span>
              <div className="bars">
                {[...Array(12)].map((_, i) => (
                  <div key={i}></div>
                ))}
              </div>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}
