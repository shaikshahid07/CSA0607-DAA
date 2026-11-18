# CO2 - Debugging and Optimisation: SentinelOps SOC Alert-Triage Module

**Course:** CSA06 Design and Analysis of Algorithms  
**Student:** Shaik Shahid - Register No. 192424311

A Security Operations Centre module with four functions (alert sorting, blocklist lookup, signature search,
closest login pair) had nine defects. This repository contains the systematic debugging of the original code,
the corrected version, an optimised production version, the test harness, the experiments and the report.

## Repository layout

```
CO2_Debugging_Optimisation/
├── Pseudocode/
│   ├── 01_sort_alerts.md          corrected + optimised pseudocode
│   ├── 02_is_blocked.md
│   ├── 03_find_signature.md
│   └── 04_closest_logins.md
├── Source_Code/
│   ├── original_module.py         the buggy code exactly as given (+ demo run)
│   ├── corrected_module.py        debugged, not rewritten - every change marked  # FIX Dn
│   ├── optimised_module.py        production version (sorted, hash set, Horspool, pruning, divide and conquer)
│   ├── test_harness.py            130 checks on the corrected AND the optimised code
│   ├── debug_steps.py             insertion trace, alignment table, fixes applied one at a time
│   ├── experiments.py             operation counts and run times (part d)
│   ├── CO2_Experiments.ipynb      Jupyter notebook that runs all experiments (outputs saved inside)
│   └── make_screenshots.py        renders the execution logs as the screenshots used in the report
├── Report/
│   └── CO2_SentinelOps_Report.docx
├── Supporting_Files/
│   ├── datasets/                  question test data (JSON) + two seeded sample datasets (CSV)
│   ├── execution_logs/            output of every script, saved exactly as printed
│   ├── results/                   experiment results as CSV (5 files)
│   ├── graphs/                    four graphs (PNG)
│   ├── screenshots/               execution-output screenshots used in the report
│   └── notebook_run/              graphs produced by the notebook's own run
└── README.md
```

## The nine defects

| ID | Function | Faulty line | Fix |
|---|---|---|---|
| D1 | `sort_alerts` | `while j > 0 and ...` | `while j >= 0 and ...` |
| D2 | `sort_alerts` | `alerts[j] = key` | `alerts[j + 1] = key` |
| D3 | `is_blocked` | `return False` when the address matches | `return True` |
| D4 | `is_blocked` | `else: return False` inside the loop; nothing returned after it | remove the `else`, add `return False` after the loop |
| D5 | `find_signature` | `range(n - m)` | `range(n - m + 1)` |
| D6 | `find_signature` | `if j == m - 1:` after the inner loop | `for ... else:` (hit only if no `break`) |
| D7 | `closest_logins` | `min_dist = 0` | `min_dist = math.inf` |
| D8 | `closest_logins` | `if d > min_dist:` | `if d < min_dist:` |
| D9 | `closest_logins` | `for j in range(len(events))` | `for j in range(i + 1, len(events))` |

## How to run

Python 3.9 or newer. Only the standard library is needed for the module and the harness;
`matplotlib` is needed for the graphs, and `pandas` + `jupyter` for the notebook.

```bash
cd Source_Code
python original_module.py      # actual (wrong) output of the original code
python debug_steps.py          # traces + staged fixes
python corrected_module.py     # corrected output
python optimised_module.py     # optimised output
python test_harness.py         # 130 checks, exit code 0 when all pass
python experiments.py          # about one minute; writes ../Supporting_Files/results and graphs
jupyter notebook CO2_Experiments.ipynb
```

## Results at a glance (random data, seed 2026)

| Function | Before | After |
|---|---|---|
| `sort_alerts`, 10,000 random alerts | 22,297,542 comparisons (insertion sort) | 70,911 (`sorted`) |
| `is_blocked`, 1,000 queries, 100,000 addresses | 75,396,223 comparisons | 1,000 hash lookups |
| `find_signature`, 200,000 chars, 4-char pattern | 207,835 comparisons (brute force) | 55,287 (Horspool) |
| `find_signature`, worst case (log of A's, pattern AAAAAAAB, n = 10,000) | 79,944 comparisons | 9,993 (Horspool) |
| `closest_logins`, 8,000 events | 64,000,000 distance computations (original) | 13,478 (pruned), 9,391 (divide and conquer) |
| `closest_logins`, worst case for the simple pruning (two vertical lines, n = 4,000) | 7,998,000 (corrected brute force) | 3,998,000 (pruned) but only 4,280 (divide and conquer) |

Counts are identical on every run; run times vary slightly between machines.
