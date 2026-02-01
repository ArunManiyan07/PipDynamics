import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_DIR = os.path.join(BASE_DIR, "mt5_forex_data", "M15")
OUTPUT_DIR = os.path.join(BASE_DIR, "OP", "M15")
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "m15_data_with_order_blocks.csv")

LIQ_WINDOW = 10
all_pairs = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".csv"):
        continue

    pair = file.split("_")[0]
    path = os.path.join(INPUT_DIR, file)

    df = pd.read_csv(path)
    df.columns = [c.capitalize() for c in df.columns]
    df["pair"] = pair

    # Liquidity
    df["Liquidity_High"] = df["High"].rolling(LIQ_WINDOW).max()
    df["Liquidity_Low"] = df["Low"].rolling(LIQ_WINDOW).min()

    # Order Blocks
    df["OrderBlock"] = 0
    df.loc[
        (df["Close"].shift(1) < df["Open"].shift(1)) &
        (df["Close"] > df["High"].shift(1)),
        "OrderBlock"
    ] = 1

    df.loc[
        (df["Close"].shift(1) > df["Open"].shift(1)) &
        (df["Close"] < df["Low"].shift(1)),
        "OrderBlock"
    ] = -1

    all_pairs.append(df)

final_df = pd.concat(all_pairs, ignore_index=True)
final_df.dropna(inplace=True)
final_df.to_csv(OUTPUT_PATH, index=False)

print("🔥 M15 processed data READY")
print("📁 Saved at:", OUTPUT_PATH)
