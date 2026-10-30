"""
Generates the screenshots (code / terminal output PNGs), graphs and the merge-sort diagram
used in the reports.  Run from the repository root:  python3 Supporting_Files/tools/make_assets.py
"""
import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SHOTS = os.path.join(ROOT, "Supporting_Files", "screenshots")
GRAPHS = os.path.join(ROOT, "Supporting_Files", "graphs")
DATA = os.path.join(ROOT, "Supporting_Files", "datasets")
os.makedirs(SHOTS, exist_ok=True)
os.makedirs(GRAPHS, exist_ok=True)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SIZE = 15

plt.rcParams.update({
    "font.family": "Liberation Serif", "font.size": 11, "axes.grid": True,
    "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})
C1, C2, C3, GREY = "#1f4e79", "#c0504d", "#2e7d32", "#555555"


def rd(path):
    with open(os.path.join(ROOT, path)) as f:
        return f.read().split("\n")


def shot(lines, title, name, numbered=None):
    """Render lines of text as a white 'terminal/editor' screenshot."""
    f = ImageFont.truetype(FONT, SIZE)
    fb = ImageFont.truetype(FONT_B, SIZE)
    lh = SIZE + 6
    gutter = 0
    if numbered:
        gutter = 6 * (SIZE - 5) + 14
    maxlen = max(len(l) for l in lines) if lines else 10
    cw = f.getlength("M")
    w = int(gutter + maxlen * cw + 40)
    w = max(w, 640)
    head = 34
    h = int(head + len(lines) * lh + 24)
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w - 1, head - 1], fill="#e8e8e8")
    d.line([0, head - 1, w, head - 1], fill="#b0b0b0")
    for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        d.ellipse([12 + i * 20, 11, 24 + i * 20, 23], fill=c)
    d.text((82, 8), title, font=fb, fill="#222222")
    y = head + 10
    for i, line in enumerate(lines):
        if numbered:
            d.text((8, y), f"{numbered + i:>4}", font=f, fill="#999999")
            d.line([gutter - 6, y - 3, gutter - 6, y + lh - 3], fill="#dddddd")
        colour = "#111111"
        s = line.lstrip()
        if numbered and s.startswith("#"):
            colour = "#2e7d32"
        elif not numbered and (s.startswith("MERGE") or "OK" == s[-2:]):
            colour = "#1f4e79"
        d.text((gutter + 8, y), line, font=f, fill=colour)
        y += lh
    d.rectangle([0, 0, w - 1, h - 1], outline="#b0b0b0")
    img.save(os.path.join(SHOTS, name))
    return os.path.join(SHOTS, name)


def code_shot(rel, start, end, name):
    lines = rd(rel)[start - 1:end]
    return shot(lines, f"{os.path.basename(rel)}  (lines {start}-{end})", name, numbered=start)


def out_shot(rel, start, end, name, title=None):
    lines = rd(rel)[start - 1:end]
    return shot(lines, title or "Terminal  -  python3 " + os.path.basename(rel).replace("output.txt", ""), name)


def find(rel, text, nth=1):
    for n, l in enumerate(rd(rel), 1):
        if text in l:
            nth -= 1
            if nth == 0:
                return n
    raise ValueError(text)


def build_shots():
    M1c, M1o = "Module_1_Merge_Sort/Source_Code/merge_sort.py", "Module_1_Merge_Sort/Report/output.txt"
    M2c, M2o = "Module_2_Quick_Sort/Source_Code/quick_sort.py", "Module_2_Quick_Sort/Report/output.txt"
    M3c, M3o = "Module_3_Binary_Search/Source_Code/binary_search.py", "Module_3_Binary_Search/Report/output.txt"
    M4c, M4o = ("Module_4_Strassen_Matrix_Multiplication/Source_Code/strassen.py",
                "Module_4_Strassen_Matrix_Multiplication/Report/output.txt")

    # ---- Module 1
    code_shot(M1c, find(M1c, "def merge(arr"), find(M1c, "def sort_orders") - 2, "m1_code_merge_sort.png")
    out_shot(M1o, 1, find(M1o, "COMPARISON ESTIMATES") - 3, "m1_output_trace.png", "Terminal  -  python3 merge_sort.py")
    out_shot(M1o, find(M1o, "COMPARISON ESTIMATES") - 1, find(M1o, "TIMING") - 1, "m1_output_analysis.png",
             "Terminal  -  python3 merge_sort.py (continued)")
    # ---- Module 2
    code_shot(M2c, find(M2c, "def partition_first"), find(M2c, "# ---------------------------------------------------------------- proposed design") - 2,
              "m2_code_quick_sort.png")
    code_shot(M2c, find(M2c, "def median_of_three_index"), find(M2c, "def quick_sort_random") - 2, "m2_code_improved.png")
    out_shot(M2o, 1, find(M2o, "ESTIMATES FOR") - 2, "m2_output_partition.png", "Terminal  -  python3 quick_sort.py")
    out_shot(M2o, find(M2o, "ESTIMATES FOR") - 1, len(rd(M2o)) - 1, "m2_output_analysis.png",
             "Terminal  -  python3 quick_sort.py (continued)")
    # ---- Module 3
    code_shot(M3c, find(M3c, "def binary_search_any"), find(M3c, "def binary_search_recursive") - 2, "m3_code_binary_search.png")
    out_shot(M3o, 1, find(M3o, "Search for 105") - 2, "m3_output_search.png", "Terminal  -  python3 binary_search.py")
    out_shot(M3o, find(M3o, "Why sorted order matters"), len(rd(M3o)) - 1, "m3_output_analysis.png",
             "Terminal  -  python3 binary_search.py (continued)")
    # ---- Module 4
    code_shot(M4c, find(M4c, "def strassen(A, B"), find(M4c, "# ---------------------------------------------------------------- numpy hybrid") - 2,
              "m4_code_strassen.png")
    out_shot(M4o, 1, find(M4o, "SCALAR OPERATIONS FOR") - 2, "m4_output_sample.png", "Terminal  -  python3 strassen.py")
    out_shot(M4o, find(M4o, "SCALAR OPERATIONS FOR") - 1, find(M4o, "TIMING (numpy") - 1, "m4_output_counts.png",
             "Terminal  -  python3 strassen.py (continued)")


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPHS, name), dpi=170)
    plt.close(fig)


