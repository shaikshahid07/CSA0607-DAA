# QUESTION 3: SUM OF SQUARES OF DISTINCT COUNTS OF ALL SUBARRAYS

def sum_counts(nums):
    total = 0
    n = len(nums)

    for i in range(n):
        distinct = set()
        for j in range(i, n):
            distinct.add(nums[j])
            count = len(distinct)
            total += count * count

    return total


nums = list(map(int, input("Enter array elements: ").split()))
result = sum_counts(nums)
print("Sum of squares of distinct counts:", result)
