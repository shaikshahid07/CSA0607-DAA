"""
Generates graphs, flowcharts and rendered code/output images from results.json.
Name: Shaik Shahid, Reg. No. 192424311  |  CSA0607 CO1 Assignment
Run after run_experiments.py:  python make_figures.py
"""
import json, os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
GRAPHS = os.path.join(ROOT, "Report", "Tables_and_Graphs")
SRC_SHOTS = os.path.join(ROOT, "Report", "Source_Code_Screenshots")
OUT_SHOTS = os.path.join(ROOT, "Report", "Output_Screenshots")
T1 = os.path.join(ROOT, "Task_1_Algorithm_Design")
for d in (GRAPHS, SRC_SHOTS, OUT_SHOTS, T1):
    os.makedirs(d, exist_ok=True)

plt.rcParams.update({"font.family": "Liberation Serif", "font.size": 11,
                     "axes.facecolor": "white", "figure.facecolor": "white",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": "#dddddd", "grid.linewidth": 0.6})

R = json.load(open(os.path.join(HERE, "results.json")))
N = [r["n"] for r in R]
C = {"linear": "#1f3a5f", "binary_rec": "#b5482a", "binary_iter": "#b5482a", "hash": "#2e7d4f"}
LAB = {"linear": "Linear search", "binary_rec": "Binary search (recursive)",
       "binary_iter": "Binary search (iterative)", "hash": "Hash table"}
MK = {"linear": "o", "binary_rec": "s", "binary_iter": "^", "hash": "D"}


def series(key):
    return [r[key] for r in R]


# ---------------------------------------------------------------- graphs
def fig_time(kind, fname, title):
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for a in ("linear", "binary_rec", "binary_iter", "hash"):
        ax.plot(N, [v * 1e6 for v in series(f"{a}_time_{kind}_s")], marker=MK[a], color=C[a],
                ls="--" if a == "binary_iter" else "-", lw=1.8, ms=6, label=LAB[a])
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Number of records, n"); ax.set_ylabel("Time per search (microseconds)")
    ax.set_title(title); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(GRAPHS, fname), dpi=200); plt.close(fig)


def fig_comparisons():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for a in ("linear", "binary_rec", "hash"):
        ax.plot(N, series(f"{a}_cmp_avg"), marker=MK[a], color=C[a], lw=1.8, ms=6, label=LAB[a] + " (measured)")
    nn = np.array(N, float)
    ax.plot(N, nn / 2, color="#888888", ls=":", lw=1.2, label="n/2 (theory, linear)")
    ax.plot(N, np.log2(nn) - 1, color="#888888", ls="-.", lw=1.2, label="log2(n) - 1 (theory, binary)")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Number of records, n"); ax.set_ylabel("Average key comparisons per search")
    ax.set_title("Average comparisons vs input size"); ax.legend(frameon=False, fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(GRAPHS, "fig_comparisons_vs_n.png"), dpi=200); plt.close(fig)


def fig_preproc():
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(N, series("sort_time_s"), marker="s", color=C["binary_rec"], lw=1.8, label="Sorting (for binary search)")
    ax.plot(N, series("hash_build_time_s"), marker="D", color=C["hash"], lw=1.8, label="Hash table build")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Number of records, n"); ax.set_ylabel("Preprocessing time (seconds)")
    ax.set_title("Preprocessing cost vs input size"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(GRAPHS, "fig_preprocessing.png"), dpi=200); plt.close(fig)


def total_cost(r, k):
    """Total seconds to serve k searches including preprocessing (one build)."""
    return {"linear": k * r["linear_time_avg_s"],
            "binary": r["sort_time_s"] + k * r["binary_rec_time_avg_s"],
            "hash": r["hash_build_time_s"] + k * r["hash_time_avg_s"]}


def fig_total():
    r = R[-1]
    ks = np.logspace(0, 6, 60)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for name, col, lab in (("linear", C["linear"], "Linear (no preprocessing)"),
                           ("binary", C["binary_rec"], "Sort + binary search"),
                           ("hash", C["hash"], "Build hash table + lookup")):
        ax.plot(ks, [total_cost(r, k)[name] for k in ks], color=col, lw=1.8, label=lab)
    ax.axvline(50000, color="#555555", ls=":", lw=1)
    ax.text(50000 * 1.15, ax.get_ylim()[0] * 3 if False else 2e-2, "50,000 searches", rotation=90, fontsize=9, color="#555555")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Number of searches served per build, k"); ax.set_ylabel("Total time incl. preprocessing (seconds)")
    ax.set_title("Total cost at n = 1,000,000"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(GRAPHS, "fig_total_cost_1M.png"), dpi=200); plt.close(fig)


# ---------------------------------------------------------------- flowcharts
def box(ax, x, y, w, h, text, kind="proc"):
    if kind == "term":
        p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.25", fc="white", ec="black", lw=1.2)
        ax.add_patch(p)
    elif kind == "dec":
        ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], closed=True, fc="white", ec="black", lw=1.2))
    else:
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec="black", lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5)


