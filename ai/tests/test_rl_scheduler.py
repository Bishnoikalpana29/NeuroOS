import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rl_agent import QLearningAgent
from rl_scheduler_env import (
    ACTION_NAMES,
    N_ACTIONS,
    N_STATES,
    Proc,
    average_metrics,
    fcfs,
    get_state,
    sjf,
    step,
)

DEMO = [Proc(1, 0, 7, 1), Proc(2, 1, 9, 2), Proc(3, 2, 6, 3), Proc(4, 3, 5, 2)]


def test_fcfs_average_waiting_time():
    assert average_metrics(fcfs(DEMO))[1] == 9.75


def test_sjf_beats_fcfs_on_waiting_time():
    assert average_metrics(sjf(DEMO))[1] < average_metrics(fcfs(DEMO))[1]


def test_state_in_range():
    assert 0 <= get_state(DEMO) < N_STATES


def test_reward_is_a_number_for_every_action():
    for action in range(N_ACTIONS):
        reward, scores = step(DEMO, action)
        assert isinstance(reward, float)
        assert set(scores) == set(ACTION_NAMES)


def test_agent_learns_rewarded_action():
    agent = QLearningAgent(N_STATES, N_ACTIONS)
    for _ in range(50):
        agent.update(3, 2, 1.0)
    assert agent.choose_action(3, explore=False) == 2


def test_agent_save_and_load(tmp_path):
    agent = QLearningAgent(N_STATES, N_ACTIONS)
    agent.update(5, 1, 0.5)
    path = tmp_path / "q.json"
    agent.save(path)
    loaded = QLearningAgent.load(path)
    assert loaded.q[5, 1] == agent.q[5, 1]