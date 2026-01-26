# ------------------------------
# PipDynamics Day 1: Forex Data Collection & Basic Plot
# ------------------------------

# Step 1: Import libraries
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Download USD/EUR historical data (last 1 year)
data = yf.download("EURUSD=X", start="2024-01-01", end="2025-12-30")

# Step 3: Save data to CSV (easy for future use)
data.to_csv("EURUSD.csv")
print("CSV saved successfully! Here's first 5 rows:")
print(data.head())

# Step 4: Basic plot of closing price
plt.figure(figsize=(12,6))
plt.plot(data['Close'], color='blue', label='Close Price')
plt.title("USD/EUR Closing Price Trend")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()
