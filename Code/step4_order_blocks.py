import os
import pandas as pd

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load liquidity data
# -------------------------------------------------
input_path = os.path.join(BASE_DIR, "OP", "data_with_smc_liquidity.csv")
df = pd.read_csv(input_path)

# -------------------------------------------------
# SMC: Order Blocks
# -------------------------------------------------
df['OrderBlock'] = 0

for i in range(1, len(df)):
    # Bullish Order Block
    if df.loc[i, 'BOS'] == 1 and df.loc[i-1, 'Close'] < df.loc[i-1, 'Open']:
        df.loc[i, 'OrderBlock'] = 1

    # Bearish Order Block
    elif df.loc[i, 'BOS'] == -1 and df.loc[i-1, 'Close'] > df.loc[i-1, 'Open']:
        df.loc[i, 'OrderBlock'] = -1

# -------------------------------------------------
# Save output
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "OP", "data_with_order_blocks.csv")
df.to_csv(output_path, index=False)

print("Step 4 completed ✅ Order Blocks identified")
print("Saved at:", output_path)
