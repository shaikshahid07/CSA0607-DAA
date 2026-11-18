# QUESTION 5: FIND THE MAXIMUM ELEMENT IN LINEAR TIME

def find_maximum(nums):
    if len(nums) == 0:
        return None

    maximum = nums[0]
    for num in nums:
        if num > maximum:
            maximum = num

    return maximum


nums = list(map(int, input("Enter array elements: ").split()))
result = find_maximum(nums)

if result is None:
    print("The list is empty.")
else:
    print("Maximum element:", result)
