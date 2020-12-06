from relationship import Relationship
import tracery
import util


# {'prop': 'hot', 'old': 0.565142070087718, 'new': 0.4322991476397663, 'memory': ''}
def get_epilogue(r):
    reflection = r.reflection
    if reflection['old'] > reflection['new']:
        print(reflection['prop'] + ' went down.')
    else:
        print(reflection['prop'] + ' went up.')
    # print(partner)
    # print(reflection['memory'])
    narrate_reflection(r)
    return ""


def narrate_reflection(r):
    partner = r.b['name']
    rules = {
        'origin': 'Alex felt #feeling# about the breakup.',
        'feeling': ['bad', 'good', 'awful', 'relieved', 'confused']
    }

    grammar = tracery.Grammar(rules)
    print(grammar.flatten('#origin#'))


# partner = r.b
# print(r)
