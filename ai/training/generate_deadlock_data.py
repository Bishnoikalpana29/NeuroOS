"""
NeuroOS Step 10 - Generate a synthetic deadlock-risk dataset.

Each row describes one random resource-allocation state using summary
features. The label (unsafe = 1, safe = 0) comes from running the real
Banker's safety algorithm, the same logic as core/deadlock/banker.cpp.
"""

import random
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "ai" / "data" / "deadlock_dataset.csv"

NUM_SAMPLES = 3000
SEED = 42


def is_safe(allocation, need, available):
    """Banker's safety algorithm. Returns True if a safe sequence exists."""
    n = len(allocation)
    m = len(available)
    work = list(available)
    finished = [False] * n

    progress = True
    while progress:
        progress = False
        for i in range(n):
            if not finished[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                finished[i] = True
                progress = True
    return all(finished)


def make_state(rng):
    """Create one random valid state (Max >= Allocation, resources add up)."""
    n = rng.randint(3, 8)   # processes
    m = rng.randint(2, 4)   # resource types

    total = [rng.randint(6, 15) for _ in range(m)]

    # Hand out resources at random, never exceeding the total.
    allocation = [[0] * m for _ in range(n)]
    left = list(total)
    for i in range(n):
        for j in range(m):
            give = rng.randint(0, min(left[j], 3))
            allocation[i][j] = give
            left[j] -= give
    available = left

    maximum = [
        [allocation[i][j] + rng.randint(0, 6) for j in range(m)]
        for i in range(n)
    ]
    need = [[maximum[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    return n, m, allocation, maximum, need, available, total


def build_row(n, m, allocation, maximum, need, available, total):
    """Summary features that do not depend on n or m, so one model fits all sizes."""
    total_sum = sum(total)
    alloc_sum = sum(sum(r) for r in allocation)
    need_sum = sum(sum(r) for r in need)
    avail_sum = sum(available)

    # How many processes could run right now with only the free resources?
    runnable_now = sum(
        1 for i in range(n) if all(need[i][j] <= available[j] for j in range(m))
    )
    # Tightest resource: smallest available relative to the biggest single need.
    max_need_per_resource = [max(need[i][j] for i in range(n)) for j in range(m)]
    scarcity = min(
        available[j] / (max_need_per_resource[j] + 1) for j in range(m)
    )

    return {
        "num_processes": n,
        "num_resources": m,
        "utilization": round(alloc_sum / total_sum, 3),
        "avg_need": round(need_sum / (n * m), 3),
        "avg_available": round(avail_sum / m, 3),
        "need_to_available_ratio": round(need_sum / (avail_sum + 1), 3),
        "runnable_fraction": round(runnable_now / n, 3),
        "scarcity": round(scarcity, 3),
        "unsafe": 0 if is_safe(allocation, need, available) else 1,
    }


def main():
    rng = random.Random(SEED)
    rows = [build_row(*make_state(rng)) for _ in range(NUM_SAMPLES)]
    df = pd.DataFrame(rows)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

    print(f"Saved {len(df)} rows to {DATA_PATH}")
    print("\nLabel counts (0 = safe, 1 = unsafe):")
    print(df["unsafe"].value_counts().sort_index())
    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()