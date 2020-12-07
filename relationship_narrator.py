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
from interests import INTERESTS

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
        f'#b# said that perhaps they were\'t quite ready yet. ',
        'ily_challenge':
        f"#a# says \"I love you\"",
        'ily_result': [
            '#b# could not say it back. #a# is hurt, but is understanding.'
            if event['success_ratio'] < 1 else
            f'#b# returns the words {util.enthusiastically(enthusiasm)}.'
        ],
        'a':
        a['name'],
        'b':
        b['name'],
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
        f"{time}{a['name']} walked {adverb} toward {b['name']}{followup}"
    ]
    print(text + random.choice(APPROACHES) + "\n\n")


CHUNK_SIZE = 12


def narrate_committed(events):
    if len(events) == 0:
        return
    # First the phase change event:
    chunks = list(util.divide_chunks(events, CHUNK_SIZE))
    # For now it's the same as dating :(
    # for chunk in chunks:
    # narrate_dating_chunk(chunk)


def narrate_dating_chunk(events):
    protag = events[0]['protagonist']
    person = events[0]['person']
    # Then describe their experiences:
    experiences = [e for e in events if e['type'] == EventType.EXPERIENCE]
    conflicts = [e for e in events if e['type'] == EventType.CONFLICT]
    commits = [e for e in events if e['type'] == EventType.COMMIT]
    if (len(commits) > 0):
        narrate_commit(commits[0])
    counts = {'open': 0, 'extra': 0, 'libido': 0}
    for e in experiences:
        counts[e['target_property']] += e['delta']
    common_exp_type = max(counts, key=lambda k: counts[k])
    they = random.choice(['The two of them', 'The couple', 'They'])
    pre = random.choice(['found that they ', '', ''])
    loved = random.choice([
        'continued', 'liked', 'loved', 'enjoyed', 'spent much time',
        'continued to bond by'
    ])
    E_DESC = {
        'open': 'going on adventures together',
        # TODO: with hobbies, we can do something interesting
        'extra': 'socializing with friends and colleagues',
        'libido': 'having tons of sex',
    }
    e_delta = sum([e['delta'] for e in experiences])
    c_delta = sum([e['delta'] for e in conflicts])
    logging.debug(f"experience delta: {e_delta}")

    print("\n")
    print(f"{they} {pre}{loved} {E_DESC[common_exp_type]}.")
    if conflicts:
        narrate_conflicts_texture(conflicts, e_delta)
    else:
        adj = util.rank([
            f"felt moderately engaged with the relationship.",
            f"was content with how things were",
            f"felt their eyes light up when looking at {person['name']}.",
            f"was enthralled with the relationship.",
        ], e_delta + c_delta / 2)
        print(f"{protag['name']} {adj}.")


def narrate_conflicts_texture(conflicts, e_delta):
    protag = conflicts[0]['protagonist']
    person = conflicts[0]['person']
    delta = sum([e['delta'] for e in conflicts])
    counts = {
        'open': 0,
        'extra': 0,
        'libido': 0,
        'neuro': 0,
        'commit': 0,
        'con': 0,
        'exp': 0,
        'agree': 0,
        'hot': 0
    }
    for e in conflicts:
        counts[e['target_property']] += e['delta']
    common_exp_type = min(counts, key=lambda k: counts[k])
    a_higher = protag[common_exp_type] > person[common_exp_type]
    a = protag
    b = person
    if not a_higher:
        a = person
        b = protag
    they = random.choice(['The two of them', 'The couple', 'They'])
    often = util.rank([
        'rarely fought, but when they did they', 'occasionally', 'sometimes',
        'often', 'always'
    ],
        len(conflicts) / CHUNK_SIZE * 1.5)
    fought = random.choice(
        ['disagreed', 'fought', 'quarrelled', 'had spats', 'argued'])
    about = random.choice(['about', 'over'])
    C_DESC = {
        'open': [
            f"{b['name']}'s reluctance to try new things",
            f"{a['name']} pushing {b['name']} out of {b['their']} comfort zone"
        ],
        'extra': [
            f"{b['name']}'s lack of social energy",
            f"{a['name']}'s overly gregarious spirit"
        ],
        'libido': [
            f"{b['name']}'s aggressive sex drive",
            f"{a['name']}'s lack of interest in sex"
        ],
        'neuro': [f"{a['name']}'s anxiety"],
        'con': [
            f"{b['name']}'s messiness",
            f"{a['name']}'s preference for cleanliness"
        ],
        'hot': [f"{b['name']}'s insecurity about their appearance"],
        'exp': [f"{b['name']}'s lack of experience with relationships"],
        'agree': [f"{b['name']}'s lack of agreeability"],
        'commit': [f"{b['name']}'s lack of commitment to the relationship"]
    }
    print(
        f"{they} {often} {fought} {about} {random.choice(C_DESC[common_exp_type])}. "
    )

    logging.debug(f"conflict delta: {delta}")
    scaled_delta = util.scale(delta, -3, 1, 1, 0)
    expansion = util.rank([
        "usually forgotten about the next day",
        "quick to resolve",
        "barely cause for concern",
        "minor",
        "somewhat virulent",
        "draining",
        "explosive",
    ], scaled_delta)
    fights = random.choice(
        ['scuffles', 'disagreements', 'fights', 'arguments', 'spats'])
    if delta + e_delta > 0:
        conj = ", but" if scaled_delta > 0.5 else ";"
        connect = random.choice([
            f"{conj} {b['name']} was often willing to apologize and make things right. ",
            f"{conj} {b['name']} was open to coming up with new solutions.",
            f"{conj} {b['name']} was happy to adapt for {a['name']}.",
            f"{conj} {b['name']} was willing to sacrifice for the good of the relationship."
        ])
        # Insert apology artifact here!
        adverb = util.adverb(util.scale(delta + e_delta, 0, 3, 0, 1))
        adjective = random.choice(['happy', 'content', 'satisfied', 'pleased'])
        rel = random.choice([
            'with how things were going', 'with the relationship',
            'despite the arguments'
        ])
        overall = f"Alex was {adverb} {adjective} {rel}"
    else:
        conj = ", but" if scaled_delta < 0.5 else ";"
        connect = random.choice([
            f"{conj} {b['name']} was rarely willing to give {a['name']} the benefit of the doubt. ",
            f"{conj} {b['name']} didn't apologize easily.",
            f"{conj} {b['name']} didn't seem to want to make any changes. ",
            f"{conj} {b['name']} didnt care to work to come up with a good solution.",
        ])
        clause = random.choice([
            'began to feel disengaged',
            f"started to feel their mind wandering when talking to {person['name']}",
            f"found themselves ignoring messages from {person['name']} more and more often",
            f"found themselves enjoying time spent with {person['name']} less and less",
            f"began to feel like planning dates with {person['name']} was a chore",
            f"found themselves going to {business_gen.get_business()} alone",
        ])
        overall = f"Alex {clause}"
    print(f'These {fights} were {expansion}{connect} {overall}.')


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
        last_event = None
        for event in events:
            narrate_event(event)
            narrate_time(last_event, event)
            last_event = event

        # narrate_committed(events)
        # for event in events:
        #    narrate_event(event)
    elif phase == Phase.COMMITTED and events:
        narrate_committed(events)


