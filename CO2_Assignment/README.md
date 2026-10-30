# CSA06 – Design and Analysis of Algorithms · Assignment 2 (CO2)

Brute-force and exhaustive-search techniques: sorting, sequential search, string matching, closest pair, convex hull, exhaustive search, and the Day-4 design challenge (redesign of Q6).

**Name:** Shaik Shahid · **Reg. No.:** 192424311 · **Language:** Python 3 (matplotlib for graphs)

## Repository structure
```
CO2_Assignment/
├── Q1_Sorting_Algorithms/            Selection / Bubble / Insertion under 3 designed datasets (+extras)
├── Q2_Sequential_Search/             comparison counts, operating boundary, 1 hangar -> 20 facilities
├── Q3_Brute_Force_String_Matching/   low-work, engineered high-work and realistic log test conditions
├── Q4_Brute_Force_Closest_Pair/      pair-count derivation, 7 input sizes, 1-second acceptability limit
├── Q5_Brute_Force_Convex_Hull/       hull derived from the "all points on one side" principle, visualised
├── Q6_Exhaustive_Search/             bit-mask enumeration, verified n=5 instance, growth to n=22
├── Q7_Day4_Design_Challenge/         Q6 redesign: V0 exhaustive -> V1 incremental+feasibility cut -> V2 + bound
├── Final_Report/CO2_Assignment_Report.docx
└── README.md
```
Each question folder contains `Pseudocode/` (pseudocode **and predictions written before running**), `Implementation_Code/` (script + `results/` with raw CSV/JSON and captured console output) and `Output_Screenshots/` (terminal-output images and graphs).

## How to run
```
cd Q1_Sorting_Algorithms/Implementation_Code && python q1_sorting.py
cd Q2_Sequential_Search/Implementation_Code  && python q2_sequential_search.py
cd Q3_Brute_Force_String_Matching/Implementation_Code && python q3_string_matching.py
cd Q4_Brute_Force_Closest_Pair/Implementation_Code    && python q4_closest_pair.py
cd Q5_Brute_Force_Convex_Hull/Implementation_Code     && python q5_convex_hull.py
cd Q6_Exhaustive_Search/Implementation_Code           && python q6_exhaustive_search.py
cd Q7_Day4_Design_Challenge/Implementation_Code       && python q7_design_challenge.py
```
Requirements: Python 3, `matplotlib` (Q5 also uses `numpy` once for a log-log slope). Fixed random seeds; operation counts are identical on every machine, times will differ. Q6 (n = 22) and Q4 (n = 8000) take several seconds; Q7 about a minute.

## Headline results (operation counts are the primary evidence)
| Q | Key finding |
|---|-------------|
| Q1 | n=1000, 95%-sorted data: Insertion 23,597 comparisons vs Selection 499,500 and Bubble 498,680 -> recommend Insertion Sort |
| Q2 | Comparisons = position (successful) or n (unsuccessful); boundary f·n ≈ 3.2×10⁶ at 10% CPU; hash index recommended for the 20-facility service at high request rates |
| Q3 | Same n=10⁴: 9,992 vs 13,389 vs 497,550 comparisons – structure of text/pattern, not n, decides the work |
| Q4 | Pairs = n(n−1)/2 exactly; 1-second limit reached at about 3,160 drones |
| Q5 | Edge rule: all other points on one closed side (+ segment rule for collinear points); work ≈ n^2.8 with sorted scan order, 12.7× fewer tests with shuffled order |
| Q6 | Candidates = 2ⁿ; n=20 -> 1.08 s, n=22 -> 5.1 s; deploy up to 20 packages for a 5-second limit |
| Q7 | Pruned search visits 54 nodes instead of 1,048,576 at n=20 (random instance) – but a designed worst case shows pruning can fail |

## Notes
* The `*_terminal_output*.png` images are rendered from the console output captured in `results/*_output.txt`; the graphs come directly from the scripts.
* Predictions that turned out wrong are reported as such in the report (Q4 constants, Q5 growth exponent, Q6 constants, several Q7 predictions).
