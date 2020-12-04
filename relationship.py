import random
import util
import conflict_dialogue
import statistics
import business_gen
import math
from enum import Enum


def scale_trait(val):
    return 1 / (1 + math.exp(-1 * val))


def gauss(base, var):
    return util.clamp(random.gauss(base, var), 0, 1)


def binary_roll(stats):
    # Given array of values 0-1, roll for a true or false outcome
    # that is true an average of the average of the input values
    # eg [0,1] => 50% [0.25, 0.5, 0.75] => 50%
    mean = sum(stats) / len(stats)
    return random.random() < mean


def get_location():
    template = random.choice(['restaurant', 'hardcode'])
    if template == 'restaurant':
        return f"at {business_gen.get_business()}"
    else:
        return random.choice(['at a bar', 'at the local swimming pool', 'in graduate school', 'in a subway station',
                              'in a life drawing class', 'in a pottery studio', 'using the same CrossFit Groupon', 'on an escalator', 'at an axe-throwing bar', 'at a screening of "The Graduate"', 'in the waiting room of CityMD'])


CONFLICT_TARGETS = [
    'hot', 'open', 'extra', 'agree', 'neuro', 'commit', 'libido', 'exp', 'con'
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
    'con': 'messy'
}


class Event(Enum):
    MEETING = 'meeting'
    COMMIT = 'commit'
    CONFLICT = 'conflict'
    EXPERIENCE = 'experience'
    DEVELOPMENT = 'development'
    NOTHING = 'nothing'


class Phase(Enum):
    COURTING = 'courting'
    DATING = 'dating'
    COMMITTED = 'committed'


PHASE_COMMIT_THRESHOLDS = {
    Phase.COURTING: 2,
    Phase.DATING: 5,
    Phase.COMMITTED: 10,
}

PHASE_SCORE_THRESHOLDS = {
    Phase.COURTING: 0.5,
    Phase.DATING: 1,
    Phase.COMMITTED: 1.5,
}


def get_interest(a, b):
    # Function describing how interested a is in b
    d_hotness = b['hot'] * b['hot'] / a['hot']
    return util.clamp(random.gauss(d_hotness, 0.1), 0, 1)


