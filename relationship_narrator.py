import util
import statistics
import pprint
import business_gen
import prologue
import random
import logging
import humanize
import conflict_narrator
from relationship import EventType, PROP_NAMES, Relationship, Phase
from narrate_time import narrate_time
import tracery
import artifacts
from tracery.modifiers import base_english
from util import get_ab
from interests import INTERESTS, getInterestRules

# logging.basicConfig(level=logging.DEBUG)


def narrate(r: Relationship):
    # Given a relationship object, break the events within into their distinct
    # phases and pass them to narrate_phase
    events = r.events
    saved_events = []
    print(
        f"<p>Alex met {events[0]['person']['name']} {events[0]['location']}.</p>")
    print(
        f"<p class='system'>{events[0]['person']['name']}:</p>")
    for prop in r.b:
        if (type(r.b[prop]) == float):
            print(f"<p class='system prop'>{prop}: {round(r.b[prop], 2)}</p>")
    print(
        f"<p class='system prop'>interests: {', '.join(r.b['interests'])}</p>")
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
            saved_events.append(event)
        narrate_phase(chunk, phase)
    r.events = saved_events
    events = saved_events

    # knock alex's confidence just a touch
    # logging.debug(f"Alex's confidence is {a['confidence']}")
    r.a['confidence'] *= .9 + random.random() * 0.1
    # logging.debug(f"Alex's confidence is {a['confidence']}")
    print(f"<p>They never saw each other again.</p>")
    if len(events) > 0:
        print(
            f"<p class='system'>This relationship lasted for only {humanize.naturaldelta(events[-1]['date'] - events[0]['date'])}, reaching the <tt>{r.phase.value}</tt> stage before ending.</p>")

# Given a chunk of events and phase, narrate events in that style
# Right now there aren't that many changes to narration based on phase
# but we keep the infrastructure for now


def narrate_phase(events, phase):
    if events:
        logging.debug(f'Narrating {len(events)} events in phase {phase}')
    if phase == Phase.COURTING:
        narrate_events(events)
    elif phase == Phase.DATING and events:
        prologue.get_partner_description(events[0]['person'])
        narrate_events(events)
    elif phase == Phase.COMMITTED and events:
        narrate_committed(events)


# Given a block of events, narrate the next event
# Maintain an array of events that happened up until that point
# so the narrator can take them into account.
def narrate_events(events):
    current_events = []
    for event in events:
        narrate_event(event, current_events)
        if current_events:
            narrate_time(current_events[-1], event)
        current_events.append(event)


# Call the appropriate function based on event type
def narrate_event(event, events):
    # logging.debug(pprint.pformat(event))
    if event is None:
        return
    if event['type'] == EventType.MEETING:
        narrate_meeting(event, events)
    elif event['type'] == EventType.COMMIT:
        narrate_commit(event, events)
    elif event['type'] == EventType.EXPERIENCE:
        narrate_experience(event, events)
    elif event['type'] == EventType.CONFLICT:
        narrate_conflict(event, events)
    else:
        time_passed(event, events)


# Get some basic descriptor based on the property with the highest value
# This is what Alex notices first about the person
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


