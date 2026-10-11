# CO1_AT1 - ShopSphere Scalability Audit

**Course:** CSA0607 - Design and Analysis of Algorithms
**Assessment:** CO1 - Assessment Tool 1 (IT Application-Based Problem Solving)
**Student:** Shaik Shahid  |  **Reg. No.:** 192424311
**Language:** Python 3 (run in VS Code)

## What this project does
ShopSphere is an online shop that will grow from 100,000 to 1,000,000 products.
This project checks five back-end modules (M1 to M5), finds out how their running
time grows, and decides which ones must be redesigned. Servers are assumed to do
10^8 basic operations per second and the nightly window is 10 minutes.

## Folder structure
```
CO1_AT1/
├── Question_1/
│   ├── Source_Code/      Python programs (one file per question part)
│   └── Report/           Report (Word and PDF) and output screenshots
└── README.md
```

## Source code files
| File | Part | What it does |
|---|---|---|
| `part_b_m1_m2_counts.py` | (b) | Counts M1 comparisons and M2 audits, checks n = 1,024 |
| `part_c_binary_search.py` | (c) | Binary search (iterative and recursive), checks log2(n) + 1 |
| `part_d_master_theorem.py` | (d) | Master Theorem cases, builds M4 and M5 recurrences |
| `part_e_search_cases.py` | (e) | Best, average, worst cases for S1 and S2 |
| `part_f_asymptotic_proof.py` | (f) | Checks 3n^2 <= f(n) <= 63n^2 and that f(n) is not O(n) |
| `part_g_scalability.py` | (g) | Time estimates at n = 100,000 and 1,000,000, M1 redesign test |
| `run_all.py` | all | Runs all six files one after another |

## How to run
1. Open `CO1_AT1/Question_1/Source_Code` in VS Code.
2. Open a terminal and run one file, for example `python part_b_m1_m2_counts.py`.
3. Or run everything with `python run_all.py`.

Only standard Python 3 is needed. No extra packages are required.

## Results at a glance (n = 1,000,000)
| Module | Complexity | Time | 10-minute window |
|---|---|---|---|
| M1 duplicate detector | Theta(n^2) | 83.3 minutes | FAILS |
| M2 rate limiter | Theta(n) (the n log n claim is wrong) | 0.010 s | OK |
| S1 sequential search | Theta(n) | 0.0075 s (average) | OK |
| S2 binary search | Theta(log n) | 0.2 microseconds | OK |
| M4 current design | Theta(n^2) | 5.6 hours | FAILS |
| M4 redesign | Theta(n log n) | 0.209 s | OK |
| M5 analytics engine | Theta(n log^2 n) | 2.1 s | OK |
| Report generator f(n) | Theta(n^2) | 8.3 hours | FAILS |

**Redesign needed:** M1 (use a hash set), M4 (use the no-replication design) and the
report generator (remove the quadratic step).

## Report
The full answers with step-by-step maths, code screenshots, output screenshots and
analysis are in `Question_1/Report/CSA0607_CO1_AT1_Report.docx` (also as PDF). The report has the code pasted as text and screenshots of the outputs in `Report/output_screenshots/`.
