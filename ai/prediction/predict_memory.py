import os
import joblib
import pandas as pd


# Locate the trained model
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AI_DIR = os.path.dirname(CURRENT_DIR)

MODEL_PATH = os.path.join(
    AI_DIR,
    "models",
    "memory_prediction_model.pkl"
)


def predict_page_access(recent_accesses, time_since_last_access):
    """Predict whether a page will be accessed soon."""

    if not os.path.exists(MODEL_PATH):
        print("ERROR: Trained model not found.")
        print("Run ai/training/train_memory_model.py first.")
        return

    model = joblib.load(MODEL_PATH)

    input_data = pd.DataFrame(
        [[recent_accesses, time_since_last_access]],
        columns=[
            "recent_accesses",
            "time_since_last_access"
        ]
    )

    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    print("\n========== AI PAGE PREDICTION ==========")
    print("Recent accesses:", recent_accesses)
    print("Time since last access:", time_since_last_access)

    if prediction == 1:
        print("Prediction: Page is likely to be accessed soon.")
    else:
        print("Prediction: Page is unlikely to be accessed soon.")

    print(
        "Probability of future access: {:.2f}%".format(
            probabilities[list(model.classes_).index(1)] * 100
        )
    )

    print("========================================")


if __name__ == "__main__":
    # Example prediction
    predict_page_access(
        recent_accesses=8,
        time_since_last_access=1
    )

    predict_page_access(
        recent_accesses=1,
        time_since_last_access=10
    )