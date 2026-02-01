import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz
import os

# ---------------- CONFIG ----------------
TIMEFRAME = mt5.TIMEFRAME_H1   # Change to M5 / M15 if needed
YEARS = 5
SAVE_DIR = "mt5_forex_data"

PAIRS = [
    "EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","NZDUSD",
    "EURGBP","EURJPY","GBPJPY","AUDJPY",
    "EURCHF","EURAUD","GBPAUD","EURNZD","AUDNZD"
]


# ----------------------------------------

# Create folder
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize MT5
if not mt5.initialize():
    print("❌ MT5 initialization failed")
    mt5.shutdown()
    quit()

print("✅ MT5 initialized")

timezone = pytz.timezone("UTC")
end_date = datetime.now(timezone)
start_date = end_date.replace(year=end_date.year - YEARS)

for pair in PAIRS:
    print(f"⬇️ Downloading {pair}...")

    mt5.symbol_select(pair, True)

    rates = mt5.copy_rates_range(
        pair,
        TIMEFRAME,
        start_date,
        end_date
    )

    if rates is None or len(rates) == 0:
        print(f"⚠️ No data for {pair}")
        continue

    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    file_path = f"{SAVE_DIR}/{pair}_{YEARS}Y_H1.csv"
    df.to_csv(file_path, index=False)

    print(f"✅ Saved: {file_path}")

mt5.shutdown()
print("🔥 ALL DONE")
