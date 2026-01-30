import MetaTrader5 as mt5

# Initialize MT5 connection
if not mt5.initialize():
    print("❌ MT5 initialize failed")
    mt5.shutdown()
else:
    print("✅ MT5 connected successfully")

mt5.shutdown()
