import util
import pprint
import business_gen
import prologue
import random
import logging
import conflict_narrator
from relationship import EventType, PROP_NAMES, Relationship, Phase
from narrate_time import narrate_time
import tracery
import artifacts
from tracery.modifiers import base_english
from util import get_ab
from interests import INTERESTS, getInterestRules

logging.basicConfig(level=logging.DEBUG)


def narrate(r: Relationship):
    # Given a relationship object, break the events within into their distinct
    # phases and pass them to narrate_phase
    events = r.events
    print(f"Alex met {events[0]['person']['name']} {events[0]['location']}. ")
    for phase in [Phase.COURTING, Phase.DATING, Phase.COMMITTED]:
        chunk = []
        while True:
            if len(events) == 0:
                break
            if events[0].get('phase', phase) != phase:
                # Move on to next phase
                break
            event = events.pop(0)
            chunk.append(event)
        narrate_phase(chunk, phase)

    # knock alex's confidence just a touch
    # logging.debug(f"Alex's confidence is {a['confidence']}")
    r.a['confidence'] *= .9 + random.random() * 0.1
    # logging.debug(f"Alex's confidence is {a['confidence']}")
    print("They never saw each other again.")

# Given a chunk of events and phase, narrate events in that style
# Right now there aren't that many changes to narration based on phase
# but we keep the infrastructure for now


def narrate_phase(events, phase):
    if events:
        logging.debug(f'Narrating {len(events)} events in phase {phase}')
    if phase == Phase.COURTING:
        narrate_events(events)
    elif phase == Phase.DATING and events:
        prologue.get_prologue(events[0]['person'])
        narrate_events(events)
    elif phase == Phase.COMMITTED and events:
        narrate_committed(events)


# Given a block of events, narrate the next event
# Maintain an array of events that happened up until that point
# so the narrator can take them into account.
def narrate_events(events):
    current_events = []
    for event in events:
        narrate_event(event, current_events)
        if current_events:
            narrate_time(current_events[-1], event)
        current_events.append(event)


# Call the appropriate function based on event type
def narrate_event(event, events):
    # logging.debug(pprint.pformat(event))
    if event is None:
        return
    if event['type'] == EventType.MEETING:
        narrate_meeting(event, events)
    elif event['type'] == EventType.COMMIT:
        narrate_commit(event, events)
    elif event['type'] == EventType.EXPERIENCE:
        narrate_experience(event, events)
    elif event['type'] == EventType.CONFLICT:
        narrate_conflict(event, events)
    else:
        time_passed(event, events)


# Get some basic descriptor based on the property with the highest value
# This is what Alex notices first about the person
def get_salient_property(person):
    m = 0
    k = ''
    for key in person:
        try:
            if person[key] > m:
                k = key
                m = person[key]
        except:
            pass
    props = {
        'hot': [
            f"{person['name']}'s {random.choice(['lithe', 'well-defined', 'striking'])} {random.choice(['features', 'body', 'muscles'])}"
        ],
        'open': [
            f"{person['name']}'s {random.choice(['pealing laughter', 'earnest expression'])}"
        ],
        'con': [f"{person['name']}'s intense focus"],
        'extra': [
            f"{person['name']}'s friendly {random.choice(['disposition', 'demeanor', 'attitude'])}"
        ],
        'agree': [f"a quiet kindness in {person['name']}'s movements"],
        'neuro': [f"a raw intensity in {person['name']}'s articulations"],
        'libido': [f"{person['name']}'s deep sexual energy"],
        'confidence': [f"{person['name']}'s easygoing confidence"],
        'commit': [f"{person['name']}'s even, placid tones"],
        'exp': [f"an unexpected depth in {person['name']}'s eyes"],
        'interest': [f"{person['name']} glancing over every now and again"]
    }
    return random.choice(props[k])


def get_interest_sentence(a, b, interest):
    adjective = [
        'noticed', 'was struck by', 'was fascinated by',
        "couldn't help but notice"
    ]
    prop = get_salient_property(b)
    return f"{a['name']} {random.choice(adjective)} {prop}. "


