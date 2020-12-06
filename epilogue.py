from relationship import Relationship
import tracery
import util
import random
from interests import INTERESTS
from narrate_time import narrate_month
import datetime
# {'prop': 'hot', 'old': 0.565142070087718, 'new': 0.4322991476397663, 'memory': ''}
def get_epilogue(r, date):
    a = r.a
    interest = random.choice(r.a['interests'])
    hobbies = r.a['hobbies']
    # partner = r.b['name']
    reflection = r.reflection

    # if r.phase == Phase.COURTING:
    get_outlook(a)

    if random.random() > 0.7:
        narrate_month(date)
    narrate_alex(a, interest, hobbies)

    # if reflection['old'] > reflection['new']:
    #     print(reflection['prop'] + ' went down.')
    # else:
    #     print(reflection['prop'] + ' went up.')

    # narrate_reflection(reflection)
    return ""


def narrate_alex(a, interest, hobbies):
    a_verb = random.choice(INTERESTS[interest]['verb'])
    hobby = random.choice(hobbies)
    rules = {
        'origin':
        f'#a# spent #modifer# time #doing# {hobby}, and #a_they# #started# {a_verb} #amount#.',
        'modifer':
        ['a lot', 'a huge amount', 'some', 'a little', 'a small amount of'],
        'doing': [
            'practicing', 'watching YouTube videos about', 'enjoying',
            'obsessing over'
        ],
        'started': [
            'began to', 'made time to', 'started to', 'went back to',
            'went back to', 'prioritized going to', 'went to',
            'chilled while #a_they#'
        ],
        'amount': [
            'often', 'every now and then', 'occasionally', 'excitedly',
            'as frequently as possible', 'with enthisuasm'
        ],
        'hobby': hobby,
        'a':
        a['name'],
        'a_they':
        a['they'],
    }
    grammar = tracery.Grammar(rules)
    print(grammar.flatten('#origin#'))


def narrate_reflection(reflection):
    # memory = reflection['memory']
    rules = {
        'origin': 'Alex felt #feeling# about the breakup.',
        'feeling': ['bad', 'good', 'awful', 'relieved', 'confused']
    }

    grammar = tracery.Grammar(rules)
    print(grammar.flatten('#origin#'))


def get_outlook(a):
    if a['confidence'] > .6:
        rules = {
            'origin': '#confident_statement#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'confident_statement': [
                'Things had been going well for #a#',
                '#a# invested time in #a_their# friendships',
                '#a# felt #chill#',
                '#a# felt #chill# regarding the encounter'
            ],
            'chill': ['undeterred', 'unbothered', 'at ease', 'aloof', 'untroubled', 'nonchalant']
        }
    else:
        rules = {
            'origin': '#insecure_statement#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'insecure_statement': [
                'Everything harder for a while',
                '#a# wondered if #a_they# were unlovable',
                '#a# did not feel #great# after that',
                'Everything felt a little gray'
            ],
            'great': ['great', 'good', 'well', 'excited', 'confident', 'encouraged', '']
        }
    print(tracery.Grammar(rules).flatten('#origin#'))
