# QUESTION 7: CREATE A LIST CONTAINING ONLY UNIQUE ELEMENTS

def unique_elements(nums):
    result = []
    seen = set()

    for num in nums:
        if num not in seen:
            result.append(num)
            seen.add(num)

    return result


nums = list(map(int, input("Enter array elements: ").split()))
result = unique_elements(nums)
print("List containing unique elements:", result)
