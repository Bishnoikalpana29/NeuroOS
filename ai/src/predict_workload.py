import pandas as pd
from pathlib import Path

import joblib


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "ai" / "models" / "workload_model.joblib"


def predict_workload(arrival_time, priority, memory, io):
    """Predict the CPU burst time for a NeuroOS process."""

    model = joblib.load(MODEL_PATH)

    process_features = [[
        arrival_time,
        priority,
        memory,
        io,
    ]]

    feature_names = [
        "arrival_time",
        "priority",
        "memory",
        "io",
    ]

    process_features = pd.DataFrame(
        process_features,
        columns=feature_names,
    )

    prediction = model.predict(process_features)

    return float(prediction[0])


if __name__ == "__main__":
    # Example NeuroOS process:
    # arrival_time = 4
    # priority = 1
    # memory = 140 MB
    # io = 30
    predicted_burst = predict_workload(
        arrival_time=4,
        priority=1,
        memory=140,
        io=30,
    )

    print("========================================")
    print(" NeuroOS AI Workload Prediction")
    print("========================================")
    print("Process features:")
    print("Arrival time : 4")
    print("Priority     : 1")
    print("Memory       : 140")
    print("I/O          : 30")
    print()
    print(f"Predicted CPU burst time: {predicted_burst:.2f}")
    print("========================================")