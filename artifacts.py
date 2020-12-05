import random
import util
import math
from relationship import EventType, PROP_NAMES, Relationship, Phase
import tracery

# def narrate_artifact(evt: Event):


def get_nickname(name):
    rules = {
        'origin': '#nick#',
        'nick': ['#l#-#dog#', '#name##suffix#'],
        'l': name[0],
        'dog': ['dog', 'dawg', 'cat', 'catz', 'star', 'Z', 'qt', 'babe', 'bob', 'mack'],
        'name': [name, '#l'],
        'num': ['420', '69'] + [str(n + 80) for n in range(20)],
        'suffix': ['#num#', '_#num#', '#dog##num#']
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")


def get_first_date(a_nick, b_nick, a_interest, b_interest):
    rules = {
        'origin': ['#a#\n'],
        'a': [
            '#a_pre##a1_start##punc##a_ask#\n#b_pre##b2_start##b_resp#',
            '#a_pre##a1_start##punc#\n#b_pre##b2_start##b_ask#'],
        'a_pre': f"{a_nick}: ",
        'b_pre': f"{b_nick}: ",
        'punc': ['. ', '! ', '... '],
        'a1_start': [
            'it was really nice to spend time with you',
            'i had fun tonight',
            f"{util.adverb(a_interest)} can’t stop thinking about you",
            "i had a great time",
            "hope you had a nice time",
            f"you are {util.adverb(a_interest)} great",
            "hey, thanks for hanging out"
        ],
        'a_ask': [
            'repeat soon?',
            'can i see you again?',
            'when can i see you again?',
            'when are u free next?',
            'again sometime?'
        ],
        'b2': ['#b2_start##b2_resp#'],
        'b2_start': [
            'Hey! ',
            'Heya! ',
            'Yo! ',
            'Hello ',
            'Whats up ',
            '',
        ],
        'b_ask': [
            'See me again soon?',
            'Want to do it again?',
            'When are you free next?',
            "Let's do it again sometime",
        ],
        'b_resp': [
            f'I had a {util.adverb(b_interest)} wonderful time.',
            f'I had a {util.adverb(b_interest)} awesome time.',
            f'I had a {util.adverb(b_interest)} fantastic time.',
            "You're cute.",
            "You're a cutie.",
        ]
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")
