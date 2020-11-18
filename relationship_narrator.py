import util
import random
import conflict_dialogue
from relationship import Event, PROP_NAMES, Relationship, Phase


def narrate(r: Relationship):
    return narrate_events(r.events)


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
        'hot': [f"{person['name']}'s {random.choice(['lithe', 'well-defined', 'striking'])} {random.choice(['features', 'body', 'muscles'])}"],
        'open': [f"{person['name']}'s {random.choice(['pealing laughter', 'earnest expression'])}"],
        'con': [f"{person['name']}'s intense focus"],
        'extra': [f"{person['name']}'s friendly {random.choice(['disposition', 'demeanor', 'attitude'])}"],
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
    adjective = ['noticed', 'was struck by',
                 'was fascinated by', "couldn't help but notice"]
    prop = get_salient_property(b)
    adverbs = ['vaguely', 'somewhat', 'kind of', 'moderately', 'very',
               'strangely', 'immediately', 'violently']
    interested = ['intrigued', 'interested',
                  'smitten', 'obsessed', 'lovestruck']
    return f"{a['name']} {random.choice(adjective)} {prop}. "


def narrate_meeting(event):
    if event['delta'] == -1:
        return ""
    text = ""
    a = event['protagonist'] if event['protagonist_initiated'] else event['person']
    b = event['person'] if event['protagonist_initiated'] else event['protagonist']
    if event['protagonist_initiated']:
        text += get_interest_sentence(event['protagonist'],
                                      event['person'], event['protagonist']['interest'])
    else:
        text += get_interest_sentence(event['person'],
                                      event['protagonist'],
                                      event['person']['interest'])
    adverb = util.rank(['nervously', 'shyly', 'quietly', '',
                        'gently', 'intently', 'boldly'], a['interest'])

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
            'phone number',
            'email',
            'contact',
            'phone number scrawled onto a crumpled piece of paper',
            'phone number hastily scribbled on a napkin',
            'email address dashed onto a post-it note',
            'Discord server invite',
            'laughter echoing in their ears',
            'smile etched into their memory',
            'Instagram handle'
        ])
        follow3 = random.choice([
            f"{a['name']} left with {b['name']}'s {contact}. ",
            f"{b['name']} left with {a['name']}'s {contact}. ",
        ])
        ACCEPTS = [
            f". {b['name']} returned a flirtatious glance. {follow2}{follow3}",
            f". {b['name']} waved in return. {follow2}{follow2}",
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
    return text + random.choice(APPROACHES) + "\n\n"


def narrate_events(events):
    text = "They met " + events[0]['location'] + ". "
    for event in events:
        if event is None:
            continue
        if event['type'] == Event.MEETING:
            text += narrate_meeting(event)
        elif event['type'] == Event.DEVELOPMENT:
            text += narrate_development(event)
        elif event['type'] == Event.CONFLICT:
            text += narrate_conflict(event)
        else:
            text += time_passed(event)
    text += "They never saw each other again.\n\n"
    return text


def narrate_courting_development(event, a, b):
    if (event['delta'] == 0):
        return f"Out of the corner of Alex's eye, {a['name']} tried to work up the courage to say something, but failed."
    else:
        return f"{a['name']} sidled up next to {b['name']} and asked about {b['their']} "


def narrate_development(event):
    a = event['protagonist'] if event['protagonist_initiated'] else event['person']
    b = event['person'] if event['protagonist_initiated'] else event['protagonist']

    if (event['delta'] == 0):
        return f"{a['name']} thought about doing something nice for {b['name']}, but just couldn't muster up the energy today. Maybe next time. "
    else:
        return f"{a['name']} decided to stop by the grocery store to pick up some flowers. {b['name']} was delighted. "


def narrate_conflict(event):
    # TODO EMILY
    # The conflict event has a lot of properties that we can use to influence the generated text.
    # You can view how they are constructed in the function process_conflict
    # The most interesting ones are probably:
    # target_property: the conflict is based around this property. the closer the team's two scores,
    # the more easily they can navigate the conflict.
    # team_score, handicap, target. team_score represents how much effort the couple put in to
    # resolving the problem. target - handicap is the required level of effort. if they fall short, the relationship
    # is damaged.
    # if (random.random() < 1):
    #    return conflict_dialogue.get(event)
    target_p = event['target_property']
    prop_name = PROP_NAMES[target_p]
    if (target_p == 'extra'):
        return f"{event['protagonist']['name']} and {event['person']['name']} had a disagreement about whether to go to a party or stay in. "
    character_a = event['protagonist']['name'] if event['protagonist'][
        target_p] > event['person'][target_p] else event['person']['name']
    return f"They fought because {character_a} was too {prop_name}. "


def time_passed(event):
    return ""
    if event['duration'] == 1:
        days = 'day'
    else:
        days = 'days'
    if (event['protagonist']['interest'] < event['person']['interest']):
        return f"Alex didn't text {event['person']['name']} for {event['duration']} {days}. \n"
    else:
        return f"It was {event['duration']} {days} before Alex heard from {event['person']['name']} again.\n"
