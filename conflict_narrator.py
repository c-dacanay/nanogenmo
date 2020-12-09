import tracery
import humanize
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
                'was never interested in doing what #a# wanted to do',
                'was never interested in trying new things',
                'was only interested in doing boring activities',
                'was not willing to branch out for date ideas',
                'was too boring',
            ],
            'extra': [
                'was never interested in doing anything social',
                'was not interested enough in socializing',
                'was only interested in staying home',
            ],
            'libido': [
                'was not initiating sex often enough',
                'was not asking #a# for sex often enough',
                'was not passionate enough about the relationship',
            ],
            'con': [
                'was too messy',
                'was too disorganized',
                'was not hardworking enough',
            ],
            'neuro': [
                'was not paying paying enough attention to the relationship',
                'was not texting often enough',
                'was not arranging dates often enough',
            ],
            'agree': [
                'never wanted to adapt for the sake of the relationship',
                'was often rude to #b#'
            ],
            'exp': [
                'was too immature',
                'was kind of a crybaby'
            ],
            'hot': [
                'was not hot enough',
                'needed to hit the gym'
            ]
        }
    else:
        # problems for if a is lower than b
        PROBLEM_NAMES = {
            'open': [
                'was always #pushing# #a# to do weird new activities',
                "was not understanding of the fact that #a# really did not enjoy discovering things the way #b# did",
            ],
            'extra': [
                'was always #pushing# #a# to socialize',
                "was not understanding of the fact that #a# really did not enjoy socializing the way #b# did",
            ],
            'libido': [
                'was always #pushing# #a# for more sex',
                "was not understanding of the fact that #a# just didn't like sex as much as #b#"
            ],
            'con': [
                'was too nitpicky',
                'was too obsessed with details',
                'was too much of a clean freak',
            ],
            'neuro': [
                'was too neurotic',
                'was too anxious',
                'was too insecure',
            ],
            'agree': [
                'was too wishy washy',
                'lacked a spine'
            ],
            'exp': [
                'had unachievable standards',
            ],
            'hot': [
                'was too desired, always getting unwanted attention',
                'was too hot, making #b# feel insecure',
                'was too charming to others',
                'was too flirty with coworkers'
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
        'met': [
            'later met up at #location#',
            'later got on the phone'
        ],
        'location': business_gen.get_business(desc=False),
        'discuss': [
            'to discuss',
            'to talk',
            'to chat',
            'to hash things out',
            'to continue the conversation'],
        'texture': util.rank([
            '#b_name# sighed, and swiped the message away.',
            '#b_name# blinked slowly.',
            '#b_name# rubbed their eyes.',
            '#b_name# took a deep breath.',
            '#b_name# gasped anxiously.',
            '#b_name#\'s finger trembled as they dismissed the message.',
            '#b_name# was shocked.',
            '#b_name# was mortified.',
            '#b_name# was incensed.',
        ], random.gauss(b['neuro'], 0.1)),
        'b_name': b['name'],
        'b_they': b['they'],
        'b_their': b['their'],
        'a_name': a['name'],
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten('#origin#')


def get_problem_statement(a, b, problem_phrase, event):
    rules = {
        'origin': ['#problem_statement#. #anger# #reaction#.'],
        'problem_statement': [
            '#a# was #upset# because #a_they# felt that #b# #problem#',
            '#a# told #b# that #b# #problem#',
        ],
        'anger': [
            "It just wouldn't do. ",
            "Something had to change. ",
            "#a# wondered if #b# would be willing to do things differently."
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
        'agree': [
            '#b# wanted to please #a##apology#'
            '#b# didn\'t want #a# to be angry#apology#'
        ],
        'commit': [
            '#b# wanted to do right by the relationship#apology#',
            '#b# didn\'t want to lose their partner#apology#',
        ],
        'interest': [
            '#b# didn\'t want to lose #a##apology#',
            '#b# liked #a# quite a bit#apology#',
        ],
        'neuro': [
            '#b# was #angry##worse#',
            '#b# accused #a# of not liking them enough#worse#',
            '#b# accused #a# of not being invested enough in the relationship#worse#',
        ],
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
            ', and apologized profusely',
            ', and promised to make amends',
            ', and put on a display of repentance',
            ', and bought flowers for #a# the next day',
            ', and bought a coffee for #a# the next morning',
        ],
        'worse': [
            '. #they# #argued# #bitterly#.',
            '. #they# failed to reach a conclusion.',
        ],
        'they': ['They', 'The couple', 'The pair'],
        'a': a['name'],
        'a_they': a['they'],
        'b': b['name'],
        'argued': ['argued', 'fought', 'clashed'],
        'bitterly': ['bitterly', 'heatedly', 'for hours', 'late into the night', 'acridly', 'acidly', 'venemously'],
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
        conflicts = [e for e in event['prev'] if e['initiated']]
        ago = ''
        if conflicts:
            # There were previou fights about it.
            # One morning, the fight they had in December about Susan's laziness floated into ALex's mind.
            main = '#time# the #fight# they had #ago# about #b# #problem# #floated#.'
            ago = humanize.naturaldelta(
                event['date'] - conflicts[len(conflicts) - 1]['date'])
        elif event['prev']:
            # THere were previous aborted fights.
            main = 'The idea that #b# #problem# came back #a#\'s #mind#.'
        else:
            main = '#time# #a# #thought# that #perhaps# #b# #problem#.'

        rules = {
            'origin': '#main# #but#',
            'main': main,
            'a': a['name'],
            'b': b['name'],
            'b_their': b['their'],
            'time': ['One morning', 'One day'],
            'mind': ['mind', 'head'],
            'ago': ago,
            'floated': ['floated back into #b_their# #mind#', 'drifted into #b_their# #mind#'],
            'perhaps': ['perhaps', 'maybe', '', 'it was possible that', 'compared to previous partners'],
            'thought': ['thought', 'considered', 'wondered', 'felt concerned'],
            'problem': problem_phrase,
            'pushing': ['pushing', 'telling', 'convincing', 'nagging', 'dragging'],
            'but': [
                '#a# pushed the thought the the back of #a_their# mind, and #return#',
                'But the thought would fade, and #a# #return#',
                '#a# let the thought fade away, and #return#'
            ],
            'return': [
                '#returned# to #a_their# coffee.',
                '#returned# to #a_their# breakfast.',
                '#returned# to #a_their# work.',
                f"#returned# to reading about {random.choice(a['hobbies'])}" if a[
                    'hobbies'] else 'returned to reading.',
                f"#returned# to watching Youtube videos about {random.choice(a['hobbies'])}" if a[
                    'hobbies'] else 'returned to surfing the Internet.',
            ],
            'returned': ['returned', 'went back'],
            'a_their': a['their'],
        }
        import pdb
        try:
            print(tracery.Grammar(rules).flatten('#origin#'))
        except:
            pdb.set_trace()

        return

    if random.random() < abs(event['delta']):
        # The bigger the event, the more chance we narrate it explicitly
        # Print some pretext
        artifact_pretext = artifacts.get_fight_trigger(event)
        print(artifact_pretext)

        if random.random() < 0.5:
            # Describe meeting
            meetup = get_meetup(a, b)
            print(meetup)

        # A expresses the complaint
        complaint = get_problem_statement(a, b, problem_phrase, event)
        print(complaint)

        # B responds
        response = get_response(a, b, event)
        print(response)

        print('\n')
    else:
        narrate_conflict_zoomout(a, b, event, problem_phrase)


def narrate_conflict_zoomout(a, b, event, problem_phrase):
    response = get_response(a, b, event)
    problem_statement = tracery.Grammar(
        {
            'origin': "#They# #sometimes# #fought# because #a# felt that #b# #problem#. ",
            'problem': problem_phrase,
            'pushing': 'pushing',
            'sometimes': util.rank(['occasionally', 'sometimes', 'often', 'frequently', 'always'], util.scale(event['delta'], -1, 0.5, 1, 0)),
            'fought': ['fought', 'argued', 'clashed', 'scuffled'],
            'They': ['They', 'The couple'],
            'a': a['name'],
            'b': b['name'],
        }).flatten('#origin#')
    print(problem_statement)


def narrate_minor_conflict(a, b, event, problem_phrase):
    problem_statement = tracery.Grammar(
        {
            'origin': "#a# #asked# #b# to #a# felt that #b# was #problem#. ",
            # Alex asked Tracy to be more hot
            'problem': problem_phrase,
            'pushing': 'pushing',
            'sometimes': util.rank(['occasionally', 'sometimes', 'often', 'frequently', 'always'], util.scale(event['delta'], -1, 0.5, 1, 0)),
            'fought': ['fought', 'argued', 'clashed', 'scuffled'],
            'They': ['They', 'The couple'],
            'a': a['name'],
            'b': b['name'],
        }).flatten('#origin#')
    print(problem_statement)
