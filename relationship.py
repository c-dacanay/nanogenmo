import random
import util
from enum import Enum

LOCATIONS = ['bar', 'pool', 'school', 'subway station']


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
    protag_interest = get_interest(protagonist, person)
    person_interest = get_interest(person, protagonist)

    events.append({
        'type': Event.MEETING,
        'location': random.choice(LOCATIONS),
        'protag_interest': protag_interest,
        'person_interest': person_interest,
    })

    while relationship_health > 0:
        # Determine the random chance of some event occuring:
        # TODO: adjust based on character properties
        chance_conflict = 0.5
        chance_development = 0.33
        if (random.random() < chance_development):
            # A development occurred!
            delta = random.random() / 2
            events.append({
                'type': Event.DEVELOPMENT,
                'relationship_health': relationship_health,
                'delta': delta,
                'protag_interest': protag_interest,
                'person_interest': person_interest,
            })
        elif (random.random() < chance_conflict):
            # Roll dice for resolution quality
            resolution_quality = random.random()
            delta = 0.1 - resolution_quality
            events.append({
                'type': Event.CONFLICT,
                'relationship_health': relationship_health,
                'delta': delta,
                'protag_interest': protag_interest,
                'person_interest': person_interest,
            })
        else:
            delta = -0.1
            if events[len(events) - 1]['type'] == Event.NOTHING:
                events[len(events) - 1]['duration'] += 1
                events[len(events) - 1]['delta'] += delta
            else:
                events.append({
                    'type': Event.NOTHING,
                    'duration': 1,
                    'delta': delta,
                    'person': person,
                })
        relationship_health += delta

    # Collapse NOTHING events together
    return events


def narrate_events(events):
    text = ""
    for event in events:
        if event['type'] == Event.MEETING:
            text += "They met in a " + event['location'] + ".\n"
        elif event['type'] == Event.DEVELOPMENT:
            text += "They developed.\n"
        elif event['type'] == Event.CONFLICT:
            text += "They fought.\n"
        else:
            text += time_passed(event)
    text += "They broke up.\n\n"
    return text


def time_passed(event):
    # "It was X days before Alex heard from Person again
    if event['duration'] == 1:
        days = 'day'
    else:
        days = 'days'
    return f"It was {event['duration']} {days} before Alex heard from {event['person']['name']} again.\n"
