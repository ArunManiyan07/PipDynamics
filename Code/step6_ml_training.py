import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------------------------------
# Project root
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------
# Load final signal data
# -------------------------------------------------
data_path = os.path.join(BASE_DIR, "OP", "final_trading_signals.csv")
df = pd.read_csv(data_path)

# -------------------------------------------------
# Feature selection
# -------------------------------------------------
features = [
    'EMA',
    'RSI',
    'BOS',
    'Dist_Liq_High',
    'Dist_Liq_Low',
    'OrderBlock'
]

X = df[features]
y = df['Signal']

# -------------------------------------------------
# Train-test split
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------------------------
# Decision Tree model
# -------------------------------------------------
model = DecisionTreeClassifier(
    max_depth=6,
    class_weight='balanced',
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------------------------------
# Evaluation
# -------------------------------------------------
y_pred = model.predict(X_test)

print("Decision Tree Results")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier

# -------------------------------------------------
# Random Forest model
# -------------------------------------------------
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    class_weight='balanced',
    random_state=42
)

rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("\nRandom Forest Results")
print(confusion_matrix(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

