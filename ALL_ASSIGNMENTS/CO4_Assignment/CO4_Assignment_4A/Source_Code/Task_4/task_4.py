"""Task 4 - Pseudocode forensics: faulty vs corrected WordBreak.
substring(Text, j, i) = characters at positions j+1 .. i (1-indexed), i.e. Text[j:i] in Python.
Author: Shaik Shahid | Reg No: 192424311 | CSA0607 Design and Analysis of Algorithms
"""
import random


def word_break_faulty(text, dictionary, trace=False):
    n = len(text)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        DP[i] = False
        for j in range(0, i):
            if text[j:i] in dictionary:                  # DEFECT: DP[j] is never checked
                DP[i] = True
                if trace:
                    print(f"  i={i}: j={j} '{text[j:i]}' in dictionary -> DP[{i}] = TRUE")
                break
        if trace and not DP[i]:
            print(f"  i={i}: no substring ending here is in the dictionary -> DP[{i}] = FALSE")
    return DP[n], DP


def word_break_fixed(text, dictionary, trace=False):
    n = len(text)
    DP = [False] * (n + 1)
    DP[0] = True
    for i in range(1, n + 1):
        DP[i] = False
        for j in range(0, i):
            if DP[j] and text[j:i] in dictionary:        # FIX: prefix text[0:j] must be segmentable
                DP[i] = True
                if trace:
                    print(f"  i={i}: j={j} DP[{j}]=TRUE and '{text[j:i]}' in dictionary -> DP[{i}] = TRUE")
                break
        if trace and not DP[i]:
            print(f"  i={i}: no j with DP[j]=TRUE and dictionary word -> DP[{i}] = FALSE")
    return DP[n], DP


def reference(text, dictionary):
    """Independent recursive reference answer (memoised)."""
    memo = {}

    def go(s):
        if s == "":
            return True
        if s in memo:
            return memo[s]
        memo[s] = any(s.startswith(w) and go(s[len(w):]) for w in dictionary)
        return memo[s]
    return go(text)


if __name__ == "__main__":
    text, dic = "catdog", {"ca", "dog"}
    print(f"=== Failing input: Text='{text}', Dictionary={sorted(dic)} ===")
    print("Faulty algorithm trace:")
    r1, d1 = word_break_faulty(text, dic, True)
    print("  DP =", d1, "-> returns", r1)
    print("Corrected algorithm trace:")
    r2, d2 = word_break_fixed(text, dic, True)
    print("  DP =", d2, "-> returns", r2)
    print("Reference answer:", reference(text, dic))
    assert r1 is True and r2 is False and reference(text, dic) is False

    text, dic = "catdog", {"cat", "dog"}
    print(f"\n=== Regression input: Text='{text}', Dictionary={sorted(dic)} ===")
    print("Faulty algorithm trace:")
    r1, d1 = word_break_faulty(text, dic, True)
    print("  DP =", d1, "-> returns", r1)
    print("Corrected algorithm trace:")
    r2, d2 = word_break_fixed(text, dic, True)
    print("  DP =", d2, "-> returns", r2)
    assert r1 is True and r2 is True and reference(text, dic) is True

    print("\n=== Extra cases ===")
    for t, dd in [("", {"a"}), ("a", {"a"}), ("aaaa", {"a", "aa"}), ("applepenapple", {"apple", "pen"}),
                  ("catsandog", {"cats", "dog", "sand", "and", "cat"}), ("xyz", {"yz"})]:
        print(f"  Text='{t}' Dict={sorted(dd)} -> faulty={word_break_faulty(t, dd)[0]}, "
              f"fixed={word_break_fixed(t, dd)[0]}, reference={reference(t, dd)}")

    print("\n=== Random validation (500 instances) ===")
    random.seed(5)
    faulty_wrong = 0
    for _ in range(500):
        t = "".join(random.choice("ab") for _ in range(random.randint(1, 8)))
        dd = {"".join(random.choice("ab") for _ in range(random.randint(1, 3))) for _ in range(random.randint(1, 3))}
        assert word_break_fixed(t, dd)[0] == reference(t, dd)
        faulty_wrong += word_break_faulty(t, dd)[0] != reference(t, dd)
    print(f"Corrected matched the reference on all 500; faulty was wrong on {faulty_wrong}.")
