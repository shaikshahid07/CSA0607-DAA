# QUESTION 8: SORT AN ARRAY USING BUBBLE SORT

def bubble_sort(nums):
    n = len(nums)

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True

        if not swapped:
            break

    return nums


nums = list(map(int, input("Enter array elements: ").split()))
result = bubble_sort(nums)
print("Sorted array:", result)
