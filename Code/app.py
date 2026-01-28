import streamlit as st
import pandas as pd
from step5_signal_logic import get_current_recommendations
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="PipDynamics", layout="wide")
st.title("📈 PipDynamics – Forex Market Recommendations")

# -------------------------------------------------
# MOD 9️⃣ Auto refresh (5 minutes)
# -------------------------------------------------
st_autorefresh(interval=300000, key="auto_refresh")

# -------------------------------------------------
# MOD 5️⃣ Last updated time (IST)
# -------------------------------------------------
ist = pytz.timezone("Asia/Kolkata")
last_updated = datetime.now(ist).strftime("%d %b %Y – %I:%M %p IST")
st.caption(f"🕒 Last updated: {last_updated}")

# -------------------------------------------------
# Load data
# -------------------------------------------------
df = pd.read_csv("OP/final_trading_signals.csv")

# Get recommendations
signals = get_current_recommendations(df)

# Create table
table = pd.DataFrame(signals)

# -------------------------------------------------
# MOD 1️⃣ Signal Strength
# -------------------------------------------------
def signal_strength(conf):
    if conf >= 0.75:
        return "🔥 Strong"
    elif conf >= 0.50:
        return "⚠️ Medium"
    else:
        return "💤 Weak"

table["strength"] = table["confidence"].apply(signal_strength)

# Format confidence
table["confidence"] = table["confidence"].map(lambda x: f"{x:.2f}")

# -------------------------------------------------
# 🎨 Signal coloring
# -------------------------------------------------
def color_signal(val):
    if val == "BUY":
        return "background-color: #c6f6d5; color: black;"
    elif val == "SELL":
        return "background-color: #fed7d7; color: black;"
    else:  # HOLD
        return "background-color: #fefcbf; color: black;"

# -------------------------------------------------
# Main table display
# -------------------------------------------------
st.subheader("📊 Market Recommendations")

st.dataframe(
    table[["pair", "signal", "strength", "confidence"]]
        .style.applymap(color_signal, subset=["signal"]),
    use_container_width=True
)

# -------------------------------------------------
# MOD 8️⃣ Pair Detail View
# -------------------------------------------------
st.divider()
st.subheader("🔍 Pair Indicator Details")

selected_pair = st.selectbox(
    "Select a currency pair",
    table["pair"].unique()
)

pair_df = df[df["pair"] == selected_pair].iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("RSI", pair_df["RSI"])
col2.metric("BOS", pair_df["BOS"])
col3.metric("Order Block", pair_df["OrderBlock"])
col4.metric("Signal", pair_df["Signal"])
