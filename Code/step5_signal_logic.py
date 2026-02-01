from live_data_mt5 import get_live_data
import os
import pandas as pd
import joblib

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "OP", "data_with_order_blocks.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "rf_h1_directional_model.pkl")

df = pd.read_csv(DATA_PATH)
ml_model = joblib.load(MODEL_PATH)

# -------------------------------------------------
# ML PREDICTION (FIXED)
# -------------------------------------------------
def ml_predict_direction(row):
    X = pd.DataFrame([{
        "EMA": row["EMA"],
        "RSI": row["RSI"],
        "BOS": row["BOS"]
    }])
    return ml_model.predict(X)[0]

# -------------------------------------------------
# LIVE TREND (UNCHANGED)
# -------------------------------------------------
def get_live_trend(pair, timeframe):
    symbol = pair.replace("/", "")
    live_df = get_live_data(symbol, timeframe=timeframe, bars=20)

    if live_df.empty or len(live_df) < 2:
        return "FLAT"

    last_close = live_df.iloc[-1]["close"]
    prev_close = live_df.iloc[-2]["close"]

    if last_close > prev_close:
        return "UP"
    elif last_close < prev_close:
        return "DOWN"
    else:
        return "FLAT"

# -------------------------------------------------
# FINAL RECOMMENDATIONS (H1 ML + SMC FILTER)
# -------------------------------------------------
def get_current_recommendations(df, timeframe=None):
    results = []

    for pair in df["pair"].unique():
        pair_df = df[df["pair"] == pair]
        last_row = pair_df.iloc[-1]

        # -------- ML SIGNAL --------
        ml_signal = ml_predict_direction(last_row)

        if ml_signal == 1:
            signal = "BUY"
            confidence = 0.60
        elif ml_signal == -1:
            signal = "SELL"
            confidence = 0.60
        else:
            signal = "HOLD"
            confidence = 0.40

        # -------- SMC FILTER (FIXED) --------
        if signal == "BUY":
            if last_row["OrderBlock"] != 1:
                signal = "HOLD"
                confidence = 0.40

        if signal == "SELL":
            if last_row["OrderBlock"] != -1:
                signal = "HOLD"
                confidence = 0.40

        # -------- LIVE CONFIRMATION --------
        if timeframe is not None and signal != "HOLD":
            live_trend = get_live_trend(pair, timeframe)

            if signal == "BUY" and live_trend == "UP":
                confidence += 0.25
            elif signal == "SELL" and live_trend == "DOWN":
                confidence += 0.25
            else:
                signal = "HOLD"
                confidence = 0.40

        confidence = min(round(confidence, 2), 0.99)

        results.append({
            "pair": pair,
            "signal": signal,
            "confidence": confidence
        })

    return results
