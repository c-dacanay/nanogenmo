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
    return narrate_events(r.a, r.events)


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


def narrate_commit(event):
    a, b = get_ab(event)
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
        f'#b# said that perhaps they weren\'t quite ready yet. ',
        'ily_challenge':
        f"#a# said \"I love you\"",
        'ily_result': [
            '#b# could not say it back. #a# was #hurt#'
            if event['success_ratio'] < 1 else
            f'#b# returned the words {util.enthusiastically(enthusiasm)}.'
        ],
        'hurt': util.rank(
            [
                'hurt, but said #a_they# understood.',
                'wounded. A tear fell from #a#\'s left eye. ',
                'devasted. #a_they# had hoped #b#\'s response might have been different this time',
                'mortified. #a# shouted that #b# was wasting #a#\'s time. #b# shrugged. '
            ],
            util.scale(event.get('prev', 0), 0, 3, 0, 1)
        ),
        'a':
        a['name'],
        'b':
        b['name'],
        'a_they': a['they']
    }
    grammar = tracery.Grammar(rules)
    if event['phase'] == Phase.COURTING:
        print(grammar.flatten('#courting_phase#'))
    elif event['phase'] == Phase.DATING:
        print(grammar.flatten('#dating_phase#'))
    print('\n')


def narrate_meeting(event):
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
        ['nervously', 'shyly', 'quietly', '', 'gently', 'intently', 'boldly'],
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
        f"{time}{a['name']} walked {adverb}toward {b['name']}{followup}"
    ]
    print(text + random.choice(APPROACHES) + "\n\n")


def narrate_committed(events):
    print("The couple lived happily ever after")


def narrate_events(a, events):
    a = a
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
    a['confidence'] *= .9 + random.random() * 0.1
    # logging.debug(f"Alex's confidence is {a['confidence']}")
    print("They never saw each other again.\n\n")


def narrate_event(event):
    # logging.debug(pprint.pformat(event))
    if event is None:
        return
    if event['type'] == EventType.MEETING:
        narrate_meeting(event)
    elif event['type'] == EventType.COMMIT:
        narrate_commit(event)
    elif event['type'] == EventType.EXPERIENCE:
        narrate_experience(event)
    elif event['type'] == EventType.CONFLICT:
        narrate_conflict(event)
    else:
        time_passed(event)


def narrate_phase(events, phase):
    if events:
        logging.debug(f'Narrating {len(events)} events in phase {phase}\n')
    if phase == Phase.COURTING:
        for event in events:
            narrate_event(event)
    elif phase == Phase.DATING and events:
        print(prologue.get_prologue(events[0]['person']))
        print('\n')
        last_event = None
        for event in events:
            narrate_event(event)
            narrate_time(last_event, event)
            last_event = event

    elif phase == Phase.COMMITTED and events:
        narrate_committed(events)


