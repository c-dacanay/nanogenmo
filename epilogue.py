from relationship import Relationship, Phase
import tracery
import util
import random
from interests import INTERESTS
from narrate_time import narrate_month
from util import rank
import datetime

def get_epilogue(r, date):
    a = r.a
    b = r.b
    interest = random.choice(r.a['interests'])
    hobby = random.choice(r.a['hobbies'])

    reflection = r.reflection

    if r.phase == Phase.DATING:
        narrate_reflection(a, b, reflection)
        narrate_memory(a, b, reflection, interest)
    else:
        get_outlook(a)
    narrate_alex(a, interest, hobby)
    #TODO random event / new hobby

    if random.random() > 0.7:
        narrate_month(date)
    if random.random() > 0.5:
        andthen()

    return ""

def narrate_memory(a, b, reflection, interest):
    if reflection['memory']:
        rules = {
            'memory_sentence': [f"#time# #remembered# #{reflection['memory']}#. #reaction#."],
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'b': b['name'],
            'b_their': b['their'],
            'b_they': b['they'],
            'time': ['Every now and then when #a# was #action#', 'Some mornings, in those tender moments between sleep and wake,', 'One night, while #a# was #action#', 'Randomly when #a# was #action#', 'When #a# was #action#', 'One evening while #a# was #action#'],
            'action': ['going to bed', 'getting groceries', f"going to {random.choice(INTERESTS[interest]['location'])}",'daydreaming', 'getting ready for work', 'making plans for a vacation', f"reading about {interest}" ],
            'remembered': ['#a_they# couldn\'t help but think about', '#a_they# remebered', '#a# recalled', '#a_they# imagined', '#a_they# thought about'],
            'open': ['#b#\'s enthusiastic charm', '#b#\'s gentle hand on #a_their#\'s, beckoning', '#b#\'s open and excited response when trying something new together'],
            'extra': ['#b#\'s melodic laughter', 'watching #b# at a party while #b_they# charmed the whole room'],
            'libido': ['the curve #b#\'s neck as #b_they# undressed', 'the smell of #b#\'s skin as they held each other', '#b#\'s electric touch against #a_their# skin', '#b#\'s body silhouetted against the moonlight'],
            'con': ['one of #b#\'s intellectual ramblings', 'watching #b#\'s back as #b_they# did the dishes', 'what #b# would say about the state of #a_their# home'],
            'agree': ['#b#\'s comforting presence', f"going to {random.choice(INTERESTS[interest]['location'])} and teaching #b# everything #a_they# knew", 'the ease and enjoyment of sitting on #b#\'s floor, talking for hours'],
            'exp': ['#b#\'s kind yet discerning expression as #b_they# would evaluate #a#', 'one of #b#\'s stories about #b_their# ex. #a# wondered what #a_their# story would sound like when #b# told it.'],
            'hot': ['the way #b# would turn heads as #b_they# walked down the street', 'admiring #b#\'s face as #b_they# got ready for work', 'staring into #b#\'s eyes for hours'],
            'neuro': ['one of #b#\'s emotional breakdowns', 'brushing #a_their# hands through #b#\'s hair as #b_they# endured another mood swing', '#b#\'s constant refrain: "thank you for staying being with me"'],
            'commit': ['meeting #b#\'s parents', 'talking about moving in with #b#', 'long discussions about #a_their# future with #b#'],
            'reaction': rank(['#a# sighed and dismissed the thought',
                '#a# tried to push #b# out of #a_their# mind', 
                '#a# bit #a_their# lip and moved on with #a_their# day',
                'In that moment #a# felt overcome with affection, and loss',
                '#a# wondered, surprised by #a_their# own desperation, if anyone other than #b# would do',
                '#a# took in a deep breath as tears welled up in #a_their# eyes. There was no one like #b_their#' 
                ], a['interest'])
        }
        print(tracery.Grammar(rules).flatten('#memory_sentence#'))

def narrate_alex(a, interest, hobby):
    a_verb = random.choice(INTERESTS[interest]['location'])
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
            'confident_statement': rank([
                '#a# invested time in #a_their# #nonromantic#',
                '#a# felt #chill# regarding the encounter'
                'Overall, things had been going quite well for #a#',
            ], a['confidence']/2),
            'chill': ['undeterred', 'unbothered', 'at ease', 'aloof', 'untroubled', 'nonchalant'],
            'nonromantic': ['friendships', 'career', 'hobbies', 'stack of unread books']
        }
    else:
        rules = {
            'origin': '#insecure_statement#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'insecure_statement': rank([
                '#a# #felt# #a_they# were #unlovable#',
                '#Things# felt #hard# for a while',
                '#a# did not feel #great# after that',
                '#a# #avoid#'
            ], a['confidence']/2),
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

    rules = {
        'origin': '#afterward# #realized# that #they# #might# #change#. #intent#.',
        'afterward': ['Immediately after the break up,', 'Later', 'After the relationship ended', 'While the relationship fell apart'],
        'realized': ['#a# realized', '#b# told #a#', '#a# had the dawning realization'],
        'might': ['could be', 'were', 'might be', 'were just', 'had been'],
        'change': ref_statement,
        'intent': rank(['It hurt to realize', '#a# would have to work on it', '#a# resolved to improve', '#a# decided to change'], a['confidence']),
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
                'vain during #their# relationship with #b#'
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