class Relationship:
    phase = Phase.COURTING
    health = 0
    progress = 0

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.a['concessions'] = {
            'open': 0,
            'extra': 0,
            'libido': 0,
            'commit': 0,
            'con': 0,
            'hot': 0,
            'neuro': 0,
            'agree': 0,
            'exp': 0,
        }
        self.b['concessions'] = {
            'open': 0,
            'extra': 0,
            'libido': 0,
            'commit': 0,
            'con': 0,
            'hot': 0,
            'neuro': 0,
            'agree': 0,
            'exp': 0,
        }

    def simulate_experience(self):
        '''
        Simulate an experience event based on the current state
        An experience has the following properties:
            - type (open, extra, commit, libido)
            - threshold (0-1 value)
        '''
        # decide who has an opportunity to initiate the experience
        # a is always the initiator, b responds
        a = self.a
        b = self.b
        if random.random() < 0.5:
            a = self.b
            b = self.a

        # roll for odds of the person actually initiating the experience
        if binary_roll([a['interest'], a['commit']]):
            exp_type = random.choice(['open', 'open', 'extra', 'libido'])
            thresh = random.gauss(a[exp_type], 0.1)
            experience = {
                'type': Event.EXPERIENCE,
                'target_property': exp_type,
                'threshold': thresh,
                'rejected': False,
                'bonding': 0,
                'delta': 0,
                'protagonist': self.a,
                'person': self.b,
                'protagonist_initiated': a == self.a
            }
            # Roll for rejection based on concession damage, interest, commit, and agree

            # only have potential concession damage if the proposed event is congruent
            # with the existing traits. Eg, if A proposes a high open activity but A is
            # lower open than B, no concession damage is taken.
            delta = abs(b[exp_type] - thresh)
            if thresh > b[exp_type] and a[exp_type] > b[exp_type]:
                dmg = delta
            elif thresh < b[exp_type] and a[exp_type] < b[exp_type]:
                dmg = delta
            else:
                dmg = 0

            concession_roll = gauss(b['concessions'][exp_type] + delta, 0.1)
            PHASE_EXPERIENCE_AGREE = {
                Phase.COURTING: 1.2,
                Phase.DATING: 1.1,
                Phase.COMMITTED: 1,
            }
            agree_roll = gauss(
                statistics.mean([b['interest'], b['commit'], b['agree']]),
                0.1,
            ) * PHASE_EXPERIENCE_AGREE[self.phase]

            if agree_roll < concession_roll:
                # reject experience
                experience['rejected'] = True
                return experience
            b['concessions'][exp_type] += dmg
            experience['concession'] = dmg
            experience['delta'] = gauss(1 - concession_roll, 0.2)
            return experience
        return {
            'type': Event.NOTHING,
            'health': self.health,
            'delta': -0.1,
            'protagonist': self.a,
            'person': self.b,
        }

    def simulate_conflict(self, person_initiated, target_property=random.choice(CONFLICT_TARGETS)):
        # decide who has an opportunity to initiate the conflict
        # a is always the initiator, b responds
        a = self.a
        b = self.b
        if random.random() < 0.5:
            a = self.b
            b = self.a

        e = {
            'type': Event.CONFLICT,
            'protagonist': self.a,
            'person': self.b,
            'protagonist_initiated': a == self.a
        }

        # A chooses a thing to conflict about. Weighted sample based on concession damage,
        # so A more likely to choose 'libido' if a high level of existing libido concession.
        e['target_property'] = random.choices(
            population=list(a['concessions'].keys()),
            weights=list(a['concessions'].values())
        )[0]

        # A chooses whether or not to actually fight about it.
        # Fighting is more likely if concession damage is high or
        # if A's neuroticism is high.
        e['concession_roll'] = gauss(a['concessions'][target_property], 0.2)
        e['neuro_roll'] = gauss(a['neuro'], 0.2)

        if e['concession_roll'] < 0.5 and e['neuro_roll'] < 0.5:
            # If it isn't a big deal, return an event with 'initiated' key set to False
            e['initiated'] = False
            e['delta'] = 0
            return e

        e['initiated'] = True

        # Now the conflict has begun. The team must work together to assuage
        # A's concession damage.
        e['target'] = a['concessions'][e['target_property']]
        e['handicap'] = util.scale(random.random(), 0, 1, -0.25, 0.25)

        def get_rolls(p):
            variance = (1.05 - p['exp']) / 4
            rolls = {
                'agree': random.gauss(p['agree'], variance),
                'neuro': random.gauss(p['neuro'], variance),
                'commit': random.gauss(p['commit'], variance),
                'interest': random.gauss(p['interest'], variance)
            }
            rolls['score'] = rolls['agree'] * 0.33 + \
                rolls['commit'] * 0.33 + \
                rolls['interest'] * 0.33 - rolls['neuro']
            return rolls

        e['a_rolls'] = get_rolls(a)
        e['b_rolls'] = get_rolls(b)

        team_score = (e['a_rolls']['score'] + e['b_rolls']['score']) / 2

        # calculate relationship health delta:
        # if the team met the goal: benefit accordingly. But punish more than reward.
        if (team_score + e['handicap'] < e['target']):
            # the team fell short of the goal: punish proportionally.
            delta = team_score + e['handicap'] - e['target'] * 2
        else:
            delta = (team_score + e['handicap'] - e['target']) / 2

        # Now do concession modifiers:
        if delta > 0:
            # They resolved the argument!
            a['concessions'][target_property] *= 0.5
        else:
            # The person who gave more to the conflict is disappointed.
            loser = a
            if e['a_rolls']['score'] < e['b_rolls']['score']:
                loser = b
            loser['interest'] *= 0.9
        e['delta'] = delta

        return e

    def simulate_meeting(self):
        if binary_roll([self.a['confidence'], self.a['interest']]):
            delta = random.gauss(self.b['interest'], 0.3) - 0.5
            return {
                'type': Event.MEETING,
                'location': get_location(),
                'protagonist': self.a,
                'person': self.b,
                'protagonist_initiated': True,
                'delta': delta,
            }
        if binary_roll([self.b['confidence'], self.b['interest']]):
            delta = random.gauss(self.a['interest'], 0.3) - 0.5
            return {
                'type': Event.MEETING,
                'location': get_location(),
                'protagonist': self.a,
                'person': self.b,
                'protagonist_initiated': False,
                'delta': delta,
            }
        return {
            'type': Event.MEETING,
            'location': get_location(),
            'protagonist': self.a,
            'person': self.b,
            # Hardcode delta to -1 to represent neither party approaching the other
            'delta': -1
        }

    def simulate_commit(self, event):
        # Person only has the opportunity to commit event if conditions are met

        # Simulate a commitment event
        a = self.a
        b = self.b
        protag_init = random.random() > 0.5
        if protag_init:
            a = self.b
            b = self.a
        # Roll for whether or not they actually do it
        if not binary_roll([a['confidence'], a['interest'], a['commit']]):
            return self.simulate_nothing()

        event = {
            'type': Event.COMMIT,
            'protagonist': self.a,
            'person': self.b,
            'protagonist_initiated': protag_init,
        }

        # Roll for whether commit event succeeds:
        # TODO add concession damage?
        score = random.gauss(b['interest'], 0.1) + \
            random.gauss(b['commit'], 0.1)
        ratio = score / PHASE_SCORE_THRESHOLDS[self.phase]
        event['success_ratio'] = ratio
        if ratio > 1.2:
            # Random increase to interest + commitment if the response was enthusiastic
            a['commit'] *= 1 + random.random() * 0.1
            a['interest'] *= 1 + random.random() * 0.2
            a['commit'] *= 1 + random.random() * 0.1
            b['interest'] *= 1 + random.random() * 0.2
            a['neuro'] *= 0.9 + random.random() * 0.1
        elif ratio < 0.8:
            # Debuffs if response was not enthusiastic:
            a['commit'] *= 0.9 + random.random() * 0.1
            a['interest'] *= 0.8 + random.random() * 0.2
            a['commit'] *= 0.9 + random.random() * 0.1
            b['interest'] *= 0.8 + random.random() * 0.2
            a['neuro'] *= 1 + random.random() * 0.1

        event['delta'] = (ratio - 1) / 2

        if ratio > 1 and self.phase == Phase.COURTING:
            self.phase = Phase.DATING
            event['phase'] = self.phase
        # TODO: actually make it 2 commit events happen first
        elif ratio > 1 and self.phase == Phase.DATING:
            self.phase = Phase.COMMITTED
            event['phase'] = self.phase

        return event

    def simulate_nothing(self):
        return {
            'type': Event.NOTHING,
            'health': self.health,
            'duration': 1,
            'delta': -0.1,
            'protagonist': self.a,
            'person': self.b,
        }

    def next_event(self, event):
        PHASE_EXPERIENCE_CHANCES = {
            Phase.COURTING: 0.9,
            Phase.DATING: 0.8,
            Phase.COMMITTED: 0.5,
        }
        PHASE_CONFLICT_CHANCES = {
            Phase.COURTING: 0,
            Phase.DATING: 0.2,
            Phase.COMMITTED: 0.5,
        }
        # odds of conflict increase based on neuro
        neuro_mod = util.scale(
            (self.a['neuro'] + self.b['neuro']) / 2, 0, 1, 0.7, 1.3)
        chance_conflict = PHASE_CONFLICT_CHANCES[self.phase] * neuro_mod

        if self.health > PHASE_COMMIT_THRESHOLDS[self.phase] and event.get('delta', 0) > 0.25 and event.get('type') != Event.COMMIT:
            event = self.simulate_commit(event)
        elif event.get('rejected') and self.phase != Phase.COURTING:
            # only trigger a fight if they are in DATING phase
            event = self.simulate_conflict(
                event['protagonist_initiated'], event['target_property'])
        elif (random.random() < PHASE_EXPERIENCE_CHANCES[self.phase]):
            # A development occurred!
            event = self.simulate_experience()
        elif (random.random() < chance_conflict):
            event = self.simulate_conflict(random.random() < 0.5)
        else:
            event = self.simulate_nothing()

        return event

    def simulate(self):
        # Given a pair of people, simulate a relatonship between them
        # We represent a relationship as an array of events represented by dictionaries / objects
        # Then use separate code to turn the array of events into text
        self.events = []
        self.a['interest'] = get_interest(self.a, self.b)
        self.b['interest'] = get_interest(self.b, self.a)

        # simulate attempt to ask out person:
        meeting = self.simulate_meeting()
        self.events.append(meeting)
        self.health += meeting['delta']

        event = {}

        while self.health > 0:
            # Determine the random chance of some event occuring:
            # TODO: adjust based on character properties
            event = self.next_event(event)
            if not event:
                continue
            self.events.append(event)
            self.health += event['delta']
            self.a = event['protagonist']
            self.b = event['person']

        # compress all NOTHING events together
        events = [self.events.pop(0)]
        while len(self.events) > 0:
            event = self.events.pop(0)
            last_event = events[len(events) - 1]
            if last_event['type'] == Event.NOTHING and event['type'] == Event.NOTHING:
                last_event['delta'] += event['delta']
            else:
                events.append(event)
        self.events = events
        return self.events
