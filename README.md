# NeuroOS

## AI-Driven Adaptive Operating System Resource Manager

NeuroOS is an AI-assisted Operating System resource management
platform that combines classical Operating System algorithms with
Machine Learning and Reinforcement Learning.

The goal of NeuroOS is to explore how Artificial Intelligence can
help an Operating System make adaptive decisions related to process
scheduling, memory management, and resource allocation.

---

## Project Objectives

- Simulate process management and CPU scheduling.
- Implement classical CPU scheduling algorithms.
- Develop an AI-based adaptive scheduling mechanism.
- Simulate memory management and page replacement.
- Develop predictive page replacement using AI.
- Implement Banker's Algorithm for deadlock avoidance.
- Predict potential resource contention and deadlock risks.
- Demonstrate process synchronization using semaphores.
- Demonstrate inter-process communication using pipes.
- Compare traditional OS techniques with AI-assisted techniques.

---

## Core Operating System Concepts

NeuroOS covers:

- Process Management
- CPU Scheduling
- Memory Management
- Paging
- Page Replacement
- Deadlock Avoidance
- Resource Allocation
- Process Synchronization
- Semaphores
- Readers-Writers Problem
- Inter-Process Communication
- Pipes

---

## Artificial Intelligence Components

The AI layer will provide:

- Workload Prediction
- CPU Burst Prediction
- Reinforcement Learning based Scheduling
- Predictive Page Replacement
- Deadlock-Risk Prediction

---

## Technology Stack

| Category | Technology |
|---|---|
| System Programming | C++ |
| AI / ML | Python |
| Machine Learning | Scikit-learn |
| Reinforcement Learning | Python |
| Visualization | Streamlit |
| Operating System | Linux |
| Version Control | Git & GitHub |

---

## Project Architecture

```text
                         NEUROOS
                            |
             +--------------+--------------+
             |              |              |
        PROCESS          MEMORY         RESOURCE
       MANAGEMENT       MANAGEMENT       MANAGEMENT
             |              |              |
        SCHEDULING       PAGING          BANKER
             |              |              |
             +--------------+--------------+
                            |
                       AI LAYER
                            |
             +--------------+--------------+
             |              |              |
        PREDICTION        RL          RISK ANALYSIS
             |              |              |
             +--------------+--------------+
                            |
                       DASHBOARD

 ## Project Structure

```text
NeuroOS/
│
├── core/
│   ├── process/
│   ├── scheduler/
│   ├── memory/
│   ├── deadlock/
│   └── synchronization/
│
├── ipc/
│
├── ai/
│   ├── data/
│   ├── models/
│   ├── training/
│   └── prediction/
│
├── dashboard/
│
├── tests/
│
├── results/
│
├── docs/
│
└── README.md

## Performance Evaluation

NeuroOS will evaluate system performance using:

- CPU utilization
- Average waiting time
- Average turnaround time
- Throughput
- Context switches
- Page faults
- Memory utilization
- Resource utilization
- Deadlock risk

Traditional OS algorithms will be compared with AI-assisted
approaches wherever applicable.

---

## Current Status

🚧 **Project under development**

---

## Future Scope

NeuroOS can be extended with:

- Real-time system monitoring
- Advanced reinforcement learning algorithms
- GPU resource management
- Container resource management
- Cloud workload optimization
- Intelligent energy-aware scheduling
- Real operating-system kernel integration

## Step 6 - RL Adaptive CPU Scheduler

An AI scheduler that learns which scheduling algorithm (FCFS, SJF, Round Robin or Priority) to use for a given workload.

### How it works
- **State:** a batch of processes is summarised by 3 features (average burst length, burst variability, arrival spread), each bucketed into 3 levels, giving 27 states.
- **Action:** choose one of FCFS, SJF, RR or Priority.
- **Reward:** how much better the chosen algorithm's blended score (50% average waiting time + 50% average response time) is than the average of all four algorithms.
- **Learning:** tabular Q-learning with epsilon-greedy exploration, trained for 20,000 episodes. Each episode is one random workload.

