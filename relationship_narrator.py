import util
import random
import conflict_dialogue
from relationship import Event, PROP_NAMES, Relationship, Phase


def narrate(r: Relationship):
    return narrate_events(r.events)


def get_interest_sentence(name, interest):
    adverbs = ['vaguely', 'somewhat', 'kind of', 'moderately', 'very',
               'strangely', 'immediately', 'violently']
    interested = ['intrigued', 'interested',
                  'smitten', 'obsessed', 'lovestruck']
    adverb = util.rank(adverbs, interest)
    interested_w = util.rank(interested, interest)
    return f"{name} was {adverb} {interested_w}. "


def narrate_meeting(event):
    if event['delta'] == -1:
        return ""
    text = ""
    a = event['protagonist'] if event['protagonist_initiated'] else event['person']
    b = event['person'] if event['protagonist_initiated'] else event['protagonist']
    if event['protagonist_initiated']:
        text += get_interest_sentence('Alex', event['protagonist']['interest'])
    else:
        text += get_interest_sentence(event['person']
                                      ['name'], event['person']['interest'])
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
        ACCEPTS = [
            f". {b['name']} returned a flirtatious glance. Soon, they got to talking. ",
            f". {b['name']} waved in return. Alex left with {b['name']}'s phone number. ",
            f". {b['name']} smiled back. They exchanged several friendly words. "
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
        f"{time}{a['name']} gazed {adverb} at {b['name']}{followup}",
        f"{time}{a['name']} giggled {adverb}{followup}",
        f"{time}{a['name']} walked {adverb}toward {b['name']}{followup}"
    ]
    return text + random.choice(APPROACHES)


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
