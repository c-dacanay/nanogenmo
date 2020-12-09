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
                'never was interested in doing what #a# wanted to do',
                'never wanted to try new things',
                f"only wanted to do things related to {', '.join(b['interests'])}; only things #b# liked to do ",
                'was too boring',
            ],
            'extra': [
                'was never interested in doing anything social',
                'never wanted to socialize',
                'never wanted to go out',
                'was only interested in staying home',
            ],
            'libido': [
                'didn\'t initiate sex often enough',
                'didn\'t want to have sex often enough',
                'didn\'t want to be intimate often enough',
                'was not passionate enough about the relationship',
            ],
            'con': [
                'was too messy',
                'was too disorganized',
                'was not hardworking enough',
                'was too lazy',
            ],
            'neuro': [
                'was not paying paying enough attention to the relationship',
                'was not texting often enough',
                'was not arranging dates often enough',
                'talked too much to their friends',
            ],
            'agree': [
                'never wanted to adapt for the sake of the relationship',
                'was often rude to #b#',
                'was too unfriendly',
                'was too disagreeable'
            ],
            'exp': [
                'was too immature',
                'was kind of a crybaby'
                'was too jealous',
                'didn\'t communicate their needs well'
            ],
            'hot': [
                'was not attractive enough',
                'needed to hit the gym',
                'needed to go on a diet',
                'needed to take care of themselves better',
            ],
            'commit': [
                'was not committed enough',
                'was not interested in #b# enough',
                'was not invested enough',
                "didn't want to push the relationship forward",
            ]
        }
    else:
        # problems for if a is lower than b
        PROBLEM_NAMES = {
            'open': [
                'was always #pushing# #a# to do weird new activities',
                "didn't understand that #a# did not enjoy discovering things the way #b# did",
                "pushed #a# out of their comfort zone too often",
                "didn't respect what #a# wanted to do on dates",
            ],
            'extra': [
                "pushed #a# to socialize when they didn't want to",
                "didn't understand that #a# did not enjoy socializing the way #b# did",
                "didn't respect that sometimes #a# just wanted to stay in",
                "didn't get that #a# didn't want to go out all the time",
            ],
            'libido': [
                'pushed #a# for sex too often',
                "didn't understand that #a# just didn't like sex as much as #b#",
                "cared way too much about physical intimacy",
                "put too much emphasis on their sex life"
            ],
            'con': [
                'was too nitpicky',
                'was too obsessed with details',
                'was too much of a clean freak',
                'was too much of a grinder'
            ],
            'neuro': [
                'was too neurotic',
                'was too anxious',
                'was too insecure',
                'was too jealous'
            ],
            'agree': [
                'was too wishy washy',
                'lacked a spine',
                'always let other people make the decisions',
                'never had a strong opinion about anything'
            ],
            'exp': [
                'had unachievable standards',
                'wanted to talk about feelings too often',
                'wanted to talk about the relationship too much',
                'wanted to talk too much',
            ],
            'hot': [
                'was too desired, always getting unwanted attention',
                'was too hot, making #b# feel insecure',
                'was too charming to others',
                'was too flirty with coworkers'
            ],
            'commit': [
                'was too serious about the relationship',
                'was too invested in the relationship',
                "was pushing the relationship too fast",
                "was moving the relationship too quickly"
            ]
        }
    return PROBLEM_NAMES[target_p]


def get_meetup(a, b):
    rules = {
        'origin': [
            '\n#they# #met# #discuss#.',
        ],
        'they': ['They', 'The couple'],
        'met': [
            'later met up at #location#',
            'later got on the phone',
            'arranged a time',
            'met up',
        ],
        'location': business_gen.get_business(desc=False),
        'discuss': [
            'to discuss',
            'to talk',
            'to chat',
            'to hash things out',
            'to continue the conversation'
        ],
        'b_name': b['name'],
        'b_they': b['they'],
        'b_their': b['their'],
        'a_name': a['name'],
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten('#origin#')


def get_problem_statement(a, b, problem_phrase, event):
    if event['prev']:
        again = 'again '
    else:
        again = ''
    rules = {
        'origin': [
            '#problem_statement#. #anger# #reaction#.',
            '#problem_statement#. #anger# #reaction#. #texture#',
        ],
        'problem_statement': [
            f'#a# {again}was #upset# because #a_they# felt that #b# #problem#',
            f'#a# {again}told #b# that #b# #problem#',
        ],
        'anger': util.rank([
            "#a# emphasized that they weren't angry, just wanted the best for the relationship. ",
            "#a# wondered if #b# would be willing to do things differently."
            "It just wouldn't do. ",
            "#a# was angry. ",
            "Something had to change. ",
        ], event['target']),
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
        ], event['neuro_roll']),
        'texture': util.rank([
            '#b# sighed, and swiped the message away.',
            '#b# blinked slowly.',
            '#b# rubbed their eyes.',
            '#b# took a deep breath.',
            '#b# gasped anxiously.',
            '#b#\'s finger trembled as they dismissed the message.',
            '#b# was shocked.',
            '#b# was mortified.',
            '#b# was incensed.',
        ], random.gauss(b['neuro'], 0.1))
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


