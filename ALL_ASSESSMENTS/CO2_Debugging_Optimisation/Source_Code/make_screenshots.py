"""
Renders the saved execution logs (Supporting_Files/execution_logs/*.txt) as terminal-style PNG images
(Supporting_Files/screenshots/*.png) for the report.  The text in every image is copied unchanged from the
log file produced by really running the script; nothing is typed by hand.

Run with:   python make_screenshots.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent / "Supporting_Files"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG, FG, BAR = (30, 30, 30), (220, 220, 220), (60, 60, 60)
OK, BAD, DIM = (120, 220, 120), (240, 110, 110), (150, 150, 150)


def render(lines, command, out_name, max_width=1100):
    longest = max(len(l) for l in lines + [command])
    size = max(10, min(15, int((max_width - 40) / (longest * 0.602))))
    font = ImageFont.truetype(FONT, size)
    cw = font.getlength("M")
    lh = int(size * 1.45)
    width = int(cw * longest + 40)
    height = int(lh * (len(lines) + 1) + 70)
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, 34], fill=BAR)
    for k, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse([14 + 22 * k, 11, 26 + 22 * k, 23], fill=c)
    d.text((90, 8), "Terminal - SentinelOps", font=ImageFont.truetype(FONT, 13), fill=DIM)
    y = 46
    d.text((20, y), "$ " + command, font=font, fill=(130, 190, 255))
    y += lh
    for line in lines:
        color = FG
        if "[PASS]" in line or "RESULT:" in line and "0 failed" in line:
            color = OK
        elif "[FAIL]" in line:
            color = BAD
        d.text((20, y), line, font=font, fill=color)
        y += lh
    img.save(ROOT / "screenshots" / out_name)
    return out_name


def read(name):
    return (ROOT / "execution_logs" / name).read_text().rstrip("\n").split("\n")


def split_at(lines, marker_test):
    parts, cur = [], []
    for l in lines:
        if marker_test(l) and cur:
            parts.append(cur)
            cur = []
        cur.append(l)
    parts.append(cur)
    return parts


made = []
made.append(render(read("01_original_run.txt"), "python original_module.py", "s01_original_run.png"))

dbg = split_at(read("02_debug_steps_run.txt"), lambda l: l.startswith("=" * 20))
for tag, part in zip(("a_insertion_trace", "b_alignment_table", "c_staged_fixes"), dbg):
    made.append(render(part, "python debug_steps.py", f"s02{tag}.png"))

made.append(render(read("03_corrected_run.txt"), "python corrected_module.py", "s03_corrected_run.png"))
made.append(render(read("04_optimised_run.txt"), "python optimised_module.py", "s04_optimised_run.png"))

h = read("05_test_harness_run.txt")
blanks = [i for i, line in enumerate(h) if not line.strip()]
cuts = [min(blanks, key=lambda i: abs(i - target)) for target in (len(h) // 4, len(h) // 2, 3 * len(h) // 4)]
chunks = [h[:cuts[0]], h[cuts[0] + 1:cuts[1]], h[cuts[1] + 1:cuts[2]], h[cuts[2] + 1:]]
for tag, part in zip("abcd", chunks):
    made.append(render(part, "python test_harness.py", f"s05{tag}_test_harness.png"))

e = read("06_experiments_run.txt")
k = next(i for i, l in enumerate(e) if l.startswith("E4a"))
made.append(render(e[:k - 1], "python experiments.py   (part 1: E1 sorting, E2 blocklist, E3 signature)", "s06a_experiments_part1.png", 1250))
made.append(render(e[k:], "python experiments.py   (part 2: E4 closest pair)", "s06b_experiments_part2.png", 1250))
print("\n".join(made))
