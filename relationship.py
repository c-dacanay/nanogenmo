import random
import util
import conflict_dialogue
import statistics
import business_gen
from enum import Enum


def binary_roll(stats):
    # Given array of values 0-1, roll for a true or false outcome
    # that is true an average of the average of the input values
    # eg [0,1] => 50% [0.25, 0.5, 0.75] => 50%
    return random.random() < statistics.mean(stats)


def get_location():
    template = random.choice(['restaurant', 'hardcode'])
    if template == 'restaurant':
        return f"at {business_gen.get_business()}"
    else:
        return random.choice(['at a bar', 'at the local swimming pool', 'in graduate school', 'in a subway station',
                              'in a life drawing class', 'in a pottery studio', 'using the same CrossFit Groupon', 'on an escalator', 'at an axe-throwing bar', 'at a screening of "The Graduate"', 'in the waiting room of CityMD'])


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

def get_interest(protagonist, person):
    # For now only use hotness
    # Return value 0-1 reflecting the difference in hotness
    # Use gaussian random noise for variance
    d_hotness = (person['hot'] - protagonist['hot'] + 1)/2
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
        }
        self.b['concessions'] = {
            'open': 0,
            'extra': 0,
            'libido': 0,
            'commit': 0,
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
            exp_type = random.choice(['open', 'extra', 'libido'])
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
            # Calcualte concession threshold and reject if this experience
            # would put b's concession score over the threshold.
            # TODO allow other person to reject for other reasons
            concession_threshold = b['interest'] + b['commit'] + b['agree']
            delta = abs(b[exp_type] - thresh)
            if b['concessions'][exp_type] + delta > concession_threshold:
                # reject experience
                experience['rejected'] = True
                return experience
            b['concessions'][exp_type] += delta
            experience['concession'] = b[exp_type] - thresh 
            # Increase relatinonship health and progress by random value
            experience['delta'] = random.random()
            return experience
        return {
            'type': Event.NOTHING,
            'health': self.health,
            'delta': -0.1,
            'protagonist': self.a,
            'person': self.b,
        }

    def simulate_development(self):
        '''
        Simulate a development event based on the current state of the
        relationship
        '''
        def get_rolls(p):
            variance = (1.05 - p['exp']) / 4
            return util.clamp(random.gauss(p['interest'], variance) / 2 + random.gauss(p['commit'], variance) / 2, 0, 1)
        delta = 0
        protagonist_initiated = False
        if random.random() < 0.5:
            initiator = self.a
            receiver = self.b
            protagonist_initiated = True
        else:
            initiator = self.b
            receiver = self.a
            protagonist_initiated = False

        thresh = 0.5
        init_roll = get_rolls(initiator)
        recv_roll = get_rolls(receiver) - 0.5

        if init_roll > thresh:
            self.b['interest'] += recv_roll
            delta = recv_roll / 2

        return {
            'type': Event.DEVELOPMENT,
            'phase': self.phase,
            'delta': delta,
            'recv': recv_roll,
            'protagonist_initiated': protagonist_initiated,
            'protagonist': self.a,
            'person': self.b,
        }

    def simulate_conflict(self, target_property=random.choice(CONFLICT_TARGETS)):
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
                rolls['commit'] * 0.25 + \
                rolls['interest'] * 0.25 - rolls['neuro']
            return rolls

        target = abs(self.b[target_property] - self.a[target_property])
        handicap = random.random() / 4 - 0.5
        protag_rolls = get_rolls(self.a)
        person_rolls = get_rolls(self.b)
        team_score = (protag_rolls['score'] + person_rolls['score']) / 2

        # calculate relationship health delta:
        # if the team met the goal: benefit accordingly. But punish more than reward.
        if (team_score + handicap < target):
            # the team fell short of the goal: punish proportionally.
            delta = team_score + handicap - target
            if protag_rolls['score'] < person_rolls['score']:
                self.a['interest'] *= 0.8
            else:
                self.b['interest'] *= 0.8
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
            'protagonist': self.a,
            'person': self.b,
            'protagonist_initiated': random.random() < 0.5
        }

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
        score = random.gauss(b['interest'], 0.1) + random.gauss(b['commit'], 0.1)
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
        chance_experience = .9
        PHASE_CONFLICT_CHANCES = {
            Phase.COURTING: 0,
            Phase.DATING: 0.1,
            Phase.COMMITTED: 0.2,
        }
        
        if self.health > PHASE_COMMIT_THRESHOLDS[self.phase] and event.get('delta', 0) > 0.25 and event.get('type') != Event.COMMIT:
            event = self.simulate_commit(event)
        elif event.get('rejected') and self.phase != Phase.COURTING:
            # only trigger a fight if they are in DATING phase
            event = self.simulate_conflict(event['target_property'])
        elif (random.random() < chance_experience):
            # A development occurred!
            event = self.simulate_experience()
        elif (random.random() < PHASE_CONFLICT_CHANCES[self.phase]):
            event = self.simulate_conflict()
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
                continue;
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
