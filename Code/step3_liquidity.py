import os
import pandas as pd

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load SMC structure data
# -------------------------------------------------
input_path = os.path.join(BASE_DIR, "OP", "data_with_smc_structure.csv")
df = pd.read_csv(input_path)

# -------------------------------------------------
# SMC: Liquidity Zones
# -------------------------------------------------
window = 10

df['Liquidity_High'] = df['High'].rolling(window).max()
df['Liquidity_Low'] = df['Low'].rolling(window).min()

# Distance to liquidity (useful for ML)
df['Dist_Liq_High'] = df['Liquidity_High'] - df['Close']
df['Dist_Liq_Low'] = df['Close'] - df['Liquidity_Low']

# -------------------------------------------------
# Save output
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "OP", "data_with_smc_liquidity.csv")
df.to_csv(output_path, index=False)

print("Step 3 completed ✅ Liquidity zones added")
print("Saved at:", output_path)