def narrate_commit(event, events):
    a, b = get_ab(event)
    if event['initiated']:
        enthusiasm = util.scale(event['success_ratio'], 1, 3, 0, 1)
        rules = {
            'courting_phase': ['#dating#'],
            'dating_phase': ['#iloveyou#'],
            'dating': ['#dating_challenge# #dating_result#'],
            'iloveyou': ['#ily_challenge# #ily_result#'],
            'dating_challenge': [
                "#a# asked to start dating.",
                "#a# asked if #b# would be interested in dating.",
            ],
            'dating_result':
            f"#b# agreed {util.enthusiastically(enthusiasm)}. "
            if event['success_ratio'] >= 1 else
            f'#b# said that {b["they"]} needed more time. ',
            'ily_challenge':
            f"#a# said \"I love you,\"",
            'ily_result': [
                'but #b# could not say it back. #a# was #hurt#'
                if event['success_ratio'] < 1 else
                f'and #b# returned the words {util.enthusiastically(enthusiasm)}.'
            ],
            'hurt': util.rank(
                [
                    'hurt, but said #a_they# understood.',
                    'wounded. A tear fell from #a#\'s left eye. ',
                    'devasted. #a_they.capitalize# had hoped #b#\'s response might have been different this time.',
                    'mortified. #a# shouted that #b# was wasting #a#\'s time. #b# shrugged. '
                ],
                util.scale(event.get('prev', 0), 0, 3, 0, 1)
            ),
            'a': a['name'],
            'b': b['name'],
            'a_they': a['they']
        }

    elif event['initiate_ratio'] > 1:
        # Narrate a failed commit event held back by confidence
        rules = {
            'courting_phase': '#origin#',
            'dating_phase': '#origin#',
            'origin': [
                '#a# felt nervous, but excited. ',
                "#a# had the urge to ask #b# about how they felt about the relationship, but wasn't quite confident enough to ask. ",
            ],
            'a': a['name'],
            'b': b['name'],
        }
    else:
        # Not interested enough.
        rules = {
            'courting_phase': '#origin#',
            'dating_phase': '#origin#',
            'origin': [
                "#a# continued to use dating apps from time to time. ",
                "#a# had yet to mention #b# to their parents. ",
            ],
            'a': a['name'],
            'b': b['name'],
            'interest': a['interests'],
        }
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    if event['phase'] == Phase.COURTING:
        print(grammar.flatten('#courting_phase#'))
    elif event['phase'] == Phase.DATING:
        print(grammar.flatten('#dating_phase#'))
    print('\n')


def narrate_meeting(event, events):
    if event['delta'] == -1:
        return
    text = ""
    a, b = get_ab(event)
    if event['protagonist_initiated']:
        text += get_interest_sentence(event['protagonist'], event['person'],
                                      event['protagonist']['interest'])
    else:
        text += get_interest_sentence(event['person'], event['protagonist'],
                                      event['person']['interest'])
    adverb = util.rank(
        ['nervously', 'shyly', 'quietly', 'gently', 'intently', 'boldly'],
        a['interest'])

    if event['delta'] <= 0:
        REJECTIONS = [
            f", but {b['name']} averted {b['their']} eyes. ",
            f", but {b['name']} did not respond. ",
            f", but {b['name']} quickly turned away. ",
        ]
        followup = random.choice(REJECTIONS)
    else:
        follow2 = random.choice([
            f'Soon, they got to talking and found themselves engaged in animated conversation. ',
            f"They exchanged several friendly words, before agreeing to meet again sometime soon. "
        ])
        contact = random.choice([
            'phone number', 'email', 'contact',
            'phone number scrawled onto a crumpled piece of paper',
            'phone number hastily scribbled on a napkin',
            'email address dashed onto a post-it note',
            'Discord server invite', 'laughter echoing in their ears',
            'smile etched into their memory', 'Instagram handle'
        ])
        follow3 = random.choice([
            f"{a['name']} left with {b['name']}'s {contact}. ",
            f"{b['name']} left with {a['name']}'s {contact}. ",
        ])
        ACCEPTS = [
            f". {b['name']} returned a flirtatious glance. {follow2}{follow3}",
            f". {b['name']} waved in return. {follow2}{follow3}",
            f". {b['name']} smiled back. {follow2}{follow3}"
        ]
        followup = random.choice(ACCEPTS)
    time = random.choice([
        'After a few moments, ',
        '',
        'After several minutes, ',
        'Eventually, ',
    ])
    APPROACHES = [
        f"{time}{a['name']} waved {adverb}{followup}",
        f"{time}{a['name']} smiled {adverb}{followup}",
        f"{time}{a['name']} began to gaze {adverb} at {b['name']}{followup}",
        f"{time}{a['name']} giggled {adverb}{followup}",
        f"{time}{a['name']} walked {adverb} toward {b['name']}{followup}"
    ]
    print(text + random.choice(APPROACHES) + "")


