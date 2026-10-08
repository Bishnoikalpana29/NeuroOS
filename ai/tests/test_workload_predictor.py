from pathlib import Path
import sys

import pytest


# Allow imports from ai/src
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "ai" / "src"

sys.path.insert(0, str(SRC_PATH))

from predict_workload import predict_workload


MODEL_PATH = PROJECT_ROOT / "ai" / "models" / "workload_model.joblib"


def test_model_exists():
    """The trained workload model should exist."""
    assert MODEL_PATH.exists()


def test_prediction_returns_number():
    """The workload predictor should return a numeric prediction."""

    prediction = predict_workload(
        arrival_time=4,
        priority=1,
        memory=140,
        io=30,
    )

    assert isinstance(prediction, float)


def test_prediction_is_reasonable():
    """The predicted CPU burst should be within a reasonable range."""

    prediction = predict_workload(
        arrival_time=4,
        priority=1,
        memory=140,
        io=30,
    )

    assert 0 <= prediction <= 20