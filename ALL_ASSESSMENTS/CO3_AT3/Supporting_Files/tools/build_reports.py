"""Builds the five Word reports. Run from anywhere:  python3 Supporting_Files/tools/build_reports.py"""
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from report_lib import *  # noqa
from report_lib import math as eq  # formula line helper
import math  # restore the stdlib module name

DATA = os.path.join(ROOT, "Supporting_Files", "datasets")
HDR = f"CSA06 CO3 Case Study  |  {STUDENT} ({REG})"


def csvrows(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def save(d, rel):
    p = os.path.join(ROOT, rel)
    d.save(p)
    print("saved", rel)


# ======================================================================= PART (a) rows
CASE_ROWS = {
    1: ["Module 1 – Nightly Order Consolidation",
        "Sort about 10,000,000 orders per night by timestamp for the audit report, before the reporting deadline.",
        "(i) Stability: orders of the same second from different gateways must keep arrival order.\n"
        "(ii) Guaranteed running time: the report must finish every night, so the worst case matters.\n"
        "(iii) Memory: out-of-place merging needs an extra buffer of the same size as the data.\n"
        "(iv) The data may be larger than RAM.",
        "An unstable sort (e.g. plain Quick Sort or Heap Sort) breaks gateway-by-gateway reconciliation and fails the audit; "
        "an O(n²) sort needs about 5×10¹³ comparisons and misses the deadline."],
    2: ["Module 2 – Live Seller Leaderboard",
        "Re-sort the scores of 100,000 sellers every few seconds; data is almost always nearly sorted.",
        "(i) Worst-case behaviour: first-element pivot on sorted / nearly sorted data gives splits of 0 and n−1.\n"
        "(ii) Recursion depth up to n (stack overflow risk).\n"
        "(iii) Stability is not required, memory should stay small (in-place).\n"
        "(iv) Nearly sorted input is the normal case, not a rare one.",
        "T(n) = Θ(n²): about 5×10⁹ comparisons per refresh instead of about 1.7×10⁶; the leaderboard freezes during sales."],
    3: ["Module 3 – Order Lookup",
        "Find an order by timestamp in the consolidated list of 10,000,000 orders; return the first of several equal timestamps.",
        "(i) Sorted-data precondition: binary search is valid only on the sorted output of Module 1.\n"
        "(ii) Duplicates: the standard search returns any match, not the first.\n"
        "(iii) Static array, no extra memory needed; mid computation must not overflow.",
        "A linear scan costs up to 10,000,000 comparisons per lookup (seconds under load); searching unsorted data with binary search "
        "returns wrong answers."],
    4: ["Module 4 – Recommendation Scores",
        "Compute C = A × B for n × n matrices with n = 1,024 so that scores can be refreshed more than once a day.",
        "(i) Matrix size: n³ = 1,073,741,824 scalar multiplications for the conventional method.\n"
        "(ii) Memory: 8 MiB per float64 matrix; Strassen needs about 3n² extra elements.\n"
        "(iii) Strassen reduces multiplications but increases additions, overhead and rounding error.\n"
        "(iv) n must be a power of two (pad otherwise).",
        "The conventional method keeps recommendations at one refresh a day; naive full-depth Strassen "
        "may be slower in practice because of overhead."],
}

CASE_HEAD = ["Module", "Computational requirement", "Key issues", "Consequence of a poor algorithm"]
CASE_W = [1.1, 1.5, 2.3, 1.5]


def case_table(d, mods):
    table(d, [CASE_HEAD] + [CASE_ROWS[m] for m in mods], widths=CASE_W, size=9, bold_first_col=True, keep=(len(mods) == 1))


# ======================================================================= MODULE 1
def module1():
    d = new_doc(HDR)
    title_block(d, "Module 1 – Merge Sort for Nightly Order Consolidation",
                "KartIQ Retail Data Analytics Platform | Parts (a) and (b)")
    h(d, "1. Case Understanding (Part a)")
    case_table(d, [1])
    para(d, "Decision: use Merge Sort. It is the standard stable O(n log n) comparison sort with a guaranteed worst case, "
            "and it extends naturally to external (disk-based) sorting.")

    h(d, "2. Divide, Conquer and Combine (Part b)")
    bullets(d, [("Divide: ", "split A[lo..hi] at mid = ⌊(lo+hi)/2⌋ into two halves of almost equal size (no comparisons)."),
                ("Conquer: ", "sort both halves recursively; a sub-array of size 0 or 1 is already sorted (base case)."),
                ("Combine: ", "merge the two sorted halves with two pointers. When the timestamps are equal the element of the "
                              "LEFT half is taken first (“<=”), which preserves arrival order.")])
    para(d, "Pseudocode (file Pseudocode/merge_sort_pseudocode.txt):", after=2).paragraph_format.keep_with_next = True
    txt = read_text("Module_1_Merge_Sort/Pseudocode/merge_sort_pseudocode.txt")
    code(d, txt.split("ALGORITHM ExternalMergeSort")[0].split("ALGORITHM MergeSort", 1)[0].strip() + "\n\n" +
         "ALGORITHM MergeSort" + txt.split("ALGORITHM MergeSort", 1)[1].split("Recurrence :")[0].rstrip(), size=8.2)

    h(d, "3. Execution Trace on the Sample Orders")
    para(d, "Input (arrival order): (105,O1), (102,O2), (105,O3), (101,O4), (102,O5), (103,O6).")
    graph(d, "m1_merge_tree.png", "Figure 1. Divide tree and the five merges for the sample orders.", 6.3)
    table(d, [["Merge", "Left run", "Right run", "Result", "Comparisons"],
              ["M1", "(105,O1)", "(102,O2)", "(102,O2), (105,O1)", "1"],
              ["M2", "(102,O2), (105,O1)", "(105,O3)", "(102,O2), (105,O1), (105,O3)", "2"],
              ["M3", "(101,O4)", "(102,O5)", "(101,O4), (102,O5)", "1"],
              ["M4", "(101,O4), (102,O5)", "(103,O6)", "(101,O4), (102,O5), (103,O6)", "2"],
              ["M5", "(102,O2), (105,O1), (105,O3)", "(101,O4), (102,O5), (103,O6)",
               "(101,O4), (102,O2), (102,O5), (103,O6), (105,O1), (105,O3)", "4"],
              ["", "", "", "Total comparisons", "10"]],
          widths=[0.6, 1.55, 1.55, 2.0, 0.9], size=9, align_center_cols=(0, 4))
    para(d, "Stability proof on the sample. ", bold_prefix=None)
    d.paragraphs[-1].runs[0].font.bold = True
    bullets(d, ["Timestamp 105: O1 arrived before O3. In M2 the comparison is 105 (left, O1) <= 105 (right, O3), so O1 is copied first. "
                "In M5 the two 105-orders are the last elements of the left run and are copied in the same order: O1, O3.",
                "Timestamp 102: O2 (left run) and O5 (right run) are compared in M5 as 102 <= 102, so O2 goes first: O2, O5.",
                "Hence every group of equal timestamps appears in arrival order (the program checks this automatically, see Figure 3)."])

    h(d, "4. Recurrence and Complexity")
    para(d, "Dividing costs O(1), merging n elements costs at most n − 1 comparisons, so")
    eq(d, "T(n) = 2 T(n/2) + (n − 1),   T(1) = 0")
    para(d, "Expansion for n = 2ᵏ: T(n) = 2T(n/2) + n − 1 = 4T(n/4) + (n − 2) + (n − 1) = … = 2ᵏT(1) + k·n − (2ᵏ − 1). Therefore")
    eq(d, "T(n) = n lg n − n + 1  =  Θ(n log n)")
    para(d, "Master Theorem check: a = 2, b = 2, f(n) = Θ(n) = Θ(n^(log₂ 2)), case 2, so T(n) = Θ(n log n). "
            "Merge Sort has the same bound in the best, average and worst case; only the constant changes "
            "(best case about (n/2) lg n comparisons when the input is already sorted).")
    table(d, [["n (measured, random data)", "Measured comparisons", "n lg n − n + 1 (upper bound)"]] +
          [[f"{n:,}", f"{c:,}", f"{n * int(math.log2(n)) - n + 1:,}"]
           for n, c in ((8, 15), (32, 122), (128, 739), (512, 3970), (2048, 19967), (8192, 96113))],
          widths=[2.2, 2.0, 2.4], size=9.5, align_center_cols=(0, 1, 2))

    h(d, "5. Estimate for 10,000,000 Orders")
    n = 10_000_000
    table(d, [["Quantity", "Calculation", "Value"],
              ["log₂ n", "log₂(10⁷) = 7 × 3.3219", "23.2535 (⌈lg n⌉ = 24)"],
              ["Comparisons ≈ n lg n", "10⁷ × 23.2535", f"{n * math.log2(n):,.0f} ≈ 2.33 × 10⁸"],
              ["Worst case n⌈lg n⌉ − 2^⌈lg n⌉ + 1", "10⁷×24 − 16,777,216 + 1", "223,222,785"],
              ["Best case ≈ (n/2) lg n", "sorted input", f"{n * math.log2(n) / 2:,.0f}"],
              ["Quadratic sort for comparison", "n(n−1)/2", "≈ 5 × 10¹³"],
              ["Memory (16 B/record)", "data 160 MB + auxiliary buffer 160 MB", "≈ 320 MB"]],
          widths=[2.2, 2.4, 2.0], size=9.5)
    para(d, "Assumption: a record is a timestamp (8 bytes) plus an order ID (8 bytes) = 16 bytes; real objects with strings are larger, "
            "which is another reason to sort compact keys or indexes. At an illustrative 10⁸ comparisons per second the 2.2×10⁸ "
            "comparisons need roughly 2–3 seconds of comparison work, against about 6 days for 5×10¹³ comparisons.")

    h(d, "6. Memory and Data That Does Not Fit in RAM")
    bullets(d, [("Memory: ", "Merge Sort is not in place; the merge needs an auxiliary array of n records, so space is O(n) "
                             "(allocate it once and reuse it at every level, not a new array per merge)."),
                ("External merge sort: ", "(1) read chunks that fit in RAM (e.g. 1,000,000 orders), sort each with Merge Sort and write it "
                                          "to disk as a sorted run → 10 runs; (2) k-way merge the 10 runs with a min-heap keyed by "
                                          "(timestamp, run index). The run index is the tie-breaker, so stability is preserved across runs."),
                ("Cost: ", "two sequential passes over 160 MB (read + write each), and n lg k = 10⁷ × lg 10 ≈ 33,219,281 comparisons in the merge pass."),
                ("Other options: ", "the gateways already deliver time-ordered streams, so a k-way merge of the gateway streams "
                                    "(or Timsort-style natural runs) avoids most of the sorting work.")])

    h(d, "7. Implementation Screenshots")
    shot(d, "m1_code_merge_sort.png", "Figure 2. Source code: merge() and merge_sort() (Source_Code/merge_sort.py).")
    shot(d, "m1_output_trace.png", "Figure 3. Program output: divide/merge trace and stability check.")
    shot(d, "m1_output_analysis.png", "Figure 4. Program output: estimates, recurrence check and external merge demonstration.")

    h(d, "8. Experimental Results")
    graph(d, "m1_merge_sort_graph.png", "Figure 5. Measured comparisons and running time of Merge Sort versus n.")
    para(d, "The measured comparisons stay just below n lg n − n + 1 and the running time follows c·n lg n, confirming the recurrence. "
            "(Timings are from pure Python on the submission machine; only the growth rate matters.)")

    h(d, "9. Limitations, Trade-offs and Recommendation")
    bullets(d, ["Trade-off: guaranteed O(n log n) and stability are paid for with O(n) extra memory and more data movement than Quick Sort.",
                "Limitation: sorting 10⁷ Python objects needs far more than 320 MB; use compact arrays, or sort a key/index array.",
                "Improvement: external merge sort for data larger than RAM; k-way merge of already sorted gateway streams; "
                "insertion sort for runs shorter than about 16 elements.",
                "Condition to change: if the input arrives as long pre-sorted runs, switch to a natural / k-way merge, which is also stable "
                "and close to O(n log k)."])
    save(d, "Module_1_Merge_Sort/Report/Module_1_Merge_Sort_Report.docx")


# ======================================================================= MODULE 2
def module2():
    d = new_doc(HDR)
    title_block(d, "Module 2 – Quick Sort for the Live Seller Leaderboard",
                "KartIQ Retail Data Analytics Platform | Parts (a) and (c)")
    h(d, "1. Case Understanding (Part a)")
    case_table(d, [2])

    h(d, "2. Divide, Conquer and Combine")
    bullets(d, [("Divide: ", "partition A[lo..hi] around a pivot so that smaller scores are on its left and the others on its right; "
                             "the pivot is then in its final position."),
                ("Conquer: ", "sort the left and right parts recursively."),
                ("Combine: ", "nothing to do, because the parts are already in place; all the work is in Partition (n − 1 comparisons).")])
    para(d, "Pseudocode (file Pseudocode/quick_sort_pseudocode.txt):", after=2).paragraph_format.keep_with_next = True
    txt = read_text("Module_2_Quick_Sort/Pseudocode/quick_sort_pseudocode.txt")
    code(d, txt.split("Recurrences")[0].split("\n", 2)[2].strip(), size=8.2)

    h(d, "3. One Partition Step on the Sample Scores")
    para(d, "Scores: 42, 17, 63, 8, 55, 29. Pivot = first element = 42, i = 0 (i marks the last score known to be smaller than the pivot).")
    table(d, [["j", "A[j]", "A[j] < 42 ?", "Action", "Array after the step", "i"],
              ["start", "–", "–", "pivot = 42", "42, 17, 63, 8, 55, 29", "0"],
              ["1", "17", "yes", "i=1, swap A[1],A[1]", "42, 17, 63, 8, 55, 29", "1"],
              ["2", "63", "no", "none", "42, 17, 63, 8, 55, 29", "1"],
              ["3", "8", "yes", "i=2, swap A[2],A[3]", "42, 17, 8, 63, 55, 29", "2"],
              ["4", "55", "no", "none", "42, 17, 8, 63, 55, 29", "2"],
              ["5", "29", "yes", "i=3, swap A[3],A[5]", "42, 17, 8, 29, 55, 63", "3"],
              ["end", "–", "–", "swap A[0],A[3]", "29, 17, 8, 42, 55, 63", "3"]],
          widths=[0.5, 0.5, 0.9, 1.5, 2.3, 0.4], size=9, align_center_cols=(0, 1, 2, 5))
    para(d, "Result: pivot 42 is at index 3 (final position); left part {29, 17, 8} (all < 42), right part {55, 63}. "
            "The partition used 5 = n − 1 comparisons. Sorting the whole sample needs 9 comparisons and recursion depth 3.")

    h(d, "4. Why the First-Element Pivot Makes the Leaderboard Slow")
    para(d, "The leaderboard data is already (almost) sorted. In sorted data the first element is the smallest of its sub-array, so "
            "Partition produces an empty left part and a right part of n − 1 elements, again with its smallest element in front, and so on. "
            "The “divide” step is completely unbalanced: the recursion depth becomes n and each level still pays a full scan. "
            "Quick Sort only works well when the pivot splits the data roughly in half; with this pivot rule the common case "
            "(nearly sorted) is exactly the worst case.")

    h(d, "5. Recurrences and Solutions")
    table(d, [["Case", "Recurrence", "Solution"],
              ["Best (balanced split)", "T(n) = 2T(n/2) + (n − 1), T(1) = 0", "T(n) = n lg n − n + 1 = Θ(n log n)"],
              ["Worst (sorted / nearly sorted, first pivot)", "T(n) = T(n − 1) + (n − 1), T(1) = 0",
               "T(n) = (n−1) + (n−2) + … + 1 = n(n − 1)/2 = Θ(n²)"],
              ["Average (random order / random pivot)", "T(n) = (n − 1) + (2/n) Σ T(i)", "≈ 2n ln n = 1.39 n lg n = Θ(n log n)"]],
          widths=[1.9, 2.4, 2.3], size=9.5)
    para(d, "Worst-case solution by expansion: T(n) = T(n−1) + (n−1) = T(n−2) + (n−2) + (n−1) = … = Σ k (k = 1..n−1) = n(n−1)/2. "
            "Best case by the Master Theorem: a = 2, b = 2, f(n) = Θ(n), case 2, Θ(n log n).")

    h(d, "6. Estimate for 100,000 Sellers (Nearly Sorted)")
    n = 100_000
    table(d, [["Case", "Calculation", "Comparisons"],
              ["First-element pivot, nearly sorted (worst)", "n(n − 1)/2 = 10⁵ × 99,999 / 2", f"{n * (n - 1) // 2:,}  (≈ 5.0 × 10⁹)"],
              ["Balanced pivot (median-of-three, best case)", "n lg n = 10⁵ × 16.61", f"{n * math.log2(n):,.0f}  (≈ 1.7 × 10⁶)"],
              ["Random pivot, average", "2n ln n", f"{2 * n * math.log(n):,.0f}"],
              ["Ratio worst / best", "4,999,950,000 / 1,660,964", "≈ 3,010 ×"],
              ["Recursion depth", "worst n vs. best ≈ lg n", "100,000 frames vs. about 17"]],
          widths=[2.5, 2.2, 1.9], size=9.5)
    para(d, "At an illustrative 10⁹ comparisons per second the worst case needs about 5 seconds per refresh (the freeze), while the "
            "balanced case needs about 2 milliseconds. The deep recursion (100,000 frames) can also overflow the call stack.")

    h(d, "7. Proposed Improved Pivot Strategy")
    bullets(d, [("Median-of-three: ", "use the median of A[lo], A[mid], A[hi] as pivot. On sorted and nearly sorted data it picks the "
                                      "middle element, so splits are balanced and the best-case recurrence applies."),
                ("Smaller side first: ", "recurse into the smaller part and loop on the larger one; stack depth ≤ lg n ≈ 17."),
                ("Insertion sort for tiny parts (≤ 16): ", "fewer calls and very fast on nearly sorted small ranges."),
                ("Safety net (introsort): ", "if the depth exceeds 2 lg n, switch to Heap Sort, so even adversarial inputs stay O(n log n)."),
                ("Alternative: ", "a random pivot gives expected O(n log n) for every input; if only very few scores move between refreshes, "
                                  "an adaptive sort (insertion sort / Timsort, O(n + inversions)) is even cheaper.")])
    table(d, [["n (nearly sorted)", "First pivot", "n(n−1)/2", "Median-of-three", "Random pivot", "n lg n"]] +
          [[f"{int(r['n']):,}", f"{int(r['first_cmp']):,}", f"{int(r['n']) * (int(r['n']) - 1) // 2:,}",
            f"{int(r['median3_cmp']):,}", f"{int(r['random_cmp']):,}", f"{int(r['n']) * math.log2(int(r['n'])):,.0f}"]
           for r in csvrows("quick_sort_timing.csv")],
          widths=[1.1, 1.1, 1.1, 1.3, 1.1, 0.9], size=9, align_center_cols=(0, 1, 2, 3, 4, 5))
    para(d, "Measured comparisons (program output): the first-element pivot follows n(n−1)/2 almost exactly; median-of-three stays at or below n lg n.", italic=True, size=10)

    h(d, "8. Implementation Screenshots")
    shot(d, "m2_code_quick_sort.png", "Figure 1. Source code: first-element pivot Partition and Quick Sort (Source_Code/quick_sort.py).")
    shot(d, "m2_code_improved.png", "Figure 2. Source code: median-of-three pivot, smaller-side recursion.")
    shot(d, "m2_output_partition.png", "Figure 3. Program output: partition trace on the sample scores.", 6.0)
    shot(d, "m2_output_analysis.png", "Figure 4. Program output: estimates for 100,000 sellers and measured comparisons.")
    graph(d, "m2_quick_sort_graph.png", "Figure 5. Nearly sorted data: first-element pivot is quadratic, median-of-three and random pivot are n log n.")

    h(d, "9. Limitations, Trade-offs and Recommendation")
    bullets(d, ["Trade-off: Quick Sort is in place (O(log n) stack) and fast in practice, but it is not stable and its worst case depends on the pivot rule.",
                "Median-of-three removes the sorted-input worst case but not every adversarial input; the introsort fallback guarantees O(n log n).",
                "Condition to change: if only a handful of scores change between refreshes (inversions k ≪ n lg n), use insertion sort / Timsort "
                "with O(n + k); if equal scores must keep a fixed order, use a stable sort."])
    save(d, "Module_2_Quick_Sort/Report/Module_2_Quick_Sort_Report.docx")


# ======================================================================= MODULE 3
def module3():
    t = {r["method"]: float(r["avg_seconds_per_lookup"]) for r in csvrows("binary_search_timing.csv")}
    d = new_doc(HDR)
    title_block(d, "Module 3 – Binary Search for Order Lookup",
                "KartIQ Retail Data Analytics Platform | Parts (a) and (d)")
    h(d, "1. Case Understanding (Part a)")
    case_table(d, [3])

    h(d, "2. Why Sorted Order Is Essential")
    para(d, "Binary search compares the key with the middle element and then discards one whole half. This is correct only if all elements "
            "on one side of the middle are ≤ it and all on the other side are ≥ it, i.e. the list is sorted by timestamp. "
            "On unsorted data the discarded half may contain the key. Example (program output, Figure 3): in the unsorted sample list the "
            "timestamp 101 exists at index 3, but binary search returns −1 (not found). The sorted list of Module 1 is therefore a precondition, and "
            "because Module 1 uses a stable sort, the first element of a group of equal timestamps is also the earliest arrival.")

    h(d, "3. Divide, Conquer and Combine")
    bullets(d, [("Divide: ", "compute mid = lo + (hi − lo)/2 (overflow-safe) and compare A[mid] with the key."),
                ("Conquer: ", "continue in only ONE half (left if key < A[mid], right if key > A[mid])."),
                ("Combine: ", "nothing; the answer of the half is the answer of the whole.")])
    para(d, "Pseudocode (file Pseudocode/binary_search_pseudocode.txt):", after=2).paragraph_format.keep_with_next = True
    txt = read_text("Module_3_Binary_Search/Pseudocode/binary_search_pseudocode.txt")
    code(d, txt.split("Recurrence :")[0].split("\n", 2)[2].strip(), size=8.2)

    h(d, "4. Recurrence and Maximum Comparisons")
    eq(d, "T(n) = T(n/2) + 1,   T(1) = 1")
    para(d, "Expansion: T(n) = T(n/2) + 1 = T(n/4) + 2 = … = T(n/2ᵏ) + k. The range reaches size 1 when k = lg n, so "
            "T(n) = lg n + 1 for n = 2ᵏ and, for any n, T(n) = ⌊lg n⌋ + 1 = Θ(log n). Master Theorem: a = 1, b = 2, "
            "f(n) = Θ(1) = Θ(n^0), case 2, T(n) = Θ(log n).")
    n = 10_000_000
    table(d, [["Quantity", "Calculation", "Value"],
              ["Maximum comparisons for n = 10,000,000", "⌊log₂(10⁷)⌋ + 1 = ⌊23.2535⌋ + 1", "24"],
              ["Linear search worst case", "n", "10,000,000"],
              ["Speed-up in comparisons", "10,000,000 / 24", f"≈ {n / 24:,.0f} ×"],
              ["Check: 2²³ = 8,388,608 < 10⁷ < 2²⁴ = 16,777,216", "range halves at most 24 times", "24 iterations"]],
          widths=[2.8, 2.5, 1.3], size=9.5)
    para(d, "Verified by the program: simulated worst case on 10,000,000 sorted timestamps = 24 iterations. "
            "Space: O(1) for the iterative version, O(log n) stack for the recursive version.")

    h(d, "5. Modified Search: First Order with a Given Timestamp")
    para(d, "The standard search stops at the first hit, which may be any of several equal timestamps (for key 102 it returned index 2, order O5, "
            "while the first one is O2 at index 1). The modification: when A[mid] equals the key, record mid as a candidate but continue the "
            "search in the LEFT half (hi = mid − 1). The last recorded candidate is the leftmost match. The recurrence is unchanged "
            "(still one comparison per halving); the only difference is that the search always runs until the range is empty, so the worst case "
            "⌊lg n⌋ + 1 = 24 is also reached for successful searches.")
    table(d, [["Key", "Iterations (lo, hi, mid → decision)", "Result"],
              ["102", "(0,5,2) hit, record, go left → (0,1,0) 101<102, go right → (1,1,1) hit, record, go left", "index 1 → (102, O2)"],
              ["105", "(0,5,2) 102<105, right → (3,5,4) hit, record, left → (3,3,3) 103<105, right", "index 4 → (105, O1)"],
              ["101", "(0,5,2) 102>101, left → (0,1,0) hit, record, left", "index 0 → (101, O4)"],
              ["104 (absent)", "(0,5,2) right → (3,5,4) 105>104, left → (3,3,3) 103<104, right", "not found (−1)"]],
          widths=[1.0, 4.0, 1.6], size=9)

    h(d, "6. Implementation Screenshots")
    shot(d, "m3_code_binary_search.png", "Figure 1. Source code: standard and first-occurrence binary search (Source_Code/binary_search.py).")
    shot(d, "m3_output_search.png", "Figure 2. Program output: trace on the sample list (standard vs first-occurrence).")
    shot(d, "m3_output_analysis.png", "Figure 3. Program output: unsorted-data failure, 24 iterations for 10,000,000 orders, steps versus n.")

    h(d, "7. Experimental Results")
    graph(d, "m3_binary_search_graph.png", "Figure 4. Comparisons versus n: ⌊lg n⌋+1 for binary search against n for linear search.", 4.8)
    para(d, f"Measured average lookup in a list of 1,000,000 orders (pure Python, duplicates present): binary search "
            f"{t['binary_first'] * 1e6:.1f} microseconds, linear scan {t['linear'] * 1e3:.2f} milliseconds "
            f"(about {t['linear'] / t['binary_first']:,.0f} times slower).")

    h(d, "8. Limitations, Trade-offs and Recommendation")
    bullets(d, ["Trade-off: O(log n) lookup and O(1) memory need a sorted static array; inserting a new order costs O(n) (or a re-merge).",
                "Orders that arrive after the nightly consolidation should be kept in a small separate sorted buffer and searched first, then merged at night.",
                "Condition to change: if lookups are by order ID with continuous inserts, use a hash index or a B-tree instead of a sorted array."])
    save(d, "Module_3_Binary_Search/Report/Module_3_Binary_Search_Report.docx")


# ======================================================================= MODULE 4
def module4():
    rows = csvrows("strassen_timing.csv")
    last = rows[-1]
    cut = {int(r["cutoff"]): float(r["seconds"]) for r in csvrows("strassen_cutoff.csv")}
    r256 = [r for r in rows if r["n"] == "256"][0]
    d = new_doc(HDR)
    title_block(d, "Module 4 – Strassen’s Method for Recommendation Scores",
                "KartIQ Retail Data Analytics Platform | Parts (a) and (e)")
    h(d, "1. Case Understanding (Part a)")
    case_table(d, [4])

    h(d, "2. Divide, Conquer and Combine")
    bullets(d, [("Divide: ", "split A, B (n × n) into four n/2 × n/2 blocks each."),
                ("Conquer: ", "compute only SEVEN block products M1…M7 recursively (the conventional method needs eight)."),
                ("Combine: ", "build the four blocks of C with additions and subtractions (8 block additions) – 18 block additions in total per level.")])
    h(d, "3. Strassen Products and Reconstruction", 2)
    table(d, [["Product", "Formula"],
              ["M1", "(A11 + A22)(B11 + B22)"], ["M2", "(A21 + A22) B11"], ["M3", "A11 (B12 − B22)"], ["M4", "A22 (B21 − B11)"],
              ["M5", "(A11 + A12) B22"], ["M6", "(A21 − A11)(B11 + B12)"], ["M7", "(A12 − A22)(B21 + B22)"]],
          widths=[1.0, 3.0], size=10, align_center_cols=(0,), )
    eq(d, "C11 = M1 + M4 − M5 + M7,   C12 = M3 + M5,   C21 = M2 + M4,   C22 = M1 − M2 + M3 + M6")
    para(d, "Pseudocode (file Pseudocode/strassen_pseudocode.txt):", after=2).paragraph_format.keep_with_next = True
    txt = read_text("Module_4_Strassen_Matrix_Multiplication/Pseudocode/strassen_pseudocode.txt")
    code(d, txt.split("Recurrence :")[0].split("\n", 2)[2].strip(), size=8.2)

    h(d, "4. Verification on the 2 × 2 Sample")
    para(d, "A = [[1, 7], [3, 5]],  B = [[1, 3], [7, 5]]  (a11=1, a12=7, a21=3, a22=5; b11=1, b12=3, b21=7, b22=5).")
    table(d, [["Product", "Calculation", "Value"],
              ["M1", "(1 + 5)(1 + 5)", "36"], ["M2", "(3 + 5)(1)", "8"], ["M3", "1 (3 − 5)", "−2"], ["M4", "5 (7 − 1)", "30"],
              ["M5", "(1 + 7)(5)", "40"], ["M6", "(3 − 1)(1 + 3)", "8"], ["M7", "(7 − 5)(7 + 5)", "24"]],
          widths=[1.0, 3.0, 1.0], size=10, align_center_cols=(0, 2))
    table(d, [["Entry", "Strassen", "Conventional", "Match"],
              ["C11", "M1 + M4 − M5 + M7 = 36 + 30 − 40 + 24 = 50", "1·1 + 7·7 = 50", "yes"],
              ["C12", "M3 + M5 = −2 + 40 = 38", "1·3 + 7·5 = 38", "yes"],
              ["C21", "M2 + M4 = 8 + 30 = 38", "3·1 + 5·7 = 38", "yes"],
              ["C22", "M1 − M2 + M3 + M6 = 36 − 8 − 2 + 8 = 34", "3·3 + 5·5 = 34", "yes"]],
          widths=[0.7, 3.2, 1.9, 0.7], size=9.5, align_center_cols=(0, 3))
    para(d, "C = [[50, 38], [38, 34]]. Strassen used 7 multiplications and 18 additions/subtractions; the conventional method uses 8 multiplications and 4 additions.")

    h(d, "5. Recurrence and Solution")
    eq(d, "T(n) = 7 T(n/2) + Θ(n²),   M(n) = 7 M(n/2), M(1) = 1")
    para(d, "Expanding for n = 2ᵏ: M(n) = 7ᵏ = 7^(lg n) = n^(lg 7) ≈ n^2.807. Master Theorem: a = 7, b = 2, f(n) = Θ(n²); "
            "since n^(log₂ 7) = n^2.807 grows faster than n² (case 1), T(n) = Θ(n^(log₂ 7)) = Θ(n^2.81). "
            "Additions: A(n) = 7A(n/2) + 18(n/2)² with A(1) = 0 gives A(2ᵏ) = 6(7ᵏ − 4ᵏ).")

    h(d, "6. Operation Counts for n = 1,024 (k = 10)")
    table(d, [["Method", "Scalar multiplications", "Scalar additions", "Total"],
              ["Conventional", "n³ = 1,073,741,824", "n²(n−1) = 1,072,693,248", "2,146,435,072"],
              ["Strassen (to 1×1)", "7¹⁰ = 282,475,249", "6(7¹⁰ − 4¹⁰) = 1,688,560,038", "1,971,035,287"],
              ["Hybrid, cutoff 128 (3 levels)", "7³ × 128³ = 719,323,136", "741,130,240", "1,460,453,376"],
              ["Hybrid, cutoff 64 (4 levels)", "7⁴ × 64³ = 629,407,744", "672,288,768", "1,301,696,512"],
              ["Hybrid, cutoff 8 (op-count optimum)", "7⁷ × 8³ = 421,654,016", "678,896,320", "1,100,550,336"]],
          widths=[1.9, 1.7, 1.9, 1.1], size=9)
    bullets(d, ["Multiplications: 282,475,249 / 1,073,741,824 = 0.263, i.e. Strassen needs 26.3 % of the multiplications (73.7 % fewer, 3.8 times less).",
                "Total operations: only 0.918 times the conventional total (8.2 % fewer) because the 18 block additions per level add 1.69 × 10⁹ additions.",
                "Memory: one 1,024 × 1,024 float64 matrix = 8 MiB; A, B, C = 24 MiB; Strassen temporaries about 3n² elements = 24 MiB more."])

    h(d, "7. Why Strassen May Still Not Be Faster in Practice")
    bullets(d, [("Extra additions and memory traffic: ", "18 matrix additions per level plus temporaries; real speed is limited by memory bandwidth and cache misses, not only by multiplications."),
                ("Recursion overhead: ", "at a 1 × 1 leaf the work per call is tiny; the measured numpy-based recursion down to 1 × 1 blocks at n = 256 took "
                                         f"{float(r256['strassen_cutoff1_s']):.1f} s against {float(r256['conventional_loops_s']):.2f} s for the conventional row-by-column loops."),
                ("Optimised libraries: ", "BLAS kernels use SIMD, blocking and multiple cores and run at near hardware peak; "
                                          f"for n = 1,024 numpy BLAS took {float(last['numpy_blas_s']):.4f} s, our hybrid with cutoff 128 took {float(last['hybrid128_s']):.4f} s."),
                ("Numerical stability: ", "the weaker error bounds of Strassen matter for floating-point scores."),
                ("Size: ", "the break-even point of real implementations is typically a few hundred to a few thousand; padding to a power of two is also needed for other n.")])

    h(d, "8. Practical Hybrid")
    para(d, "Use Strassen only for the top two or three levels of recursion and switch to an optimised conventional (blocked / BLAS) kernel once the blocks "
            "are at most 64–128. For n = 1,024 and cutoff 128 this performs 7³ = 343 block products of size 128 × 128 (719,323,136 multiplications, "
            "33 % fewer than conventional) and keeps the recursion shallow. Further refinements: reuse preallocated buffers for M1…M7, use the Winograd "
            "variant (15 instead of 18 additions), pad odd sizes with zeros, and verify with a randomised check (C x = A (B x)) in production.")
    table(d, [["Cutoff", "Multiplications", "Total ops (mult + add)", "Ratio to conventional"]] +
          [[str(c), f"{m:,}", f"{tt:,}", f"{tt / 2146435072:.3f}"] for c, m, tt in
           ((1, 282475249, 1971035287), (8, 421654016, 1100550336), (16, 481890304, 1108079872), (32, 550731776, 1181223936),
            (64, 629407744, 1301696512), (128, 719323136, 1460453376), (256, 822083584, 1653932032), (1024, 1073741824, 2146435072))],
          widths=[0.9, 1.9, 2.1, 1.7], size=9, align_center_cols=(0, 1, 2, 3))
    para(d, "Measured wall-clock result (numpy, n = 512, best of 3): "
            + ", ".join(f"cutoff {c}: {cut[c]:.4f} s" for c in (64, 128, 256, 512)) +
            ". On this machine the pure library multiplication (cutoff 512) is fastest, so the recommendation is: benchmark on the production hardware, "
            "and keep the hybrid only where it wins.", italic=True, size=10.5)

    h(d, "9. Implementation Screenshots")
    shot(d, "m4_code_strassen.png", "Figure 1. Source code: Strassen recursion with cutoff (Source_Code/strassen.py).")
    shot(d, "m4_output_sample.png", "Figure 2. Program output: products, reconstruction and verification on the 2 × 2 sample.", 6.0)
    shot(d, "m4_output_counts.png", "Figure 3. Program output: operation counts and cutoff table for n = 1,024.")
    graph(d, "m4_strassen_operations_graph.png", "Figure 4. Multiplication counts versus n, and total operations versus cutoff for n = 1,024.")
    graph(d, "m4_cutoff_timing_graph.png", "Figure 5. Measured time versus cutoff (n = 512, numpy leaves).", 4.0)

    h(d, "10. Limitations, Trade-offs and Recommendation")
    bullets(d, ["Trade-off: about 26 % of the multiplications (full recursion) in exchange for more additions, 3n² extra memory, more complex code and weaker numerical stability.",
                "Recommendation: hybrid Strassen with a leaf size of 64–128 using an optimised kernel, enabled only if a benchmark on the real hardware shows a gain.",
                "Condition to change: if the matrices are sparse, or n is below roughly 1,000–2,000, or the library kernel is faster in the benchmark, use the plain blocked / BLAS multiplication."])
    save(d, "Module_4_Strassen_Matrix_Multiplication/Report/Module_4_Strassen_Report.docx")


# ======================================================================= FINAL DESIGN
def final():
    d = new_doc(HDR)
    title_block(d, "Final Design and Analysis", "KartIQ: Divide-and-Conquer Engine | Parts (a) and (f)")
    h(d, "1. Case Understanding Summary (Part a)")
    case_table(d, [1, 2, 3, 4])
    para(d, "Common thread: all four modules are divide-and-conquer problems, but they differ in what matters most – stability and a guaranteed "
            "bound (Module 1), robustness on nearly sorted data (Module 2), a sorted precondition (Module 3) and matrix size (Module 4).")

    h(d, "2. Final Algorithmic Design (Part f)")
    table(d, [["Module", "Chosen algorithm", "Time complexity", "Extra memory", "Reason for the choice"],
              ["1. Order consolidation", "Merge Sort (stable, top-down; external k-way merge if data > RAM)",
               "Θ(n log n) in all cases; ≈ 2.2×10⁸ comparisons for 10⁷ orders",
               "O(n): ≈ 160 MB buffer (16 B records); external: O(RAM) + heap of k",
               "Stable (equal timestamps keep gateway arrival order), guaranteed worst case, merges naturally from disk."],
              ["2. Seller leaderboard", "Quick Sort with median-of-three pivot, smaller-side recursion, insertion sort for ≤ 16 elements, heap-sort fallback (introsort)",
               "Θ(n log n) expected and guaranteed with fallback; ≈ 1.7×10⁶ comparisons for 10⁵ sellers",
               "O(log n) stack, in place",
               "Removes the n² behaviour (5×10⁹ comparisons) on nearly sorted data; no stability needed; fast, cache-friendly."],
              ["3. Order lookup", "Binary Search, first-occurrence variant on the Module 1 output",
               "O(log n); at most 24 iterations for 10⁷ orders (best case O(1) for the standard version)",
               "O(1) iterative",
               "Needs only the sorted array; returns the first (earliest) order of equal timestamps; 416,667× fewer comparisons than a scan."],
              ["4. Recommendation scores", "Hybrid Strassen (top 3 levels, cutoff 128) with an optimised conventional kernel at the leaves",
               "Θ(n^2.81) above the cutoff; 7³×128³ = 719,323,136 multiplications for n = 1,024 (vs 1,073,741,824)",
               "≈ 3n² elements = 24 MiB temporaries plus A, B, C = 24 MiB",
               "Saves 33 % of the multiplications while avoiding the overhead of deep recursion."]],
          widths=[0.9, 1.5, 1.5, 1.2, 1.6], size=8.5, bold_first_col=True)

    h(d, "3. Main Trade-off and Condition to Change", 2)
    table(d, [["Module", "Main trade-off", "One condition under which I would change the decision"],
              ["1", "Guaranteed O(n log n) and stability are paid for with O(n) extra memory and more data movement.",
               "Data larger than RAM, or input already arrives as sorted gateway streams → external / k-way (natural) merge, O(n log k)."],
              ["2", "Speed and O(log n) space are bought with instability and a pivot heuristic that adversarial inputs can still defeat.",
               "Only a few scores change per refresh (few inversions) → insertion sort / Timsort in O(n + inversions); or equal scores need a stable order → Merge Sort."],
              ["3", "O(log n) lookup with O(1) memory requires a sorted, static array; inserts cost O(n).",
               "Continuous inserts or lookups by order ID → hash index or B-tree."],
              ["4", "Fewer multiplications are paid for with more additions, extra memory and weaker numerical stability.",
               "Benchmark shows the BLAS kernel is faster (as measured here at n = 1,024), n is small or the matrices are sparse → plain blocked / sparse multiplication."]],
          widths=[0.6, 2.9, 3.1], size=9, align_center_cols=(0,))

    h(d, "4. Workload Summary and Comparison", 2)
    table(d, [["Module", "Workload", "Poor choice", "Chosen design", "Improvement"],
              ["1", "10,000,000 orders", "O(n²) sort: ≈ 5×10¹³ comparisons (or unstable sort: audit fails)", "Merge Sort: ≈ 2.2×10⁸", "≈ 220,000× fewer comparisons"],
              ["2", "100,000 sellers", "First pivot: 4,999,950,000", "Median-of-three: ≈ 1,660,964", "≈ 3,010× fewer"],
              ["3", "10,000,000 orders", "Linear scan: 10,000,000", "Binary search: 24", "≈ 416,667× fewer"],
              ["4", "n = 1,024", "Conventional: 1,073,741,824 mults", "Hybrid (cutoff 128): 719,323,136", "33 % fewer mults (73.7 % with full recursion)"]],
          widths=[0.6, 1.2, 2.0, 1.6, 1.2], size=9, align_center_cols=(0,))
    graph(d, "final_workload_comparisons.png", "Figure 1. Comparisons at the production workloads (log scale).", 5.4)

    h(d, "5. End-to-End Pipeline", 2)
    para(d, "Nightly: Module 1 sorts the day’s orders (stable) → the sorted list is the index for Module 3 lookups the next day. Every few seconds: "
            "Module 2 re-sorts the seller scores in place. Periodically (more often than daily): Module 4 recomputes C = A × B with the hybrid kernel. "
            "Each module’s report in this repository contains pseudocode, runnable code, traces, recurrences, graphs and screenshots.")

    h(d, "6. Recommendations", 2)
    bullets(d, ["Deploy Merge Sort with a single reusable buffer; add external k-way merge for peak days; sort compact key arrays rather than objects.",
                "Replace the first-element pivot by median-of-three (with insertion-sort cutoff and heap-sort fallback); monitor the recursion depth.",
                "Keep a small sorted “intraday” buffer for orders that arrive after consolidation, so binary search stays valid.",
                "Benchmark the Strassen hybrid on the production hardware before enabling it; keep BLAS as the default."])

    h(d, "Declaration (Code of Conduct)", 2)
    para(d, f"I {STUDENT} (Reg. No. {REG}) certify that this submission is my original work and that I have adhered to the guidelines "
            "specified for this assessment. I understand that any violation of academic integrity rules will result in disciplinary action.")
    para(d, "Signature of the Student: ____________________        Date: ______________")
    save(d, "Final_Design_and_Analysis/Final_Design_and_Analysis.docx")


if __name__ == "__main__":
    module1(); module2(); module3(); module4(); final()
