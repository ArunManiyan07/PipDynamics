import os
import pandas as pd

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load indicator output
# -------------------------------------------------
input_path = os.path.join(BASE_DIR, "OP", "data_with_indicators.csv")
df = pd.read_csv(input_path)

# -------------------------------------------------
# SMC: Market Structure & BOS
# -------------------------------------------------
df['prev_high'] = df['High'].shift(1)
df['prev_low'] = df['Low'].shift(1)

df['BOS'] = 0
df.loc[df['High'] > df['prev_high'], 'BOS'] = 1
df.loc[df['Low'] < df['prev_low'], 'BOS'] = -1

# -------------------------------------------------
# Save output
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "OP", "data_with_smc_structure.csv")
df.to_csv(output_path, index=False)

print("Step 2 completed ✅ SMC Market Structure added")
print("Saved at:", output_path)
