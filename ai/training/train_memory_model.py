import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# Get the project directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AI_DIR = os.path.dirname(CURRENT_DIR)

DATA_PATH = os.path.join(
    AI_DIR,
    "data",
    "page_history.csv"
)

MODEL_DIR = os.path.join(
    AI_DIR,
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "memory_prediction_model.pkl"
)


def train_model():
    print("========================================")
    print(" NeuroOS AI Memory Prediction Training")
    print("========================================")

    # Check whether the dataset exists
    if not os.path.exists(DATA_PATH):
        print("ERROR: Dataset not found:", DATA_PATH)
        return

    # Load the dataset
    data = pd.read_csv(DATA_PATH)

    print("\nDataset loaded successfully.")
    print("Dataset shape:", data.shape)

    # Check the required columns
    required_columns = [
        "page_id",
        "recent_accesses",
        "time_since_last_access",
        "future_access"
    ]

    for column in required_columns:
        if column not in data.columns:
            print("ERROR: Missing column:", column)
            return

    # Select input features
    features = [
        "recent_accesses",
        "time_since_last_access"
    ]

    X = data[features]
    y = data["future_access"]

    # Check that both target classes are present
    if y.nunique() < 2:
        print("ERROR: Dataset must contain both target classes 0 and 1.")
        return

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # Create the AI model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nModel training completed.")
    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))
    print("Test accuracy: {:.2f}%".format(accuracy * 100))

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # Save the trained model
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, MODEL_PATH)

    print("Model saved successfully:")
    print(MODEL_PATH)

    print("\nAI memory prediction training finished.")


if __name__ == "__main__":
    train_model()