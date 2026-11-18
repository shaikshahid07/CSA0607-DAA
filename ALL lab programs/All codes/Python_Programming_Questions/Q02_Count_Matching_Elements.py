# QUESTION 2: COUNT MATCHING ELEMENTS IN TWO ARRAYS

def find_intersection_values(nums1, nums2):
    set1 = set(nums1)
    set2 = set(nums2)

    answer1 = sum(1 for num in nums1 if num in set2)
    answer2 = sum(1 for num in nums2 if num in set1)

    return [answer1, answer2]


nums1 = list(map(int, input("Enter first array: ").split()))
nums2 = list(map(int, input("Enter second array: ").split()))

result = find_intersection_values(nums1, nums2)
print("Output:", result)
