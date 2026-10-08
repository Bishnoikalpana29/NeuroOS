from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "ai" / "data" / "workload_dataset.csv"
MODEL_PATH = PROJECT_ROOT / "ai" / "models" / "workload_model.joblib"


def load_dataset():
    """Load the NeuroOS workload dataset."""
    return pd.read_csv(DATA_PATH)


def train_model():
    """Train and evaluate the workload prediction model."""

    data = load_dataset()

    # Input features used to predict CPU burst time.
    features = [
        "arrival_time",
        "priority",
        "memory",
        "io",
    ]

    target = "burst_time"

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5
    r2 = r2_score(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("========================================")
    print(" NeuroOS AI Workload Prediction Model")
    print("========================================")
    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print()
    print("Model evaluation:")
    print(f"MAE              : {mae:.3f}")
    print(f"RMSE             : {rmse:.3f}")
    print(f"R2 Score         : {r2:.3f}")
    print()
    print(f"Model saved to   : {MODEL_PATH}")
    print("========================================")


if __name__ == "__main__":
    train_model()