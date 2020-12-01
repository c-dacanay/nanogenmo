def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def rank(arr, val):
    # given value 0-1 get nearest index from array
    val = clamp(val, 0, 0.99)
    return arr[int(val * len(arr))]

def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def scale(old_value, old_min, old_max, new_min, new_max):
    return( (old_value - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min
