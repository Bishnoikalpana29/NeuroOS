# NeuroOS — Integration and System Testing Report

## 1. Project
NeuroOS — AI-Driven Adaptive Operating System Resource Manager.

## 2. Test Summary
- AI automated tests: 16 passed, 0 failed.
- Memory management: FIFO and LRU test cases passed.
- Deadlock avoidance: Safe sequence, resource requests, unsafe-state detection, and invalid allocation checks passed.
- Process management: Process table displayed successfully.
- CPU scheduling: FCFS, SJF, Priority, and Round Robin executed.
- Synchronization: Shared counter reached 400000; producer-consumer test completed.
- System monitoring: Five measurements were collected and written to CSV.
- Dashboard: Streamlit dashboard rendered system metrics and charts.
- Workload prediction: Model trained and a sample prediction completed.
- Deadlock risk prediction: Model trained and risk prediction tests passed.

## 3. AI Model Evaluation

### Workload Prediction
- Training samples: 40
- Testing samples: 10
- MAE: 0.350
- RMSE: 0.435
- R-squared: 0.987

These metrics were obtained using the project's small dataset and should not be treated as proof of real-world predictive accuracy.

### Deadlock Risk Prediction
- Training samples: 2400
- Testing samples: 600
- Accuracy: 0.902
- Unsafe-state recall: 0.903
- Confusion matrix:
  - Actual safe: 168 predicted safe, 19 predicted unsafe
  - Actual unsafe: 40 predicted safe, 373 predicted unsafe

These results use generated data. Evaluation on representative real-world workloads is still required.

## 4. Memory Management Results
For the reference sequence 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2 with three frames:
- FIFO: 10 page faults, 3 hits.
- LRU: 9 page faults, 4 hits.

Additional tests for one frame, repeated page references, and an empty reference sequence produced the expected results.

## 5. CPU Scheduling Results
The scheduler executable completed and reported the following averages:

| Algorithm | Average Turnaround | Average Waiting | Average Response |
|---|---:|---:|---:|
| FCFS | 10.75 | 7.00 | 7.00 |
| SJF | 9.25 | 5.50 | 5.50 |
| Priority | 10.50 | 6.75 | 6.75 |
| Round Robin | 8.75 | 5.00 | 2.00 |

The Round Robin Gantt chart requires additional correctness review, including adjacent intervals for the same process. These execution results are not a complete proof of scheduler correctness.

## 6. Monitoring Sample
A sample of five measurements was collected successfully. During that sample:
- CPU utilization varied from 0.00% to 69.23%.
- Memory utilization was approximately 84% to 85%.
- The reported process count varied from 335 to 338.

These values describe the test machine during that run and are not fixed performance benchmarks.

## 7. Automated AI Tests
Command:
python -m pytest .\ai\tests -v

Result:
16 passed in 4.99 seconds.

The suite covered workload prediction, deadlock risk prediction, and reinforcement-learning scheduler tests.

## 8. Known Limitations
- AI model evaluation currently relies on small or generated datasets.
- The workload prediction model has not been verified as integrated with the C++ CPU scheduler.
- The AI memory prediction model has not been verified as integrated with the C++ page-replacement decisions.
- Component tests do not establish that all modules operate together as one fully integrated operating system.
- Round Robin scheduling output needs further correctness validation.
- Monitoring measurements depend on the host machine and test conditions.

## 9. Conclusion
The tested components compiled or executed successfully, the dashboard rendered, and all 16 AI tests passed. Further integration, scheduler validation, and evaluation with representative workloads are required before making claims about real-world performance.
