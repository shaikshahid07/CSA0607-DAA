# QUESTION 6: SORT THE LIST AND FIND ITS MAXIMUM ELEMENT

def find_maximum_after_sorting(nums):
    if len(nums) == 0:
        return None

    nums.sort()
    return nums[-1]


nums = list(map(int, input("Enter array elements: ").split()))
result = find_maximum_after_sorting(nums)

if result is None:
    print("The list is empty.")
else:
    print("Sorted list:", nums)
    print("Maximum element:", result)
