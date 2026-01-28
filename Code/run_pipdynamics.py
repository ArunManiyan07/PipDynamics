import pandas as pd
from step5_signal_logic import get_current_recommendations

df = pd.read_csv("OP/final_trading_signals.csv")

signals = get_current_recommendations(df)

for s in signals:
    print(f"{s['pair']} → {s['signal']} ({s['confidence']})")
