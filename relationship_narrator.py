import util
import random
import conflict_dialogue
from relationship import Event, PROP_NAMES, Relationship


def narrate(r: Relationship):
    return narrate_events(r.events)


def get_interest_sentence(name, interest):
    adverbs = ['only vaguely', 'only somewhat', 'kind of', 'moderately', 'very',
               'strongly', 'immediately', 'violently']
    interested = ['intrigued', 'interested',
                  'smitten', 'obsessed', 'lovestruck']
    adverb = adverbs[int(interest * len(adverbs))]
    interested_w = interested[util.clamp(
        int(interest * len(interested)), 0, len(interested) - 1)]
    return f"{name} was {adverb} {interested_w}. "


def narrate_events(events):
    text = ""
    for event in events:
        if event['type'] == Event.MEETING:
            text += "They met in a " + event['location'] + ". "
            text += get_interest_sentence('Alex',
                                          event['protagonist']['interest'])
        elif event['type'] == Event.DEVELOPMENT:
            text += narrate_development(event)
        elif event['type'] == Event.CONFLICT:
            text += narrate_conflict(event)
        else:
            text += time_passed(event)
    text += "They broke up.\n\n"
    return text


def narrate_development(event):
    character_a = event['protagonist']['name'] if event['protagonist_initiated'] else event['person']['name']
    character_b = event['person']['name'] if event['protagonist_initiated'] else event['protagonist']['name']

    if (event['delta'] == 0):
        return f"{character_a} thought about doing something nice for {character_b}, but just couldn't muster up the energy today. Maybe next time. "
    else:
        return f"{character_a} decided to stop by the grocery store to pick up some flowers. {character_b} was delighted. "


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
