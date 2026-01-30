from live_data_mt5 import get_live_data
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(BASE_DIR, "OP", "data_with_order_blocks.csv")
df = pd.read_csv(input_path)

# ---------------------------------------------
# LIVE TREND (FIXED)
# ---------------------------------------------
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


# ---------------------------------------------
# FINAL RECOMMENDATIONS
# ---------------------------------------------
def get_current_recommendations(df, timeframe=None):
    results = []

    for pair in df["pair"].unique():
        pair_df = df[df["pair"] == pair]
        last_row = pair_df.iloc[-1]

        # ---- PAST SIGNAL ----
        if last_row["Signal"] == 1:
            signal = "BUY"
            confidence = 0.55
        elif last_row["Signal"] == -1:
            signal = "SELL"
            confidence = 0.55
        else:
            signal = "HOLD"
            confidence = 0.40

        # ---- LIVE CONFIRMATION ----
        if timeframe is not None:
            live_trend = get_live_trend(pair, timeframe)

            if signal == "BUY" and live_trend == "UP":
                confidence += 0.25
            elif signal == "SELL" and live_trend == "DOWN":
                confidence += 0.25
            elif signal == "HOLD" and live_trend in ["UP", "DOWN"]:
                signal = "BUY" if live_trend == "UP" else "SELL"
                confidence += 0.30

        confidence = min(round(confidence, 2), 0.99)

        results.append({
            "pair": pair,
            "signal": signal,
            "confidence": confidence
        })

    return results
