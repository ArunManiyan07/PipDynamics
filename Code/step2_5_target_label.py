import os
import pandas as pd
import numpy as np

# ==========================================================
# PATHS
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(BASE_DIR, "OP", "data_with_smc_structure.csv")
output_path = os.path.join(BASE_DIR, "OP", "data_with_target_labels.csv")

# ==========================================================
# LOAD DATA
# ==========================================================
print("📥 Loading dataset...")
df = pd.read_csv(input_path)
df.columns = df.columns.str.lower()

if "time" in df.columns:
    df = df.sort_values("time").reset_index(drop=True)

print("Dataset shape:", df.shape)

# ==========================================================
# ATR CALCULATION
# ==========================================================
high_low = df["high"] - df["low"]
high_close = abs(df["high"] - df["close"].shift())
low_close = abs(df["low"] - df["close"].shift())

true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
df["atr"] = true_range.rolling(14).mean()

# ==========================================================
# TARGET GENERATION (CLEAN DIRECTIONAL LOGIC)
# ==========================================================
print("🎯 Generating clean directional targets...")

df["target"] = 0

FORWARD_WINDOW = 20
REWARD_MULTIPLE = 2

for i in range(50, len(df) - FORWARD_WINDOW):

    price = df.loc[i, "close"]
    atr = df.loc[i, "atr"]

    if np.isnan(atr) or atr <= 0:
        continue

    buy_sl = price - atr
    buy_tp = price + REWARD_MULTIPLE * atr

    sell_sl = price + atr
    sell_tp = price - REWARD_MULTIPLE * atr

    buy_result = None
    sell_result = None

    # Simulate forward
    for j in range(i + 1, i + 1 + FORWARD_WINDOW):

        high = df.loc[j, "high"]
        low = df.loc[j, "low"]

        # BUY outcome
        if buy_result is None:
            if low <= buy_sl:
                buy_result = -1
            elif high >= buy_tp:
                buy_result = 1

        # SELL outcome
        if sell_result is None:
            if high >= sell_sl:
                sell_result = -1
            elif low <= sell_tp:
                sell_result = 1

        # If both decided, stop early
        if buy_result is not None and sell_result is not None:
            break

    # Decide label
    if buy_result == 1 and sell_result != 1:
        df.loc[i, "target"] = 1
    elif sell_result == 1 and buy_result != 1:
        df.loc[i, "target"] = -1
    else:
        df.loc[i, "target"] = 0

df = df.dropna().reset_index(drop=True)
df.to_csv(output_path, index=False)

print("✅ Clean target generation complete.")
print("Final shape:", df.shape)
