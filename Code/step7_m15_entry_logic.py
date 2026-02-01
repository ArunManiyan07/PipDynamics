import pandas as pd

# -------------------------------------------------
# M15 ENTRY LOGIC
# -------------------------------------------------
def get_m15_entry(pair_df, h1_signal):
    """
    pair_df : M15 dataframe of a single pair (latest rows at bottom)
    h1_signal : "BUY", "SELL", "HOLD"
    """

    # Safety check
    if pair_df is None or len(pair_df) < 2:
        return {
            "entry": "NO TRADE",
            "reason": "Not enough M15 data",
            "sl": None,
            "tp": None
        }

    # If H1 says HOLD → no trade
    if h1_signal == "HOLD":
        return {
            "entry": "NO TRADE",
            "reason": "H1 HOLD",
            "sl": None,
            "tp": None
        }

    last = pair_df.iloc[-1]
    prev = pair_df.iloc[-2]

    # -------------------------------------------------
    # BUY LOGIC
    # -------------------------------------------------
    if h1_signal == "BUY":

        # 1️⃣ Sell-side liquidity sweep
        if last["Low"] < last["Liquidity_Low"]:

            # 2️⃣ Bullish Order Block respected
            if last["OrderBlock"] == 1:

                # 3️⃣ Bullish candle confirmation
                if last["Close"] > last["Open"] and last["Close"] > prev["High"]:

                    sl = last["Liquidity_Low"]
                    tp = last["Close"] + (last["Close"] - sl) * 2  # 1:2 RR

                    return {
                        "entry": "BUY",
                        "reason": "M15 liquidity sweep + bullish OB + candle",
                        "sl": round(sl, 5),
                        "tp": round(tp, 5)
                    }

    # -------------------------------------------------
    # SELL LOGIC
    # -------------------------------------------------
    if h1_signal == "SELL":

        # 1️⃣ Buy-side liquidity sweep
        if last["High"] > last["Liquidity_High"]:

            # 2️⃣ Bearish Order Block respected
            if last["OrderBlock"] == -1:

                # 3️⃣ Bearish candle confirmation
                if last["Close"] < last["Open"] and last["Close"] < prev["Low"]:

                    sl = last["Liquidity_High"]
                    tp = last["Close"] - (sl - last["Close"]) * 2  # 1:2 RR

                    return {
                        "entry": "SELL",
                        "reason": "M15 liquidity sweep + bearish OB + candle",
                        "sl": round(sl, 5),
                        "tp": round(tp, 5)
                    }

    # -------------------------------------------------
    # DEFAULT
    # -------------------------------------------------
    return {
        "entry": "NO TRADE",
        "reason": "M15 conditions not met",
        "sl": None,
        "tp": None
    }
