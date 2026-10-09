"""
NeuroOS Step 6 - Scheduling simulator.

Python versions of FCFS, SJF (non-preemptive), Round Robin and Priority
(non-preemptive, lower number = higher priority) that use the same
process fields as core/scheduler/scheduler.h.
"""

from dataclasses import dataclass


@dataclass
class Proc:
    pid: int
    arrival: int
    burst: int
    priority: int


def _run_nonpreemptive(procs, pick_key):
    """Generic non-preemptive scheduler. pick_key chooses among ready processes."""
    remaining = sorted(procs, key=lambda p: (p.arrival, p.pid))
    time = 0
    results = {}

    while remaining:
        ready = [p for p in remaining if p.arrival <= time]
        if not ready:
            time = min(p.arrival for p in remaining)
            continue

        p = min(ready, key=pick_key)
        remaining.remove(p)

        start = time
        time += p.burst
        completion = time
        turnaround = completion - p.arrival
        waiting = turnaround - p.burst
        response = start - p.arrival
        results[p.pid] = (turnaround, waiting, response)

    return results


def fcfs(procs):
    return _run_nonpreemptive(procs, lambda p: (p.arrival, p.pid))


def sjf(procs):
    return _run_nonpreemptive(procs, lambda p: (p.burst, p.arrival, p.pid))


def priority_scheduling(procs):
    return _run_nonpreemptive(procs, lambda p: (p.priority, p.arrival, p.pid))


def round_robin(procs, quantum=4):
    procs = sorted(procs, key=lambda p: (p.arrival, p.pid))
    remaining = {p.pid: p.burst for p in procs}
    first_start = {}
    completion = {}
    queue = []
    time = 0
    i = 0  # index of next process to arrive
    n = len(procs)

    while len(completion) < n:
        # admit everything that has arrived
        while i < n and procs[i].arrival <= time:
            queue.append(procs[i])
            i += 1

        if not queue:
            time = procs[i].arrival
            continue

        p = queue.pop(0)
        if p.pid not in first_start:
            first_start[p.pid] = time

        run = min(quantum, remaining[p.pid])
        time += run
        remaining[p.pid] -= run

        # admit processes that arrived during this slice
        while i < n and procs[i].arrival <= time:
            queue.append(procs[i])
            i += 1

        if remaining[p.pid] > 0:
            queue.append(p)
        else:
            completion[p.pid] = time

    results = {}
    for p in procs:
        turnaround = completion[p.pid] - p.arrival
        waiting = turnaround - p.burst
        response = first_start[p.pid] - p.arrival
        results[p.pid] = (turnaround, waiting, response)
    return results


def average_metrics(results):
    """results: {pid: (turnaround, waiting, response)} -> averages."""
    n = len(results)
    avg_tat = sum(r[0] for r in results.values()) / n
    avg_wt = sum(r[1] for r in results.values()) / n
    avg_rt = sum(r[2] for r in results.values()) / n
    return avg_tat, avg_wt, avg_rt


ALGORITHMS = {
    "FCFS": fcfs,
    "SJF": sjf,
    "RR": round_robin,
    "Priority": priority_scheduling,
}

import random

ACTION_NAMES = list(ALGORITHMS.keys())  # ["FCFS", "SJF", "RR", "Priority"]


def generate_workload(rng=random):
    """Create a random batch of processes with a random 'profile'."""
    n = rng.randint(4, 8)
    profile = rng.choice(["short", "long", "mixed", "bursty"])

    procs = []
    for pid in range(1, n + 1):
        if profile == "short":
            burst = rng.randint(2, 6)
        elif profile == "long":
            burst = rng.randint(10, 20)
        elif profile == "mixed":
            burst = rng.choice([rng.randint(2, 5), rng.randint(15, 25)])
        else:  # bursty: many near-simultaneous arrivals
            burst = rng.randint(3, 12)

        if profile == "bursty":
            arrival = rng.randint(0, 2)
        else:
            arrival = rng.randint(0, 15)

        procs.append(Proc(pid, arrival, burst, rng.randint(1, 5)))
    return procs


def _bucket(value, low, high):
    if value < low:
        return 0
    if value < high:
        return 1
    return 2


def get_state(procs):
    """Turn a workload into a state number from 0 to 26."""
    bursts = [p.burst for p in procs]
    mean_b = sum(bursts) / len(bursts)
    var = sum((b - mean_b) ** 2 for b in bursts) / len(bursts)
    cv = (var ** 0.5) / mean_b  # burst variability
    arrivals = [p.arrival for p in procs]
    spread = (max(arrivals) - min(arrivals)) / sum(bursts)

    a = _bucket(mean_b, 6, 12)
    b = _bucket(cv, 0.35, 0.7)
    c = _bucket(spread, 0.1, 0.4)
    return a * 9 + b * 3 + c


N_STATES = 27
N_ACTIONS = len(ACTION_NAMES)


def evaluate_all(procs, quantum=4):
    """Average waiting time AND response time of every algorithm."""
    out = {}
    for name, fn in ALGORITHMS.items():
        res = fn(procs, quantum) if name == "RR" else fn(procs)
        _, wt, rt = average_metrics(res)
        out[name] = (wt, rt)
    return out


W_WAIT = 0.5   # weight on waiting time
W_RESP = 0.5   # weight on response time


def _score(wt, rt):
    return W_WAIT * wt + W_RESP * rt


def step(procs, action):
    """Reward = how much better the chosen algorithm's blended score is than average."""
    metrics = evaluate_all(procs)
    scores = {name: _score(*m) for name, m in metrics.items()}
    baseline = sum(scores.values()) / len(scores)
    chosen = scores[ACTION_NAMES[action]]
    reward = (baseline - chosen) / (baseline + 1e-9)
    return reward, scores