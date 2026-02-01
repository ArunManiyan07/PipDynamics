import pandas as pd
from step5_signal_logic import get_current_recommendations

# -------------------------------------------------
# Load data
# -------------------------------------------------
h1_path = "OP/data_with_order_blocks.csv"
m15_path = "OP/M15/m15_data_with_order_blocks.csv"

h1_df = pd.read_csv(h1_path)
m15_df = pd.read_csv(m15_path)

# -------------------------------------------------
# Get signals (H1 directional bias)
# -------------------------------------------------
signals = get_current_recommendations(h1_df)

# -------------------------------------------------
# Print nicely
# -------------------------------------------------
print("\n=== FINAL H1 SIGNALS (Directional Bias) ===\n")
for s in signals:
    print(
        f"{s['pair']} | "
        f"Signal: {s['signal']} | "
        f"Confidence: {s['confidence']}"
    )
