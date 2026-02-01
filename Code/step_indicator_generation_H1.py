import os
import pandas as pd
import numpy as np

# -------------------------------------------------
# PROJECT ROOT
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "mt5_forex_data")
OUTPUT_DIR = os.path.join(BASE_DIR, "OP")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------
# FINAL 15 PAIRS
# -------------------------------------------------
PAIRS = [
    "EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","NZDUSD",
    "EURGBP","EURJPY","GBPJPY","AUDJPY",
    "EURCHF","EURAUD","GBPAUD","EURNZD","AUDNZD"
]

# -------------------------------------------------
# RSI FUNCTION (UNCHANGED LOGIC)
# -------------------------------------------------
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# -------------------------------------------------
# SMC PLACEHOLDER (REUSE YOUR LOGIC LATER)
# -------------------------------------------------
def calculate_smc(df):
    # Placeholder – integrate your existing BOS / CHoCH logic here
    df["SMC_Signal"] = 0
    return df

# -------------------------------------------------
# PROCESS ALL PAIRS
# -------------------------------------------------
all_pairs_df = []

for pair in PAIRS:
    print(f"⚙️ Processing {pair}")

    file_path = os.path.join(DATA_DIR, f"{pair}_5Y_H1.csv")

    if not os.path.exists(file_path):
        print(f"❌ File missing: {pair}")
        continue

    df = pd.read_csv(file_path)

    # Normalize column names
    df.rename(columns=str.capitalize, inplace=True)

    # Add pair column
    df["pair"] = pair

    # -------------------------------------------------
    # EMA
    # -------------------------------------------------
    df["EMA"] = df["Close"].ewm(span=20, adjust=False).mean()

    # -------------------------------------------------
    # RSI
    # -------------------------------------------------
    df["RSI"] = calculate_rsi(df["Close"])

    # -------------------------------------------------
    # SMC (reuse logic later)
    # -------------------------------------------------
    df = calculate_smc(df)

    # Drop NaNs
    df.dropna(inplace=True)

    all_pairs_df.append(df)

# -------------------------------------------------
# MERGE ALL PAIRS
# -------------------------------------------------
final_df = pd.concat(all_pairs_df, ignore_index=True)

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------
output_path = os.path.join(OUTPUT_DIR, "H1_data_with_SMC_RSI_EMA.csv")
final_df.to_csv(output_path, index=False)

print("🔥 STEP COMPLETED: Indicators added for all 15 pairs")
print("📁 Saved at:", output_path)
