import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load ML-ready dataset (H1)
# -------------------------------------------------
data_path = os.path.join(
    BASE_DIR,
    "OP",
    "data_with_target_labels.csv"
)

df = pd.read_csv(data_path)

# -------------------------------------------------
# Feature selection (BASE MODEL)
# -------------------------------------------------
features = ["EMA", "RSI", "BOS"]

X = df[features]
y = df["target"]

# -------------------------------------------------
# Train-test split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# Decision Tree (for comparison)
# -------------------------------------------------
dt_model = DecisionTreeClassifier(
    max_depth=6,
    class_weight="balanced",
    random_state=42
)

dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)

print("🌳 Decision Tree Results")
print(confusion_matrix(y_test, y_pred_dt))
print(classification_report(y_test, y_pred_dt))

# -------------------------------------------------
# Random Forest (FINAL MODEL)
# -------------------------------------------------
rf_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    class_weight="balanced",
    random_state=42
)

rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

print("\n🌲 Random Forest Results (FINAL)")
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# -------------------------------------------------
# SAVE MODEL (IMPORTANT STEP)
# -------------------------------------------------
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(MODEL_DIR, "rf_h1_directional_model.pkl")
joblib.dump(rf_model, model_path)

print("✅ RandomForest model saved at:")
print(model_path)
