"""
NeuroOS Step 10 - Predict deadlock risk for example allocation states.

IMPORTANT: this is a risk ESTIMATE from summary features. It does not
replace the Banker's Algorithm (core/deadlock/banker.cpp), and a low
risk value is NOT a guarantee that the state is safe.
"""

from pathlib import Path

import joblib
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
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


def features_from_state(allocation, maximum, available):
    """Turn a real Allocation / Max / Available state into the 8 model features."""
    n = len(allocation)
    m = len(available)
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    alloc_sum = sum(sum(r) for r in allocation)
    avail_sum = sum(available)
    total_sum = alloc_sum + avail_sum
    need_sum = sum(sum(r) for r in need)

    runnable = sum(
        1 for i in range(n) if all(need[i][j] <= available[j] for j in range(m))
    )
    max_need = [max(need[i][j] for i in range(n)) for j in range(m)]
    scarcity = min(available[j] / (max_need[j] + 1) for j in range(m))

    return {
        "num_processes": n,
        "num_resources": m,
        "utilization": alloc_sum / total_sum,
        "avg_need": need_sum / (n * m),
        "avg_available": avail_sum / m,
        "need_to_available_ratio": need_sum / (avail_sum + 1),
        "runnable_fraction": runnable / n,
        "scarcity": scarcity,
    }


def predict_risk(model, allocation, maximum, available):
    row = pd.DataFrame([features_from_state(allocation, maximum, available)])[FEATURES]
    return float(model.predict_proba(row)[0][1])  # probability of "unsafe"


def describe(risk):
    if risk >= 0.7:
        return "HIGH risk"
    if risk >= 0.4:
        return "MEDIUM risk"
    return "LOW risk (not a guarantee)"


EXAMPLES = [
    (
        "Textbook state from Step 9 Test 1 (Banker says SAFE)",
        [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
        [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        [3, 3, 2],
    ),
    (
        "Step 9 Test 5 (Banker says UNSAFE)",
        [[1, 0], [0, 1], [1, 1]],
        [[3, 2], [2, 3], [3, 3]],
        [0, 0],
    ),
    (
        "Lightly loaded system, lots of free resources",
        [[1, 0], [0, 1]],
        [[2, 2], [2, 2]],
        [8, 8],
    ),
]


def main():
    model = joblib.load(MODEL_PATH)

    print("=" * 56)
    print(" NeuroOS Deadlock-Risk Predictions (estimates only)")
    print("=" * 56)
    for title, alloc, maxim, avail in EXAMPLES:
        risk = predict_risk(model, alloc, maxim, avail)
        print(f"\n{title}")
        print(f"  Estimated unsafe probability: {risk:.2f}  ->  {describe(risk)}")

    print("\nNote: always confirm with the Banker's Algorithm (core/deadlock/).")


if __name__ == "__main__":
    main()