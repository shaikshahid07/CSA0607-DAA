# CSA0607 – Design and Analysis of Algorithms
## Assignment 4A – CO4: Algorithmic Design through Pseudocode (Greedy and Dynamic Programming)

| | |
|---|---|
| **Student name** | Shaik Shahid |
| **Registration number** | 192424311 |
| **Course code / name** | CSA0607 – Design and Analysis of Algorithms |
| **Submission date** | 18-11-2026 |
| **Repository** | https://github.com/shaikshahid07/CSA0607-DAA |

All pseudocode was designed and traced by hand first (see the report). The Python programs only *verify* the designs:
each one follows its pseudocode line by line and is cross-checked against an independent brute-force or reference method.

## Repository structure

```
CO4_Assignment_4A/
├── Source_Code/
│   ├── Task_1/   task_1.py, pseudocode.txt, output.txt, Output_Screenshots/
│   ├── Task_2/   task_2.py, pseudocode.txt, output.txt, Output_Screenshots/
│   ├── Task_3/   task_3.py, pseudocode.txt, output.txt, dp_table.png, Output_Screenshots/
│   ├── Task_4/   task_4.py, pseudocode.txt, output.txt, Output_Screenshots/
│   ├── Task_5/   task_5.py, pseudocode.txt, output.txt, graph_diagram.png, negative_graphs_diagram.png, Output_Screenshots/
│   └── Task_6/   task_6.py, pseudocode.txt, output.txt, job_timeline.png, Output_Screenshots/
├── Report/
│   ├── CO4_Assignment_4A_Report.pdf
│   └── CO4_Assignment_4A_Report.docx
└── README.md
```

## How to run

Python 3.8+ is enough; no third-party packages are needed.

```bash
cd Source_Code/Task_1 && python3 task_1.py
cd ../Task_2 && python3 task_2.py
cd ../Task_3 && python3 task_3.py
cd ../Task_4 && python3 task_4.py
cd ../Task_5 && python3 task_5.py
cd ../Task_6 && python3 task_6.py
```

Each program prints its traces and test results and ends with randomised validation (assertions fail if anything disagrees).

## Tasks and results

| Task | Topic | Technique | Key result | Time / Space |
|---|---|---|---|---|
| 1 | Repair of load-vehicle pseudocode | Greedy – fractional knapsack (value/weight ratio) | Capacity 50 → value 240 | O(n log n) / O(n) |
| 2 | Job sequencing with deadlines | Greedy – descending profit, latest free slot | Schedule C, A, D → profit 180 (190 after changing B to 70) | O(n²) / O(n) |
| 3 | 0/1 knapsack | Dynamic programming with reconstruction | Capacity 7 → value 45, items Q and R | O(nW) / O(nW) |
| 4 | WordBreak forensics | Missing DP[j] check | `catdog` with {ca, dog} fails; fixed with `DP[j] = TRUE AND …` | O(n²) pairs / O(n) |
| 5 | Dijkstra, Bellman-Ford, Floyd | Greedy → repeated relaxation → all-pairs DP | Distances from A: 0, 4, 6, 7, 10; extra negative-edge and negative-cycle graphs | O(V²), O(VE), O(V³) |
| 6 | Energy-aware job scheduling (Day-4 challenge) | Dynamic programming (weighted interval scheduling) | Jobs J2, J5, J7, J8 → value 200 | O(n log n) / O(n) |

See `Report/CO4_Assignment_4A_Report.pdf` for the full problem analysis, pseudocode, manual traces, test cases, screenshots and complexity discussion.
