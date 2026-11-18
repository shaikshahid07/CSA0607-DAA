"""
Systematic debugging walk-through for the SentinelOps module (part (b) of the task).

1. Insertion trace of sort_alerts  (original vs corrected)
2. Alignment table of find_signature on the question's log line
3. Staged re-testing: the fixes are applied ONE AT A TIME to the original source
   code (by exact text replacement, so nothing is rewritten from scratch) and the
   function is re-run after every single fix.

Run with:   python debug_steps.py
"""
import math
from pathlib import Path

SRC = Path(__file__).with_name("original_module.py").read_text()

ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
QUERIES = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
LOG, PATTERN = "FAILFAIXFAIL", "FAIL"
EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]


# ------------------------------------------------------------------ 1. insertion trace
def trace_insertion(alerts, fixed):
    """Re-run insertion sort printing the list after every pass (fixed=False reproduces the bugs)."""
    a = list(alerts)
    print(f"  start      : {[f'{n}:{s}' for n, s in a]}")
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        low = -1 if fixed else 0                      # D1: loop condition  j >= 0   vs   j > 0
        while j > low and a[j][1] < key[1]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1 if fixed else j] = key                # D2: slot  j+1   vs   j
        print(f"  pass i={i} key={key[0]}:{key[1]} placed at index {j + 1 if fixed else j}: "
              f"{[f'{n}:{s}' for n, s in a]}")
    return a


print("=" * 78)
print("1. INSERTION TRACE  -  ORIGINAL (buggy)")
trace_insertion(ALERTS, fixed=False)
print("\n   INSERTION TRACE  -  CORRECTED")
trace_insertion(ALERTS, fixed=True)


# ------------------------------------------------------------------ 2. alignment table
print("\n" + "=" * 78)
print(f"2. ALIGNMENT TABLE  -  log={LOG!r} (n={len(LOG)}), pattern={PATTERN!r} (m={len(PATTERN)})")
n, m = len(LOG), len(PATTERN)
print(f"{'i':>2} {'window':<8} {'first mismatch j':<17} {'orig j after loop':<18} "
      f"{'scanned by orig?':<17} {'orig reports':<13} {'correct'}")
for i in range(n - m + 1):
    window = LOG[i:i + m]
    mism = next((k for k in range(m) if window[k] != PATTERN[k]), None)
    j_after = mism if mism is not None else m - 1
    scanned = i < n - m                                # original used range(n - m)
    orig_hit = scanned and j_after == m - 1
    right_hit = mism is None
    print(f"{i:>2} {window:<8} {str(mism) if mism is not None else 'none':<17} "
          f"{j_after:<18} {'yes' if scanned else 'NO (skipped)':<17} "
          f"{'HIT' if orig_hit else '-':<13} {'HIT' if right_hit else '-'}")
print("   -> i=4 'FAIX' is a FALSE hit (mismatch at the last char leaves j == m-1);")
print("   -> i=8 'FAIL' is a MISSED hit (alignment never tried).")


# ------------------------------------------------------------------ 3. staged fixes
def build(*patches):
    """Return a namespace with the original module after applying the given (old, new) text patches."""
    code = SRC.split('if __name__ == "__main__":')[0]
    for old, new in patches:
        assert old in code, f"patch target not found: {old!r}"
        code = code.replace(old, new, 1)
    ns = {}
    exec(code, ns)
    return ns


P = {
    "D1": ("while j > 0 and", "while j >= 0 and"),
    "D2": ("        alerts[j] = key", "        alerts[j + 1] = key"),
    "D3": ("        if blocklist[i] == ip:\n            return False\n", "        if blocklist[i] == ip:\n            return True\n"),
    "D4": ("        else:\n            return False\n", "    return False\n"),
    "D5": ("range(n - m):", "range(n - m + 1):"),
    "D6": ("        if j == m - 1:\n            hits.append(i)",
           "        else:\n            hits.append(i)"),
    "D7": ("min_dist = 0", "min_dist = math.inf"),
    "D8": ("if d > min_dist:", "if d < min_dist:"),
    "D9": ("for j in range(len(events)):", "for j in range(i + 1, len(events)):"),
}

print("\n" + "=" * 78)
print("3. STAGED RE-TESTING (each row = original code + the listed fixes only)")

print("\n--- sort_alerts   expected: [('A2', 9), ('A4', 9), ('A3', 5), ('A1', 3), ('A5', 1)]")
for label, fixes in [("original", []), ("+ D1", ["D1"]), ("+ D1 + D2", ["D1", "D2"])]:
    ns = build(*[P[f] for f in fixes])
    print(f"  {label:<10}: {ns['sort_alerts'](list(ALERTS))}")

print("\n--- is_blocked    expected: True, True, False   (queries 10.0.0.9, 10.0.0.5, 8.8.8.8)")
for label, fixes in [("original", []), ("+ D3", ["D3"]), ("+ D3 + D4", ["D3", "D4"])]:
    ns = build(*[P[f] for f in fixes])
    print(f"  {label:<10}: {[ns['is_blocked'](BLOCKLIST, q) for q in QUERIES]}   "
          f"empty blocklist -> {ns['is_blocked']([], '10.0.0.5')}")

print("\n--- find_signature   expected: [0, 8]")
for label, fixes in [("original", []), ("+ D5", ["D5"]), ("+ D5 + D6", ["D5", "D6"])]:
    ns = build(*[P[f] for f in fixes])
    try:
        out = ns["find_signature"](LOG, PATTERN)
    except Exception as e:                          # D6 fixed alone is not reached here
        out = f"error: {e}"
    print(f"  {label:<10}: {out}")

print("\n--- closest_logins   expected: ((0, 5), 1.4142135623730951)")
for label, fixes in [("original", []), ("+ D8", ["D8"]), ("+ D8 + D7", ["D8", "D7"]),
                     ("+ D8 + D7 + D9", ["D8", "D7", "D9"])]:
    ns = build(*[P[f] for f in fixes])
    print(f"  {label:<15}: {ns['closest_logins'](EVENTS)}")
print("  (the three closest_logins fixes depend on each other: D8 alone finds nothing,")
print("   D8 + D7 reports the point paired with itself at distance 0, and D9 removes that.)")
