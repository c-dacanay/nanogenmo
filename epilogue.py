from relationship import Relationship, Phase
import tracery
import util
import random
from interests import INTERESTS
from narrate_time import narrate_month
import datetime
# {'prop': 'hot', 'old': 0.565142070087718, 'new': 0.4322991476397663, 'memory': ''}
def get_epilogue(r, date):
    a = r.a
    b = r.b
    interest = random.choice(r.a['interests'])
    hobbies = r.a['hobbies']
    reflection = r.reflection

    if r.phase == Phase.DATING:
        narrate_reflection(a, b, reflection)
        #TODO narrate memory
   
    get_outlook(a)
    narrate_alex(a, interest, hobbies)
    #TODO narrate affect

    if random.random() > 0.7:
        narrate_month(date)
    if random.random() > 0.5:
        andthen()

    return ""


def narrate_alex(a, interest, hobbies):
    a_verb = random.choice(INTERESTS[interest]['verb'])
    hobby = random.choice(hobbies)
    rules = {
        'origin':
        f'#a# took #modifer# time #doing# {hobby}, and #a_they# #started# {a_verb} #amount#.',
        'modifer':
        ['a lot', 'a huge amount of', 'some', 'a little', 'a small amount of'],
        'doing': [
            'practicing', 'watching YouTube videos about', 'enjoying',
            'obsessing over', 'having fun while'
        ],
        'started': [
            'began to', 'made plans to', 'started to', 'went back to', 'prioritized going to', 'went to',
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
    print(tracery.Grammar(rules).flatten('#origin#'))

def get_outlook(a):
    if a['confidence'] > .5:
        rules = {
            'origin': '#confident_statement#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'confident_statement': [
                'Overall, things had been going well for #a#',
                '#a# invested time in #a_their# #nonromantic#',
                '#a# felt #chill#',
                '#a# felt #chill# regarding the encounter'
            ],
            'chill': ['undeterred', 'unbothered', 'at ease', 'aloof', 'untroubled', 'nonchalant'],
            'nonromantic': ['friendships', 'career', 'hobbies', 'stack of unread books']
        }
    else:
        rules = {
            'origin': '#insecure_statement#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'insecure_statement': [
                '#Things# felt #hard# for a while',
                '#a# #felt# #a_they# were unlovable',
                '#a# did not feel #great# after that'
            ],
            'Things': ['Everything', 'Life', 'Getting up', 'Dating'],
            'great': ['great', 'good', 'well', 'excited', 'confident', 'encouraged'],
            'felt': ['felt as if', 'was sure that', 'felt certain that', 'wondered if'],
            'hard': ['hard', 'grey', 'difficult', 'lonely', 'like a struggle', 'impossible']
        }
    print(tracery.Grammar(rules).flatten('#origin#'))

def narrate_reflection(a, b, reflection):
    # memory = reflection['memory']
    ref_statement = get_reflection(a, b, reflection)
    # rules = {
    #     'origin': 'Alex felt #feeling# about the breakup.',
    #     'feeling': ['bad', 'good', 'awful', 'relieved', 'confused']
    # }
    rules = {
        'origin': '#afterward# #realized# that #they# #might# #change#. #intent#.',
        'afterward': ['Immediately after the break up,', 'Later', 'After the relationship ended', 'While the relationship fell apart'],
        'realized': ['#a# realized', '#b# texted #a#', '#a# had the dawning realization'],
        'might': ['could be', 'were', 'might be', 'were just', 'had been'],
        'change': ref_statement,
        'intent': ['#a# decided to change', '#a# would have to work on it', 'It hurt to realize', '#a# resolved to improve'],
        'a': a['name'],
        'they': a['they'],
        'their': a['their'],
        'b': b['name'],
        # 'them': a['them']
    }
    print(tracery.Grammar(rules).flatten('#origin#'))

def andthen():
    rules = {
    'origin': '#then#...',
    'then': ['Then Alex saw', 'Until there was', 'Then, one day']
    # 'them': a['them']
    }
    print(tracery.Grammar(rules).flatten('#origin#'))

def get_reflection(a, b, reflection):
    if reflection['old'] > reflection['new']:
        #if prop went down
        PROP_CHANGE = {
            'open': [
                'obsessed with novely',
                'overly interested in new activities all the time',
                'too eccentric',
                'excessively impulsive'
            ],
            'extra': [
                'overly gregarious',
                'too much of a social butterfly',
                'insensitive to #their# partners social needs'
            ],
            'libido': [
                'too overt about sex',
                'asked for physical intimacy too much',
                'too physically needy'
            ],
            'con': [
                'excessively nitpicky',
                'too critical of #their# partners work ethic',
                'too particular about being clean'
            ],
            'agree': [
                'a door mat in relationships',
                'never stood up for #their# needs',
                'too obliging to #their# romantic partners'
            ],
            'exp': [
                'too particular about #their# partners',
                'too harsh about #their# parthers relationship experience'
            ],
            'hot': [
                'not attracting the type of person #they# want',
                'cared too much about how #they# looked'
            ],
            'neuro': [
                'too insecure',
                'overly controlling',
                'not tending to #their# mental health'
            ],
            'commit': [
                'too invested in the idea of a long term relationship',
                'overly committed',
                'rushed in too quickly'
            ]
        } 
        return random.choice(PROP_CHANGE[reflection['prop']])
    else:
        return reflection['prop'] + ' went up.'


