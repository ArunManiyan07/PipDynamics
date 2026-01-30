import MetaTrader5 as mt5
import pandas as pd

def get_live_data(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M5, bars=100):
    if not mt5.initialize():
        raise RuntimeError("MT5 initialize failed")

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    mt5.shutdown()

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    return df
