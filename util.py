def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def rank(arr, val):
    # given value 0-1 get nearest index from array
    return arr[int(val * len(arr))]
