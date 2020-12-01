import random
import util
import math

MODIFIERS = {
    'open': 0.25,
    'agree': 0.25,
    'interest': 0.25,
    'commit': 0.25,
    'neuro': -1,
}


def get_conflict_sentence(tproperty, a, b, target):
    # target is value 0-1 representing intensity
    # TODO modulate based on intensity
    gt = 'gt' if a[tproperty] > b[tproperty] else 'lt'
    adverb = random.choice(['kind of', 'really', 'intensely'])
    CONFLICT_SENTENCES = {
        'hot': {
            'gt': [
                f'I {adverb} wish you put more effort into your appearance. ',
            ],
            'lt': [
                f"Sometimes I {adverb} feel worried that I'm not attractive enough for you. "
            ]
        },
        'open': {
            'gt': [f'I {adverb} want to go to SeaWorld with you.'],
            'lt': [f"I {adverb} don't like going to SeaWorld."],
        },
        'extra': {
            'gt': [
                f'I {adverb} want to go hang out with my friends tonight. Do you want to come?',
            ],
            'lt': [f'I {adverb} wish we spent more time alone together. '],
        },
        'agree': {
            'gt': [
                f'I {adverb} feel like I make more concessions in this relationship than you.'
            ],
            'lt': [
                f'I {adverb} feel like you spend a lot of energy making other people happy. '
            ]
        },
        'neuro': {
            'gt': [f"You make it {adverb} difficult for me to trust you. "],
            'lt': [f"Your neuroticism is {adverb} frustrating for me. "]
        },
        'commit': {
            'gt': [
                f"I {adverb} feel like this relationship is moving too slowly for me. "
            ],
            'lt': [
                f"I {adverb} feel like this relationship is moving too fast for me. "
            ]
        },
        'libido': {
            'gt': [f"I {adverb} want to have more sex. "],
            'lt': [f"I {adverb} want to have less sex. "]
        },
        'exp': {
            'gt': [
                f"I {adverb} feel like my previous relationships have been more fulfulling than this one. "
            ],
            'lt': [f"I'm {adverb} jealous of your exes! "]
        }
    }
    return CONFLICT_SENTENCES[tproperty][gt][0] + '\n'


def get_resolution_sentence(event, a, b):
    return f"{a['name'].upper()}: I'm sorry. Let's resolve the argument. \n"


def get_response_sentence(event, a, prop, prop_score):
    RESPONSES = {
        'open': [
            "I don't understand why this is a problem.",
            "Okay I'm willing to explore new avenues with you. "
        ],
        'agree': [
            'What gives you the right to complain about me like that?',
            "You're right. I'll make an effort to change if it'll make you happy."
        ],
        'neuro': [
            "I hear what you're saying. ",
            "*inconsolable weeping* ",
        ],
        'commit': [
            'Well should we break up then?',
            "I'm willing to work this out because I care about having a healthy relationship. ",
        ],
        'interest': ["So be it then.", "But I love you! "],
    }
    responses = RESPONSES[prop]
    ind = util.clamp(math.floor(prop_score * len(responses)), 0,
                     len(responses) - 1)
    return f"{a['name'].upper()}: {responses[ind]}\n"


def get(event):
    # Get conflict dialogue
    character_a = event['protagonist'] if event[
        'protagonist_initiated'] else event['person']
    character_b = event['person'] if event['protagonist_initiated'] else event[
        'protagonist']
    rolls_a = event['protag_rolls'] if event[
        'protagonist_initiated'] else event['person_rolls']
    rolls_b = event['person_rolls'] if event[
        'protagonist_initiated'] else event['protag_rolls']

    dialogue = f"Shortly afterward, {character_a['name']} messaged {character_b['name']} on Discord.\n\n"

    conflict_sentence = get_conflict_sentence(event['target_property'],
                                              character_a, character_b,
                                              event['target'])

    dialogue += f"{character_a['name'].upper()}: Hey, {conflict_sentence}\n"

    # resimulate argument kinda
    team_score = event['handicap']
    char_a_props = ['open', 'agree', 'neuro', 'commit', 'interest']
    random.shuffle(char_a_props)
    char_b_props = ['open', 'agree', 'neuro', 'commit', 'interest']
    random.shuffle(char_b_props)

    while team_score + event['handicap'] < event['target']:
        if len(char_a_props) == 0:
            break
        char_b_prop = char_b_props.pop()
        next_sentence = get_response_sentence(event, character_b, char_b_prop,
                                              rolls_b[char_b_prop])
        modifier = MODIFIERS[char_b_prop]
        team_score += rolls_b[char_b_prop] * modifier

        dialogue += next_sentence

        char_a_prop = char_a_props.pop()
        next_sentence = get_response_sentence(event, character_a, char_a_prop,
                                              rolls_a[char_a_prop])
        modifier = MODIFIERS[char_a_prop]
        team_score += rolls_a[char_a_prop] * modifier

        dialogue += next_sentence

    if team_score > event['target']:
        next_sentence = get_resolution_sentence(event, character_a,
                                                character_b)
        dialogue += next_sentence
    else:
        dialogue += "The argument was unresolved. \n\n"

    return dialogue
