import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Code/data/EURUSD.csv")

print(df.head())
print("Rows:", len(df))

# If Date column exists
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    plt.plot(df['Date'], df['Close'])
else:
    plt.plot(df['Close'])

plt.title("EUR/USD Closing Price")
plt.xlabel("Time")
plt.ylabel("Price")
plt.grid(True)
plt.show()
