# CO1 Assignment - Efficient Search Strategy for a Large-Scale Student Record System

**Name:** Shaik Shahid  **Reg. No.:** 192424311
**Course:** CSA0607 - Design and Analysis of Algorithms  (Department of Computer Science and Engineering)
**Assignment:** Assignment 1 - CO1 (50 marks)

## Project overview
A university database holds up to 1,000,000+ student records identified by unique 9-digit registration numbers. This project designs, analyses, implements and compares three different strategies for locating a registration number, and re-evaluates the design for a workload of 50,000 searches per hour with daily record updates.

## Algorithms implemented
| Approach | Strategy | Form | Preprocessing | Search (worst / average) |
|---|---|---|---|---|
| Linear search | Brute force | Iterative | none | Theta(n) / Theta(n) |
| Binary search | Decrease and conquer | Recursive (iterative variant for comparison only) | sort, Theta(n log n) | Theta(log n) / Theta(log n) |
| Hash table (chaining) | Transform and conquer | Iterative | build, Theta(n) | O(n) / Theta(1) expected |

## Main results (measured, n = 1,000,000)
| Measure | Linear | Binary (recursive) | Hash |
|---|---|---|---|
| Average search time | 20.6 ms | 2.82 us | 0.12 us |
| Average comparisons | 530,497.1 | 19.4 | 1.1 |
| Preprocessing | none | 0.3210 s | 0.9690 s |

Recommendation for the original scenario: binary search on a sorted array (Task 11). Day-4 decision: redesign to a hash table index built once per day (Task 12).

## How to run
Requirements: Python 3.9+ (tested with 3.13), `matplotlib`, `numpy`.

```bash
cd Task_8_Implementation_Testing/Source_Code
pip install matplotlib numpy
python3 run_experiments.py     # correctness tests + experiments -> results.csv / results.json
python3 make_figures.py        # graphs, flowcharts, rendered code/output images
```
`run_experiments.py` uses a fixed random seed, so the datasets are identical on every run. Running time is about a minute (linear search dominates). Times vary by machine; comparison counts do not.

## Repository structure
```
CO1_Assignment
|-- Task_1_Algorithm_Design/            design, pseudocode, flowcharts
|-- Task_2_Basic_Operation/
|-- Task_3_Mathematical_Complexity/
|-- Task_4_Case_Analysis/
|-- Task_5_Asymptotic_Analysis/
|-- Task_6_Recurrence_Formulation/
|-- Task_7_Recurrence_Solution/
|-- Task_8_Implementation_Testing/
|   `-- Source_Code/                    search_algorithms.py, run_experiments.py, make_figures.py, results.csv/json
|-- Task_9_Experimental_Performance/    tables and raw data
|-- Task_10_Theory_vs_Experiment/
|-- Task_11_Final_Recommendation/
|-- Task_12_Design_Challenge/
|-- Report/
|   |-- Source_Code_Screenshots/        rendered images of the source files
|   |-- Output_Screenshots/             rendered image and text of the console output
|   |-- Analysis/                       combined analysis (Markdown)
|   |-- Tables_and_Graphs/              performance graphs
|   `-- Documentation/                  full report (Word and PDF)
`-- README.md
```
Each task folder contains a Markdown file with the analysis for that task.

## Note on screenshots
The images in `Source_Code_Screenshots` and `Output_Screenshots` are rendered from the actual source files and the actual console output; they are not captures of a physical screen.
