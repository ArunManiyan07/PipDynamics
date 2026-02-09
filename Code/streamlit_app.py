import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
import pytz
import requests

# =================================================
# FASTAPI CONFIG
# =================================================
API_BASE = "http://127.0.0.1:8000"

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="PipDynamics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =================================================
# LOAD CSS
# =================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "styles.css"), "r", encoding="utf-8") as f:
    CSS = f.read()

# =================================================
# PAIRS
# =================================================
PAIRS = [
    "EURUSD", "GBPUSD", "USDJPY",
    "USDCHF", "USDCAD", "AUDUSD", "NZDUSD",
    "EURGBP", "EURJPY", "EURCHF", "EURCAD",
    "EURAUD", "EURNZD", "GBPJPY", "GBPCAD",
    "GBPAUD", "AUDJPY", "AUDNZD"
]

# =================================================
# MARKET STATUS
# =================================================
def is_market_open():
    now_utc = datetime.utcnow()
    wd = now_utc.weekday()
    hr = now_utc.hour
    if wd == 5:
        return False
    if wd == 6 and hr < 21:
        return False
    return True

MARKET_OPEN = is_market_open()

# =================================================
# HEADER
# =================================================
market_text = (
    "🟢 Market Open • Live data enabled"
    if MARKET_OPEN
    else "⚪ Market Closed • Last known price"
)

components.html(f"""
<html>
<head><style>{CSS}</style></head>
<body>
<div class="header">
  <h1>📈 PipDynamics</h1>
  <p>AI-powered Forex Market Recommendations</p>
</div>
<div class="market-open"><b>{market_text}</b></div>
</body>
</html>
""", height=160)

# =================================================
# SESSION STATE (PAIR + TIMEFRAME MEMORY)
# =================================================
if "pair_results" not in st.session_state:
    st.session_state.pair_results = {}

# =================================================
# USER INPUT
# =================================================
col1, col2 = st.columns(2)

with col1:
    pair = st.selectbox("Currency Pair", PAIRS)

with col2:
    timeframe = st.selectbox("Timeframe", ["M15", "H1"])

cache_key = f"{pair}_{timeframe}"

# =================================================
# GET RECOMMENDATION (FROM FASTAPI)
# =================================================
if cache_key not in st.session_state.pair_results:
    try:
        res = requests.get(
            f"{API_BASE}/recommend",
            params={"pair": pair, "timeframe": timeframe},
            timeout=5
        )
        st.session_state.pair_results[cache_key] = res.json()
    except Exception:
        st.error("⚠️ Backend not responding (FastAPI)")
        st.stop()

result = st.session_state.pair_results[cache_key]

signal = result.get("signal", "WAIT")
confidence = float(result.get("confidence", 0))
reason = result.get("reason", "")

# =================================================
# STATUS LABEL
# =================================================
def strength_label(conf, sig):
    if sig in ["BUY", "SELL"] and conf >= 80:
        return "Strong"
    if sig == "WAIT":
        return "Forming"
    if sig == "NO TRADE":
        return "Unclear"
    return "Weak"

# =================================================
# LIVE PRICE (FROM FASTAPI)
# =================================================
try:
    price_res = requests.get(
        f"{API_BASE}/price",
        params={"pair": pair},
        timeout=5
    ).json()

    live_price = price_res.get("live_price")
    last_close = price_res.get("last_close")
except Exception:
    live_price = None
    last_close = None

price_change = None
if live_price and last_close:
    price_change = ((live_price - last_close) / last_close) * 100

price_display = f"{live_price:.5f}" if live_price else "--.--"

if price_change is not None:
    arrow = "▲" if price_change >= 0 else "▼"
    change_color = "#22c55e" if price_change >= 0 else "#ef4444"
    change_display = f"{arrow} {abs(price_change):.2f}%"
else:
    change_color = "#94a3b8"
    change_display = "--"

price_status = "🟢 Live Price" if MARKET_OPEN else "⚪ Market Closed"
price_class = "" if MARKET_OPEN else "closed"

# =================================================
# TIME
# =================================================
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist).strftime("%A | %d %b %Y | %I:%M:%S %p")

# =================================================
# MAIN UI (UNCHANGED)
# =================================================
components.html(f"""
<html>
<head><style>{CSS}</style></head>
<body>

<div class="main-grid">

  <div class="signal-card">
    <div class="signal-text {signal.lower()}">{signal}</div>

    <div class="signal-meta">
      Status: <b>{strength_label(confidence, signal)}</b>
    </div>

    <div class="confidence-bar">
      <div class="confidence-fill" style="width:{confidence}%"></div>
    </div>

    <div class="confidence-text">
      Model Conviction: <b>{int(confidence)}%</b>
    </div>

    <div class="signal-reason">
      {reason if reason else "Based on structure, momentum & volatility"}
    </div>
  </div>

  <div class="price-card {price_class}">
    <div class="price-pair">{pair}</div>
    <div class="price-value">{price_display}</div>
    <div class="price-change" style="color:{change_color}">
      {change_display}
    </div>
    <div class="price-status">{price_status}</div>
  </div>

</div>

<div class="timestamp">{now}</div>

</body>
</html>
""", height=560, scrolling=False)

