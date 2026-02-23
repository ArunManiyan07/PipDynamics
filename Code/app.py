from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
from typing import Optional
import logging

from step5_signal_logic import get_recommendation_for_pair
from live_data_mt5 import get_live_price


# =================================================
# APP INIT
# =================================================
app = FastAPI(
    title="PipDynamics Backend",
    description="AI-powered Forex signal & live price API",
    version="4.0.0"
)


# =================================================
# LOGGING
# =================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pipdynamics")


# =================================================
# CORS
# =================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =================================================
# UTIL
# =================================================
def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_pair(pair: str) -> str:
    return pair.replace("/", "").upper()


def normalize_signal(signal: str) -> str:
    if signal in {"BUY", "SELL", "WAIT"}:
        return signal
    return "WAIT"


def map_signal(signal: str):
    if signal == "BUY":
        return "Bullish", "Buy"
    elif signal == "SELL":
        return "Bearish", "Sell"
    return "Neutral", "No Bias"


def scale_confidence(value: float) -> float:
    """
    Convert 0-1 model output into 0-100 percentage
    Clamp safely between 0 and 100
    """
    if value <= 1:
        value = value * 100
    return round(max(0, min(value, 100)), 2)


# =================================================
# HEALTH
# =================================================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": utc_now()
    }


# =================================================
# VERSION
# =================================================
@app.get("/version")
def version():
    return {
        "version": app.version,
        "timestamp": utc_now()
    }


# =================================================
# SIGNAL
# =================================================
@app.get("/signal")
def signal(
    pair: str = Query(...),
    timeframe: str = Query("H1"),
    debug: Optional[bool] = False
):

    try:
        clean_pair = normalize_pair(pair)
        clean_tf = timeframe.upper()

        result = get_recommendation_for_pair(clean_pair, clean_tf)

        if not result:
            raise ValueError("Empty signal engine response")

        raw_signal = normalize_signal(result.get("signal", "WAIT"))
        raw_conf = float(result.get("confidence", 0))

        confidence = scale_confidence(raw_conf)
        trend, bias = map_signal(raw_signal)

        logger.info(
            f"{clean_pair} {clean_tf} → {raw_signal} | CONF: {confidence}"
        )

        response = {
            "pair": clean_pair,
            "timeframe": clean_tf,
            "signal": raw_signal,
            "trend": trend,
            "bias": bias,
            "confidence": confidence,
            "entry": result.get("entry"),
            "sl": result.get("sl"),
            "tp": result.get("tp"),
            "rr": result.get("rr"),
            "reasons": result.get("reasons", []),
            "generated_at": utc_now()
        }

        if debug:
            response["ml_debug"] = result

        return response

    except Exception as e:
        logger.error(f"Signal error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Signal engine failure"
        )


# =================================================
# LIVE PRICE
# =================================================
@app.get("/price")
def price(pair: str = Query(...)):

    try:
        clean_pair = normalize_pair(pair)

        live_price, last_close = get_live_price(clean_pair)

        return {
            "pair": clean_pair,
            "live_price": live_price,
            "last_close": last_close,
            "timestamp": utc_now()
        }

    except Exception as e:
        logger.error(f"Price error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Price feed unavailable"
        )