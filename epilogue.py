from relationship import Relationship, Phase
import tracery
import util
import random
from interests import INTERESTS, getInterestRules
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
        print('<p>')
        narrate_reflection(a, b, reflection)
        narrate_memory(a, b, reflection, interest)
        print('</p>')
    
    print('<p>')
    narrate_alex(a, interest, hobby)
    narrate_ran(a, b)
    get_outlook(a)
    print('</p>')

    if random.random() > 0.7:
        narrate_month(date)
    # if random.random() > 0.5:
    #     andthen()

    return ""

def narrate_ran(a, b):
    rules = {
        'origin': ['They texted #b# once#response#.', '', '', '', f'They considered getting more interested in {random.choice(list(INTERESTS))}.'],
        'a': a['name'],
        'a_they': a['they'],
        'a_their': a['their'],
        'b': b['name'],
        'b_their': b['their'],
        'b_they': b['they'],
        'response': rank([', but #b_they# didn\'t respond', ' but #b_they# politely asked for space', ' and #a_they# got a few messages back, but #b_they# were clearly uninterested',' and #b_they# chatted with them, but it did little for #a#'], b['agree'])
    }
    print(tracery.Grammar(rules).flatten('#origin#'))

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
            'action': ['going to bed', 'getting groceries', f"going to {random.choice(INTERESTS[interest]['location'])}", 'daydreaming', 'getting ready for work', 'making plans for a vacation', f"reading about {interest}"],
            'remembered': ['#a_they# couldn\'t help but think about', '#a_they# remembered', '#a# recalled', '#a_they# imagined', '#a_they# thought about'],
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
                              '#a# took in a deep breath as tears welled up in #a_their# eyes. There was no one like #b#'
                              ], a['interest'])
        }
        rules.update(getInterestRules(a, b, interest))
        print(tracery.Grammar(rules).flatten('#memory_sentence#'))


def narrate_alex(a, interest, hobby):
    a_verb = random.choice(INTERESTS[interest]['location'])
    rules = {
        'origin': ['#texture##a_does#', '#statement#'],
        'texture': ['Everything felt harder for a while. ', 'Time seemed to pass in slow motion. ', '#a# couldn\'t deny the slow monotony of their life—in attempt to improve it, ', 
        'The days felt shorter without a partner to fill them. ', 'Alex\'s calendar filled up with ease and '],
        'statement': ['#a# wondered if they were going to spend the rest of their life in search for someone who might understand them.', '#a# listened to #music# and thought about their future.', 'While #a# aimed to be independent and confident alone, #a_they# were sometimes struck with the cold shock of solitude.', '#a# journaled about #event#.', '#a# deleted all the dating apps off their phone (again).'],
        'music': ['Mitski', 'The National', 'Broken Social Scene', 'Phoebe Bridgers', 'Frank Ocean', 'SZA', 'Carly Rae Jepsen', 'Lorde', 'Fleetwood Mac', 'Robyn'] ,
        'event': ['recent workplace drama', 'achieving their goals', 'current events', 'their political perspective', 'their fraught familial relationships', 'the futility of online dating'],
        'a_does':
        [f'#a# took time #doing# {hobby}.', f'#a# #started# {a_verb} #amount#.'],
        'modifer':
        ['a lot', 'lots of', 'some', 'a little', 'a small amount of'],
        'doing': [
            'to practice', 'to watch YouTube videos about', 'enjoying',
            'obsessing over', 'delving into', 'appreciating', 'taking pleasure in'
        ],
        'started': [
            'went to', 'made plans to go to', 'started to go to', 'went back to', 'prioritized going to', 'spent time at',
            'chilled at'
        ],
        'amount': [
            'often', 'every now and then', 'occasionally', 'as an act of self care',
            'as frequently as #they# could'
        ],
        'hobby': hobby,
        'a':
        a['name'],
        'a_they':
        a['they'],
    }
    rules.update(getInterestRules(a, {'name': ''}, interest))
    print(tracery.Grammar(rules).flatten('#origin#'))


