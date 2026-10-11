import sys
from pathlib import Path

import joblib
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ai" / "prediction"))
sys.path.insert(0, str(ROOT / "ai" / "training"))

from generate_deadlock_data import is_safe
from predict_deadlock import MODEL_PATH, describe, predict_risk

SAFE_STATE = (
    [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    [3, 3, 2],
)
UNSAFE_STATE = (
    [[1, 0], [0, 1], [1, 1]],
    [[3, 2], [2, 3], [3, 3]],
    [0, 0],
)


def _need(alloc, maxim):
    return [[maxim[i][j] - alloc[i][j] for j in range(len(maxim[0]))]
            for i in range(len(maxim))]


def test_python_safety_check_matches_banker_cpp_results():
    a, m, av = SAFE_STATE
    assert is_safe(a, _need(a, m), av) is True
    a, m, av = UNSAFE_STATE
    assert is_safe(a, _need(a, m), av) is False


def test_model_file_exists():
    assert MODEL_PATH.exists(), "Run: py ai\\training\\train_deadlock_model.py"


def test_risk_is_a_probability():
    model = joblib.load(MODEL_PATH)
    risk = predict_risk(model, *SAFE_STATE)
    assert 0.0 <= risk <= 1.0


def test_unsafe_state_scores_higher_than_safe_state():
    model = joblib.load(MODEL_PATH)
    assert predict_risk(model, *UNSAFE_STATE) > predict_risk(model, *SAFE_STATE)


@pytest.mark.parametrize("risk,label", [(0.9, "HIGH"), (0.5, "MEDIUM"), (0.1, "LOW")])
def test_describe_levels(risk, label):
    assert label in describe(risk)