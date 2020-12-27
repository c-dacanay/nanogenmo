import random
import util
import tracery
from tracery.modifiers import base_english

# This is a little too mad-lib-y right now.
# Could pull some language from a corpus.
# Would this flow better after f'{person["they"].capitalize()} met at a x'?

# Sylvan: could we get a protagonist argument in get_prologue? Or should that be handled elsewhere
# I just think using protag's name in these strings could add better variation

def get_prologue(person):
    rules = {
        'origin': [
            "#time#, Alex #realized# that #name# was a #hot# person with #extra#. When it came to their relationship, #name# was #neuro# and #agree#. #they.capitalize# was #con# and #open#." 
            ],
        'time': ["Over time", "Slowly", "As the two got to know each other", "The more they saw #name#"],
        'realized': ["realized", "noticed", "discovered", "found", "saw that"],
        'name': f"{person['name']}",
        'they': f"{person['they']}",
        'hot': util.rank([
            "unremarkable",
            "typical",
            "plain-looking",
            "homely",
            "kind-eyed",
            "sweet-faced",
            "attractive",
            "charming",
            "beautiful",
            "gorgeous",
            "stunning"
        ], person['hot']),
        'extra': util.rank([
            "a reserved manner",
            "a quiet demeanor",
            "a cat-like personality",
            "a laid-back demeanor",
            "a relaxed-personality",
            "an easy smile",
            "an enthusiasstic charm",
            "a boisterous laugh",
            "a gregarious personality"
        ], person['extra']),
        'open': util.rank([
            "a picky eater and could not be convinced to try new food",
            "cautious and hated surprises",
            "a creature of habit, inflexible but reliable,"
            "usually stuck to what felt comfortable",
            "enjoyed trying new things occasionally",
            "constantly sought new hobbies and experiences",
            "impulsive in ways, always sensation-seeking,"
        ], person['open']),
        'neuro': util.rank([
            "emotionally attuned",
            "emotionally stable",
            "stoic",
            "grounded",
            "composed",
            "well-adjusted",
            "easygoing",
            "nonchalant",
            "jittery",
            "anxious",
            "high strung",
            "emotionally volatile",
            "emotionally unpredictable",
            "prone to severe mood swings",
        ], person['neuro']),
        'con': util.rank([
            "disorganized",
            "careless",
            "meandering",
            "scattered",
            "struggled but strove to be organized",
            "a bit messy",
            "tried to keep tidy",
            "clean",
            "keen",
            "detail-oriented",
            "diligent",
            "dutiful",
            "a neat freak",
            "exacting"
        ], person['con']),
        'agree': util.rank([
            "callous",
            "combative",
            "argumentative",
            "rude",
            "stubborn",
            "independent",
            "cooperative",
            "affectionate",
            "empathetic",
            "altruistic",
        ], person['agree']),
    }
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    print(grammar.flatten('<br><br>#origin#'))

def get_prologue_DEPRECATED(person):
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
            'lo': [
                f'{person["they"].capitalize()} always invented new games and inside jokes',
                f'{person["they"].capitalize()} constantly sought new hobbies and experiences',
                f'{person["they"].capitalize()} was impulsive in ways, always sensation-seeking'
            ],
            'med': [
                f'{person["they"].capitalize()} never made suggestions for dates',
                f'{person["they"].capitalize()} always stuck to what felt comfortable',
                f'{person["they"].capitalize()} enjoyed trying new things but was still quite skeptical'
            ],
            'hi': [
                f'{person["they"].capitalize()} was a picky eater and could not be convinced to try new food',
                f'{person["they"].capitalize()} was a creature of habit—inflexible, but reliable',
                f'{person["they"].capitalize()} was cautious and hated surprises'
            ]
        },
        'con': {
            'lo': ['chaotic', 'messy', 'disorganized'],
            'med': ['careless', 'meandering', 'detail-oriented'],
            'hi': ['diligent', 'exacting', 'dutiful']
        },
        'extra': {
            'lo': [
                'a boisterous laugh', 'a gregarious personality',
                'an enthusiastic charm'
            ],
            'med':
            ['an easy smile', 'a laid-back demeanor', 'a relaxed personality'],
            'hi': [
                'a quiet demeanor', 'a reserved manner',
                'a cat-like personality'
            ]
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
            'hi': ['was ready for something serious']
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

    # in strArray: [0]hot, [1]open, g[2]con, [3]extra, [4]agree, [5]neuro, [6]commit, [7]exp
    str0 = "<br><br>Over time, Alex realized that "
    str1 = f'{person["they"].capitalize()}' + " was a " + stringArray[0] + \
        " person with " + stringArray[3] + "."
    str2 = name + " seemed " + stringArray[7] + \
        " romantic relationships and " + stringArray[6] + "."
    str3 = name + " was " + stringArray[2] + " and " + \
        stringArray[4] + ". " + stringArray[1] + "."

    strings = random.sample([str1, str2, str3], k=2)
    result = str0 + listToString(strings)
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
        'exp': .5,
        'they': "she",
        'their': "her",
        'them': "her"
    }
    print(get_prologue(test_person))
