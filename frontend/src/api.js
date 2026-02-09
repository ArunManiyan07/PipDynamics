const API_BASE = "http://127.0.0.1:8000";

export async function getRecommendation(pair, timeframe) {
  const res = await fetch(
    `${API_BASE}/recommend?pair=${pair}&timeframe=${timeframe}`
  );
  if (!res.ok) throw new Error("Backend error");
  return res.json();
}

export async function getPrice(pair) {
  const res = await fetch(
    `${API_BASE}/price?pair=${pair}`
  );
  if (!res.ok) throw new Error("Price fetch failed");
  return res.json();
}
