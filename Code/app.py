import streamlit as st
import pandas as pd
from step5_signal_logic import get_current_recommendations
from live_data_mt5 import get_live_data
from datetime import datetime, time
import pytz
from streamlit_autorefresh import st_autorefresh
import MetaTrader5 as mt5

st.set_page_config(page_title="PipDynamics", layout="wide")
st.title("📈 PipDynamics – Forex Market Recommendations")

st_autorefresh(interval=300000, key="auto_refresh")

# ---------------------------------------------
# Market Status
# ---------------------------------------------
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist).time()
market_status = "🟢 OPEN" if time(5,30) <= now <= time(22,30) else "🔴 CLOSED"
st.caption(f"Market Status: **{market_status}**")

# ---------------------------------------------
# Load Past Data
# ---------------------------------------------
df = pd.read_csv("OP/final_trading_signals.csv")

# ---------------------------------------------
# Pair + Timeframe
# ---------------------------------------------
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

# ---------------------------------------------
# Recommendations (PAST + LIVE)
# ---------------------------------------------
signals = get_current_recommendations(df, timeframe)
table = pd.DataFrame(signals)
row = table[table["pair"] == selected_pair].iloc[0]

# ---------------------------------------------
# LIVE PRICE
# ---------------------------------------------
symbol = selected_pair.replace("/", "")
live_df = get_live_data(symbol, timeframe=timeframe, bars=50)

last_close = live_df.iloc[-1]["close"]
prev_close = live_df.iloc[-2]["close"]
arrow = "⬆️" if last_close > prev_close else "⬇️"

# ---------------------------------------------
# Strength
# ---------------------------------------------
def strength(conf):
    if conf >= 0.75: return "🔥 Strong"
    if conf >= 0.50: return "⚠️ Medium"
    return "💤 Weak"

# ---------------------------------------------
# DISPLAY
# ---------------------------------------------
st.divider()
st.subheader(f"📌 {selected_pair} Recommendation")

c1, c2, c3 = st.columns(3)
c1.metric("Signal", row["signal"])
c2.metric("Strength", strength(row["confidence"]))
c3.metric("Live Price", f"{round(last_close,5)} {arrow}")

# streamlit run Code/app.py

