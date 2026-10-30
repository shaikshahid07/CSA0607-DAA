"""
Test harness for the SentinelOps SOC Alert-Triage Module.

Runs every test against BOTH the corrected module (debugged original) and the
optimised module, so that the optimisations are proven not to change any output.
Run with:   python test_harness.py
Exit code 0 = all tests passed.
"""
import math
import random
import sys

import corrected_module as cor
import optimised_module as opt

passed = failed = 0


def check(name, actual, expected):
    """Print PASS/FAIL for one test case and keep the totals."""
    global passed, failed
    ok = actual == expected
    passed += ok
    failed += (not ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"        expected: {expected!r}\n        actual  : {actual!r}")


# ---------------------------------------------------------------- test data from the question paper
ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
LOG, PATTERN = "FAILFAIXFAIL", "FAIL"
EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

SORTED_ALERTS = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]


def run_sort_tests(name, sort_fn):
    print(f"\n--- sort_alerts [{name}] ---")
    check("question data -> highest first, A2 before A4", sort_fn(list(ALERTS)), SORTED_ALERTS)
    check("no alert lost or duplicated", sorted(sort_fn(list(ALERTS))), sorted(ALERTS))
    check("empty list", sort_fn([]), [])
    check("single alert", sort_fn([("X", 4)]), [("X", 4)])
    check("equal severities keep arrival order",
          sort_fn([("B", 5), ("A", 5), ("C", 5)]), [("B", 5), ("A", 5), ("C", 5)])
    check("already sorted (best case)", sort_fn(list(SORTED_ALERTS)), SORTED_ALERTS)
    check("reverse sorted (worst case)", sort_fn(list(reversed(SORTED_ALERTS))),
          [("A4", 9), ("A2", 9), ("A3", 5), ("A1", 3), ("A5", 1)])
    check("largest severity sits at index 0 (D1 boundary)",
          sort_fn([("L", 1), ("H", 9)]), [("H", 9), ("L", 1)])


def run_blocked_tests(name, make_index, blocked_fn):
    print(f"\n--- is_blocked [{name}] ---")
    idx = make_index(BLOCKLIST)
    check("10.0.0.9 (2nd entry) is blocked", blocked_fn(idx, "10.0.0.9"), True)
    check("10.0.0.5 (1st entry) is blocked", blocked_fn(idx, "10.0.0.5"), True)
    check("172.16.4.2 (last entry) is blocked", blocked_fn(idx, "172.16.4.2"), True)
    check("8.8.8.8 is not blocked", blocked_fn(idx, "8.8.8.8"), False)
    check("empty blocklist returns False (not None)", blocked_fn(make_index([]), "10.0.0.5"), False)
    check("empty ip string not blocked", blocked_fn(idx, ""), False)
    check("one-entry blocklist, match", blocked_fn(make_index(["1.1.1.1"]), "1.1.1.1"), True)
    check("one-entry blocklist, no match", blocked_fn(make_index(["1.1.1.1"]), "2.2.2.2"), False)
    check("duplicate entries in blocklist", blocked_fn(make_index(["a", "a", "b"]), "b"), True)


def run_signature_tests(name, find_fn):
    print(f"\n--- find_signature [{name}] ---")
    check("question data -> [0, 8]", find_fn(LOG, PATTERN), [0, 8])
    check("pattern at the very end of the log", find_fn("xxxxFAIL", "FAIL"), [4])
    check("pattern at the very start of the log", find_fn("FAILxxxx", "FAIL"), [0])
    check("pattern equals the whole log", find_fn("FAIL", "FAIL"), [0])
    check("pattern longer than the log", find_fn("FAI", "FAIL"), [])
    check("no occurrence", find_fn("abcdef", "xyz"), [])
    check("near miss 'FAIX' is not reported", find_fn("FAIX", "FAIL"), [])
    check("overlapping occurrences", find_fn("AAAA", "AA"), [0, 1, 2])
    check("empty log", find_fn("", "FAIL"), [])
    check("empty pattern -> no hits", find_fn("FAIL", ""), [])
    check("single-character pattern", find_fn("abcab", "a"), [0, 3])
    check("repeated prefix pattern", find_fn("AAAB", "AAB"), [1])


