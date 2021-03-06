import random
import datetime
import util
import conflict_dialogue
import logging
import statistics
import business_gen
import math
from enum import Enum
from interests import INTERESTS


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
        return random.choice([
            'at a bar', 'at the local swimming pool', 'in graduate school',
            'in a subway station', 'in a life drawing class',
            'in a pottery studio', 'using the same CrossFit Groupon',
            'on an escalator', 'at an axe-throwing bar',
            'at a screening of "The Graduate"', 'in the waiting room of CityMD'
        ])


CONFLICT_TARGETS = [
    'hot', 'open', 'extra', 'agree', 'neuro', 'commit', 'libido', 'exp', 'con'
]

PROP_NAMES = {
    'hot': 'attractiveness',
    'open': 'openness',
    'extra': 'introversion and extraversion',
    'agree': 'agreeability',
    'neuro': 'neuroticism',
    'commit': 'level of commitment',
    'libido': 'interest in sex',
    'exp': 'relationship experience',
    'con': 'conscientiousness'
}


class EventType(Enum):
    MEETING = 'meeting'
    COMMIT = 'commit'
    CONFLICT = 'conflict'
    EXPERIENCE = 'experience'
    NOTHING = 'nothing'
    DEATH = 'death'


class Phase(Enum):
    MEETING = 'meeting'
    COURTING = 'courting'
    DATING = 'dating'
    COMMITTED = 'committed'


PHASE_COMMIT_THRESHOLDS = {
    Phase.COURTING: 2.0,
    Phase.DATING: 4.0,
    Phase.COMMITTED: 6.0,
}

PHASE_SCORE_THRESHOLDS = {
    Phase.COURTING: 0.4,  # 0.4
    Phase.DATING: 0.7,  # 0.8
    Phase.COMMITTED: 2,
}


def get_interest(a, b):
    # Function describing how interested a is in b
    d_hotness = b['hot'] * b['hot'] / a['hot']
    return util.clamp(random.gauss(d_hotness, 0.1), 0.0, 1.0)


