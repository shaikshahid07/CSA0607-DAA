# QUESTION 10: SORT AN ARRAY IN ASCENDING ORDER WITHOUT BUILT-IN SORTING

def heap_sort(nums):
    n = len(nums)

    def heapify(size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and nums[left] > nums[largest]:
            largest = left

        if right < size and nums[right] > nums[largest]:
            largest = right

        if largest != root:
            nums[root], nums[largest] = nums[largest], nums[root]
            heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]
        heapify(i, 0)

    return nums


nums = list(map(int, input("Enter array elements: ").split()))
result = heap_sort(nums)
print("Sorted array:", result)