def get_outlook(a):
    if a['confidence'] > .5:
        rules = {
            'origin': '#confident_statement#, #yet# #longing#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'yet': ['yet', 'but','though', 'and still'],
            'confident_statement': rank([
                '#a# invested time in #a_their# #nonromantic#',
                '#a# felt #chill# regarding the encounter'
                'Overall, things had been going quite well for #a#',
            ], a['confidence']/2),
            'chill': ['undeterred', 'unbothered', 'at ease', 'aloof', 'untroubled', 'nonchalant'],
            'nonromantic': ['friendships', 'career', 'hobbies', 'stack of unread books'],
            'longing': rank(['#a_they# checked their phone often, expecting texts from no one', ' when #a# went to social events, #a_they# desperately wished they had a partner', '#a_they# kept re-downloading dating apps and browsing for hours', '#a#\'s friends teased them for constantly going on dates'], a['commit'])
        }
    else:
        rules = {
            'origin': '#insecure_statement#, and #longing#.',
            'a': a['name'],
            'a_they': a['they'],
            'a_their': a['their'],
            'insecure_statement': rank([
                '#a# #felt# #a_they# were #unlovable#',
                '#Things# felt #hard# for a while',
                '#a# did not feel #great# after that',
                '#a# #avoid#'
            ], a['confidence']/2),
            'longing': rank(['#a_they# longed for touch, affection and companionship', '#a_they# couldn\'t deny the lonely ache in #a_their# chest', '#a_they# scrolled endlessly on #a_their# phone, searching for someone', '#a_they# were overcome with the absence of a best friend and partner'
            ], a['commit']),
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
        'a_they': a['they'],
        'origin': '#breakup#. #afterward# #realized# that #they# #change##intent#.',
        'breakup': rank(['#a# took the break up hard', '#a# had a hard time when #b# stopped talking to them', '#a# struggled to cut #b# out of #their# life', '#a# knew the break up was for the best, but it didn\'t feel that way', '#a# felt like a great weight lifted off #their# shoulders after the relationship ended', '#a# was happy to be out of that relationship'], a['commit']),
        'afterward': ['Immediately after the break up,', 'Later,', 'After the relationship ended,', 'While the relationship fell apart,'],
        'realized': ['#a# realized', '#b# told #a#', '#a# had the dawning realization'],
        'change': ref_statement,
        'intent': rank([', and #a_they# journaled about #their# intent to change','. It hurt to realize', '. #a# would have to work on it', ', and #they# resolved to improve', '. #a# decided to change'], a['confidence']),
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
        # if prop went down
        PROP_CHANGE = {
            'open': [
                '#might# obsessed with novely',
                '#might# overly interested in new activities all the time',
                '#might# too eccentric',
                '#might# excessively impulsive'
            ],
            'extra': [
                '#might# overly gregarious',
                '#might# too much of a social butterfly',
                '#might# insensitive to #their# partners social needs'
            ],
            'libido': [
                '#might# too overt about sex',
                'asked for physical intimacy too much',
                '#might# too physically needy'
            ],
            'con': [
                '#might# excessively nitpicky',
                '#might# too critical of #their# partners work ethic',
                '#might# too particular about being clean'
            ],
            'agree': [
                '#might# a door mat in relationships',
                'never stood up for #their# needs',
                '#might# too obliging to #their# romantic partners'
            ],
            'exp': [
                '#might# too particular about #their# partners',
                '#might# too harsh about #their# parthers relationship experience'
            ],
            'hot': [
                '#might# too superficial about picking partners',
                '#might# vain during #their# relationship with #b#'
            ],
            'neuro': [
                '#might# too insecure',
                '#might# overly controlling',
                '#might# neglecting #their# mental health'
            ],
            'commit': [
                '#might# too invested in the idea of a long term relationship',
                '#might# overly committed',
                'rushed in too quickly'
            ]
        }

        changeStatement = random.choice(PROP_CHANGE[reflection['prop']])
        rules = {
            'origin': changeStatement,
            'might': ['could be', 'were', 'might be', 'were just', 'had been'],
        }
        return tracery.Grammar(rules).flatten('#origin#')

    else:
        # prop went up
        PROP_CHANGE = {
            'open': [
                '#might# really closed off to new things',
                '#might# stuck in #their# on ways',
                '#might# unenthusiasatic about #their# partners interests'
            ],
            'extra': [
                '#might# always holding #b# back from socializing',
                '#might# afraid of social engagements',
                '#might# too introverted'
            ],
            'libido': [
                '#might# insecure about physical intimacy',
                '#might# too physically distant'
            ],
            'con': [
                '#might# excessively messy',
                '#might# lazy and inconsiderate in #their# relationships',
                'did not put in enough effort'
            ],
            'agree': [
                '#might# too stubborn about #their# needs',
                'never adapted to what #b# wanted',
                'refused to adapt for #b#'
            ],
            'exp': [
                '#might# naive about relationships',
                'failed to see the patterns in #their# previous relationship experiences'
            ],
            'hot': [
                'should have put more effort in taking care of #their# physical apperance',
                'might not be attracting the type of people #they# wanted'
            ],
            'neuro': [
                '#might# too easygoing',
                '#might# too apathetic about the relationship'
            ],
            'commit': [
                'did not value #b#\'s dedication',
                'were constantly holding #their# relationship back',
                '#might# afraid of commitment'
            ]
        }

        changeStatement = random.choice(PROP_CHANGE[reflection['prop']])
        rules = {
            'origin': changeStatement,
            'might': ['could be', 'were', 'might be', 'were just', 'had been'],
        }
        return tracery.Grammar(rules).flatten('#origin#')