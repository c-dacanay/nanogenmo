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

def adverb_rank(val):
    return rank([
        "scarcely",
        "barely",
        "hardly",
        "imperceptiby",
        "faintly",
        "sort oy",
        "more or less",
        "slightly",
        "moderately",
        "fairly",
        "kind of",
        "somewhat",
        "gently",
        "modestly",
        "pretty",
        "rather",
        "quite",
        "really",
        "very",
        "notably",
        "very much",
        "positively",
        "greatly",
        "strongly",
        "deeply",
        "entirely",
        "totally",
        "enormously",
        "extremely",
        "incredibly",
        "intensely",
        "thoroughly",
        "utterly",
        "absolutely",
        "completely",
    ], val)
