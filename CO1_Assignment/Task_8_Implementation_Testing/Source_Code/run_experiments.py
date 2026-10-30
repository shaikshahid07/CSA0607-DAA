"""
Experiment driver for the CO1 assignment (CSA0607).  Name: Shaik Shahid, Reg. No. 192424311
Usage:  python run_experiments.py            -> writes results.json and results.csv next to this file
Testing procedure (identical for every algorithm):
  * Dataset: n unique 9-digit registration numbers drawn with random.sample (seed 192424311),
    stored in random (unsorted) order.  The SAME list is given to every algorithm.
  * Sorted copy is produced for binary search; hash table is built from the same list.
  * Queries: first element, middle element, last element (of the unsorted list), an absent key,
    plus random present keys (average case).
  * Time = mean per-search wall-clock time (time.perf_counter) over all queries of that kind.
"""
import csv, json, os, random, sys, time
import search_algorithms as sa

sys.setrecursionlimit(10000)
SEED = 192424311
SIZES = [1_000, 10_000, 100_000, 1_000_000]
HERE = os.path.dirname(os.path.abspath(__file__))


def timed(fn, queries):
    t0 = time.perf_counter()
    for q in queries:
        fn(q)
    return (time.perf_counter() - t0) / len(queries)


def correctness_tests():
    """Small-scale correctness test: every algorithm must agree with Python's `in`."""
    rnd = random.Random(1)
    for n in (0, 1, 2, 3, 10, 257, 1000):
        data = rnd.sample(range(190_000_000, 195_000_000), n)
        srt = sa.sort_records(data)
        ht = sa.HashTable(data)
        probes = data[:50] + [190_000_000 - 1, 195_000_001, 192_424_311]
        for k in probes:
            truth = k in data
            assert (sa.linear_search(data, k) != -1) == truth
            r = sa.binary_search_recursive(srt, k, 0, len(srt) - 1)
            assert (r != -1) == truth and (r == -1 or srt[r] == k)
            r2 = sa.binary_search_iterative(srt, k)
            assert (r2 != -1) == truth
            assert ht.search(k) == truth
    return True


def run():
    assert correctness_tests()
    print("Correctness tests: PASSED (n = 0,1,2,3,10,257,1000; present and absent keys)")
    results = []
    for n in SIZES:
        rnd = random.Random(SEED + n)
        data = rnd.sample(range(190_000_000, 195_000_000), n)     # unsorted, unique
        absent = 189_999_999                                       # below the range -> never present
        first, mid, last = data[0], data[n // 2], data[-1]
        qn = {1_000: 300, 10_000: 100, 100_000: 40, 1_000_000: 15}[n]   # random present keys
        rand_keys = [data[rnd.randrange(n)] for _ in range(qn)]

        # ---- preprocessing
        t0 = time.perf_counter(); srt = sa.sort_records(data); t_sort = time.perf_counter() - t0
        t0 = time.perf_counter(); ht = sa.HashTable(data);      t_hash = time.perf_counter() - t0
        hi = n - 1
        rec = lambda k: sa.binary_search_recursive(srt, k, 0, hi)
        itr = lambda k: sa.binary_search_iterative(srt, k)
        lin = lambda k: sa.linear_search(data, k)
        hsh = ht.search

        # ---- sanity: all algorithms agree on every query used
        for k in [first, mid, last, absent] + rand_keys:
            truth = k != absent
            assert (lin(k) != -1) == truth and (rec(k) != -1) == truth
            assert (itr(k) != -1) == truth and hsh(k) == truth

        # ---- comparison counts
        def lin_c(k): return sa.linear_search_counted(data, k)[1]
        def rec_c(k):
            c = [0]; sa.binary_search_recursive_counted(srt, k, 0, hi, c); return c[0]
        def hsh_c(k): return ht.search_counted(k)[1]
        def avg(f, ks): return sum(f(k) for k in ks) / len(ks)

        row = {"n": n, "sort_time_s": t_sort, "hash_build_time_s": t_hash,
               "hash_table_size": ht.m,
               "hash_max_chain": max(len(b) for b in ht.table if b),
               "hash_avg_chain_nonempty": sum(len(b) for b in ht.table if b) / sum(1 for b in ht.table if b)}
        for name, fn, cf in (("linear", lin, lin_c), ("binary_rec", rec, rec_c),
                             ("binary_iter", itr, None), ("hash", hsh, hsh_c)):
            # repeat cheap searches so timer resolution is not an issue
            rep = 1 if name == "linear" else 200
            def timeit(qs):
                return timed(fn, qs * rep)
            row[f"{name}_time_first_s"] = timeit([first])
            row[f"{name}_time_mid_s"] = timeit([mid])
            row[f"{name}_time_last_s"] = timeit([last])
            row[f"{name}_time_absent_s"] = timeit([absent])
            row[f"{name}_time_avg_s"] = timeit(rand_keys)
            if cf:
                row[f"{name}_cmp_first"] = cf(first)
                row[f"{name}_cmp_mid"] = cf(mid)
                row[f"{name}_cmp_last"] = cf(last)
                row[f"{name}_cmp_absent"] = cf(absent)
                row[f"{name}_cmp_avg"] = avg(cf, rand_keys)
        results.append(row)
        print(f"n={n:>9,}  sort={t_sort:.4f}s  hash build={t_hash:.4f}s  "
              f"linear avg={row['linear_time_avg_s']*1e6:.1f}us  "
              f"bin(rec) avg={row['binary_rec_time_avg_s']*1e6:.2f}us  "
              f"hash avg={row['hash_time_avg_s']*1e6:.2f}us", flush=True)

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader(); w.writerows(results)
    return results


if __name__ == "__main__":
    run()
