from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import Dict, Optional

from step5_signal_logic import get_recommendation_for_pair
from live_data_mt5 import get_live_price

# =================================================
# APP SETUP
# =================================================
app = FastAPI(
    title="PipDynamics Backend",
    description="AI-powered Forex signal & live price API",
    version="1.0.0"
)

# =================================================
# CORS CONFIG (REACT)
# =================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================
# UTILS
# =================================================
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def normalize_signal(raw_signal: str) -> str:
    """
    Normalize ML signal to frontend-expected values
    """
    if raw_signal == "HOLD":
        return "WAIT"
    if raw_signal not in {"BUY", "SELL", "WAIT", "NO TRADE"}:
        return "WAIT"
    return raw_signal

# =================================================
# HEALTH CHECK
# =================================================
@app.get("/")
def health() -> Dict[str, str]:
    return {
        "status": "ok",
        "service": "PipDynamics Backend",
        "timestamp": utc_now()
    }

# =================================================
# SIGNAL ENDPOINT
# =================================================
@app.get("/recommend")
def recommend(
    pair: str = Query(..., description="Forex pair like EURUSD"),
    timeframe: str = Query("M15", description="Timeframe M15 / H1")
) -> Dict:

    try:
        result = get_recommendation_for_pair(pair, timeframe)

        if not isinstance(result, dict):
            raise ValueError("Invalid signal format")

        raw_signal = result.get("signal", "WAIT")
        signal = normalize_signal(raw_signal)

        return {
            "pair": pair,
            "timeframe": timeframe,
            "signal": signal,
            "confidence": float(result.get("confidence", 0)),
            "reason": result.get("reason", "No clear structure"),
            "generated_at": utc_now()
        }

    except Exception as e:
        # Safe fallback (UI will never break)
        return {
            "pair": pair,
            "timeframe": timeframe,
            "signal": "WAIT",
            "confidence": 0.0,
            "reason": "Signal engine unavailable",
            "error": str(e),
            "generated_at": utc_now()
        }

# =================================================
# PRICE ENDPOINT
# =================================================
@app.get("/price")
def price(
    pair: str = Query(..., description="Forex pair like EURUSD")
) -> Dict:

    try:
        live_price, last_close = get_live_price(pair)

        return {
            "pair": pair,
            "live_price": live_price,
            "last_close": last_close,
            "timestamp": utc_now()
        }

    except Exception as e:
        return {
            "pair": pair,
            "live_price": None,
            "last_close": None,
            "error": "Price feed unavailable",
            "details": str(e),
            "timestamp": utc_now()
        }