def run_closest_tests(name, closest_fn):
    print(f"\n--- closest_logins [{name}] ---")
    pair, dist = closest_fn(EVENTS)
    check("question data -> pair (0, 5)", pair, (0, 5))
    check("question data -> distance sqrt(2)", math.isclose(dist, math.sqrt(2)), True)
    check("empty events", closest_fn([]), (None, None))
    check("one event", closest_fn([(1, 1)]), (None, None))
    pair, dist = closest_fn([(0, 0), (3, 4)])
    check("exactly two events -> (0, 1) and 5.0", (pair, dist), ((0, 1), 5.0))
    pair, dist = closest_fn([(1, 1), (9, 9), (1, 1)])
    check("duplicate location -> distance 0, pair (0, 2)", (pair, dist), ((0, 2), 0.0))
    pair, dist = closest_fn([(0, 0), (0, 5), (0, 9), (0, 10)])
    check("all on one vertical line", (pair, dist), ((2, 3), 1.0))
    pair, dist = closest_fn([(0, 0), (1, 0), (5, 5), (6, 5)])
    check("tie (two pairs at distance 1) -> first pair (0, 1)", (pair, dist), ((0, 1), 1.0))
    pair, dist = closest_fn([(5, 5), (5, 5), (5, 5)])
    check("all identical points", (pair, dist), ((0, 1), 0.0))


# ---------------------------------------------------------------- run the unit tests on both modules
run_sort_tests("corrected", cor.sort_alerts)
run_sort_tests("optimised sorted()", opt.sort_alerts)
run_sort_tests("optimised insertion_sort_alerts", lambda a: opt.insertion_sort_alerts(a))
run_blocked_tests("corrected", lambda b: b, cor.is_blocked)
run_blocked_tests("optimised hash set", opt.build_blocklist, opt.is_blocked)
run_blocked_tests("optimised sequential", lambda b: b, opt.is_blocked_sequential)
run_signature_tests("corrected", cor.find_signature)
run_signature_tests("optimised brute force", opt.find_signature)
run_signature_tests("optimised Horspool", opt.find_signature_horspool)
run_signature_tests("optimised str.find", opt.find_signature_builtin)
run_closest_tests("corrected", cor.closest_logins)
run_closest_tests("optimised pruned", opt.closest_logins)
run_closest_tests("optimised divide-and-conquer", opt.closest_logins_dc)

# ---------------------------------------------------------------- equivalence on random data
print("\n--- random equivalence tests (optimised output must equal corrected output) ---")
rng = random.Random(2026)

ok = True
for _ in range(300):
    data = [(f"A{k}", rng.randint(1, 6)) for k in range(rng.randint(0, 40))]
    ok &= opt.sort_alerts(data) == cor.sort_alerts(list(data)) == opt.insertion_sort_alerts(list(data))
check("sort: 300 random lists (many equal severities)", ok, True)

ok = True
for _ in range(300):
    log = "".join(rng.choice("AB") for _ in range(rng.randint(0, 30)))
    pat = "".join(rng.choice("AB") for _ in range(rng.randint(0, 5)))
    ref = cor.find_signature(log, pat)
    ok &= (opt.find_signature(log, pat) == ref == opt.find_signature_horspool(log, pat)
           == opt.find_signature_builtin(log, pat))
check("signature: 300 random logs/patterns (3 algorithms agree)", ok, True)

ok = True
for _ in range(300):
    ev = [(rng.randint(0, 6), rng.randint(0, 6)) for _ in range(rng.randint(0, 40))]   # small grid -> many ties
    ref = cor.closest_logins(ev)
    ok &= opt.closest_logins(ev) == ref == opt.closest_logins_dc(ev)
check("closest pair: 300 random tie-heavy batches (3 algorithms agree)", ok, True)

ok = True
for _ in range(20):
    ev = [(rng.uniform(0, 500), rng.uniform(0, 500)) for _ in range(500)]
    ref = cor.closest_logins(ev)
    ok &= opt.closest_logins(ev) == ref == opt.closest_logins_dc(ev)
check("closest pair: 20 random float batches of 500 events", ok, True)

print(f"\nRESULT: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