def get_conflict_thought(a, b, event, problem_phrase):
    logging.debug("FIGHT ABORTED")
    conflicts = [e for e in event['prev'] if e['initiated']]
    ago = ''
    if conflicts:
        # There were previou fights about it.
        # One morning, the fight they had in December about Susan's laziness floated into ALex's mind.
        main = '#time#, the #fight# they had #ago# about how #b# #problem# #floated#.'
        ago = humanize.naturaldelta(
            event['date'] - conflicts[len(conflicts) - 1]['date']) + ' ago'
    elif event['prev']:
        # THere were previous aborted fights.
        main = 'The idea that #b# #problem# came back to #a#\'s #mind#.'
    else:
        main = '#time# #a# #thought# that #perhaps# #b# #problem#.'
    but = '#resolve#' if event['initiated'] else '#but#'

    rules = {
        'origin': f"{main} {but}",
        'a': a['name'],
        'a_they': a['they'],
        'a_their': a['their'],
        'b': b['name'],
        'b_their': b['their'],
        'time': ['One morning', 'One day'],
        'mind': ['mind', 'head'],
        'ago': ago,
        'floated': ['floated back into #a#\'s #mind#', 'drifted into #a#\'s #mind#'],
        'perhaps': ['perhaps', 'maybe', '', '', 'compared to previous partners'],
        'thought': ['thought', 'considered', 'felt bothered', 'felt concerned', 'had the thought', 'was discussing #b# with a friend and realized'],
        'problem': problem_phrase,
        'pushing': ['pushing', 'telling', 'convincing', 'nagging', 'dragging'],
        'but': [
            '#pushed_back#, and #return#',
            '#pushed_back#. '
        ],
        'pushed_back': [
            '#a# pushed the thought the the back of #a_their# mind',
            '#a# let the thought fade away',
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
        'resolve': [
            '#texture# #a# resolved to bring it up to #b# next time they saw each other.'
        ],
        'texture': util.rank([
            '#a# #return#. It wasn\'t a big deal, but nonetheless',
            '#a# exhaled slowly. Perhaps it could be resolved with a simple conversation. ',
            '#a# bit #a_their# lip. It was becoming more and more bothersome the more #a_they# thought about it.',
            '#a# clenched #a_their# fist. It was really not something #a# valued in a partner',
            '#a# felt themselves shaking with anger.',
        ], (event['target'])),
        'fight': ['fight', 'argument', 'dispute', 'spat']
    }
    return tracery.Grammar(rules).flatten('#origin#')


def narrate_conflict(event):
    a, b = get_ab(event)
    target_p = event['target_property']

    logging.debug(event['delta'])
    # First get a description of the conflict
    problem_phrase = get_problem(a, b, target_p)

    if not event['initiated']:
        # A was grumpy, but didn't actually initiate a fight.
        print(get_conflict_thought(a, b, event, problem_phrase))
        return

    if random.random() < abs(event['delta']):
        # The bigger the event, the more chance we narrate it explicitly
        # Print some pretext
        rules = {
            'origin': [
                '#message# #meetup# #complaint# #response#\n',
                '#message# #complaint# #response#\n',
                '#thought# #meetup# #response#\n',
                '#thought# #response#\n',
            ],
            'thought': get_conflict_thought(a, b, event, problem_phrase),
            'message': artifacts.get_fight_trigger(event),
            'meetup': get_meetup(a, b),
            'complaint': get_problem_statement(a, b, problem_phrase, event),
            'response': get_response(a, b, event)
        }
        print(tracery.Grammar(rules).flatten('#origin#'))
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
