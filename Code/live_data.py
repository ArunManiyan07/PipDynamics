import yfinance as yf

def get_live_price(pair):
    symbol = pair.replace("/", "") + "=X"
    data = yf.download(symbol, period="1d", interval="5m")
    return data
