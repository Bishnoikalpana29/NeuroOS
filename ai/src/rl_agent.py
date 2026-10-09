"""
NeuroOS Step 6 - Q-learning agent.

One decision per episode (pick a scheduling algorithm for a workload),
so the update is the simple bandit-style Q-learning rule:
    Q[s, a] += alpha * (reward - Q[s, a])
"""

import json
import random
from pathlib import Path

import numpy as np


class QLearningAgent:
    def __init__(self, n_states, n_actions, alpha=0.1, epsilon=1.0,
                 epsilon_min=0.05, epsilon_decay=0.999):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.q = np.zeros((n_states, n_actions))

    def choose_action(self, state, explore=True):
        """Epsilon-greedy: explore randomly, otherwise pick the best known action."""
        if explore and random.random() < self.epsilon:
            return random.randrange(self.n_actions)
        return int(np.argmax(self.q[state]))

    def update(self, state, action, reward):
        self.q[state, action] += self.alpha * (reward - self.q[state, action])

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {"q": self.q.tolist(), "n_states": self.n_states,
                "n_actions": self.n_actions}
        path.write_text(json.dumps(data))

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text())
        agent = cls(data["n_states"], data["n_actions"], epsilon=0.0)
        agent.q = np.array(data["q"])
        return agent