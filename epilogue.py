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
    else:
        get_outlook(a)
    narrate_alex(a, interest, hobbies)
    #TODO random event / new hobby

    if random.random() > 0.7:
        narrate_month(date)
    if random.random() > 0.5:
        andthen()

    return ""


def narrate_alex(a, interest, hobbies):
    a_verb = random.choice(INTERESTS[interest]['location'])
    hobby = random.choice(hobbies)
    rules = {
        'origin':
        f'#a# took #modifer# time #doing# {hobby}, and #a_they# #started# {a_verb} #amount#.',
        'modifer':
        ['a lot', 'lots of', 'some', 'a little', 'a small amount of'],
        'doing': [
            'to practice', 'to watch YouTube videos about', 'enjoying',
            'obsessing over', 'delving into', 'appreciating', 'taking pleasure in'
        ],
        'started': [
            'went to', 'made plans to go to', 'started to go to', 'went back to', 'prioritized going to', 'spent time at',
            'chilled at the'
        ],
        'amount': [
            'often', 'every now and then', 'occasionally', 'excitedly',
            'as frequently as #they# could', 'with enthisuasm'
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
                '#a# #felt# #a_they# were #unlovable#',
                '#a# did not feel #great# after that',
                '#a# #avoid#'
            ],
            'Things': ['Everything', 'Life', 'Getting up', 'Dating'],
            'great': ['great', 'good', 'well', 'excited', 'confident', 'encouraged', 'enthusiastic'],
            'felt': ['felt as if', 'was sure that', 'felt certain that', 'wondered if'],
            'hard': ['hard', 'grey', 'difficult', 'lonely', 'like a struggle', 'impossible', 'boring', 'uneventful'],
            'unlovable': ['unlovable', 'unattractive', 'not fun to be around', 'repellant', 'too desperate'],
            'avoid': ['#tried# to get #their# mind off of things', '#tried# not to be #bugged# by it'],
            'tried': ['tried', 'attempted'],
            'bugged': ['annoyed', 'bothered', 'annoyed', 'troubled', 'discouraged']
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
        'realized': ['#a# realized', '#b# told #a#', '#a# had the dawning realization'],
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
                'had been vain in #their# relationship with #b#'
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
        #prop went up 
        PROP_CHANGE = {
            'open': [
                'really closed off to new things',
                'stuck in #their# on ways',
                'unenthusiasatic about #their# partners interests'
            ],
            'extra': [
                'always holding #b# back from socializing',
                'afraid of social engagements',
                'too introverted'
            ],
            'libido': [
                'insecure about physical intimacy',
                'too physically distant'
            ],
            'con': [
                'excessively messy',
                'lazy and inconsiderate in #their# relationships',
                'did not put in enough effort'
            ],
            'agree': [
                'too stubborn about #their# needs',
                'never adapted to what #b# wanted',
                'refused to adapt for #b#'
            ],
            'exp': [
                'naive about relationships',
                'not reflecting about #their# previous relationship experiences'
            ],
            'hot': [
                'not taking care of #their# physical apperance',
                'not attracting the type of people #they# wanted'
            ],
            'neuro': [
                'boring',
                'too relaxed'
            ],
            'commit': [
                'did not value #b#\'s dedication',
                'holding #their# relationship back',
                'afraid of commitment'
            ]
        } 
        
        return random.choice(PROP_CHANGE[reflection['prop']])