def narrate_experience(event):
    a, b = get_ab(event)
    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        print(artifacts.get_first_date(event))
    if event['rejected']:
        # TODO
        return
    if event['target_property'] == 'open':
        rules = {
            'a':
            a['name'],
            'b':
            b['name'],
            'their':
            a['their'],
            'hobby':
            [f"{random.choice(INTERESTS[event['interest']]['hobbies'])}"],
            # types of classes
            'food_class': [
                'grilling', 'cheesemaking', 'cooking', 'bartending',
                'cocktail-making', 'beer-brewing', 'breadmaking'
            ],
            'proposed': [
                "asked to", "begged to", "proposed that they",
                "wondered if it would be fun to", "suggested that they",
                "wanted to", "invited #b# to"
            ],
            'hobby_proposal': [
                f"#a# #proposed# go to {random.choice(INTERESTS[event['interest']]['location'])}.",
                f"#a# #proposed# {random.choice(INTERESTS[event['interest']]['verb'])}."
            ]
        }
        grammar = tracery.Grammar(rules)
        print(grammar.flatten('#hobby_proposal#'))
        logging.debug(
            f"OPEN EXPERIENCE {event['interest']} {event['threshold']}")
    elif event['target_property'] in ['extra', 'libido']:
        rules = {
            'origin':
            f"#they# #enjoyed# #{event['target_property']}#.",
            'extra':
            util.rank([
                'a tranquil night together',
                'a tranquil evening watching Netflix',
                'a quiet night in together',
                'a night out together',
                'an evening hanging out with friends',
                'an afternoon people-watching',
                'a boisterous night out at the club',
            ], event['threshold']),
            'libido':
            util.rank([
                'a quiet evening together',
                'a subdued evening together',
                'a passionate evening together',
                'an intensely passionate evening together',
            ], event['threshold']),
            'they': [
                'They', 'The couple', '#a# and #b#', 'The two of them',
                'The pair'
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
        print(tracery.Grammar(rules).flatten('#origin#'))
    else:
        rules = {
            'origin': [
                f"#a# #{event['target_property']}#.",
            ],
            'hot': util.rank([
                'sometimes gave off a mildly unpleasant odor',
                'liked to brag about how infrequently their hair needed to be washed',
                'often met #b# for dates wearing an old college sweatshirt and an ill-fitting pair of jeans',
                'fell asleep sometimes without washing up first. ',
                'considered indulging in more skincare products. ',
                'liked to go shopping for the latest trendy fashions. ',
                'went shopping for organic groceries. That figure didn\'t keep itself in shape!',
                'spent the #day# at the gym. That body didn\'t keep itself in shape!',
            ], event['threshold']),
            'con': util.rank([
                'had a lot of dishes piled up in the sink. ',
                'was messy.',
                'forgot to do their laundry yesterday. ',
                'had a couple of dishes piled up in the sink. ',
                'was disorganized. ',
                'noticed they needed to vacuum the carpet.'
                'decided to start keeping a daily todo list. ',
                'went shopping and purchased a daily planner. ',
                'spent the #day# #cleaning# the apartment. ',
                'spent the #day #cleaning# the apartment. It was moderately dusty. ',
                'spent the #day# #cleaning# the bathroom. It certainly was in need of some attention. ',
            ], event['threshold']),
            'exp': util.rank([
                'was upset with #b#, but said nothing. ',
                'was jealous of #b#\'s moderately attractive co-worker.',
                'asked #b# how they were feeling about the relationship. The couple had an earnest conversation about where things were going.',
                '#a# suggested that they begin a weekly relationship-checkin process. #b# agreed happily. '
            ], event['threshold']),
            'neuro': util.rank([
                '#a# had not heard from #b# for a couple days.',
                '#b# had a night out with friends planned today. #a# was happy to pass the evening doing other things',
                '#b# had not responded to #a#\'s text messages for a few hours. #a# sent a followup.',
                'worried when #b# said that they sometimes preferred to be alone. ',
                'worried that #b# did not actually find them to be attractive. '
                'worried that #b# would leave them some day soon. ',
            ], event['threshold']),
            'cleaning': ['tidying', 'cleaning', 'organizing']
            'day': ['day', 'morning', 'afternoon', 'evening'],
            'a': a['name']
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
