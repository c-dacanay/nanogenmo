import tracery
import random
import business_gen
from util import get_ab
import util
import logging
import artifacts


def get_problem(a, b, target_p):
    if a[target_p] > b[target_p]:
        # problems for if a is higher than b
        PROBLEM_NAMES = {
            'open': [
                'never interested in doing what #a# wanted to do',
                'too boring',
            ],
            'extra': [
                'never interested in doing anything social',
                'only interested in staying home',
            ],
            'libido': [
                'not initiating sex often enough',
                'not passionate enough about the relationship',
            ],
            'con': [
                'too messy',
                'not hardworking enough',
            ],
            'neuro': [
                'not paying paying enough attention to the relationship',
                'was not texting often enough',
            ],
            'agree': [
                'never wanted to adapt for the sake of the relationship',
                'often rude'
            ],
            'exp': [
                'was too immature',
                'was kind of a crybaby'
            ],
            'hot': [
                'was not hot enough'
            ]
        }
    else:
        # problems for if a is lower than b
        PROBLEM_NAMES = {
            'open': [
                'always #pushing# to do weird activities',
            ],
            'extra': [
                'always #pushing# to socialize',
            ],
            'libido': [
                'always #pushing# for sex',
                'always touching me in inappropriate situations',
            ],
            'con': [
                'too nitpicky',
                'too obsessed with details',
            ],
            'neuro': [
                'too neurotic',
                'too anxious',
                'too insecure',
            ],
            'agree': [
                'too wishy washy',
            ],
            'exp': [
                'too demanding',
            ],
            'hot': [
                'too hot'
            ]
        }
    return PROBLEM_NAMES[target_p]


def get_meetup(a, b):
    rules = {
        'origin': [
            '#texture# \n#they# #met# #discuss#.',
            '\n#they# #met# #discuss#.',
        ],
        'they': ['They', 'The couple'],
        'met': ['later met up at #location#', 'later got on the phone'],
        'location': business_gen.get_business(),
        'discuss': ['to discuss', 'to talk', 'to chat'],
        'texture': [
            '#b_name# blinked slowly.',
            '#b_name# rubbed their eyes.',
            '#b_name# sighed, and swiped the message away.',
            '#b_name# took a deep breath.',
        ],
        'b_name': b['name'],
        'b_they': b['they'],
        'b_their': b['their'],
        'a_name': a['name'],
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten('#origin#')


def get_problem_statement(a, b, problem_phrase, event):
    rules = {
        'origin': ['#problem_statement#. #reaction#.'],
        'problem_statement': [
            '#a# was #upset# because #a_they# felt that #b# was #problem#',
            '#a# told #b# that #b# was #problem#',
            '"Hey, I feel like you are #problem#"',
            '"Hey, you are really #problem#"',
        ],
        'upset': ['upset', 'frustrated', 'mad', 'angry'],
        'a': a['name'],
        'a_they': a['they'],
        'b': b['name'],
        'problem': problem_phrase,
        'pushing': ['pushing', 'telling', 'convincing', 'nagging', 'dragging'],
        'reaction': util.rank([
            '#a#\'s voice was gentle, but firm',
            '#a#\'s voice was soft, but firm',
            '#a# asked #b# if there was anything they could do to help.',
            '#a# looked at #b# silently, waiting for a response',
            '#a# folded their arms, glaring at #b#',
            '#a#\'s voice was harsh',
            '#a#\'s voice was cold',
            '#a#\'s tones were accusing',
        ], event['neuro_roll'])
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten('#origin#')


def get_response(a, b, event):
    biggest_roll = max(event['rolls'], key=lambda k: abs(
        event['rolls'][k]) if k != 'neuro' else 0)
    rules = {
        'pos': f"#{biggest_roll}#",
        'neg': "#neuro#",
        'agree': ['#b# wanted to please #a##apology#'],
        'commit': ['#b# wanted to do right by the relationship#apology#', ],
        'interest': ['#b# didn\'t want to lose #a##apology#'],
        'neuro': ['#b# was #angry##worse#'],
        'angry': [
            'furious',
            'upset',
            'angry',
            'offended',
            'livid',
            'pissed',
            'defensive',
        ],
        'apology': [
            ', and immediately apologized',
            ', and promised to make amends',
            ', and put on a display of repentance',
            ', and bought flowers for #a# the next day',
        ],
        'worse': [
            '. The couple argued for hours.',
            '. The couple failed to reach a conclusion.',
        ],
        'a': a['name'],
        'a_they': a['they'],
        'b': b['name'],
    }
    grammar = tracery.Grammar(rules)
    if (event['delta'] > 0):
        return grammar.flatten('#pos#')
    else:
        return grammar.flatten('#neg#')


def narrate_conflict(event):
    a, b = get_ab(event)
    target_p = event['target_property']

    logging.debug(event['delta'])
    # First get a description of the conflict
    problem_phrase = get_problem(a, b, target_p)

    if not event['initiated']:
        # A was grumpy, but didn't actually initiate a fight.
        logging.debug("FIGHT ABORTED")
        rules = {
            'origin': '#sometimes# #a# #thought# that #perhaps# #b# was #problem#. #but#',
            'a': a['name'],
            'b': b['name'],
            'sometimes': ['Sometimes', 'Often', 'Occasionally', 'From time to time', 'Some nights', 'On rare occassion'],
            'perhaps': ['perhaps', 'maybe', '', 'it was possible that', 'compared to previous partners at least, that'],
            'thought': ['thought', 'considered', 'wondered', 'felt concerned'],
            'problem': problem_phrase,
            'pushing': ['pushing', 'telling', 'convincing', 'nagging', 'dragging'],
            'but': [
                '#a# pushed the thought the the back of #a_their# mind, and #return#',
                'But the thought would fade, and #return#',
                '#a# let the thought fade away, and #return#'
            ],
            'return': [
                '#a# #returned# to #a_their# coffee.'
                '#a# #returned# to #a_their# breakfast.'
                '#a# #returned# to #a_their# work.'
                f"#a# #returned# to reading about {random.choice(a['hobbies'])}" if a[
                    'hobbies'] else '',
                f"#a# #returned# to watching Youtube videos about {random.choice(a['hobbies'])}" if a[
                    'hobbies'] else '',
                '',
            ],
            'returned': ['returned', 'continued', 'went back to'],
            'a_their': a['their'],
        }
        print(tracery.Grammar(rules).flatten('#origin#'))
        return

    # Print some pretext
    artifact_pretext = artifacts.get_fight_trigger(event)
    print(artifact_pretext)

    # Describe meeting
    meetup = get_meetup(a, b)
    print(meetup)

    # A expresses the complaint
    complaint = get_problem_statement(a, b, problem_phrase, event)
    print(complaint)

    # B responds
    response = get_response(a, b, event)
    print(response)
