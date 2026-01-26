import pandas as pd
import os

print("Running from:", os.getcwd())

pairs = {
    "EURUSD": "EURUSD.csv",
    "GBPUSD": "GBPUSD.csv",
    "USDJPY": "USDJPY.csv",
    "AUDUSD": "AUDUSD.csv"
}

all_data = []

for pair, file in pairs.items():
    print("Trying to load:", file)
    df = pd.read_csv(f"data/{file}")
    df['pair'] = pair
    all_data.append(df)

merged_df = pd.concat(all_data, ignore_index=True)
merged_df.to_csv("data/forex_4pairs.csv", index=False)

print("SUCCESS ✅ forex_4pairs.csv created")
print(merged_df.head())
