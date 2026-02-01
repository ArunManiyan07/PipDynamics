import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

# ---------------- CONFIG ----------------
TIMEFRAME = mt5.TIMEFRAME_M15      # M15
SAVE_DIR = "mt5_forex_data/M15"

PAIRS = [
    "EURUSD","GBPUSD","USDJPY","USDCHF","USDCAD","NZDUSD",
    "EURGBP","EURJPY","GBPJPY","AUDJPY",
    "EURCHF","EURAUD","GBPAUD","EURNZD","AUDNZD"
]

# ----------------------------------------

os.makedirs(SAVE_DIR, exist_ok=True)

if not mt5.initialize():
    print("❌ MT5 initialization failed")
    mt5.shutdown()
    quit()

print("✅ MT5 initialized (M15)")

timezone = pytz.timezone("UTC")
end_date = datetime.now(timezone)

# 🔥 IMPORTANT CHANGE: only 1 year for M15
start_date = end_date - timedelta(days=365)

for pair in PAIRS:
    print(f"⬇️ Downloading {pair} (M15)...")

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
    df["time"] = pd.to_datetime(df["time"], unit="s")

    file_path = f"{SAVE_DIR}/{pair}_1Y_M15.csv"
    df.to_csv(file_path, index=False)

    print(f"✅ Saved: {file_path}")

mt5.shutdown()
print("🔥 M15 ALL DONE")
