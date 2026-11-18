# QUESTION 9: SEARCH FOR AN ELEMENT USING BINARY SEARCH
# This program sorts the input first because binary search requires sorted data.
# The displayed position is 1-based in the sorted array.

def binary_search(arr, key):
    arr.sort()
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == key:
            return mid + 1
        elif arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1


arr = list(map(int, input("Enter array elements: ").split()))
key = int(input("Enter key to search: "))
position = binary_search(arr, key)

if position != -1:
    print("Sorted array:", arr)
    print("Element", key, "is found at position", position)
else:
    print("Element", key, "is not found")