def narrate_committed(events):
    print("The couple lived happily ever after")


def narrate_rejection(event, events):
    a, b = get_ab(event)
    rules = {
        'origin': "#Onday# #want#, #reject#.",
        'a': a['name'],
        'b': b['name'],
        'Onday': [
            f"On {event['date'].strftime('%A')},",
            f"{event['date'].strftime('%A')} came around.",
            "Later that week,"
        ],
        'want': [
            '#a# asked #b# if they wanted to hang out',
            f'#a# asked #b# if {b["they"]} were free',
            '#a# wanted to hang out with #b#',
            '#a# wanted to see #b#',
        ],
        'reject': [
            'but #b# was busy',
            'but #b# forgot to return #a#\'s message',
            'but #b# had other plans',
            'but #b# never responded to #a#\'s message'
        ]
    }
    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        print(artifacts.get_date_artifact(event, events))
    else:
        print(tracery.Grammar(rules).flatten('#origin#'))
    return


def narrate_experience(event, events):
    a, b = get_ab(event)

    if event['rejected']:
        narrate_rejection(event, events)
        return

    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        print(artifacts.get_date_artifact(event, events))

    if event['target_property'] == 'open':
        rules = {
            'mood': util.rank([
                "Having a strong preference for what #they# wanted to do for date night,",
                f"Having been obsessed with {event['interest']} more than ever lately,",
                "Wanting to have a nice evening together,",
                "Wanting to surprise #b#,",
                "In effort to mix up what they usually do,",
                "In the mood for adventure,"
            ], event['threshold']),
            'proposed': [
                "asked #b# to", "begged #b# to", "proposed that they",
                "wondered if it would be fun to", "suggested that they",
                "wanted to", "invited #b# to"
            ],
            'hobby_proposal': [
                f"#mood# #a# #proposed# go to {random.choice(INTERESTS[event['interest']]['location'])} together.",
                f"#mood# #a# #proposed# {random.choice(INTERESTS[event['interest']]['verb'])} together."
            ],
            'response': util.rank([
                "I'd love to!", "Sounds like fun!", "Yes, let's do it,", "Sure!", "Okay,", "Oh, okay,", "I guess so...", "Do we have to?", "You know I don't like that,"
            ], 1-event['delta']),
            'reply': ['"#response#" #b# replied.']
        }
        rules.update(getInterestRules(a, b, event['interest']))
        grammar = tracery.Grammar(rules)
        print(grammar.flatten('<p>#hobby_proposal# #reply#</p>'))
        # logging.debug(
        #    f"OPEN EXPERIENCE {event['interest']} {event['threshold']} a: {a['open']} b: {b['open']}")
    elif event['target_property'] in ['extra', 'libido']:
        rules = {
            'origin':
            f"#Onday# #{event['target_property']}#.",
            'day': ['day', 'morning', 'afternoon', 'evening'],
            'Onday': [
                f"On {event['date'].strftime('%A')}, #they#",
                f"{event['date'].strftime('%A')} came around. #they.capitalize#",
                "Later that week, #they#"
            ],
            'extra':
            util.rank([
                '#enjoyed# a tranquil #day# watching Netflix',
                '#enjoyed# a tranquil #day# watching Youtube videos',
                '#enjoyed# a tranquil #day# watching a movie',
                '#enjoyed# a quiet #day# reading together',
                '#enjoyed# a night out together at the bar',
                '#enjoyed# a #day# hanging out with friends',
                '#enjoyed# a #day# of people-watching',
                '#enjoyed# a night out at the club',
            ], event['threshold']),
            'libido':
            util.rank([
                'lay in bed together, but without touching',
                'lay in bed together, holding hands',
                'shared a kiss',
                '#enjoyed# a passionate evening together',
                '#enjoyed# an intensely passionate evening together',
            ], event['threshold']),
            'they': [
                'they', 'the couple', '#a# and #b#', 'the two of them',
                'the pair'
            ],
            'enjoyed':
            util.rank([
                'spent', 'happily spent', 'enjoyed',
                'excitedly spent', 'savored',
                'reveled in', 'relished'
            ], event['delta']),
            'a':
            a['name'],
            'b':
            b['name'],
        }
        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)
        print(grammar.flatten("#origin#"))
    else:
        rules = {
            'origin': [
                f"#Onday# #{event['target_property']}#",
            ],
            'Onday': [
                f"On {event['date'].strftime('%A')}, ",
                f"{event['date'].strftime('%A')} came around. ",
                "Later that week, "
            ],
            'hot': util.rank([
                '#b# noticed that #a# sometimes gave off a mildly unpleasant odor.',
                f'#a# bragged to #b# about how infrequently {a["their"]} hair needed to be washed.',
                '#a# met #b# wearing an old college sweatshirt and an ill-fitting pair of jeans.',
                '#b# noticed #a# went to sleep without washing up first.',
                '#a# bought more skincare products.',
                '#a# went shopping for the latest trendy fashions.',
                '#a# went shopping for organic groceries. That figure didn\'t keep itself in shape!',
                '#a# spent the #day# at the gym. That body didn\'t keep itself in shape!',
            ], event['threshold']),
            'con': util.rank([
                '#b# noticed #a# had a lot of dishes piled up in the sink.',
                '#a# decided to call in sick to work. After all, you only live once.',
                f'#a# forgot to do {a["their"]} laundry.',
                '#a# left a couple of dishes piled up in the sink.',
                f'#a# noticed {a["they"]} needed to vacuum the carpet.',
                '#a# decided to start keeping a daily todo list.',
                f'#a# spent the #day# arranging {a["their"]} books by color and subject.',
                '#a# went shopping and purchased a daily planner.',
                '#a# stayed late at work.',
                '#a# spent the #day# #cleaning# the apartment.',
                '#a# spent the #day #cleaning# the apartment. It was moderately dusty.',
                '#a# spent the #day# #cleaning# the bathroom. It certainly was in need of some attention.',
            ], event['threshold']),
            'exp': util.rank([
                '#a# was upset with #b#, but said nothing.',
                '#a# was jealous of #b#\'s moderately attractive co-worker.',
                f'#a# asked #b# how {b["they"]} felt about the relationship. The couple had an earnest conversation about where things were going.',
                f'#a# suggested that they enact weekly relationship check-ins. #b# agreed happily.'
            ], event['threshold']),
            'neuro': util.rank([
                '#a# fretted. #a# had not heard from #b# for a couple days.',
                '#b# had a night out with friends planned. #a# was happy to pass the evening doing other things.',
                '#b# had not responded to #a#\'s text messages for a few hours. #a# sent a followup.',
                f'#a# worried when #b# said that {a["they"]} sometimes preferred to be alone.',
                '#a# worried that #b# did not actually find them to be attractive. '
                '#b# kept a journal of how long it took for #a# to text them back.',
                '#a# worried that #b# would leave them some day soon. ',
            ], event['threshold']),
            'cleaning': ['tidying', 'cleaning', 'organizing'],
            'day': ['day', 'morning', 'afternoon', 'evening'],
            'a': a['name'],
            'b': b['name'],
        }
        print(tracery.Grammar(rules).flatten('#origin#'))
        # logging.debug(f"Event: {event}")


def narrate_conflict(event, events):
    conflict_narrator.narrate_conflict(event)


def time_passed(event, events):
    return ""
