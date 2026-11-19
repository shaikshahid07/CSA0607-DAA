"""Task 4 - WordBreak: faulty algorithm, failing input, repair, regression."""
import time


def wordbreak_faulty(text, dictionary, verbose=False):
    n = len(text)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        for j in range(0, i):
            if text[j:i] in dictionary:          # BUG: DP[j] is not checked
                DP[i] = True
                if verbose:
                    print(f"  i={i}: substring '{text[j:i]}' (j={j}) in dictionary -> DP[{i}]=True")
                break
    return DP[n], DP


def wordbreak_fixed(text, dictionary, verbose=False):
    n = len(text)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        for j in range(0, i):
            if DP[j] and text[j:i] in dictionary:  # FIX: prefix text[0:j] must be breakable
                DP[i] = True
                if verbose:
                    print(f"  i={i}: DP[{j}]=True and '{text[j:i]}' in dictionary -> DP[{i}]=True")
                break
    return DP[n], DP


def wordbreak_optimised(text, dictionary):
    """Fixed algorithm + optimisation: only try words no longer than the longest dictionary word."""
    n = len(text)
    maxlen = max((len(w) for w in dictionary), default=0)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        for j in range(i - 1, max(-1, i - maxlen - 1), -1):
            if DP[j] and text[j:i] in dictionary:
                DP[i] = True
                break
    return DP[n]


def main():
    print("=== TASK 4: WordBreak forensics ===")
    text, dic = "catsanddogs", {"cats", "dogs"}   # 'and' missing -> cannot be segmented
    print("\n[Failing input] Text =", text, " Dictionary =", sorted(dic))
    print(" Faulty algorithm trace:")
    r1, dp1 = wordbreak_faulty(text, dic, verbose=True)
    print("  Faulty result:", r1, " DP =", [int(x) for x in dp1])
    print(" Fixed algorithm trace:")
    r2, dp2 = wordbreak_fixed(text, dic, verbose=True)
    print("  Fixed result:", r2, " DP =", [int(x) for x in dp2])
    print("  Correct answer is False (the middle 'and' is not a dictionary word)")

    print("\n[Regression input] Text = applepenapple  Dictionary = [apple, pen]")
    d = {"apple", "pen"}
    t = "applepenapple"
    print("  Faulty:", wordbreak_faulty(t, d)[0], " Fixed:", wordbreak_fixed(t, d)[0])

    print("\n[Additional tests, faulty vs fixed]")
    tests = [("", {"a"}), ("a", {"a"}), ("b", {"a"}),
             ("leetcode", {"leet", "code"}), ("catsandog", {"cats", "dog", "sand", "and", "cat"}),
             ("aaaa", {"a", "aa"}), ("xay", {"a"})]
    for t, d in tests:
        print(f"  Text='{t}' dict={sorted(d)} faulty={wordbreak_faulty(t, d)[0]} "
              f"fixed={wordbreak_fixed(t, d)[0]} optimised={wordbreak_optimised(t, d)}")

    print("\n[Performance: fixed vs length-bounded optimisation]")
    d = {"a", "aa", "aaa"}
    for n in (250, 500, 1000):
        t = "a" * (n - 1) + "b"
        t0 = time.perf_counter()
        r1 = wordbreak_fixed(t, d)[0]
        t1 = time.perf_counter()
        r2 = wordbreak_optimised(t, d)
        t2 = time.perf_counter()
        print(f"  n={n:>4}: fixed={1000*(t1-t0):9.2f} ms  optimised={1000*(t2-t1):7.2f} ms  same result={r1 == r2} ({r1})")


if __name__ == "__main__":
    main()
