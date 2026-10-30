# CO3_AT3 – Divide-and-Conquer Engine of KartIQ (Retail Data Analytics Platform)

**Course:** CSA06 – Design and Analysis of Algorithms  |  **Student:** Shaik Shahid (192424311)

| Module | Algorithm | Pseudocode | Code | Report |
|---|---|---|---|---|
| 1 – Nightly Order Consolidation | Stable Merge Sort (+ external merge) | `Module_1_Merge_Sort/Pseudocode` | `merge_sort.py` | `Module_1_Merge_Sort_Report.docx` |
| 2 – Live Seller Leaderboard | Quick Sort, first pivot vs median-of-three | `Module_2_Quick_Sort/Pseudocode` | `quick_sort.py` | `Module_2_Quick_Sort_Report.docx` |
| 3 – Order Lookup | Binary Search, first-occurrence variant | `Module_3_Binary_Search/Pseudocode` | `binary_search.py` | `Module_3_Binary_Search_Report.docx` |
| 4 – Recommendation Scores | Strassen + hybrid | `Module_4_Strassen_Matrix_Multiplication/Pseudocode` | `strassen.py` | `Module_4_Strassen_Report.docx` |

`Final_Design_and_Analysis/` holds the combined case understanding table (part a), final design, trade-offs and declaration (part f).
Each module's `Report/output.txt` is the captured program output.

## Run
Requires Python 3.9+, `numpy` (Module 4 timing), `matplotlib`, `Pillow`, `python-docx` (only to rebuild assets/reports).
```
cd Module_1_Merge_Sort/Source_Code && python3 merge_sort.py
cd Module_2_Quick_Sort/Source_Code && python3 quick_sort.py
cd Module_3_Binary_Search/Source_Code && python3 binary_search.py
cd Module_4_Strassen_Matrix_Multiplication/Source_Code && python3 strassen.py   # about 1 minute
```
Run from inside each `Source_Code` folder (timing CSVs are written to `Supporting_Files/datasets`).

## Supporting_Files
`datasets/` sample inputs and timing results · `screenshots/` code and output images · `graphs/` plots and merge tree ·
`tools/` scripts that regenerate screenshots, graphs and reports (`make_assets.py`, `build_reports.py`) ·
`_previous_version_backup/` earlier draft of this submission (kept, not used).
