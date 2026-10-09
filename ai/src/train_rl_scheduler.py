"""
NeuroOS Step 6 - Train the RL adaptive scheduler and compare it
against the four fixed algorithms.
"""

import random
from pathlib import Path

import numpy as np

from rl_agent import QLearningAgent
from rl_scheduler_env import (
    ACTION_NAMES,
    N_ACTIONS,
    N_STATES,
    _score,
    evaluate_all,
    generate_workload,
    get_state,
    step,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "ai" / "models" / "rl_scheduler_q_table.json"

EPISODES = 20000
TEST_WORKLOADS = 1000
SEED = 42


def train():
    random.seed(SEED)
    np.random.seed(SEED)

    agent = QLearningAgent(N_STATES, N_ACTIONS)

    for episode in range(1, EPISODES + 1):
        workload = generate_workload()
        state = get_state(workload)
        action = agent.choose_action(state)
        reward, _ = step(workload, action)
        agent.update(state, action, reward)
        agent.decay_epsilon()

        if episode % 5000 == 0:
            print(f"Episode {episode:>6} / {EPISODES}  epsilon = {agent.epsilon:.3f}")

    agent.save(MODEL_PATH)
    print(f"\nQ-table saved to: {MODEL_PATH}\n")
    return agent


def compare(agent):
    """Test on fresh workloads the agent has never seen."""
    random.seed(SEED + 1)  # different workloads from training

    totals = {name: 0.0 for name in ACTION_NAMES}
    totals["RL Agent"] = 0.0
    totals["Best possible"] = 0.0
    choices = {name: 0 for name in ACTION_NAMES}

    for _ in range(TEST_WORKLOADS):
        workload = generate_workload()
        waits = {n: _score(*m) for n, m in evaluate_all(workload).items()}
        state = get_state(workload)
        action = agent.choose_action(state, explore=False)

        for name in ACTION_NAMES:
            totals[name] += waits[name]
        totals["RL Agent"] += waits[ACTION_NAMES[action]]
        totals["Best possible"] += min(waits.values())
        choices[ACTION_NAMES[action]] += 1

    print("=" * 44)
    print(f" Average waiting time over {TEST_WORKLOADS} unseen workloads")
    print("=" * 44)
    for name, total in sorted(totals.items(), key=lambda kv: kv[1]):
        print(f"{name:<14} {total / TEST_WORKLOADS:8.2f}")
    print("=" * 44)
    print("RL Agent algorithm choices:", choices)


if __name__ == "__main__":
    trained_agent = train()
    compare(trained_agent)