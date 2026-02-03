import pandas as pd
import joblib
import os
import numpy as np

from live_data_mt5 import get_live_data

# =================================================
# PATHS
# =================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_h1_directional_model.pkl")

# =================================================
# LOAD MODEL
# =================================================
ml_model = joblib.load(MODEL_PATH)

# =================================================
# INDICATORS
# =================================================
def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # EMA
    df["EMA"] = df["close"].ewm(span=20, adjust=False).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / (avg_loss + 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))

    return df

# =================================================
# ML PROBABILITY (CONFIDENCE ONLY)
# =================================================
def get_ml_bias(row):
    X = pd.DataFrame([{
        "EMA": row["EMA"],
        "RSI": row["RSI"]
    }])

    try:
        probs = ml_model.predict_proba(X)[0]
        buy_prob = float(probs[1])
        sell_prob = float(probs[0])
        return buy_prob - sell_prob   # bias only
    except Exception:
        return 0.0

# =================================================
# STRONGER TREND (PRICE ACTION)
# =================================================
def get_trend(df: pd.DataFrame) -> str:
    if len(df) < 50:
        return "FLAT"

    recent_high = df["high"].iloc[-20:].max()
    recent_low = df["low"].iloc[-20:].min()

    if df["close"].iloc[-1] > recent_high * 0.998:
        return "UP"
    if df["close"].iloc[-1] < recent_low * 1.002:
        return "DOWN"
    return "FLAT"

# =================================================
# 🔥 FINAL RECOMMENDATION ENGINE (GUARANTEED DISTRIBUTION)
# =================================================
def get_recommendation_for_pair(pair: str, timeframe: str = "M15"):

    df = get_live_data(pair, timeframe=timeframe, bars=300)
    if df is None or len(df) < 150:
        return {"signal": "NO DATA", "confidence": 0, "reason": "Insufficient data"}

    df = add_indicators(df)
    last = df.iloc[-1]

    trend = get_trend(df)
    rsi = last["RSI"]
    ml_bias = get_ml_bias(last)

    # =================================================
    # 1️⃣ RULE-BASED DIRECTION (PRIMARY)
    # =================================================
    if trend == "UP" and rsi < 70:
        signal = "BUY"
        confidence = 65 + (70 - rsi) * 0.5
    elif trend == "DOWN" and rsi > 30:
        signal = "SELL"
        confidence = 65 + (rsi - 30) * 0.5
    else:
        return {
            "signal": "HOLD",
            "confidence": 50,
            "reason": "Market ranging / no structure"
        }

    # =================================================
    # 2️⃣ ML CONFIDENCE ADJUSTMENT (NOT DIRECTION)
    # =================================================
    if signal == "BUY" and ml_bias > 0:
        confidence += 8
    elif signal == "SELL" and ml_bias < 0:
        confidence += 8
    else:
        confidence -= 5

    confidence = int(np.clip(confidence, 55, 90))

    # =================================================
    # 3️⃣ FINAL OUTPUT
    # =================================================
    if confidence < 60:
        return {
            "signal": "WAIT",
            "confidence": confidence,
            "reason": "Weak confirmation"
        }

    return {
        "signal": signal,
        "confidence": confidence,
        "reason": "Price action + momentum alignment"
    }
