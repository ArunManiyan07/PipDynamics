const API_BASE = "http://127.0.0.1:8000";

// ==============================
// GENERIC SAFE FETCH
// ==============================
async function safeFetch(url) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `API Error ${response.status}: ${errorText || "Unknown error"}`
      );
    }

    const data = await response.json();

    if (!data || typeof data !== "object") {
      throw new Error("Invalid JSON response from server");
    }

    return data;
  } catch (error) {
    clearTimeout(timeout);

    if (error.name === "AbortError") {
      console.error("Request timed out");
      throw new Error("Server timeout. Please try again.");
    }

    console.error("API Fetch Failed:", error.message);
    throw error;
  }
}

// ==============================
// HELPER: CLEAN INPUTS
// ==============================
function formatPair(pair) {
  return pair?.replace("/", "").toUpperCase();
}

function formatTimeframe(tf) {
  return tf?.toUpperCase();
}

// ==============================
// SIGNAL API
// ==============================
export async function getRecommendation(pair, timeframe) {
  if (!pair || !timeframe) {
    throw new Error("Pair and timeframe required");
  }

  const cleanPair = formatPair(pair);
  const cleanTimeframe = formatTimeframe(timeframe);

  const url = `${API_BASE}/signal?pair=${encodeURIComponent(
    cleanPair
  )}&timeframe=${encodeURIComponent(cleanTimeframe)}`;

  console.log("Calling Signal API:", url);

  return safeFetch(url);
}

// ==============================
// PRICE API
// ==============================
export async function getPrice(pair) {
  if (!pair) {
    throw new Error("Pair required");
  }

  const cleanPair = formatPair(pair);

  const url = `${API_BASE}/price?pair=${encodeURIComponent(cleanPair)}`;

  console.log("Calling Price API:", url);

  return safeFetch(url);
}