def narrate_experience(event):
    a, b = get_ab(event)
    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        print(artifacts.get_first_date(event))
    if event['rejected']:
        rules = {
            'origin': "#Onday# #want#, #reject#. \n",
            'a': a['name'],
            'b': b['name'],
            'Onday': [
                f"On {event['date'].strftime('%A')},",
                f"{event['date'].strftime('%A')} came around.",
                "Later that week,"
            ],
            'want': [
                '#a# asked #b# if they wanted to hang out',
                '#a# asked #b# if they were free',
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
        print(tracery.Grammar(rules).flatten('#origin#'))
        return
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
            'reply': ["'#response#' #b# replied."]
        }
        rules.update(getInterestRules(a, b, event['interest']))
        grammar = tracery.Grammar(rules)
        print(grammar.flatten('#hobby_proposal# #reply#'))
        logging.debug(
            f"OPEN EXPERIENCE {event['interest']} {event['threshold']} a: {a['open']} b: {b['open']}")
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
                '#enjoyed# intensely passionate evening together',
            ], event['threshold']),
            'they': [
                'they', 'the couple', '#a# and #b#', 'the two of them',
                'the pair'
            ],
            'enjoyed':
            util.rank([
                'spent', 'were happy to spend', 'enjoyed',
                'were excited to spend', 'were thrilled to spend', 'savored',
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
                f"#Onday# #{event['target_property']}#.",
            ],
            'Onday': [
                f"On {event['date'].strftime('%A')}, ",
                f"{event['date'].strftime('%A')} came around. ",
                "Later that week, "
            ],
            'hot': util.rank([
                '#b# noticed that #a# sometimes gave off a mildly unpleasant odor',
                '#a# bragged to #b# about how infrequently their hair needed to be washed',
                '#a# met #b# wearing an old college sweatshirt and an ill-fitting pair of jeans',
                '#a# went to sleep without washing up first. ',
                '#a# bought more skincare products. ',
                '#a# went shopping for the latest trendy fashions. ',
                '#a# went shopping for organic groceries. That figure didn\'t keep itself in shape!',
                '#a# spent the #day# at the gym. That body didn\'t keep itself in shape!',
            ], event['threshold']),
            'con': util.rank([
                '#b# noticed #a# had a lot of dishes piled up in the sink',
                '#a# decided to call in sick to work. After all, you only live once',
                '#a# forgot to do their laundry.',
                '#a# left a couple of dishes piled up in the sink',
                '#a# noticed they needed to vacuum the carpet',
                '#a# decided to start keeping a daily todo list',
                '#a# spent the #day# arranging their books by color and subject',
                '#a# went shopping and purchased a daily planner',
                '#a# stayed late at work',
                '#a# spent the #day# #cleaning# the apartment',
                '#a# spent the #day #cleaning# the apartment. It was moderately dusty',
                '#a# spent the #day# #cleaning# the bathroom. It certainly was in need of some attention',
            ], event['threshold']),
            'exp': util.rank([
                '#a# was upset with #b#, but said nothing. ',
                '#a# was jealous of #b#\'s moderately attractive co-worker.',
                '#a# asked #b# how they were feeling about the relationship. The couple had an earnest conversation about where things were going.',
                '#a# suggested that they begin a weekly relationship-checkin process. #b# agreed happily. '
            ], event['threshold']),
            'neuro': util.rank([
                '#a# fretted. #a# had not heard from #b# for a couple days.',
                '#b# had a night out with friends planned. #a# was happy to pass the evening doing other things',
                '#b# had not responded to #a#\'s text messages for a few hours. #a# sent a followup.',
                '#a# worried when #b# said that they sometimes preferred to be alone. ',
                '#a# worried that #b# did not actually find them to be attractive. '
                '#b# kept a journal of how long it took for #a# to text them back',
                '#a# worried that #b# would leave them some day soon. ',
            ], event['threshold']),
            'cleaning': ['tidying', 'cleaning', 'organizing'],
            'day': ['day', 'morning', 'afternoon', 'evening'],
            'a': a['name'],
            'b': b['name']
        }
        print(tracery.Grammar(rules).flatten('#origin#'))
        # logging.debug(f"Event: {event}")


def narrate_experience_DEPRECATED(event):
    a, b = get_ab(event)
    if event['rejected']:
        result = f"{b['name']} refused. "
    else:
        lower_dict = {
            'libido':
            f'{b["name"]} generally preferred less adventurous sex',
            'extra':
            f'{b["name"]} generally preferred a quieter evening',
            'open':
            f'{b["name"]} generally preferred to do something they were used to',
        }
        higher_dict = {
            'libido': f'{b["name"]} generally preferred more adventurous sex',
            'extra': f'{b["name"]} generally preferred to socialize',
            'open': f'{b["name"]} generally preferred to do something new',
        }
        concession = lower_dict[event['target_property']] if event[
            'concession'] < 0 else higher_dict[event['target_property']]
        logging.debug(
            f"Concession damage for {event['target_property']} is {round(event['concession'], 2)}"
        )
        if abs(event['concession']) > 0.2:
            result = f"{concession}, but agreed anyway. "
        else:
            result = f"{b['name']} agreed {util.enthusiastically(1.5 - abs(event['concession']) / 0.2)}. "
        result += util.rank([
            f"Unfortunately, {b['name']} ended up wishing {b['they']} had done something else instead. ",
            "Unfortunately, it was just so-so. ",
            f"{b['name']} found {b['their']} mind wandering. ",
            "They had a moderately entertaining time. ",
            "It was moderately entertaining. ",
            "They had a wonderful evening. ",
            "They had a mindblowing evening. ",
            "They had an incredible time. ",
            f"It was the most enjoyable time Alex had spent with anyone in a while. ",
        ], event['delta'])

    experiences = {
        'open': [f'go on a boring date', 'go on an exciting date'],
        'libido': [f'have vanilla sex', f'have kinky sex'],
        'extra': [
            f'come over and watch Netflix', 'go out to the club',
            'go to a big party'
        ],
    }
    activity = util.rank(experiences[event['target_property']],
                         event['threshold'])
    rules = {
        'origin': ['#a# #invited# #activity#. #result#'],
        'invited': ['invited #b# to', 'asked #b# to', 'suggested that they'],
        'activity': activity,
        'result': result,
        'a': f'{a["name"]}',
        'b': f'{b["name"]}',
    }
    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        print(artifacts.get_first_date(event))

    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    print(grammar.flatten("#origin#"))
    logging.debug(
        f"The relationship health changed by {round(event['delta'], 2)}. ")


def narrate_conflict(event):
    conflict_narrator.narrate_conflict(event)


def time_passed(event):
    return ""