### Files
| File | Purpose |
|------|---------|
| `ai/src/rl_scheduler_env.py` | Python simulator of the four algorithms, workload generator, state and reward |
| `ai/src/rl_agent.py` | Q-learning agent |
| `ai/src/train_rl_scheduler.py` | Training and comparison script |
| `ai/src/show_policy.py` | Prints the learned policy |
| `ai/tests/test_rl_scheduler.py` | Unit tests |
| `ai/models/rl_scheduler_q_table.json` | Saved Q-table |

### Run

## Step 9 - Deadlock Management (Banker's Algorithm)

A C++ module in `core/deadlock/` that keeps the system out of deadlock.

- Stores the Allocation matrix, Max matrix and Available vector, and calculates Need = Max - Allocation.
- **Safety algorithm:** finds a safe sequence if one exists, otherwise reports an unsafe state.
- **Resource-request algorithm:** a request is denied if it exceeds the process's claim, waits if resources are not free, and is granted only if the new state stays safe.
- Rejects invalid input (wrong sizes, negative numbers, Max < Allocation).

| File | Purpose |
|------|---------|
| `core/deadlock/banker.h` | Class and result structures |
| `core/deadlock/banker.cpp` | Banker's Algorithm |
| `core/deadlock/banker_main.cpp` | Demo and test cases |
| `core/deadlock/banker_edge_tests.cpp` | Edge-case tests |

### Run
```
g++ -std=c++17 -Wall core\deadlock\banker.cpp core\deadlock\banker_main.cpp -o core\deadlock\banker.exe
core\deadlock\banker.exe
g++ -std=c++17 -Wall core\deadlock\banker.cpp core\deadlock\banker_edge_tests.cpp -o core\deadlock\banker_edge_tests.exe
core\deadlock\banker_edge_tests.exe
```

## Step 10 - AI Deadlock-Risk Prediction

A Random Forest classifier that estimates how likely a resource-allocation state is to be **unsafe**.

### How it complements Step 9
The Banker's Algorithm gives an exact answer but must scan the full matrices. The AI model gives a quick risk estimate from 8 summary features (for example utilization, fraction of runnable processes and resource scarcity). It can be used as an early warning, while the Banker's Algorithm remains the authority for actual allocation decisions.

### Honest limitations
- It is a **risk estimator**, not a replacement for the Banker's Algorithm and not a guarantee of deadlock detection.
- The dataset is **synthetic**; labels come from the Banker's safety check in Python.
- Test accuracy is about 90%, and about 10% of unsafe states were predicted as safe. A LOW risk result never guarantees safety.
- It is not integrated into the C++ module.

### Files
| File | Purpose |
|------|---------|
| `ai/training/generate_deadlock_data.py` | Creates `ai/data/deadlock_dataset.csv` |
| `ai/training/train_deadlock_model.py` | Trains and evaluates the model |
| `ai/prediction/predict_deadlock.py` | Example predictions |
| `ai/models/deadlock_risk_model.joblib` | Saved model |
| `ai/tests/test_deadlock_model.py` | Tests |

### Features and label
Features: `num_processes`, `num_resources`, `utilization`, `avg_need`, `avg_available`, `need_to_available_ratio`, `runnable_fraction`, `scarcity`. Label: `unsafe` (1 = unsafe, 0 = safe).

### Run
```
py -m pip install -r requirements.txt
py ai\training\generate_deadlock_data.py
py ai\training\train_deadlock_model.py
py ai\prediction\predict_deadlock.py
py -m pytest ai\tests\test_deadlock_model.py -v
```

### Results (600 test states)
Accuracy 0.902, unsafe recall 0.903 (373 of 413 unsafe states caught, 40 missed).
---

## Testing and Performance Evaluation

The integration and system testing results, AI model evaluation metrics, memory-management results, and known limitations are documented here:

- [Testing and Performance Report](docs/TESTING_AND_PERFORMANCE.md)

### Automated Test Results
- AI test suite: 16 tests passed.
- Memory management: FIFO and LRU test cases passed.
- Deadlock avoidance: Banker’s algorithm test cases passed.
- System monitoring and dashboard: Successfully tested.

See the testing report for detailed results and limitations.
