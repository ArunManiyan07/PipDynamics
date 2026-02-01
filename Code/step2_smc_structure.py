import os
import pandas as pd

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Input file (from Code 2 – indicator step)
# -------------------------------------------------
input_path = os.path.join(BASE_DIR, "OP", "H1_data_with_SMC_RSI_EMA.csv")

df = pd.read_csv(input_path)

# -------------------------------------------------
# SMC: Market Structure & BOS (UNCHANGED LOGIC)
# -------------------------------------------------
df['prev_high'] = df['High'].shift(1)
df['prev_low'] = df['Low'].shift(1)

df['BOS'] = 0
df.loc[df['High'] > df['prev_high'], 'BOS'] = 1
df.loc[df['Low'] < df['prev_low'], 'BOS'] = -1

# -------------------------------------------------
# Cleanup
# -------------------------------------------------
df.dropna(inplace=True)

# -------------------------------------------------
# Save final output
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "OP", "H1_final_dataset_SMC_RSI_EMA.csv")
df.to_csv(output_path, index=False)

print("🔥 FINAL STEP COMPLETED")
print("✅ EMA + RSI + SMC added for 15 pairs")
print("📁 Saved at:", output_path)
