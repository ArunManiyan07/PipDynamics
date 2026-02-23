import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# ==================================================
# CONFIG
# ==================================================
FORWARD_BARS = 10
ATR_MULTIPLIER = 1.0

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)


# ==================================================
# FEATURE ENGINEERING
# ==================================================
def generate_features(df):

    df = df.copy()
    df.columns = df.columns.str.lower()

    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema_diff"] = df["ema20"] - df["ema50"]

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df["rsi"] = 100 - (100 / (1 + rs))

    high_low = df["high"] - df["low"]
    high_close = abs(df["high"] - df["close"].shift())
    low_close = abs(df["low"] - df["close"].shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(14).mean()

    df = df.dropna().reset_index(drop=True)

    return df


# ==================================================
# CREATE BINARY TARGET (NO WAIT)
# ==================================================
def create_target(df):

    targets = []

    for i in range(len(df)):

        if i + FORWARD_BARS >= len(df):
            targets.append(np.nan)
            continue

        entry = df.loc[i, "close"]
        atr = df.loc[i, "atr"]

        future_slice = df.iloc[i+1 : i+1+FORWARD_BARS]

        up_move = future_slice["high"].max() - entry
        down_move = entry - future_slice["low"].min()

        if up_move > down_move:
            targets.append(1)      # BUY
        else:
            targets.append(-1)     # SELL

    df["target"] = targets
    df = df.dropna().reset_index(drop=True)

    return df


# ==================================================
# TRAIN MODEL
# ==================================================
def train_model(df):

    df = generate_features(df)
    df = create_target(df)

    features = ["ema_diff", "rsi", "atr"]

    X = df[features]
    y = df["target"]

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=14,
        min_samples_leaf=10,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X, y)

    print("\nTraining Report:")
    print(classification_report(y, model.predict(X)))

    return model, features


# ==================================================
# SAVE MODEL
# ==================================================
def save_model(model, features):

    model_path = os.path.join(MODEL_DIR, "rf_directional_model.pkl")
    feature_path = os.path.join(MODEL_DIR, "model_features.pkl")

    joblib.dump(model, model_path)
    joblib.dump(features, feature_path)

    print("✅ Binary directional model saved.")


# ==================================================
# MAIN
# ==================================================
if __name__ == "__main__":

    print("📥 Loading dataset...")
    data_path = os.path.join(BASE_DIR, "OP", "data_with_target_labels.csv")
    df = pd.read_csv(data_path)

    if "time" in df.columns:
        df = df.sort_values("time").reset_index(drop=True)

    model, features = train_model(df)
    save_model(model, features)

    print("🚀 Binary training completed.")