def narrate_commit(event, events):
    a, b = get_ab(event)
    if event['initiated']:
        enthusiasm = util.scale(event['success_ratio'], 1, 3, 0, 1)
        rules = {
            'courting_phase': ['<p>#dating#</p>'],
            'dating_phase': ['<p>#iloveyou#</p>'],
            'dating': ['#dating_challenge# #dating_result#'],
            'iloveyou': ['#ily_challenge# #ily_result#'],
            'dating_challenge': [
                "#a# asked to start dating.",
                "#a# asked if #b# would be interested in dating.",
            ],
            'dating_result':
            f"#b# agreed {util.enthusiastically(enthusiasm)}. "
            if event['success_ratio'] >= 1 else
            f'#b# said that {b["they"]} needed more time. ',
            'ily_challenge':
            f"#a# said \"I love you,\"",
            'ily_result': [
                'but #b# could not say it back. #a# was #hurt#'
                if event['success_ratio'] < 1 else
                f'and #b# returned the words {util.enthusiastically(enthusiasm)}.'
            ],
            'hurt': util.rank(
                [
                    'hurt, but said #a_they# understood.',
                    'wounded. A tear fell from #a#\'s left eye. ',
                    'devasted. #a_they.capitalize# had hoped #b#\'s response might have been different this time.',
                    'mortified. #a# shouted that #b# was wasting #a#\'s time. #b# shrugged. '
                ],
                util.scale(event.get('prev', 0), 0, 3, 0, 1)
            ),
            'a': a['name'],
            'b': b['name'],
            'a_they': a['they']
        }

    elif event['initiate_ratio'] > 1:
        # Narrate a failed commit event held back by confidence
        rules = {
            'courting_phase': '#origin#',
            'dating_phase': '#origin#',
            'origin': [
                '#a# felt nervous, but excited. ',
                '#a# sighed. #b# seemed so amazing. But would #b_they# return #a#\'s feelings?',
                '#a# smiled quietly to themselves. Perhaps the right time to talk to #b# would come some day. ',
                "#a# had the urge to ask #b# about how they felt about the relationship, but wasn't quite confident enough to ask. ",
            ],
            'a': a['name'],
            'b': b['name'],
            'b_they': b['they'],
        }
    else:
        # Not interested enough.
        rules = {
            'courting_phase': [
                "#a# continued to use dating apps from time to time. ",
                "#a# considered sending #b# a message, but decided not to. ",
                "#a# noticed a message from #b#. #a# ignored it. ",
                "#b# had yet to meet most of #a#'s friends. ",
            ],
            'dating_phase': [
                "#a#'s Facebook relationship status still read 'Single'. ",
                "#a# had yet to mention #b# to their parents. ",
                "#a# told #b# they were busy, but in fact #a# had no concrete plans that day. ",
                "#a# lay awake at night, mulling over exes from previous relationships. ",
            ],
            'a': a['name'],
            'b': b['name'],
            'interest': a['interests'],
        }
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    if event['phase'] == Phase.COURTING:
        print(grammar.flatten('<p>#courting_phase#</p>'))
    elif event['phase'] == Phase.DATING:
        print(grammar.flatten('<p>#dating_phase#</p>'))
    print('\n')
    narrate_commit_system(event)


def narrate_commit_system(event):
    a, b = get_ab(event)
    print(
        f"""<p class='system'>Current relationship health of {round(event['health'] - event['delta'], 2)} exceeds threshold of {event['health_threshold']} and last event improved relationship health over 0.4.</p>"""
    )
    print(
        f"""<p class='system'>
        {a['name']} with interest {round(a['interest'], 2)} and commitment {round(a['commit'], 2)}
        produces relationship advancement interest score of {round(event['initiate_ratio'])}.</p>""")
    if event['initiate_ratio'] < 1:
        print(f"""<p class='system'>Interest score did not exceed threshold of 1.0. Relationship advancement failed.</p>""")
        return
    print(
        f"""<p class='system'>Interest score exceeded threshold of 1.0. Next, {a['name']} with confidence of {round(a['confidence'], 2)}, has {int(a['confidence'] * 100)}% chance of initiating relationship advancement.</p>""")
    if not event['confidence']:
        print(
            f"""<p class='system'>Confidence test failed. {a['name']} remains silent. Relationship advancement failed.</p>""")
        return
    print(
        f"<p class='system'>{a['name']} successfully initiated relationship advancement.</p>")
    print(
        f"""<p class='system'>
        {b['name']} with interest {round(b['interest'], 2)} and commitment {round(b['commit'], 2)}
        produces relationship advancement interest score of {round(event['success_ratio'])}.</p>""")
    if event['success_ratio'] > 1:
        print(
            f"""<p class='system'>
            Relationship advancement succeeded. The relationship has reached the {event['phase'].value} stage.
            {a['name']} experienced growth in commitment, interest, and confidence, as well as a reduction in neuroticism.
            {b['name']} experienced growth in commitment, interest, and confidence.</p>""")
    else:
        print(
            f"""<p class='system'>
            Relationship advancement failed. There were {event['prev']} previous failed attempts.
            {b['name']} experienced withdrawal from the relationship, manifesting in reduced interest.
            {a['name']} experienced an increase in neuroticism and a decline in confidence.
            </p>""")
    print(
        f"<p class='system'>The relationship health is {round(event['health'], 2)}.</p>"
    )


