import random

# This is a little too mad-lib-y right now.
# Could pull some language from a corpus.
# Would this flow better after 'They met at a x'?

# Sylvan: could we get a protagonist argument in get_prologue? Or should that be handled elsewhere
# I just think using protag's name in these strings could add better variation


def get_prologue(person):
    # properties
    # not currently using neuro or libido
    name = person.get('name')

    properties = {
        'hot': {
            'lo': ['homely', 'plain looking', 'typical', 'unremarkable'],
            'med': ['charming', 'attractive', 'sweet-faced', 'kind-eyed'],
            'hi': ['beautiful', 'lovely', 'gorgeous', 'stunning']
        },
        'open': {
            'lo': ['They always invented new games and inside jokes',
                   'They constantly sought new hobbies and experiences',
                   'They were impulsive in ways, always sensation-seeking'],
            'med': ['They never made suggestions for dates', 'They always stuck to what felt comfortable',
                    'They enjoyed trying new things but were still quite skeptical'],
            'hi': ['They were a picky eater and could not be convinced to try new food', 'They were a creature of habit—inflexible, but reliable',
                   'They were cautious and hated surprises']
        },
        'con': {
            'lo': ['chaotic', 'messy', 'disorganized'],
            'med': ['careless', 'meandering', 'detail-oriented'],
            'hi': ['diligent', 'exacting', 'dutiful']
        },
        'extra': {
            'lo': ['a boisterous laugh',
                   'a gregarious personality', 'an enthusiastic charm'],
            'med': ['an easy smile',
                    'a laid-back demeanor', 'a relaxed personality'],
            'hi': ['a quiet demeanor',
                   'a reserved manner', 'a cat-like personality']
        },
        'agree': {
            'lo': ['argumentative', 'callous', 'combative'],
            'med': ['stubborn', 'independent', 'affectionate'],
            'hi': ['altruistic', 'cooperative', 'empathetic']
        },
        'neuro': {
            'lo': ['stable'],
            'med': ['empathetic'],
            'hi': ['volatile']
        },
        'commit': {
            'lo': ['wanted something casual'],
            'med': ['up for anything'],
            'hi': ['were ready for something serious']
        },
        'exp': {
            'lo': ['insecure about', 'nervous about', 'timid in'],
            'med': ['unsure of', 'open to', 'relaxed about'],
            'hi': ['secure in', 'well versed in', 'experienced in']
        }
    }

    stringArray = []
    for key in properties:
        prop = person.get(key)
        if prop > .66:
            stringArray.append(random.choice(properties[key]['hi']))
        elif prop > .33:
            stringArray.append(random.choice(properties[key]['med']))
        else:
            stringArray.append(random.choice(properties[key]['lo']))

        print(stringArray)

    # in strArray: [0]hot, [1]open, [2]con, [3]extra, [4]agree, [5]neuro, [6]commit, [7]exp
    str1 = name + " was a " + stringArray[0] + \
        " person with " + stringArray[3] + ". "
    str2 = name + " initially seemed " + stringArray[4] + \
        " romantic relationships and " + stringArray[6] + ". "
    str3 = name + " was " + stringArray[2] + " and " + \
        stringArray[7] + ". " + stringArray[1] + ". "

    strings = random.sample([str1, str2, str3], k=2)
    result = listToString(strings)
    return result


def listToString(s):
    str0 = " "
    return (str0.join(s))


if __name__ == '__main__':
    test_person = {
        'name': 'Lover',
        'hot': 1,
        'open': .5,
        'con': .5,
        'extra': .5,
        'agree': .5,
        'neuro': .5,
        'commit': .5,
        'libido': .5,
        'exp': .5
    }
    print(get_prologue(test_person))
