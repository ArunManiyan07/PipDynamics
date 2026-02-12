const API_BASE = "http://127.0.0.1:8000";

export async function getRecommendation(pair, timeframe) {
  const res = await fetch(
    `${API_BASE}/recommend?pair=${pair}&timeframe=${timeframe}`
  );
  return res.json();
}

export async function getPrice(pair) {
  const res = await fetch(
    `${API_BASE}/price?pair=${pair}`
  );
  return res.json();
}
