from relationship import EventType
import math


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
    return ((old_value - old_min) /
            (old_max - old_min)) * (new_max - new_min) + new_min


def get_ab(event):
    a = event['protagonist'] if event.get('protagonist_initiated', True) else event[
        'person']
    b = event['person'] if event.get('protagonist_initiated', True) else event[
        'protagonist']
    return a, b


def joiner(val):
    return rank([
        "but",
        "yet",
        "and"
    ], val)

def oxford_comma(list, conj):
    assert conj == "and" or conj == "or"
    if len(list) == 0:
        return ''
    if len(list) == 1:
        return list[0]
    if len(list) == 2:
        return list[0] + f' {conj} ' + list[1]
    return ', '.join(list[:-1]) + f', {conj} ' + list[-1]

def adverb(val):
    return rank([
        "scarcely",
        "barely",
        "hardly",
        "imperceptiby",
        "faintly",
        "sort of",
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


def enthusiastically(val):
    return rank([
        'apprehensively',
        'hesitantly',
        'nervously',
        'carefully',
        'somewhat apprehensively',
        'somewhat hesitantly',
        'somewhat nervously',
        'somewhat carefully',
        '',
        'willingly',
        'happily',
        'joyfully',
        'enthusiastically',
        'very willingly',
        'very happily',
        'very joyfully',
        'very enthusiastically',
    ], val)


def get_event_meta(events):
    # Return a dict containing some summary statistics about the given array of events
    # Returns a count of all conflicts and delta changes for each conflict type
    # Returns a count of all experiences and delta changes for each conflict type
    concessions = events[-1]['protagonist']['concessions']
    attr = max(concessions, key=concessions.get)
    value = concessions[attr]
    concessions = events[-1]['person']['concessions']
    b_attr = max(concessions, key=concessions.get)
    b_value = concessions[attr]
    if (b_value > value):
        value = b_value
        attr = b_attr

    # count fights
    conflicts = {}
    for e in events:
        if e['type'] == EventType.CONFLICT:
            if e['target_property'] not in conflicts:
                conflicts[e['target_property']] = {
                    'count': 0,
                    'delta': 0,
                }
            conflicts[e['target_property']]['count'] += 1
            conflicts[e['target_property']]['delta'] += e['delta']

    popular_conflict = None
    best_conflict = None
    worst_conflict = None
    max_count = -math.inf
    max_delta = -math.inf
    min_delta = math.inf
    for c in conflicts:
        if conflicts[c]['count'] > max_count:
            max_count = conflicts[c]['count']
            popular_conflict = c

        if conflicts[c]['delta'] > max_delta:
            max_delta = conflicts[c]['delta']
            best_conflict = c

        if conflicts[c]['delta'] < min_delta:
            min_delta = conflicts[c]['delta']
            worst_conflict = c

    # count experiences
    experiences = {}
    for e in events:
        if e['type'] == EventType.EXPERIENCE:
            if e['target_property'] not in experiences:
                experiences[e['target_property']] = {
                    'count': 0,
                    'delta': 0,
                }
            experiences[e['target_property']]['count'] += 1
            experiences[e['target_property']]['delta'] += e['delta']

    popular_experience = None
    best_experience = None
    worst_experience = None
    max_count = -math.inf
    max_delta = -math.inf
    min_delta = math.inf
    for c in experiences:
        if experiences[c]['count'] > max_count:
            max_count = experiences[c]['count']
            popular_experience = c

        if experiences[c]['delta'] > max_delta:
            max_delta = experiences[c]['delta']
            best_experience = c

        if experiences[c]['delta'] < min_delta:
            min_delta = experiences[c]['delta']
            worst_experience = c

    return {
        'experiences': experiences,
        'popular_experience': popular_experience,
        'worst_experience': worst_experience,
        'best_experience': best_experience,
        'conflicts': conflicts,
        'popular_conflict': popular_conflict,
        'worst_conflict': worst_conflict,
        'best_conflict': best_conflict,
        'highest_concession': attr,
    }
