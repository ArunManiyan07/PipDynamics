import pandas as pd
import joblib
import os
import numpy as np
import logging

from live_data_mt5 import get_live_data


# =================================================
# LOGGING
# =================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("signal_engine")


# =================================================
# LOAD MODEL + FEATURES
# =================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_directional_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "model_features.pkl")

try:
    ml_model = joblib.load(MODEL_PATH)
    model_features = joblib.load(FEATURE_PATH)
except Exception as e:
    raise RuntimeError(f"Model loading failed: {str(e)}")


# =================================================
# FEATURE ENGINEERING
# =================================================
def generate_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df.columns = df.columns.str.lower()

    required_cols = {"open", "high", "low", "close"}
    if not required_cols.issubset(df.columns):
        raise ValueError("Missing OHLC columns in live data")

    # EMA
    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema_diff"] = df["ema20"] - df["ema50"]

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))

    # ATR
    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(14).mean()

    df = df.dropna().reset_index(drop=True)

    return df


# =================================================
# MAIN SIGNAL FUNCTION
# =================================================
def get_recommendation_for_pair(pair: str, timeframe: str = "H1"):

    try:
        df = get_live_data(pair, timeframe=timeframe, bars=400)

        if df is None or len(df) < 60:
            return _hold_response("Insufficient live data")

        df = generate_features(df)

        if df.empty:
            return _hold_response("Feature generation failed")

        last = df.iloc[-1]

        # Prepare model input
        X = pd.DataFrame(
            [[last.get(f, 0) for f in model_features]],
            columns=model_features
        )

        probs = ml_model.predict_proba(X)[0]
        classes = ml_model.classes_

        prob_dict = dict(zip(classes, probs))

        buy_prob = float(prob_dict.get(1, 0))
        sell_prob = float(prob_dict.get(-1, 0))

        logger.info(f"{pair} → BUY:{buy_prob:.3f} SELL:{sell_prob:.3f}")

        # =================================================
        # DECISION LOGIC (BALANCED + STABLE)
        # =================================================

        edge = abs(buy_prob - sell_prob)

        # If too close → market indecision
        if edge < 0.025:
            return _hold_response("Market indecision (probabilities too close)")

        # Determine direction
        if buy_prob > sell_prob:
            direction = "BUY"
            confidence = buy_prob
        else:
            direction = "SELL"
            confidence = sell_prob

        confidence_pct = round(confidence * 100, 2)

        # Strength grading
        if confidence >= 0.70:
            strength = "Strong"
        elif confidence >= 0.60:
            strength = "Moderate"
        else:
            strength = "Weak"

        # =================================================
        # TRADE LEVELS USING ATR
        # =================================================
        price = float(last["close"])
        atr = float(last["atr"])

        risk_multiplier = 1.0
        reward_multiplier = 2.0

        if direction == "BUY":
            sl = round(price - (atr * risk_multiplier), 5)
            tp = round(price + (atr * reward_multiplier), 5)
        else:
            sl = round(price + (atr * risk_multiplier), 5)
            tp = round(price - (atr * reward_multiplier), 5)

        return {
            "signal": direction,
            "strength": strength,
            "confidence": confidence_pct,
            "entry": round(price, 5),
            "sl": sl,
            "tp": tp,
            "rr": "1:2",
            "reasons": [
                f"{strength} {direction} probability edge",
                f"Probability gap: {round(edge*100,2)}%"
            ]
        }

    except Exception as e:
        logger.error(f"Signal engine failure: {str(e)}")
        return _hold_response("Signal engine failure")


# =================================================
# HOLD RESPONSE
# =================================================
def _hold_response(reason: str):
    return {
        "signal": "WAIT",
        "strength": "Neutral",
        "confidence": 0,
        "entry": None,
        "sl": None,
        "tp": None,
        "rr": None,
        "reasons": [reason]
    }