import util
import prologue
import random
import logging
import conflict_dialogue
from relationship import Event, PROP_NAMES, Relationship, Phase

logging.basicConfig(level=logging.DEBUG)


def narrate(r: Relationship):
    return narrate_events(r.events)

def get_ab(event):
  a = event['protagonist'] if event['protagonist_initiated'] else event['person']
  b = event['person'] if event['protagonist_initiated'] else event['protagonist']
  return a,b

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

def narrate_commit(event):
    a, b = get_ab(event)
    text = f"{a['name']} asks {b['name']} for more commitment in the relationship. "
    if event['success_ratio'] > 1 and event['success_ratio'] < 2:
        text += random.choice([
            f"{b['name']} felt unsure, but agreed.",
            f"{b['name']} hesitated, but agreed.",
            f"{b['name']} agreed somewhat carefully."
        ])
    elif event['success_ratio'] > 2:
        text += random.choice([
            f"{b['name']} beamed in response. No more words were needed.",
            f"{b['name']} enthusiastically agreed.",
            f"{b['name']} agreed happily.",
        ])
    elif event['success_ratio'] < 0.5:
        text += random.choice([
            f"{b['name']} refused quickly.",
            f"{b['name']} was silent."
        ])
    else:
        text += random.choice([
            f"{b['name']} said {b['they']} needed some time to think about it."
        ])
    print(text)
  
def narrate_meeting(event):
    if event['delta'] == -1:
        return
    text = ""
    a, b = get_ab(event)
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

def narrate_dating(events):
    if len(events) == 0:
        return
    logging.debug(events[0]['protagonist'])
    # First the phase change event:
    narrate_commit(events.pop(0))
    # Then the prologue OG code:
    print(prologue.get_prologue(events[0]['person']))
    chunks = list(util.divide_chunks(events, 1))
    for chunk in chunks:
        narrate_dating_chunk(chunk)

def narrate_committed(events):
    if len(events) == 0:
        return
    # First the phase change event:
    narrate_commit(events.pop(0))
    chunks = list(util.divide_chunks(events, 8))
    # For now it's the same as dating :(
    for chunk in chunks:
        narrate_dating_chunk(chunk)

def narrate_dating_chunk(events):
    protag = events[0]['protagonist']
    # Then describe their experiences:
    experiences = [ e for e in events if e['type'] == Event.EXPERIENCE]
    conflicts = [ e for e in events if e['type'] == Event.CONFLICT]
    commits = [ e for e in events if e['type'] == Event.COMMIT]
    if (len(commits) > 0):
        narrate_commit(commits[0])
    counts = {'open': 0, 'extra': 0, 'libido': 0}
    for e in experiences:
        counts[e['target_property']] += e['delta']
    common_exp_type = max(counts, key=lambda k: counts[k])
    they = random.choice(['The two of them', 'The couple', 'They'])
    loved = random.choice(['often liked to', 'loved to', 'tended to'])
    E_DESC = {
        'open': 'go on adventures together',
        'extra': 'socialize as a couple',
        'libido': 'have sex',
    }
    delta = sum([e['delta'] for e in experiences])
    logging.debug(f"experience delta: {delta}")
    desc = util.rank([
        f"{protag['name']} found it moderately engaging",
        f"{protag['name']} was enthralled",
    ], delta/2)
    print(f"{they} {loved} {E_DESC[common_exp_type]}, {desc}.")
    counts = {'open': 0, 'extra': 0, 'libido': 0, 'neuro': 0, 'commit': 0, 'con': 0, 'exp': 0}
    for e in conflicts:
        counts[e['target_property']] += e['delta']
    common_exp_type = min(counts, key=lambda k: counts[k])
    C_DESC = {
        'open': 'They often disagreed about what to do on date nights.',
        'extra': 'They often fought about whether to stay in or go out.',
        'libido': 'They found their varying sex drive to be a challenge.',
        'neuro': 'They found nervous breakdowns to be a challenge.',
        'con': 'They found messiness to be a challenge.',
        'hot': 'They found hotness to be a challenge.',
        'exp': 'They fought about experience'
    }
    delta = sum([e['delta'] for e in conflicts])
    logging.debug(f"conflict delta: {delta}")
    print(C_DESC[common_exp_type])




def narrate_events(events):
    print(f"Alex met {events[0]['person']['name']} {events[0]['location']}. ")
    for phase in [Phase.COURTING, Phase.DATING, Phase.COMMITTED]:
        chunk = []
        while True:
            if len(events) == 0:
                break;
            if events[0].get('phase', phase) != phase:
                # Move on to next phase
                break;
            event = events.pop(0)
            chunk.append(event)
        narrate_phase(chunk, phase)
    print("They never saw each other again.\n\n")

def narrate_event(event):
    if event is None:
        return
    if event['type'] == Event.MEETING:
        narrate_meeting(event)
    elif event['type'] == Event.COMMIT:
        narrate_commit(event)
    elif event['type'] == Event.DEVELOPMENT:
        narrate_development(event)
    elif event['type'] == Event.EXPERIENCE:
        narrate_experience(event)
    elif event['type'] == Event.CONFLICT:
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
        for event in events:
            narrate_event(event)
    elif phase == Phase.COMMITTED:
        narrate_committed(events)
       

def narrate_experience(event):
    a, b = get_ab(event)
    if event['rejected']:
        result = f"{b['name']} refused. "
    else:
        lower_dict = {
            'libido': f'{b["name"]} generally preferred less adventurous sex',
            'extra': f'{b["name"]} generally preferred a quieter evening',
            'open': f'{b["name"]} generally preferred to do something they were used to.',
        }
        higher_dict = {
            'libido': f'{b["name"]} generally preferred more adventurous sex',
            'extra': f'{b["name"]} generally preferred to socialize',
            'open': f'{b["name"]} generally preferred to do something new',
        }
        concession = lower_dict[event['target_property']] if event['concession'] < 0 else higher_dict[event['target_property']]
        logging.debug(f"Concession damage for {event['target_property']} is {round(event['concession'], 2)}")
        result = f"{concession}, but agreed anyway. "
    
    experiences = {
        'open': [f'go on a boring date', 'go on an exciting date'],
        'libido': [f'have vanilla sex', f'have kinky sex'],
        'extra': [f'stay in and watch Netflix', 'go to a big party'],
    }
    activity = util.rank(experiences[event['target_property']], event['threshold'])
    print(f"{a['name']} invited {b['name']} to {activity} [{round(event['threshold'], 2)}]. {result}")
    logging.debug(f"The relationship health changed by {round(event['delta'], 2)}. ")


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
        print(f"{event['protagonist']['name']} and {event['person']['name']} had a disagreement about whether to go to a party or stay in. ")
    character_a = event['protagonist']['name'] if event['protagonist'][
        target_p] > event['person'][target_p] else event['person']['name']
    print(f"They fought because {character_a} was too {prop_name}. ")


def time_passed(event):
    #return f"1 day passed. The relationship health is {round(event['health'], 2)}. \n"
    print(random.choice([
        "A week passed quietly. \n",
        "A week went by. \n"
    ]))
