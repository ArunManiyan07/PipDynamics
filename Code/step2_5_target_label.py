import os
import pandas as pd

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# INPUT (already existing file)
# -------------------------------------------------
input_path = os.path.join(
    BASE_DIR,
    "OP",
    "data_with_smc_structure.csv"
)

df = pd.read_csv(input_path)

# -------------------------------------------------
# TARGET LABEL
# -------------------------------------------------
df["target"] = 0  # HOLD

# BUY
df.loc[
    (df["BOS"] == 1) &
    (df["Close"] > df["EMA"]) &
    (df["RSI"] > 50),
    "target"
] = 1

# SELL
df.loc[
    (df["BOS"] == -1) &
    (df["Close"] < df["EMA"]) &
    (df["RSI"] < 50),
    "target"
] = -1

# -------------------------------------------------
# SAVE AS NEW FILE (TODAY STEP)
# -------------------------------------------------
output_path = os.path.join(
    BASE_DIR,
    "OP",
    "data_with_target_labels.csv"
)

df.to_csv(output_path, index=False)

print("🔥 STEP 2.5 COMPLETED")
print("✅ Target labels added")
print("📁 Saved as:", output_path)
print(df["target"].value_counts())
