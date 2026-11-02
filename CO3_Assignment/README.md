# CSA06 Design and Analysis of Algorithms - Assignment 3 (CO3)

Divide and Conquer: Max/Min, Binary Search, Merge Sort, Quick Sort, Karatsuba, Strassen, Closest Pair, Median of Medians, Meet-in-the-Middle and the Day-4 Design Challenge.

* Student A: ____________________  (Reg. No. ____________)
* Student B: ____________________  (Reg. No. ____________)

## Folder guide

| Folder | Contents |
|---|---|
| Q1_MaxMin_Binary_Search | Max/Min D&C and Binary Search |
| Q2_MergeSort_QuickSort | Merge Sort vs Quick Sort (first-element pivot), balanced vs unbalanced inputs |
| Q3_Karatsuba_Multiplication | Standard vs Karatsuba, crossover experiment |
| Q4_Strassen_Matrix_Multiplication | Conventional vs Strassen, padding, NumPy experiments |
| Q5_Divide_Conquer_Closest_Pair | Brute force vs D&C closest pair |
| Q6_Advanced_Divide_Conquer | Median_of_Medians, Meet_in_the_Middle |
| Q7_Day4_Design_Challenge | Student A / B initial designs, joint final design, Maximum Subarray Sum |
| Final_Report | CO3_Assignment_Report.docx, Student_Contribution_Record.docx |

Each question folder has `Pseudocode/`, `Implementation_Code/` and `Output_Screenshots/` (terminal output images, graphs and the raw `.txt` output).

## How to run

Python 3.9 or newer. NumPy is needed for Q4 and Matplotlib only if you want to redraw the graphs.

```
pip install numpy
cd Q1_MaxMin_Binary_Search/Implementation_Code
python q1_maxmin_binary_search.py
```

Run the other programs the same way:

```
python q2_merge_quick_sort.py
python q3_karatsuba.py
python q4_strassen.py          (takes about 1 minute)
python q5_closest_pair.py
python q6a_median_of_medians.py
python q6b_meet_in_the_middle.py
python q7_max_subarray.py
```

Random data uses seed 2026, so operation counts are reproducible. Timings depend on the computer.

## Q7 note

The Day-4 problem used here is Maximum Subarray Sum. The Student A / Student B initial designs are drafts and must be replaced with each student's own original first ideas before submission.
