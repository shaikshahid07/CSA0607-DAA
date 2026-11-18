# QUESTION 13: CLIMBING STAIRS - COUNT DISTINCT WAYS

def climbing_stairs(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1

    first = 1
    second = 2

    for i in range(3, n + 1):
        current = first + second
        first = second
        second = current

    return second


n = int(input("Enter number of stairs: "))
result = climbing_stairs(n)
print("Number of distinct ways:", result)
