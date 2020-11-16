import random
import util
from enum import Enum

LOCATIONS = ['bar', 'pool', 'school', 'subway station']

CONFLICT_TARGETS = [
    'hot', 'open', 'extra', 'agree', 'neuro', 'commit', 'libido', 'exp'
]

PROP_NAMES = {
    'hot': 'hot',
    'open': 'open',
    'extra': 'extroverted',
    'agree': 'nice',
    'neuro': 'neurotic',
    'commit': 'serious about the relationship',
    'libido': 'interested in sex',
    'exp': 'mature for their age',
}


class Event(Enum):
    MEETING = 'meeting'
    CONFLICT = 'conflict'
    DEVELOPMENT = 'development'
    NOTHING = 'nothing'


def get_relationship(protagonist, person):
    events = get_events(protagonist, person)
    return narrate_events(events)


def get_interest(protagonist, person):
    # For now only use hotness
    # Return value 0-1 reflecting the difference in hotness
    # Use gaussian random noise for variance
    d_hotness = (person['hot'] - protagonist['hot'] + 1)/2
    return util.clamp(random.gauss(d_hotness, 0.1), 0, 1)


def get_events(protagonist, person):
    # Given a pair of people, simulate a relatonship between them
    # We represent a relationship as an array of events represented by dictionaries / objects
    # Then use separate code to turn the array of events into text
    events = []
    relationship_health = 1
    protagonist['interest'] = get_interest(protagonist, person)
    person['interest'] = get_interest(person, protagonist)

    events.append({
        'type': Event.MEETING,
        'location': random.choice(LOCATIONS),
        'protagonist': protagonist,
        'person': person,
    })

    while relationship_health > 0:
        # Determine the random chance of some event occuring:
        # TODO: adjust based on character properties
        chance_conflict = 0.5
        chance_development = 0.33
        if (random.random() < chance_development):
            # A development occurred!
            event = process_development(protagonist, person, events)
        elif (random.random() < chance_conflict):
            event = process_conflict(protagonist, person, events)
        else:
            event = {
                'type': Event.NOTHING,
                'duration': 1,
                'delta': -0.1,
                'protagonist': protagonist,
                'person': person,
            }

        events.append(event)
        relationship_health += event['delta']
        protagonist = event['protagonist']
        person = event['person']

    # Collapse NOTHING events together
    return events


def process_development(protagonist, person, events):
    def get_rolls(p):
        variance = (1.05 - p['exp']) / 4
        return random.gauss(p['interest'], variance) / 2 + random.gauss(p['commit'], variance) / 2
    delta = 0
    score = 0
    protagonist_initiated = False
    intensity = random.random()
    if random.random() < 0.5:
        protagonist_initiated = True
        # Give the protag a chance to do something nice for person:
        score = get_rolls(protagonist)
        if score > intensity:
            # Protag decides to invest into the relationship
            person['interest'] += intensity / 2
            delta = intensity / 4
    else:
        # Give the person a chance to do something nice for protag:
        score = get_rolls(person)
        if score > intensity:
            # Protag decides to invest into the relationship
            protagonist['interest'] += intensity / 2
            delta = intensity / 4
    return {
        'type': Event.DEVELOPMENT,
        'delta': delta,
        'score': score,
        'intensity': intensity,
        'protagonist_initiated': protagonist_initiated,
        'protagonist': protagonist,
        'person': person,
    }


def process_conflict(protagonist, person, events):
    # In order for the pair to successfully navigate
    # the conflict, they must have close to the same value
    # for the conflict_target property. Eg, if the conflict
    # is about "libido", the pair has a better chance of navigating
    # the issue if their libido properties are closely matched.

    # Of course, this isn't the only thing that goes into it!
    # The "difficulty" or "stakes" of the conflict determine
    # how close together their properties must be for "success"
    # The other personality traits can play a role as well.

    # Ultimately, a conflict results in a delta to the overall relationship health,
    # and a delta in both partners' interest scores. It also can end in
    # a resolved, or unresolved state. If the conflict is unresolved,
    # the delta to the relationship health in the short term is usually lower
    # but in the future a similar conflict will be more difficult to overcome.
    def get_rolls(p):
        variance = (1.05 - p['exp']) / 4
        rolls = {
            'open': random.gauss(p['open'], variance),
            'agree': random.gauss(p['agree'], variance),
            'neuro': random.gauss(p['neuro'], variance),
            'commit': random.gauss(p['commit'], variance),
            'interest': random.gauss(p['interest'], variance)
        }
        rolls['score'] = rolls['open'] * 0.25 + rolls['agree'] * 0.25 + \
            rolls['commit'] * 0.25 + rolls['interest'] * 0.25 - rolls['neuro']
        return rolls

    target_property = random.choice(CONFLICT_TARGETS)
    target = abs(person[target_property] - protagonist[target_property])
    handicap = random.random() / 4 - 0.5
    protag_rolls = get_rolls(protagonist)
    person_rolls = get_rolls(person)
    team_score = (protag_rolls['score'] + person_rolls['score']) / 2

    # calculate relationship health delta:
    # if the team met the goal: benefit accordingly. But punish more than reward.
    if (team_score + handicap < target):
        # the team fell short of the goal: punish proportionally.
        delta = team_score + handicap - target
        if protag_rolls['score'] < person_rolls['score']:
            protagonist['interest'] *= 0.8
        else:
            person['interest'] *= 0.8
    else:
        delta = (team_score + handicap - target) / 2

    return {
        'type': Event.CONFLICT,
        'target_property': target_property,
        'team_score': team_score,
        'handicap': handicap,
        'target': target,
        'protag_rolls': protag_rolls,
        'person_rolls': person_rolls,
        'delta': delta,
        'protagonist': protagonist,
        'person': person
    }


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
    character = event['protagonist']['name'] if event['protagonist_initiated'] else event['person']['name']
    characterb = event['person']['name'] if event['protagonist_initiated'] else event['protagonist']['name']
    if (event['delta'] == 0):
        return f"{character} thought about doing something nice for {characterb}, but just couldn't muster up the energy today. Maybe next time. "
    else:
        return f"{character} decided to stop by the grocery store to pick up some flowers. {characterb} was delighted. "


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
