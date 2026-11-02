import random
import time
import sys

random.seed(2026)

def brute_force_subset_sum(nums, target):
    sums = [0]
    for x in nums:
        sums = sums + [s + x for s in sums]
    return (target in sums), len(sums)

def all_subset_sums(nums):
    sums = [0]
    for x in nums:
        sums = sums + [s + x for s in sums]
    return sums

def meet_in_the_middle(nums, target):
    half = len(nums) // 2
    left = all_subset_sums(nums[:half])
    right = all_subset_sums(nums[half:])
    right.sort()
    left.sort()
    i = 0
    j = len(right) - 1
    steps = 0
    found = False
    while i < len(left) and j >= 0:
        steps += 1
        total = left[i] + right[j]
        if total == target:
            found = True
            break
        if total < target:
            i += 1
        else:
            j -= 1
    return found, len(left), len(right), steps

def find_subset(nums, target):
    half = len(nums) // 2
    left_nums = nums[:half]
    right_nums = nums[half:]
    left = {}
    for mask in range(2 ** len(left_nums)):
        s = 0
        for i in range(len(left_nums)):
            if mask >> i & 1:
                s += left_nums[i]
        left[s] = mask
    for mask in range(2 ** len(right_nums)):
        s = 0
        for i in range(len(right_nums)):
            if mask >> i & 1:
                s += right_nums[i]
        if target - s in left:
            chosen = []
            lm = left[target - s]
            for i in range(len(left_nums)):
                if lm >> i & 1:
                    chosen.append(left_nums[i])
            for i in range(len(right_nums)):
                if mask >> i & 1:
                    chosen.append(right_nums[i])
            return chosen
    return None

print("=" * 72)
print("Q6 (B) : MEET-IN-THE-MIDDLE SUBSET SUM")
print("=" * 72)

nums = [3, 34, 4, 12, 5, 2, 27, 8]
print("Demo numbers :", nums)
half = len(nums) // 2
print("Left half    :", nums[:half], " subset sums :", sorted(all_subset_sums(nums[:half])))
print("Right half   :", nums[half:], " subset sums :", sorted(all_subset_sums(nums[half:])))
for target in [9, 30, 95, 96, 100]:
    f1, total = brute_force_subset_sum(nums, target)
    f2, l, r, steps = meet_in_the_middle(nums, target)
    subset = find_subset(nums, target)
    print("target %-4d brute : %-5s  MITM : %-5s  subset = %s" % (target, f1, f2, subset))
print()

print("Experiment 1 : correctness on 300 random cases (n between 2 and 16)")
bad = 0
for i in range(300):
    n = random.randint(2, 16)
    data = [random.randint(1, 50) for j in range(n)]
    target = random.randint(1, sum(data) + 5)
    f1, total = brute_force_subset_sum(data, target)
    f2, l, r, steps = meet_in_the_middle(data, target)
    if f1 != f2:
        bad += 1
print("Wrong answers :", bad)
print()

print("Experiment 2 : search-space size (worst case = target NOT reachable)")
print("%-5s %-16s %-24s %-14s" % ("n", "Brute 2^n", "MITM 2*2^(n/2) sums", "Reduction"))
for n in [10, 16, 20, 24, 30, 40, 50, 60]:
    brute = 2 ** n
    mitm = 2 * 2 ** (n // 2)
    print("%-5d %-16d %-24d %-14.0f" % (n, brute, mitm, brute / mitm))
print()

print("Experiment 3 : running time and memory (target cannot be reached, so all sums are needed)")
print("%-5s %-14s %-14s %-16s %-16s" % ("n", "Brute time", "MITM time", "Brute stored", "MITM stored"))
rows = []
for n in [10, 14, 18, 20, 22, 24, 28, 32, 36, 40]:
    data = [random.randint(1000, 100000) * 2 for j in range(n)]
    target = sum(data) + 1
    if n <= 22:
        start = time.perf_counter()
        f1, stored1 = brute_force_subset_sum(data, target)
        t1 = time.perf_counter() - start
    else:
        t1 = float("nan")
        stored1 = 2 ** n
    start = time.perf_counter()
    f2, l, r, steps = meet_in_the_middle(data, target)
    t2 = time.perf_counter() - start
    print("%-5d %-14.5f %-14.5f %-16d %-16d" % (n, t1, t2, stored1, l + r))
    rows.append((n, t1, t2, stored1, l + r))
print("(brute force time is skipped for n above 22 : it would need 2^n sums in memory)")
print()

print("Experiment 4 : memory estimate for the stored lists (8 bytes per entry)")
print("%-5s %-18s %-18s" % ("n", "MITM memory", "Brute memory"))
for n in [20, 30, 40, 50]:
    mitm_bytes = 2 * 2 ** (n // 2) * 8
    brute_bytes = 2 ** n * 8
    print("%-5d %-18s %-18s" % (n, "%.2f MB" % (mitm_bytes / 1e6), "%.2f MB" % (brute_bytes / 1e6)))
print()

print("Experiment 5 : subset found when a solution exists (n = 30)")
data = [random.randint(1, 1000) for j in range(30)]
chosen = random.sample(data, 9)
target = sum(chosen)
subset = find_subset(data, target)
print("Target :", target)
print("Subset :", subset, " sum =", sum(subset))
