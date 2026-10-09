from pathlib import Path

from rl_agent import QLearningAgent
from rl_scheduler_env import ACTION_NAMES

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "ai" / "models" / "rl_scheduler_q_table.json"

agent = QLearningAgent.load(MODEL_PATH)

print("State  Best action   (states never visited are skipped)")
for state in range(agent.n_states):
    if agent.q[state].any():
        best = ACTION_NAMES[int(agent.q[state].argmax())]
        print(f"{state:>5}  {best}")