def build_graphs():
    # Module 1
    r = read_csv("merge_sort_timing.csv")
    n = [int(x["n"]) for x in r]
    cm = [int(x["comparisons"]) for x in r]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(n, cm, "o-", color=C1, label="measured comparisons")
    ax[0].plot(n, [x * math.log2(x) - x + 1 for x in n], "s--", color=C2, label=r"$n\lg n - n + 1$")
    ax[0].set(xlabel="n (orders)", ylabel="comparisons", title="Merge Sort: comparisons"); ax[0].legend()
    ax[1].plot(n, [float(x["seconds"]) for x in r], "o-", color=C1, label="Merge Sort (random data)")
    k = float(r[-1]["seconds"]) / (n[-1] * math.log2(n[-1]))
    ax[1].plot(n, [k * x * math.log2(x) for x in n], "--", color=GREY, label=r"$c\,n\lg n$ fit")
    ax[1].set(xlabel="n (orders)", ylabel="seconds", title="Merge Sort: running time"); ax[1].legend()
    save(fig, "m1_merge_sort_graph.png")

    # Module 2
    r = read_csv("quick_sort_timing.csv")
    n = [int(x["n"]) for x in r]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(n, [int(x["first_cmp"]) for x in r], "o-", color=C2, label="first-element pivot")
    ax[0].plot(n, [int(x["median3_cmp"]) for x in r], "s-", color=C1, label="median-of-three")
    ax[0].plot(n, [int(x["random_cmp"]) for x in r], "^-", color=C3, label="random pivot")
    ax[0].plot(n, [x * (x - 1) / 2 for x in n], ":", color=GREY, label=r"$n(n-1)/2$")
    ax[0].set(xlabel="n (sellers)", ylabel="comparisons", yscale="log", title="Nearly sorted data: comparisons"); ax[0].legend(fontsize=8)
    ax[1].plot(n, [float(x["first_s"]) for x in r], "o-", color=C2, label="first-element pivot")
    ax[1].plot(n, [float(x["median3_s"]) for x in r], "s-", color=C1, label="median-of-three")
    ax[1].plot(n, [float(x["random_s"]) for x in r], "^-", color=C3, label="random pivot")
    ax[1].set(xlabel="n (sellers)", ylabel="seconds", title="Nearly sorted data: running time"); ax[1].legend(fontsize=8)
    save(fig, "m2_quick_sort_graph.png")

    # Module 3
    ns = [10 ** k for k in range(1, 8)]
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.plot(ns, [math.floor(math.log2(x)) + 1 for x in ns], "o-", color=C1, label=r"binary search $\lfloor\lg n\rfloor+1$")
    ax.plot(ns, ns, "s--", color=C2, label="linear search (worst case n)")
    ax.set(xscale="log", yscale="log", xlabel="n (orders)", ylabel="comparisons", title="Order lookup: comparisons")
    ax.legend(fontsize=8)
    save(fig, "m3_binary_search_graph.png")

    # Module 4 : operation counts
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "strassen", os.path.join(ROOT, "Module_4_Strassen_Matrix_Multiplication", "Source_Code", "strassen.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    sizes = [2 ** k for k in range(1, 12)]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot(sizes, [x ** 3 for x in sizes], "o-", color=C2, label=r"conventional $n^3$")
    ax[0].plot(sizes, [mod.strassen_mults(x) for x in sizes], "s-", color=C1, label=r"Strassen $7^{\lg n}$")
    ax[0].plot(sizes, [mod.strassen_mults(x, 64) for x in sizes], "^-", color=C3, label="hybrid (cutoff 64)")
    ax[0].set(xscale="log", yscale="log", xlabel="n", ylabel="scalar multiplications", title="Multiplication count"); ax[0].legend(fontsize=8)
    cuts = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    tot = [mod.strassen_mults(1024, c) + mod.strassen_adds(1024, c) for c in cuts]
    ax[1].plot(cuts, [t / 1e9 for t in tot], "o-", color=C1)
    ax[1].axhline((1024 ** 3 + 1024 ** 2 * 1023) / 1e9, color=C2, ls="--", label="conventional")
    ax[1].set(xscale="log", xlabel="cutoff size", ylabel="total operations (x10$^9$)", title="n = 1024: mults + adds vs cutoff"); ax[1].legend(fontsize=8)
    save(fig, "m4_strassen_operations_graph.png")

    r = read_csv("strassen_cutoff.csv")
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.plot([int(x["cutoff"]) for x in r], [float(x["seconds"]) for x in r], "o-", color=C1)
    ax.set(xscale="log", yscale="log", xlabel="cutoff (leaf size)", ylabel="seconds (n = 512)",
           title="Measured hybrid time vs cutoff (numpy leaves)")
    save(fig, "m4_cutoff_timing_graph.png")

    # Final summary graph : operations at the production workloads
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    labels = ["Merge Sort\n10^7 orders", "Quick Sort first pivot\n10^5 sellers (worst)",
              "Quick Sort median-of-3\n10^5 sellers", "Binary search\n10^7 orders"]
    vals = [10_000_000 * math.ceil(math.log2(10_000_000)) - 2 ** 24 + 1, 100_000 * 99_999 // 2,
            100_000 * math.log2(100_000), 24]
    bars = ax.bar(labels, vals, color=[C1, C2, C3, GREY])
    ax.set_yscale("log"); ax.set_ylabel("comparisons (log scale)"); ax.set_title("Comparisons at production workloads")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.2, f"{v:,.0f}", ha="center", fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    save(fig, "final_workload_comparisons.png")


def build_merge_tree():
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 50)
    def box(x, y, text, w=14, fc="white"):
        ax.text(x, y, text, ha="center", va="center", fontsize=8.2,
                bbox=dict(boxstyle="square,pad=0.35", fc=fc, ec="black", lw=0.8))
    def line(x1, y1, x2, y2, ls="-"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-", lw=0.8, ls=ls))
    # divide levels (top half)
    ax.text(1, 48, "DIVIDE", fontsize=9, fontweight="bold")
    box(50, 45, "105 O1 | 102 O2 | 105 O3 | 101 O4 | 102 O5 | 103 O6", w=40)
    box(27, 36, "105 O1 | 102 O2 | 105 O3"); box(73, 36, "101 O4 | 102 O5 | 103 O6")
    box(17, 27, "105 O1 | 102 O2"); box(37, 27, "105 O3")
    box(63, 27, "101 O4 | 102 O5"); box(83, 27, "103 O6")
    box(10, 19.5, "105 O1"); box(24, 19.5, "102 O2"); box(56, 19.5, "101 O4"); box(70, 19.5, "102 O5")
    for a, b in [((50, 43), (27, 38)), ((50, 43), (73, 38)), ((27, 34), (17, 29)), ((27, 34), (37, 29)),
                 ((73, 34), (63, 29)), ((73, 34), (83, 29)), ((17, 25), (10, 21.5)), ((17, 25), (24, 21.5)),
                 ((63, 25), (56, 21.5)), ((63, 25), (70, 21.5))]:
        line(*a, *b)
    # merge (bottom)
    ax.text(1, 13.5, "COMBINE (merges, in order)", fontsize=9, fontweight="bold")
    box(17, 8.5, "M1: 102 O2 | 105 O1", fc="#eef3f8"); box(63, 8.5, "M3: 101 O4 | 102 O5", fc="#eef3f8")
    box(30, 2.5, "M2: 102 O2 | 105 O1 | 105 O3", fc="#eef3f8", w=20)
    box(80, 2.5, "M4: 101 O4 | 102 O5 | 103 O6", fc="#eef3f8", w=20)
    box(50, -3.5 + 3, "", w=1)
    ax.text(50, -1.5, "M5 (final): 101 O4 | 102 O2 | 102 O5 | 103 O6 | 105 O1 | 105 O3", ha="center", fontsize=8.5,
            bbox=dict(boxstyle="square,pad=0.4", fc="#dfe9f3", ec="black", lw=1))
    ax.set_ylim(-4, 50)
    save(fig, "m1_merge_tree.png")


if __name__ == "__main__":
    build_shots()
    build_graphs()
    build_merge_tree()
    print("assets created:", len(os.listdir(SHOTS)), "screenshots,", len(os.listdir(GRAPHS)), "graphs")
