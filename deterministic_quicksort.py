def deterministic_quicksort(arr):
    def quicksort(l, r):
        if l >= r:
            return

        pivot = arr[l]
        i = l + 1

        for j in range(l + 1, r + 1):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        arr[l], arr[i - 1] = arr[i - 1], arr[l]

        quicksort(l, i - 2)
        quicksort(i, r)

    quicksort(0, len(arr) - 1)
    return arr