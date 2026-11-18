"""Q3 - Brute-force string matching with character-comparison counting. Run: python q3_string_matching.py"""
import json, csv, os, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results"); os.makedirs(RES, exist_ok=True)
SHOT = os.path.join(HERE, "..", "Output_Screenshots")


def brute_force(text, pat):
    n, m = len(text), len(pat); comps = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pat[j]:
                break
            j += 1
        if j == m:
            return i, comps
    return -1, comps


def text_A(n=10000):
    return ("abcdefghij" * (n // 10 + 1))[:n], "ZERO#ALRT"


def text_B(n=10000, m=50):
    return "A" * n, "A" * (m - 1) + "B"


def text_C():
    users = ["guest", "admin1", "svc_bk", "alice", "bob", "carol", "dave", "erin"]
    lines = []
    for k in range(180):
        u = users[k % len(users)]
        lines.append(f"2026-10-28 10:{k % 60:02d}:{(k * 7) % 60:02d} AUTH FAILED user={u} ip=10.0.{k % 8}.{k % 250}\n")
    lines.append("2026-10-28 11:59:59 AUTH FAILED user=root ip=10.0.0.99\n")
    return "".join(lines), "AUTH FAILED user=root"


def report(name, text, pat, pred_lo, pred_hi=None, extra=""):
    n, m = len(text), len(pat)
    pos, c = brute_force(text, pat)
    t0 = time.perf_counter(); brute_force(text, pat); ms = (time.perf_counter() - t0) * 1e3
    print(f"{name}: n={n}, m={m}, match at {pos}, comparisons={c:,}, comps/n={c / n:.2f}, time={ms:.2f} ms  {extra}")
    print(f"    prediction: {pred_lo}" + (f" .. {pred_hi}" if pred_hi else ""))
    return dict(test=name, n=n, m=m, position=pos, comparisons=c, ratio_c_over_n=round(c / n, 3), time_ms=round(ms, 3))


if __name__ == "__main__":
    rows = []
    print("=== Q3: brute-force string matching - three designed conditions ===")
    t, p = text_A(); rows.append(report("A low work ", t, p, f"n-m+1 = {len(t) - len(p) + 1:,}"))
    t, p = text_B(); rows.append(report("B high work", t, p, f"(n-m+1)*m = {(len(t) - len(p) + 1) * len(p):,}"))
    t, p = text_C(); rows.append(report("C log text ", t, p, f"{int(1.1 * len(t)):,}", f"{int(1.5 * len(t)):,}"))
    print("\n=== Extra tests ===")
    t, p = text_B(10000, 50); rows.append(report("D match at start", "AUTH FAILED user=root" + t, "AUTH FAILED user=root", "m = 21"))
    rows.append(report("E pattern longer than text", "abc", "abcdef", "0 (no alignment)"))

    print("\n=== Scaling with n (m fixed) ===")
    print(f"{'n':>8}{'A: comps':>12}{'A: n-m+1':>12}{'B(m=50): comps':>16}{'B: (n-m+1)m':>14}{'ratio B/A':>11}")
    sc = []
    for n in (1000, 2000, 4000, 8000, 16000, 32000):
        ta, pa = text_A(n); tb, pb = text_B(n, 50)
        ca = brute_force(ta, pa)[1]; cb = brute_force(tb, pb)[1]
        sc.append((n, ca, cb)); print(f"{n:>8}{ca:>12,}{n - len(pa) + 1:>12,}{cb:>16,}{(n - 50 + 1) * 50:>14,}{cb / ca:>11.1f}")

    print("\n=== Effect of pattern length m on text of n=10,000 'A's (B-type pattern) ===")
    print(f"{'m':>6}{'comparisons':>14}{'(n-m+1)*m':>14}")
    ms = []
    for m in (5, 10, 25, 50, 100, 200, 500, 1000, 2500, 5000):
        tb, pb = text_B(10000, m); c = brute_force(tb, pb)[1]
        ms.append((m, c)); print(f"{m:>6}{c:>14,}{(10000 - m + 1) * m:>14,}")

    with open(os.path.join(RES, "q3_raw.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    json.dump({"rows": rows, "scale": sc, "m_effect": ms}, open(os.path.join(RES, "q3_raw.json"), "w"), indent=1)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot([s[0] for s in sc], [s[1] for s in sc], "o-", label="A: mismatch on first char")
    ax[0].plot([s[0] for s in sc], [s[2] for s in sc], "s-", label="B: 'AAA..AB' in 'AAAA..' (m=50)")
    ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("text length n"); ax[0].set_ylabel("character comparisons")
    ax[0].set_title("Same n, very different work"); ax[0].legend()
    ax[1].plot([m for m, c in ms], [c for m, c in ms], "o-")
    ax[1].set_xlabel("pattern length m (n = 10,000)"); ax[1].set_ylabel("character comparisons"); ax[1].set_title("Worst-case work peaks near m = n/2")
    plt.tight_layout(); plt.savefig(os.path.join(SHOT, "q3_graphs.png"), dpi=130)
