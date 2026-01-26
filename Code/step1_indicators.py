import os
import pandas as pd
import numpy as np

# -------------------------------------------------
# Get PROJECT ROOT directory (PipDynamics)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load merged data (forex_4pairs.csv)
# -------------------------------------------------
data_path = os.path.join(BASE_DIR, "Code", "data", "forex_4pairs.csv")
df = pd.read_csv(data_path)

# -------------------------------------------------
# EMA (trend)
# -------------------------------------------------
df['EMA'] = df['Close'].ewm(span=20, adjust=False).mean()

# -------------------------------------------------
# RSI (momentum)
# -------------------------------------------------
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

df['RSI'] = calculate_rsi(df['Close'])

# -------------------------------------------------
# Quick check
# -------------------------------------------------
print(df[['pair', 'Close', 'EMA', 'RSI']].tail())

# -------------------------------------------------
# Save output to OP folder (GUARANTEED)
# -------------------------------------------------
output_path = os.path.join(BASE_DIR, "OP", "data_with_indicators.csv")
df.to_csv(output_path, index=False)

print("Step 1 completed ✅ Indicators added.")
print("Saved at:", output_path)
