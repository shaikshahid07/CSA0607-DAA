# CO5 Assignment 5 - Search, Complexity and Approximation Engineering

| | |
|---|---|
| Name | Shaik Shahid |
| Register No. | 192424311 |
| Course | CSA0607 - Design and Analysis of Algorithms |
| Assignment | Assignment 5 - CO5 (Individual, 50 marks) |
| Submission date | 23-11-2026 |

## Contents

```
CO5_Assignment_5/
|-- Source_Code/
|   |-- Task_B1_Graph_Colouring/          graph_colouring.py, run_b1.py, outputs/
|   |-- Task_B2_Adversarial_Search/       adversarial_search.py, graph_colouring.py, outputs/
|   |-- Task_B3_Exact_vs_Approximation/   set_cover.py, outputs/
|   `-- Task_B4_Bin_Packing/              bin_packing.py, outputs/
|-- Report/ (report .pdf, .docx and figures/)
|   |-- CO5_Assignment_5_Report.pdf
|   `-- CO5_Assignment_5_Report.docx
`-- README.md
```

Each `outputs/` folder holds the saved program output (`.txt`) and the terminal screenshots (`screenshots/*.png`) used in the report.

## Report

`Report/CO5_Assignment_5_Report.pdf` covers all nine tasks:

- **Part A (pseudocode and analysis):** A1 graph colouring model, state, pruning, pseudocode and trace; A2 subset-sum redesign and pruning; A3 backtracking pattern and generic framework; A4 P / NP / NP-Complete / NP-Hard classification; A5 set cover and greedy approximation.
- **Part B (implementation and investigation):** B1 instrumented graph colouring with two search orders; B2 adversarial instances; B3 exact vs greedy set cover; B4 bin packing with a decision note.

## How to run

Python 3 is required. Only the standard library is used.

```
cd Source_Code/Task_B1_Graph_Colouring        && python3 run_b1.py
cd Source_Code/Task_B2_Adversarial_Search     && python3 adversarial_search.py
cd Source_Code/Task_B3_Exact_vs_Approximation && python3 set_cover.py
cd Source_Code/Task_B4_Bin_Packing            && python3 bin_packing.py
```

Task B3 takes a few seconds because the exact search on the larger instances examines millions of combinations. Random instances use fixed seeds, so the counts are the same on every run (only the millisecond timings vary slightly).

## Tasks and programs

| Task | Program | What it does |
|---|---|---|
| B1 | `graph_colouring.py`, `run_b1.py` | Backtracking graph colouring recording nodes, attempts, rejections, backtracks and depth; 12 validation tests; input order vs most-constrained-first order on 7 graphs |
| B2 | `adversarial_search.py` | Two 14-vertex graphs with m = 3: one needs 15 search nodes, the other 26,110; growth experiment for n = 8 to 18 |
| B3 | `set_cover.py` | Exact set cover (combinations by increasing size) vs greedy; 3 small cases, a counterexample, scalability table |
| B4 | `bin_packing.py` | First Fit Decreasing bin packing with allocation output, a challenging input checked against an exact search, and a scale test |
