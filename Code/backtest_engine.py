import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier


# ==========================================================
# CONFIG
# ==========================================================
INITIAL_BALANCE = 10000
RISK_PER_TRADE = 0.01
FORWARD_BARS = 10
FOLDS = 4
PROB_THRESHOLD = 0.60

SL_ATR_MULTIPLIER = 1.0
TP_ATR_MULTIPLIER = 1.5


# ==========================================================
# LOAD DATA
# ==========================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "OP", "data_with_target_labels.csv")


def load_dataset():
    print("📥 Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.lower()

    if "time" in df.columns:
        df = df.sort_values("time")

    df = df.reset_index(drop=True)
    print("Dataset shape:", df.shape)
    return df


# ==========================================================
# FEATURE ENGINEERING + ATR ALIGNED TARGET
# ==========================================================
def generate_features(df):

    df = df.copy()

    # === Indicators (shifted to prevent leakage) ===
    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean().shift(1)
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean().shift(1)
    df["ema_diff"] = df["ema20"] - df["ema50"]

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-9)

    df["rsi"] = (100 - (100 / (1 + rs))).shift(1)

    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)

    df["atr"] = tr.rolling(14).mean().shift(1)

    # ======================================================
    # TARGET: Will TP hit before SL within FORWARD_BARS?
    # ======================================================
    targets = []

    for i in range(len(df)):
        if i + FORWARD_BARS >= len(df):
            targets.append(np.nan)
            continue

        entry = df.iloc[i]["close"]
        atr = df.iloc[i]["atr"]

        if pd.isna(atr) or atr <= 0:
            targets.append(np.nan)
            continue

        sl = entry - (SL_ATR_MULTIPLIER * atr)
        tp = entry + (TP_ATR_MULTIPLIER * atr)

        future_data = df.iloc[i+1 : i+1+FORWARD_BARS]

        hit = 0
        for _, row in future_data.iterrows():
            if row["low"] <= sl:
                hit = 0
                break
            if row["high"] >= tp:
                hit = 1
                break

        targets.append(hit)

    df["target"] = targets

    df = df.dropna().reset_index(drop=True)

    return df


# ==========================================================
# TRADE SIMULATION
# ==========================================================
def simulate_trade(df, index, entry_price, atr):

    sl = entry_price - (SL_ATR_MULTIPLIER * atr)
    tp = entry_price + (TP_ATR_MULTIPLIER * atr)

    for j in range(index + 1, min(index + FORWARD_BARS, len(df))):

        high = df.iloc[j]["high"]
        low = df.iloc[j]["low"]

        if low <= sl:
            return -1

        if high >= tp:
            return TP_ATR_MULTIPLIER / SL_ATR_MULTIPLIER

    return 0


# ==========================================================
# WALK FORWARD VALIDATION
# ==========================================================
def walk_forward_validation(df):

    df = generate_features(df)

    feature_cols = ["ema20", "ema50", "ema_diff", "rsi", "atr"]

    fold_size = len(df) // (FOLDS + 1)
    all_returns = []

    print("\n🚀 Starting Final Profit-Focused Walk Forward Test...")

    for fold in range(1, FOLDS + 1):

        train_end = fold * fold_size
        test_end = min((fold + 1) * fold_size, len(df))

        train_df = df.iloc[:train_end]
        test_df = df.iloc[train_end:test_end].reset_index(drop=True)

        print(f"\n🔁 Fold {fold}")
        print("Train candles:", len(train_df))
        print("Test candles:", len(test_df))

        X_train = train_df[feature_cols]
        y_train = train_df["target"]

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=6,
            random_state=42
        )

        model.fit(X_train, y_train)

        balance = INITIAL_BALANCE

        for i in range(len(test_df) - FORWARD_BARS):

            row = test_df.iloc[i]
            atr = row["atr"]

            if atr <= 0:
                continue

            X_row = pd.DataFrame([row[feature_cols]])
            prob = model.predict_proba(X_row)[0][1]

            if prob < PROB_THRESHOLD:
                continue

            result = simulate_trade(test_df, i, row["close"], atr)

            if result == 0:
                continue

            pnl = balance * RISK_PER_TRADE * result
            balance += pnl

            all_returns.append(result)

    print_results(all_returns)
    monte_carlo_simulation(all_returns)


# ==========================================================
# RESULTS
# ==========================================================
def print_results(trade_returns):

    total = len(trade_returns)
    wins = sum(1 for r in trade_returns if r > 0)

    win_rate = (wins / total * 100) if total > 0 else 0
    avg_R = np.mean(trade_returns) if total > 0 else 0

    print("\n==============================")
    print(" FINAL WALK FORWARD RESULTS")
    print("==============================")
    print("Total Trades:", total)
    print("Win Rate: {:.2f}%".format(win_rate))
    print("Average R:", round(avg_R, 3))
    print("==============================\n")


# ==========================================================
# MONTE CARLO
# ==========================================================
def monte_carlo_simulation(trade_returns, simulations=1000):

    if len(trade_returns) == 0:
        print("No trades for Monte Carlo.")
        return

    final_balances = []

    for _ in range(simulations):

        shuffled = np.random.permutation(trade_returns)
        balance = INITIAL_BALANCE

        for r in shuffled:
            balance += balance * RISK_PER_TRADE * r

        final_balances.append(balance)

    print("==============================")
    print(" MONTE CARLO RESULTS")
    print("==============================")
    print("Median Final Balance:", round(np.median(final_balances), 2))
    print("Worst Final Balance:", round(np.min(final_balances), 2))
    print("==============================\n")


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    df = load_dataset()
    walk_forward_validation(df)
