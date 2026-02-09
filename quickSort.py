import random

def randomized_quicksort(arr):
    def quicksort(l, r):
        if l >= r:
            return

        # random pivot
        pivot_index = random.randint(l, r)
        arr[l], arr[pivot_index] = arr[pivot_index], arr[l]
        pivot = arr[l]

        lt = l      # arr[l..lt-1] < pivot
        i = l + 1
        gt = r      # arr[gt+1..r] > pivot

        while i <= gt:
            if arr[i] < pivot:
                lt += 1
                arr[lt], arr[i] = arr[i], arr[lt]
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1

        arr[l], arr[lt] = arr[lt], arr[l]

        quicksort(l, lt - 1)
        quicksort(gt + 1, r)

    quicksort(0, len(arr) - 1)
    return arr
if __name__ == "__main__":
    # Test cases
    test_cases = {
        "Empty array": [],
        "Single element": [5],
        "Random array": [7, 2, 9, 4, 1, 5, 3],
        "Already sorted": [1, 2, 3, 4, 5, 6, 7],
        "Reverse sorted": [7, 6, 5, 4, 3, 2, 1],
        "With duplicates": [4, 2, 4, 1, 4, 3, 2]
    }

    for name, arr in test_cases.items():
        original = arr.copy()
        randomized_quicksort(arr)
        print(f"{name}:")
        print("  Original:", original)
        print("  Sorted:  ", arr)
        print("-" * 40)