def arrow(ax, x1, y1, x2, y2, label=None, lx=0.12, ly=0.0, head=True):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->" if head else "-", lw=1.1, color="black", shrinkA=0, shrinkB=0))
    if label:
        ax.text((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, fontsize=9.5)


def flow(fname, title, nodes, arrows, size=(5.6, 8.2), xlim=(0, 10), ylim=(0, 16)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold")
    for n in nodes:
        box(ax, *n)
    for a in arrows:
        arrow(ax, *a)
    fig.tight_layout(); fig.savefig(os.path.join(T1, fname), dpi=200); plt.close(fig)
    fig2 = None


def flowcharts():
    # Linear search
    flow("flowchart_linear_search.png", "Flowchart: Linear Search (iterative)",
         [(5, 15, 3.4, 1, "Start", "term"), (5, 13, 5.2, 1, "Input A[0..n-1], key K", "proc"),
          (5, 11, 3, 1, "i = 0", "proc"), (5, 8.8, 4.0, 1.8, "i < n ?", "dec"),
          (5, 5.8, 4.0, 1.8, "A[i] == K ?", "dec"), (8.7, 5.8, 2.4, 1, "i = i + 1", "proc"),
          (1.3, 8.8, 2.2, 1, "return -1", "proc"), (5, 3.7, 3.0, 1, "return i", "proc"),
          (5, 1.8, 3.4, 1, "Stop", "term")],
         [(5, 14.5, 5, 13.5), (5, 12.5, 5, 11.5), (5, 10.5, 5, 9.7),
          (5, 7.9, 5, 6.7, "Yes", 0.15, 0.0), (3.0, 8.8, 2.4, 8.8, "No", -0.2, 0.2),
          (5, 4.9, 5, 4.2, "Yes", 0.15, 0.0), (7.0, 5.8, 7.5, 5.8, "No", -0.1, 0.25),
          (8.7, 6.3, 8.7, 8.8, None, 0, 0, False), (8.7, 8.8, 7.0, 8.8),
          (5, 3.2, 5, 2.3),
          (1.3, 8.3, 1.3, 1.8, None, 0, 0, False), (1.3, 1.8, 3.3, 1.8)])
    # Recursive binary search
    flow("flowchart_binary_search_recursive.png", "Flowchart: Binary Search (recursive)",
         [(5, 15.2, 4.4, 1, "Start: BS(A, K, low, high)", "term"),
          (5, 12.8, 4.2, 1.8, "low > high ?", "dec"),
          (5, 10.2, 5.6, 1, "mid = floor((low + high) / 2)", "proc"),
          (5, 8, 4.2, 1.8, "A[mid] == K ?", "dec"),
          (5, 5.4, 4.2, 1.8, "K < A[mid] ?", "dec"),
          (1.3, 12.8, 2.4, 1, "return -1\n(base case)", "proc"), (8.8, 8, 2.2, 1, "return mid", "proc"),
          (2.3, 2.6, 4.2, 1.4, "return BS(A, K,\nlow, mid-1)\n[left half]", "proc"),
          (7.7, 2.6, 4.2, 1.4, "return BS(A, K,\nmid+1, high)\n[right half]", "proc")],
         [(5, 14.7, 5, 13.7), (2.9, 12.8, 2.5, 12.8, "Yes", -0.1, 0.25),
          (5, 11.9, 5, 10.7, "No", 0.15, 0), (5, 9.7, 5, 8.9),
          (7.1, 8, 7.7, 8, "Yes", -0.1, 0.25), (5, 7.1, 5, 6.3, "No", 0.15, 0),
          (2.9, 5.4, 2.3, 3.3, "Yes", -0.8, 0.0), (7.1, 5.4, 7.7, 3.3, "No", 0.2, 0.0)])
    # Hash
    flow("flowchart_hash_lookup.png", "Flowchart: Hash Table (build once, then lookup)",
         [(5, 15.2, 3.4, 1, "Start", "term"),
          (5, 13.2, 7.4, 1.1, "BUILD: m = prime near 1.5n; create m empty buckets", "proc"),
          (5, 11.2, 7.4, 1.1, "for each record k: append k to bucket[k mod m]", "proc"),
          (5, 9.2, 5.2, 1, "SEARCH: h = K mod m", "proc"),
          (5, 7.0, 4.8, 1.8, "K in bucket[h] ?", "dec"),
          (1.9, 4.0, 3.0, 1.0, "return FOUND", "proc"), (8.1, 4.0, 3.2, 1.0, "return NOT FOUND", "proc"),
          (5, 1.6, 3.4, 1, "Stop", "term")],
         [(5, 14.7, 5, 13.75), (5, 12.65, 5, 11.75), (5, 10.65, 5, 9.7), (5, 8.7, 5, 7.9),
          (2.6, 7.0, 1.9, 4.5, "Yes", -0.7, 0.0), (7.4, 7.0, 8.1, 4.5, "No", 0.2, 0.0),
          (1.9, 3.5, 4.0, 1.9), (8.1, 3.5, 6.0, 1.9)])


# ---------------------------------------------------------------- rendered code / output images
def render_text(text, path, title, per_page=42, width=7.6, wrap=98):
    lines = []
    for ln in text.rstrip("\n").split("\n"):
        ln = ln.replace("\t", "    ")
        chunks = textwrap.wrap(ln, wrap, subsequent_indent="      ", replace_whitespace=False, drop_whitespace=False) or [""]
        lines.extend(chunks)
    pages = [lines[i:i + per_page] for i in range(0, len(lines), per_page)] or [[""]]
    outs = []
    for pi, pg in enumerate(pages, 1):
        h = 0.9 + 0.2 * len(pg)
        fig = plt.figure(figsize=(width, h))
        fig.patch.set_facecolor("white")
        fig.text(0.01, 1 - 0.35 / h, f"{title}  (rendered, page {pi}/{len(pages)})", fontsize=10, family="Liberation Serif", fontweight="bold", va="center")
        for li, ln in enumerate(pg):
            n0 = (pi - 1) * per_page + li + 1
            y = 1 - (0.75 + 0.2 * li) / h
            fig.text(0.01, y, f"{n0:>3}", fontsize=8.2, family="DejaVu Sans Mono", color="#888888", va="center")
            fig.text(0.06, y, ln, fontsize=8.2, family="DejaVu Sans Mono", va="center")
        p = path if len(pages) == 1 else path.replace(".png", f"_p{pi}.png")
        fig.savefig(p, dpi=200); plt.close(fig); outs.append(p)
    return outs


def screenshots():
    for fn in ("search_algorithms.py", "run_experiments.py", "make_figures.py"):
        txt = open(os.path.join(HERE, fn)).read()
        render_text(txt, os.path.join(SRC_SHOTS, fn.replace(".py", ".png")), f"Source: {fn}")
    out = open(os.path.join(OUT_SHOTS, "console_output.txt")).read()
    render_text("$ python run_experiments.py\n" + out, os.path.join(OUT_SHOTS, "console_output.png"), "Terminal output", per_page=60)


if __name__ == "__main__":
    fig_time("avg", "fig_avg_time_vs_n.png", "Average search time vs input size")
    fig_time("absent", "fig_worst_time_vs_n.png", "Worst-case (key absent) search time vs input size")
    fig_comparisons(); fig_preproc(); fig_total(); flowcharts(); screenshots()
    print("figures written")
