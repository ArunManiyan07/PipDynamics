from live_data_mt5 import get_live_data

df = get_live_data("GBPUSD")
print(df.tail())
