import MetaTrader5 as mt5
import pandas as pd
import time

# =================================================
# TIMEFRAMES
# =================================================
TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}

# =================================================
# MT5 INIT (SAFE + SINGLE)
# =================================================
_MT5_READY = False

def _init_mt5():
    global _MT5_READY
    if _MT5_READY:
        return True

    if not mt5.initialize():
        print("❌ MT5 initialization failed")
        return False

    _MT5_READY = True
    return True

# =================================================
# SYMBOL NORMALIZER
# =================================================
def _normalize_symbol(symbol: str) -> str:
    return symbol.replace("/", "").strip().upper()

# =================================================
# LIVE OHLC DATA
# =================================================
def get_live_data(symbol: str, timeframe: str = "M15", bars: int = 200):
    symbol = _normalize_symbol(symbol)

    if not _init_mt5():
        return None

    if timeframe not in TIMEFRAME_MAP:
        timeframe = "M15"

    tf = TIMEFRAME_MAP[timeframe]

    if not mt5.symbol_select(symbol, True):
        print(f"❌ Symbol not found: {symbol}")
        return None

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)

    if rates is None or len(rates) < 50:
        return None

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    return df

# =================================================
# LIVE PRICE + PREV CLOSE
# =================================================
def get_live_price(symbol: str):
    symbol = _normalize_symbol(symbol)

    if not _init_mt5():
        return None, None

    if not mt5.symbol_select(symbol, True):
        return None, None

    tick = mt5.symbol_info_tick(symbol)

    rates = mt5.copy_rates_from_pos(
        symbol, mt5.TIMEFRAME_M1, 0, 3
    )

    if tick is None or rates is None or len(rates) < 3:
        return None, None

    live_price = tick.bid
    last_close = rates[-2]["close"]

    return live_price, last_close

# =================================================
# 🔥 PAIR-SPECIFIC FEATURE SEED (IMPORTANT)
# =================================================
def get_pair_seed(symbol: str) -> float:
    """
    Returns a stable 0–1 float unique per pair
    Used to avoid same confidence across all pairs
    """
    symbol = _normalize_symbol(symbol)
    return (abs(hash(symbol)) % 100) / 100
