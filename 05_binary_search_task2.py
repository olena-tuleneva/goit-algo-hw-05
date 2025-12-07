def binary_search_with_upper_bound(arr, target):
    left = 0
    right = len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] >= target:
            upper_bound = arr[mid]
            right = mid - 1
        else:
            left = mid + 1

    return iterations, upper_bound

# Дані для тестування
numbers = [0.5, 1.2, 2.8, 3.3, 4.9, 5.7, 7.1]
target = 3.0

result = binary_search_with_upper_bound(numbers, target)
print(result)