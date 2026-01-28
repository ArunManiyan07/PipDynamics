import os
import pandas as pd

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load order block data
# -------------------------------------------------
input_path = os.path.join(BASE_DIR, "OP", "data_with_order_blocks.csv")
df = pd.read_csv(input_path)

# -------------------------------------------------
# Signal Logic (BUY / SELL / HOLD)
# -------------------------------------------------
df["Signal"] = 0  # 1 = Buy, -1 = Sell, 0 = Hold

for i in range(len(df)):
    # BUY
    if (
        df.loc[i, "BOS"] == 1 and
        df.loc[i, "OrderBlock"] == 1 and
        df.loc[i, "Dist_Liq_Low"] < df["Dist_Liq_Low"].quantile(0.25) and
        df.loc[i, "RSI"] < 70
    ):
        df.loc[i, "Signal"] = 1

    # SELL
    elif (
        df.loc[i, "BOS"] == -1 and
        df.loc[i, "OrderBlock"] == -1 and
        df.loc[i, "Dist_Liq_High"] < df["Dist_Liq_High"].quantile(0.25) and
        df.loc[i, "RSI"] > 30
    ):
        df.loc[i, "Signal"] = -1

# -------------------------------------------------
# Save output
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "OP", "final_trading_signals.csv")
df.to_csv(output_path, index=False)

print("Step 5 completed ✅ Trading signals generated")
print("Saved at:", output_path)
print("\nSignal distribution:")
print(df["Signal"].value_counts())

# -------------------------------------------------
# CURRENT RECOMMENDATIONS (Version 2)
# -------------------------------------------------
def get_current_recommendations(df):
    results = []

    for pair in df["pair"].unique():
        pair_df = df[df["pair"] == pair]

        # ---- SIGNAL ----
        last_signal = pair_df.iloc[-1]["Signal"]

        if last_signal == 1:
            signal = "BUY"
        elif last_signal == -1:
            signal = "SELL"
        else:
            signal = "HOLD"

        # ---- CONFIDENCE (dynamic) ----
        conditions = 0

        if pair_df.iloc[-1]["BOS"] != 0:
            conditions += 1
        if pair_df.iloc[-1]["OrderBlock"] != 0:
            conditions += 1
        if 30 < pair_df.iloc[-1]["RSI"] < 70:
            conditions += 1
        if pair_df.iloc[-1]["Dist_Liq_Low"] < pair_df["Dist_Liq_Low"].quantile(0.25):
            conditions += 1

        confidence = round(conditions / 4, 2)

        results.append({
            "pair": pair,
            "signal": signal,
            "confidence": confidence
        })

    return results
