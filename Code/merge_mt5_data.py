import pandas as pd
import glob
import os

BASE_PATH = r"C:\Users\ARUN\Documents\PipDynamics\mt5_forex_data\M15"

files = glob.glob(os.path.join(BASE_PATH, "*.csv"))
print("Files found:", len(files))

dfs = []

for file in files:
    pair = os.path.basename(file).split("_")[0]  # EURUSD_1Y_M15.csv
    df = pd.read_csv(file)
    df["pair"] = pair
    dfs.append(df)

if not dfs:
    raise ValueError("❌ No files loaded. Check BASE_PATH or extension.")

final_df = pd.concat(dfs, ignore_index=True)
final_df.to_csv("OP/final_trading_signals.csv", index=False)

print("✅ CSV created with pairs:", final_df["pair"].nunique())