def narrate_meeting_system(event):
    a, b = get_ab(event)
    if event['delta'] == -1:
        print(
            f"<p class='system'>Neither {a['name']} nor {b['name']} attempted to contact the other.</p>")
    else:
        print(f"""
            <p class='system'>{a['name']} with confidence
            {round(a['confidence'], 2)}, interest
            {round(a['interest'], 2)} initiates contact.
            </p>""")
        print(f"""
            <p class='system'>{b['name']} with interest
            {round(b['interest'], 2)} responds with
            {round(event['delta'], 2)} enthusiasm.
            </p>""")
        if (event['delta'] > 0):
            print(
                "<p class='system'>Relationship successfully advanced to the courting stage.</p>")
        else:
            print(
                "<p class='system'>Relationship failed to advance to the courting stage.</p>")


def narrate_meeting(event, events):
    a, b = get_ab(event)
    if event['delta'] == -1:

        narrate_meeting_system(event)
        return

    text = "<p>"
    if event['protagonist_initiated']:
        text += get_interest_sentence(event['protagonist'], event['person'],
                                      event['protagonist']['interest'])
    else:
        text += get_interest_sentence(event['person'], event['protagonist'],
                                      event['person']['interest'])
    adverb = util.rank(
        ['nervously', 'shyly', 'quietly', 'gently', 'intently', 'boldly'],
        a['interest'])

    if event['delta'] <= 0:
        REJECTIONS = [
            f", but {b['name']} averted {b['their']} eyes.",
            f", but {b['name']} did not respond.",
            f", but {b['name']} quickly turned away.",
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
    print(text + random.choice(APPROACHES) + "" + "</p>")

    narrate_meeting_system(event)


def narrate_committed(events):
    summary = util.get_event_meta(events)

    rules = {
        'origin': ['<p>#exp#. #conflict#</p>'],
        'exp': '#best_exp#' if summary['best_experience'] else 'The couple unfortunately never spent more time together',
        'conflict': ['#best_conflict#.', '#best_conflict#, but #worst_conflict#.', '#best_conflict#, but #popular_conflict#.'] if summary['worst_conflict'] else 'The couple never clashed.',
        'best_exp': f"Their similar levels in {PROP_NAMES.get(summary['best_experience'])} facilitated a healthy growth in their relationship",
        'worst_conflict': f"their fights over their difference in {PROP_NAMES.get(summary['worst_conflict'])} were #bitter#",
        'best_conflict': f"The couple was proud of their ability to work through their differences in {PROP_NAMES.get(summary['best_conflict'])}",
        'popular_conflict': f"the couple fought often because of differences in {PROP_NAMES.get(summary['popular_conflict'])}",
        'bitter': ['acrid', 'virulent', 'bitter', 'harsh', 'difficult', 'hard to recover from', 'emotionally exhausting']
    }
    print(tracery.Grammar(rules).flatten('#origin#</p>'))

    if events[-1]['type'] == EventType.DEATH:
        death = random.choice([
            "a meteroite striking the Earth",
            "a global pandemic",
            "an infected paper cut",
            "a falling grand piano",
            "a poorly placed pothole in the road",
            "a stroke caused by the erroneous publication of their own obituary",
            "the collapse of the Marxist state"
        ])
        print(
            f"Unfortunately, {events[-1]['person']['name']} died tragically due to {death}.")
    else:
        print(
            f"Ultimately their differences proved too great to overcome. ")


def narrate_rejection(event, events):
    a, b = get_ab(event)
    rules = {
        'origin': "#Onday# #want#, #reject#.",
        'a': a['name'],
        'b': b['name'],
        'Onday': [
            f"On {event['date'].strftime('%A')},",
            f"{event['date'].strftime('%A')} came around.",
            "Later that week,"
        ],
        'want': [
            '#a# asked #b# if they wanted to hang out',
            f'#a# asked #b# if {b["they"]} were free',
            '#a# wanted to hang out with #b#',
            '#a# wanted to see #b#',
        ],
        'reject': [
            'but #b# was busy',
            'but #b# forgot to return #a#\'s message',
            'but #b# had other plans',
            'but #b# never responded to #a#\'s message'
        ]
    }
    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        print(artifacts.get_date_artifact(event, events, True))
    else:
        print(tracery.Grammar(rules).flatten('<p>#origin#</p>'))
    return


def narrate_experience_system(event):
    a, b = get_ab(event)
    print(
        f"""<p class='system'>{a['name']} invited {b['name']} to a
        {round(event['threshold'],2)}-{event['target_property']} experience.</p>""")
    if 'interest' in event:
        print(
            f"""<p class='system'>Activity proposed: {event['interest']}.
            {b['name']} interests: {', '.join(b['interests'])}.</p>
        """)
    print(
        f"""<p class='system'>{b['name']} has {event['target_property']}
        {round(b[event['target_property']],2)} and current concession damage
        {round(b['concessions'][event['target_property']],2)}.
        Reluctance to accept invitation is {round(event['concession_roll'], 2)}.</p>""")
    # how much you don't want to do the activity due to difference
    print(
        f"""<p class='system'>{b['name']} with interest {round(b['interest'], 2)},
        commit {round(b['commit'], 2)}, agreeability {round(b['agree'], 2)}
        produces motivation to accept {round(event['agree_roll'], 2)}.</p>""")
    # motivation is determined by other factors and can outweight reluctance

    if event['rejected']:
        print(
            f"<p class='system'>Motivation did not exceed reluctance. {b['name']} rejected the invitation.</p>")
    else:
        print(
            f"<p class='system'>Motivation exceeded reluctance. {b['name']} accepted the invitation. Due to difference in {event['target_property']}, took {round(event['concession'], 2)} concession damage.</p>")
    print(
        f"<p class='system'>The relationship health is {round(event['health'], 2)}.</p>")


def narrate_experience(event, events):
    a, b = get_ab(event)

    if event['rejected'] and event['target_property'] not in ['con', 'exp', 'neuro']:
        narrate_rejection(event, events)
        narrate_experience_system(event)
        return

    detail = False

    artifact = False
    if event.get('phase') == Phase.COURTING and random.random() < 0.6:
        artifact = True
        # 50% chance to show the detail of the experience in the artifact
        detail = random.random() < 0.5
        print(artifacts.get_date_artifact(event, events, detail))

    # openness activities can fall 3 different ways
    # <.33 proposer suggests activity they like
    # <.66 proposer suggest an activity that their partner likes
    # < 1 proposer suggests any activity

    if event['target_property'] == 'open':
        rules = {
            'origin': '<p>#hobby_proposal# #reply# #outcome# </p>',
            'mood': util.rank([
                "Having a strong preference for what #they# wanted to do for date night,",
                f"Having been obsessed with {event['interest']} more than ever lately,",
                "Wanting to have a nice evening together,",
                "Wanting to surprise #b#,",
                "In effort to mix up what they usually do,",
                "In the mood for adventure,"
            ], event['threshold']),
            'proposed': [
                "asked #b# to", "begged #b# to", "proposed that they",
                "wondered if it would be fun to", "suggested that they",
                "wanted to", "invited #b# to"
            ],
            'hobby_proposal': [
                f"#mood# #a# #proposed# go to {random.choice(INTERESTS[event['interest']]['location'])} together.",
                f"#mood# #a# #proposed# {random.choice(INTERESTS[event['interest']]['verb'])} together."
            ],
            'response': util.rank([
                "I'd love to!", "Sounds like fun!", "Yes, let's do it,",
                "Sure!", "Okay,", "Oh, okay,", "I guess so...",
                "Do we have to?", "You know I don't like that,"
            ], 1-event['delta']),
            'reply': ['"#response#" #b# replied.'],
            'quality': util.rank([
                'terrible', 'pretty bad', 'okay',
                'decent', 'good',
                'joyous', 'fantastic', 'outstanding'
            ], event['delta']),
            'verdict': util.rank([
                '#b# would rather not spend their time like this in the future.',
                'Perhaps, they could try something else next time.',
                '#b# would consider doing a similar activity again.',
                f'#b# enjoyed {b["themself"]}.',
                '#b# could see the two of them doing this often.',
                '#b# loved the date.'
            ], 1 - event['concession_roll']),
            'match': f"#b# loved {event['interest']}",
            'outcome': "The two had a #quality# time. #verdict#"
        }
        rules.update(getInterestRules(a, b, event['interest']))
        grammar = tracery.Grammar(rules)
        if not detail:
            print(grammar.flatten('<p>#origin#</p>'))
        else:
            print(grammar.flatten('<p>#outcome#</p>'))
        # logging.debug(
        #    f"OPEN EXPERIENCE {event['interest']} {event['threshold']} a: {a['open']} b: {b['open']}")
    elif event['target_property'] in ['extra', 'libido']:
        #compare the target_properties of the characters
        #create boolean that asks if b > a
        
        rules = {
            'origin':
            f"#Onday# #{event['target_property']}#. #{event['target_property']}_response#",
            'day': ['day', 'morning', 'afternoon', 'evening'],
            'Onday': '#artifact#' if artifact else '#later#',
            'artifact': [
                f"On {event['date'].strftime('%A')}, #they#",
                f"{event['date'].strftime('%A')} came around. #they.capitalize#",
                f"{event['date'].strftime('%A')} arrived. #they.capitalize#",
            ],
            'later': [
                '#artifact#',
                '#artifact#',
                "Later that week, #they#"
            ],
            'extra':
            util.rank([
                '#enjoyed# a tranquil #day# watching Netflix',
                '#enjoyed# a tranquil #day# watching Youtube videos',
                '#enjoyed# a tranquil #day# watching a movie',
                '#enjoyed# a quiet #day# reading together',
                '#enjoyed# a night out together at the bar',
                '#enjoyed# a #day# hanging out with friends',
                '#enjoyed# a #day# of people-watching',
                '#enjoyed# a night out at the club',
            ], event['threshold']),
            'libido':
            util.rank([
                'lay in bed together, but without touching',
                'lay in bed together, holding hands',
                'cuddled on the couch',
                'shared a kiss',
                'made out #vigorously# #location# together before parting ways',
                'sneakily groped #b#\'s body #in_public#'
                '#enjoyed# a steamy evening together',
                '#enjoyed# an intensely passionate evening together',
            ], event['threshold']),
            'they': [
                'they', 'the couple', '#a# and #b#', 'the two of them',
                'the pair'
            ],
            'enjoyed': util.rank([
                'spent', 'happily spent', 'enjoyed',
                'excitedly spent', 'savored',
                'reveled in', 'relished'
            ], event['delta']),
            'vigorously': util.rank([
                'awkwardly', 'briefly', '', 'passionately', 'vigorously'
            ], event['delta']),
            'location': [
                "on the street", "outside #a#'s apartment", "on #b#'s doorstep", "in the back of the rideshare", 
                "outside the subway", 
            ],
            'in_public': [
                "while walking down the street", "while waiting in line at checkout"
            ]
            'a':
            a['name'],
            'b':
            b['name'],
        }
        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)
        print(grammar.flatten("#origin#"))
    else:
        rules = {
            'origin': [
                f"#Onday# #{event['target_property']}# #next#",
            ],
            'Onday': [
                f"On {event['date'].strftime('%A')}, ",
                f"{event['date'].strftime('%A')} came around. ",
                "Later that week, "
            ],
            'hot': util.rank([
                '#b# noticed that #a# sometimes gave off a mildly unpleasant odor.',
                f'#a# bragged to #b# about how infrequently {a["their"]} hair needed to be washed.',
                '#a# met #b# wearing an old college sweatshirt and an ill-fitting pair of jeans.',
                '#b# noticed #a# went to sleep without washing up first.',
                '#a# bought more skincare products.',
                '#a# went shopping for the latest trendy fashions.',
                '#a# went shopping for organic groceries. That figure didn\'t keep itself in shape!',
                '#a# spent the #day# at the gym. That body didn\'t keep itself in shape!',
            ], event['threshold']),
            'con': util.rank([
                '#b# noticed #a# had a lot of dishes piled up in the sink.',
                '#a# decided to call in sick to work. After all, you only live once.',
                f'#a# forgot to do {a["their"]} laundry.',
                '#a# left a couple of dishes piled up in the sink.',
                f'#a# noticed {a["they"]} needed to vacuum the carpet.',
                '#a# decided to start keeping a daily todo list.',
                f'#a# spent the #day# arranging {a["their"]} books by color and subject.',
                '#a# went shopping and purchased a daily planner.',
                '#a# stayed late at work.',
                '#a# spent the #day# #cleaning# the apartment.',
                '#a# spent the #day# #cleaning# the apartment. It was moderately dusty.',
                '#a# spent the #day# #cleaning# the bathroom. It certainly was in need of some attention.',
            ], event['threshold']),
            'exp': util.rank([
                '#a# was upset with #b#, but said nothing.',
                '#a# was jealous of #b#\'s moderately attractive co-worker.',
                f'#a# asked #b# how {b["they"]} felt about the relationship. The couple had an earnest conversation about where things were going.',
                f'#a# suggested that they enact weekly relationship check-ins. #b# agreed happily.'
            ], event['threshold']),
            'neuro': util.rank([
                '#b# had a night out with friends planned. #a# was happy to pass the evening doing other things.',
                '#b# had not responded to #a#\'s text messages for a few hours. #a# sent a followup.',
                '#a# fretted. #a# had not heard from #b# for a couple days.',
                f'#a# worried when #b# said that {b["they"]} sometimes preferred to be alone.',
                '#a# worried that #b# did not actually find them to be attractive.'
                '#b# kept a journal of how long it took for #a# to text them back.',
                '#a# worried that #b# would leave them some day soon.',
            ], event['threshold']),
            'cleaning': ['tidying', 'cleaning', 'organizing'],
            'day': ['day', 'morning', 'afternoon', 'evening'],
            'a': a['name'],
            'b': b['name'],
            'response': util.rank([
                '#b# was happy that the two of them shared similar habits.',
                '#b# was perfectly willing to support #a# when this happened.',
                '#b# didn\'t always understand #a#\'s actions.',
                '#b# did not appreciate #a# when things like this happened.',
            ], event['concession']),
            'rejection':
                '#b# refused to participate in this kind of behavior.',
            'next': '#rejection#' if event['rejected'] else '#response#'
        }
        print(tracery.Grammar(rules).flatten('#origin#'))
        # logging.debug(f"Event: {event}")
    prologue.narrate_interests(event, events)
    narrate_experience_system(event)


def narrate_conflict(event, events):
    conflict_narrator.narrate_conflict(event)
    conflict_narrator.narrate_conflict_system(event)


def time_passed(event, events):
    return ""
