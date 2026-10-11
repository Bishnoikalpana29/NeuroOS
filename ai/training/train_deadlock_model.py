"""
NeuroOS Step 10 - Train the deadlock-risk model.

Predicts whether a resource-allocation state is UNSAFE (1) or SAFE (0)
from summary features. This is a risk estimator, not a replacement for
the Banker's Algorithm in core/deadlock/.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    recall_score,
)
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "ai" / "data" / "deadlock_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ai" / "models" / "deadlock_risk_model.joblib"

FEATURES = [
    "num_processes",
    "num_resources",
    "utilization",
    "avg_need",
    "avg_available",
    "need_to_available_ratio",
    "runnable_fraction",
    "scarcity",
]
TARGET = "unsafe"


def main():
    data = pd.read_csv(DATA_PATH)
    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",  # handles the safe/unsafe imbalance
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("=" * 44)
    print(" NeuroOS AI Deadlock-Risk Model")
    print("=" * 44)
    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print(f"Accuracy         : {accuracy_score(y_test, predictions):.3f}")
    print(f"Unsafe recall    : {recall_score(y_test, predictions):.3f}")
    print("\nConfusion matrix (rows = actual, columns = predicted):")
    print("            pred safe  pred unsafe")
    cm = confusion_matrix(y_test, predictions)
    print(f"actual safe     {cm[0][0]:>5}        {cm[0][1]:>5}")
    print(f"actual unsafe   {cm[1][0]:>5}        {cm[1][1]:>5}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, target_names=["safe", "unsafe"]))

    print("Feature importance:")
    ranked = sorted(zip(FEATURES, model.feature_importances_), key=lambda x: -x[1])
    for name, score in ranked:
        print(f"  {name:<24} {score:.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()