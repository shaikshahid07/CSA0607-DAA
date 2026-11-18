# QUESTION 4: COUNT PAIRS WITH EQUAL VALUES AND PRODUCT OF INDICES DIVISIBLE BY K

def count_pairs(nums, k):
    count = 0
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j] and (i * j) % k == 0:
                count += 1

    return count


nums = list(map(int, input("Enter array elements: ").split()))
k = int(input("Enter value of k: "))

result = count_pairs(nums, k)
print("Number of valid pairs:", result)
