import streamlit as st
import pandas as pd
from step5_signal_logic import get_current_recommendations
from live_data_mt5 import get_live_data
from datetime import datetime, time
import pytz
import MetaTrader5 as mt5

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="PipDynamics", layout="wide")
st.title("📈 PipDynamics – Forex Market Recommendations")

# -------------------------------------------------
# Market Status
# -------------------------------------------------
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist).time()
market_status = "🟢 OPEN" if time(5,30) <= now <= time(22,30) else "🔴 CLOSED"
st.caption(f"Market Status: **{market_status}**")

# -------------------------------------------------
# Load Past Data
# -------------------------------------------------
df = pd.read_csv("OP/final_trading_signals.csv")

# -------------------------------------------------
# Pair + Timeframe
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    selected_pair = st.selectbox("Currency Pair", df["pair"].unique())

with col2:
    tf_label = st.selectbox("Timeframe", ["M5", "M15", "H1"])

TF_MAP = {
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "H1": mt5.TIMEFRAME_H1
}
timeframe = TF_MAP[tf_label]

# -------------------------------------------------
# Recommendations (PAST + LIVE inside logic)
# -------------------------------------------------
signals = get_current_recommendations(df)
table = pd.DataFrame(signals)
row = table[table["pair"] == selected_pair].iloc[0]

# -------------------------------------------------
# LIVE PRICE (MT5)
# -------------------------------------------------
symbol = selected_pair.replace("/", "")

try:
    live_df = get_live_data(symbol, timeframe=timeframe, bars=50)

    if live_df.empty or len(live_df) < 2:
        st.warning("Live price not available")
        st.stop()

except Exception as e:
    st.error(f"MT5 Error: {e}")
    st.stop()

last_close = live_df.iloc[-1]["close"]
prev_close = live_df.iloc[-2]["close"]
arrow = "⬆️" if last_close > prev_close else "⬇️"

# -------------------------------------------------
# Strength
# -------------------------------------------------
def strength(conf):
    if conf >= 0.75:
        return "🔥 Strong"
    elif conf >= 0.50:
        return "⚠️ Medium"
    else:
        return "💤 Weak"

# -------------------------------------------------
# DISPLAY
# -------------------------------------------------
st.divider()
st.subheader(f"📌 {selected_pair} Recommendation")

c1, c2, c3 = st.columns(3)
c1.metric("Signal", row["signal"])
c2.metric("Strength", strength(row["confidence"]))
c3.metric("Live Price", f"{round(last_close,5)} {arrow}")
