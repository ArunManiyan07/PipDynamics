import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Code/data/forex_4pairs.csv")
df['Date'] = pd.to_datetime(df['Date'])

plt.figure(figsize=(12,6))

for pair in df['pair'].unique():
    pair_df = df[df['pair'] == pair].copy()
    
    # Normalize prices
    pair_df['Close_norm'] = pair_df['Close'] / pair_df['Close'].iloc[0]
    
    plt.plot(pair_df['Date'], pair_df['Close_norm'], label=pair)

plt.title("Normalized Forex Closing Prices (Multi-Pair)")
plt.xlabel("Date")
plt.ylabel("Normalized Price")
plt.legend()
plt.grid(True)
plt.show()