class Relationship:
    phase = Phase.MEETING
    health = 0
    progress = 0

    def __init__(self, a, b, date):
        self.date = date
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
        logging.debug("BEGIN EXPERIENCE event")
        # decide who has an opportunity to initiate the experience
        # a is always the initiator, b responds
        a = self.a
        b = self.b
        if random.random() < 0.5:
            a = self.b
            b = self.a

        # roll for odds of the person actually initiating the experience
        if binary_roll([a['interest'], a['commit']]):
            PHASE_EXPERIENCE_TYPES = {
                Phase.COURTING: ['open', 'extra', 'libido'],
                # no neuro events currently
                Phase.DATING: ['open', 'extra', 'libido', 'con', 'exp'],
                Phase.COMMITTED:
                ['open', 'extra', 'libido', 'hot', 'con', 'exp', 'commit'],
            }
            exp_type = random.choice(PHASE_EXPERIENCE_TYPES[self.phase])
            thresh = random.gauss(a[exp_type], 0.1)
            logging.debug(
                f"{a['name']} initiatsPHASE {exp_type} experience with value {thresh}")
            experience = {
                'type': EventType.EXPERIENCE,
                'target_property': exp_type,
                'threshold': thresh,
                'rejected': False,
                'bonding': 0,
                'delta': -0.1,
                'protagonist': self.a,
                'person': self.b,
                'protagonist_initiated': a == self.a
            }
            # Roll for rejection based on concession damage, interest, commit, and agree

            if exp_type == 'open':
                # pick a hobby based on the level of experience (Threshold)
                if thresh < 0.33:  # Not very open: choose own activities
                    if a['interests']:
                        interest = random.choice(a['interests'])
                    else:
                        interest = 'do nothing'
                elif thresh < 0.66:  # lo - Medium open: choose shared or others activities
                    if b['interests']:
                        interest = random.choice(b['interests'])
                    else:
                        interest = 'do nothing'
                else:  # High open: choose new activity
                    interest = random.choice(list(INTERESTS.keys()))

                # Now calculate distance for receiver
                if interest in b['interests']:
                    # A proposed an interest that B likes
                    # If B has high open, then delta is 0.5 (they kinda like it)
                    # If B has low open, then delta is 0 (they like it)
                    delta = util.scale(b['open'], 0, 1, 0, 0.5)
                else:
                    # A proposed an interest that B doesn't like
                    # If B has high open, then delta is 0 (they like it)
                    # If B has low open, then delta is 1 (they hate it)
                    delta = util.scale(b['open'], 0, 1, 1, 0)

                # save the chosen interest in the event so we can use it
                # in narration
                experience['interest'] = interest
            else:
                # for other experience types, damage is directly calculated
                # by comparing the receiver property with the proposed threshold
                delta = abs(b[exp_type] - thresh)

            # only have potential concession damage if the proposed event is congruent
            # with the existing traits. Eg, if A proposes a high open activity but A is
            # lower open than B, no concession damage is taken.
            if thresh > b[exp_type] and a[exp_type] > b[exp_type]:
                dmg = delta
            elif thresh < b[exp_type] and a[exp_type] < b[exp_type]:
                dmg = delta
            else:
                dmg = 0

            concession_roll = gauss(b['concessions'][exp_type] + delta, 0.1)
            logging.debug(
                f"{b['name']} takes {exp_type}-damage = {dmg}")
            PHASE_EXPERIENCE_AGREE = {
                Phase.COURTING: 1.3,
                Phase.DATING: 1.15,
                Phase.COMMITTED: 1,
            }
            agree_roll = gauss(
                statistics.mean([b['interest'], b['commit'], b['agree']]),
                0.1,
            ) * PHASE_EXPERIENCE_AGREE[self.phase]

            experience['agree_roll'] = agree_roll
            experience['concession_roll'] = concession_roll
            experience['concession'] = dmg
            if agree_roll < concession_roll:
                logging.debug(f"{b['name']} rejected the offer")
                # reject experience
                experience['rejected'] = True
                return experience
            b['concessions'][exp_type] += dmg
            experience['delta'] = gauss(
                PHASE_EXPERIENCE_AGREE[self.phase] - concession_roll, 0.3)
            return experience
        logging.debug("EXPERIENCE failed - not sufficient interest")
        return {
            'type': EventType.NOTHING,
            'health': self.health,
            'delta': -0.1,
            'protagonist': self.a,
            'person': self.b,
        }

    def simulate_conflict(self):
        # decide who has an opportunity to initiate the conflict
        # a is always the initiator, b responds
        a = self.a
        b = self.b
        if random.random() < 0.5:
            a = self.b
            b = self.a
        logging.debug("BEGIN CONFLICT event")

        e = {
            'type': EventType.CONFLICT,
            'protagonist': self.a,
            'person': self.b,
            'protagonist_initiated': a == self.a
        }

        total_concession = sum(a['concessions'].values())
        # Don't fight if there's nothing to fight about,
        # this will really only apply for the very first event
        # in the relationship
        if total_concession == 0:
            return self.simulate_nothing()

        # A chooses a thing to conflict about. Weighted sample based on concession damage,
        # so A more likely to choose 'libido' if a high level of existing libido concession.
        target_property = random.choices(
            population=list(a['concessions'].keys()),
            weights=list(a['concessions'].values())
        )[0]

        e['target_property'] = target_property

        # Include previous fights
        e['prev'] = [f for f in self.events if f['type'] ==
                     EventType.CONFLICT and f['target_property'] == target_property]

        # A chooses whether or not to actually fight about it.
        # Fighting is more likely if concession damage is high or
        # if A's neuroticism is high.
        e['concession_roll'] = gauss(a['concessions'][target_property], 0.1)
        e['neuro_roll'] = gauss(a['neuro'], 0.1)
        e['target'] = a['concessions'][target_property]

        logging.debug(
            f"{target_property} is chosen, a rolls {e['concession_roll']} for existing damage and {e['neuro_roll']} for neuroticism")

        if e['concession_roll'] < 0.5 and e['neuro_roll'] < 0.5:
            # If it isn't a big deal, return an event with 'initiated' key set to False
            logging.debug("Neither sufficient to trigger a conflict, abort")
            e['initiated'] = False
            e['delta'] = 0
            return e

        e['initiated'] = True

        # Now the conflict has begun. B must assuage
        # A's concession damage.
        e['handicap'] = util.scale(random.random(), 0, 1, -0.25, 0.25)

        variance = (1.05 - b['exp']) / 4
        rolls = {
            'agree': random.gauss(b['agree'], variance) * 0.5,
            'neuro': random.gauss(b['neuro'], variance) * -1,
            'commit': random.gauss(b['commit'], variance) * 0.5,
            'interest': random.gauss(b['interest'], variance) * 0.5,
        }
        e['rolls'] = rolls

        score = rolls['agree'] + rolls['commit'] + \
            rolls['interest'] + rolls['neuro']
        e['score'] = score
        logging.debug(
            f"{b['name']} rolls {score}, needs to match {e['target'] - e['target']}")

        # calculate relationship health delta:
        # if b met the goal: benefit accordingly. But punish more than reward.
        if (score + e['handicap'] < e['target']):
            # b fell short of the goal: punish proportionally.
            # more punishment if the couple is further along in the relationship
            PHASE_CONFLICT_MULTIPLIERS = {
                Phase.COURTING: 2,
                Phase.DATING: 3,
                Phase.COMMITTED: 4,
            }
            delta = score + e['handicap'] - e['target'] * \
                PHASE_CONFLICT_MULTIPLIERS[self.phase]
        else:
            delta = (score + e['handicap'] - e['target']) / 2

        # Now do concession modifiers:
        if delta > 0:
            # They resolved the argument!
            # A feels better and recovers some concession damage
            a['concessions'][target_property] *= 0.25
        else:
            # a is pissed and loses interest in the relationship
            a['interest'] *= 0.9
        e['delta'] = delta

        return e

    def simulate_meeting(self):
        logging.debug(
            f"Meeting began, Alex has confidence f{self.a['confidence']} and interest level {self.a['interest']})"
        )
        if binary_roll([self.a['confidence'], self.a['interest']]):
            logging.debug("Meeting succeded! Alex initiates contact")
            delta = random.gauss(self.b['interest'], 0.2)
            return {
                'type': EventType.MEETING,
                'protagonist_chance': statistics.mean([self.a['confidence'], self.a['interest'], 0.6]),
                'location': get_location(),
                'protagonist': self.a,
                'person': self.b,
                'protagonist_initiated': True,
                'delta': delta,
            }
        logging.debug(
            f"Alex didn't initiate contact. {self.b['name']} has an opportunity to")
        if binary_roll([self.b['confidence'], self.b['interest']]):
            logging.debug(
                f"Meeting succeded! {self.b['name']} initiates contact")
            delta = random.gauss(self.a['interest'], 0.2)
            return {
                'type': EventType.MEETING,
                'location': get_location(),
                'protagonist': self.a,
                'person': self.b,
                'protagonist_initiated': False,
                'delta': delta,
            }
        return {
            'type': EventType.MEETING,
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
        if not protag_init:
            a = self.b
            b = self.a
        event = {
            'type': EventType.COMMIT,
            'protagonist': self.a,
            'person': self.b,
            'protagonist_initiated': protag_init,
            'phase': self.phase,
            'health': self.health,
            'delta': 0,
            'health_threshold': PHASE_COMMIT_THRESHOLDS[self.phase],
            'score_threshold': PHASE_SCORE_THRESHOLDS[self.phase],
        }

        logging.debug("BEGIN COMMIT event")
        logging.debug(
            f"{a['name']} confidence {a['confidence']}, interest {a['interest']}, commit {a['commit']}")

        # Roll for whether A is committed/interested enough to initiate:
        event['initiate_ratio'] = a['interest'] * a['commit'] * self.health / \
            PHASE_COMMIT_THRESHOLDS[self.phase] / \
            PHASE_SCORE_THRESHOLDS[self.phase]

        # Roll for whether or not A is confident enough to initiate
        event['confidence'] = binary_roll([a['confidence']])

        event['initiated'] = event['confidence'] and event['initiate_ratio'] > 1

        if not event['initiated']:
            logging.debug(
                f"COMMIT event failed")
            return event
        score = b['interest'] * b['commit'] * \
            self.health / PHASE_COMMIT_THRESHOLDS[self.phase]
        success_ratio = score / PHASE_SCORE_THRESHOLDS[self.phase]
        event['success_ratio'] = success_ratio

        logging.debug(
            f"Interest + Commitment roll = f{score}, need {PHASE_SCORE_THRESHOLDS[self.phase]} to succeed")

        if success_ratio > 1:
            # Random increase to interest + commitment + confidence if the response was enthusiastic
            logging.debug("COMMIT succeeded, initiate phase change")
            a['commit'] *= 1 + random.random() * 0.1
            a['interest'] *= 1 + random.random() * 0.1
            b['commit'] *= 1 + random.random() * 0.1
            b['interest'] *= 1 + random.random() * 0.1
            a['confidence'] *= 1 + random.random() * 0.1
            b['confidence'] *= 1 + random.random() * 0.1

            a['neuro'] *= 0.9 + random.random() * 0.1

            event['delta'] = 2
        else:
            logging.debug("COMMIT failed")
            # Check for previous attempts in this phase
            previous_attempts = [a for a in self.events if a.get('phase')
                                 == self.phase and a['type'] == EventType.COMMIT and a['protagonist_initiated'] == protag_init]
            previous_attempts_multiplier = len(previous_attempts)
            logging.debug(
                f"{previous_attempts_multiplier} previous failed attempts detected")
            event['prev'] = previous_attempts_multiplier
            # Debuffs if response was not enthusiastic:
            b['interest'] *= 0.8 + random.random() * 0.2
            a['neuro'] *= 1 + random.random() * 0.1
            a['confidence'] *= 0.8 + random.random() * 0.2
            event['delta'] = -2 * (previous_attempts_multiplier + 1)

        if success_ratio >= 1 and self.phase == Phase.COURTING:
            self.phase = Phase.DATING
        elif success_ratio >= 1 and self.phase == Phase.DATING:
            self.phase = Phase.COMMITTED

        return event

    def simulate_nothing(self):
        logging.debug("Nothing happened")
        return {
            'type': EventType.NOTHING,
            'health': self.health,
            'duration': 1,
            'delta': -0.1,
            'protagonist': self.a,
            'person': self.b,
        }

    def next_event(self, event):
        PHASE_EXPERIENCE_CHANCES = {
            Phase.COURTING: 0.9,
            Phase.DATING: 0.5,
            Phase.COMMITTED: 0.5,
        }
        PHASE_CONFLICT_CHANCES = {
            Phase.COURTING: 0.1,
            Phase.DATING: 0.5,
            Phase.COMMITTED: 0.8,
        }

        # If in COMMIT phase introduce random chance of death
        if self.phase == Phase.COMMITTED:
            if random.random() < 0.001:
                return {
                    'type': EventType.DEATH,
                    'protagonist': self.a,
                    'person': self.b,
                    'phase': self.phase,
                    'delta': self.health * -1,
                }

        # odds of conflict increase based on neuro
        neuro_mod = util.scale((self.a['neuro'] + self.b['neuro']) / 2, 0, 1,
                               0.7, 1.3)
        chance_conflict = PHASE_CONFLICT_CHANCES[self.phase] * neuro_mod

        if self.health > PHASE_COMMIT_THRESHOLDS[self.phase] and (event.get(
                'delta', 0) > 0.4) and (event.get('type') != EventType.COMMIT):
            event = self.simulate_commit(event)
        elif (random.random() < PHASE_EXPERIENCE_CHANCES[self.phase]):
            # A development occurred!
            event = self.simulate_experience()
            event['phase'] = self.phase
        elif (random.random() < chance_conflict):
            event = self.simulate_conflict()
            event['phase'] = self.phase
        else:
            event = self.simulate_nothing()
            event['phase'] = self.phase

        return event

    def simulate_reflection(self):
        # Given the relationship, determine Alex's stat change
        # TODO impliment phases
        person_a = self.a
        person_b = self.b
        logging.debug("BEGIN REFLECTION")
        max_diff = 0
        target = ''
        for x in CONFLICT_TARGETS:
            diff = abs(person_a[x] - person_b[x])
            if diff > max_diff:
                max_diff = diff
                target = x
        logging.debug(
            f"Largest property difference: {target} | Alex: {person_a[target]} | {person_b['name']}: {person_b[target]}")
        changed_prop = person_a[target]
        person_a[target] = (person_a[target] * 7 + person_b[target] * 3) / 10
        logging.debug(
            f"Alex changed: new {target} score is {person_a[target]}")
        new_prop = person_a[target]
        # Catalog events by type
        events = self.events
        event_types = {
            "hot": 1,
            "open": 1,
            "con": 1,
            "extra": 1,
            "agree": 1,
            "neuro": 1,
            "commit": 1,
            "libido": 1
        }

        event_memory = ''
        for memory in events:
            if memory['type'] == EventType.EXPERIENCE:
                for key in event_types:
                    if memory['target_property'] == key:
                        event_types[key] += 1

        for key in event_types:
            event_num = 1
            if event_types[key] > event_num:
                event_num = event_types[key]
                event_memory = key
                # print(event_memory, event_num, 'event stuff')
        logging.debug(f"memory chosen: {event_memory}")
        self.reflection = {
            'prop': target,
            'old': changed_prop,
            'new': new_prop,
            'memory': event_memory
        }

    def simulate(self):
        # Given a pair of people, simulate a relatonship between them
        # We represent a relationship as an array of events represented by dictionaries / objects
        # Then use separate code to turn the array of events into text
        self.events = []
        self.a['interest'] = get_interest(self.a, self.b)
        self.b['interest'] = get_interest(self.b, self.a)

        # simulate attempt to ask out person:
        meeting = self.simulate_meeting()
        meeting['date'] = self.date
        self.events.append(meeting)
        self.health += meeting['delta']
        if (self.health > 0):
            self.phase = Phase.COURTING

        PHASE_TIMEDELTA = {
            Phase.COURTING: datetime.timedelta(days=1),
            Phase.DATING: datetime.timedelta(days=3),
            Phase.COMMITTED: datetime.timedelta(days=7),
        }

        event = {}
        while self.health > 0:
            # Determine the random chance of some event occuring:
            # TODO: adjust based on character properties
            event = self.next_event(event)
            if not event:
                continue
            event['date'] = self.date
            self.date += PHASE_TIMEDELTA[self.phase]
            self.health += event['delta']
            event['health'] = self.health
            self.events.append(event)
            self.a = event['protagonist']
            self.b = event['person']
            logging.debug(f"relationship health is {self.health}")

        return self.events
