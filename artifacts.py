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


def get_first_date(event):
    a_nick = event['protagonist']['nickname']
    b_nick = event['person']['nickname']
    a_interest = event['protagonist']['interest']
    b_interest = event['person']['interest']
    time = event['date']

    rules = {
        'origin': ['#a#\n'],
        'a': [
            '#a_pre##a_start##punc#\n#b_pre##b_start##b_ask#'],
        'b': ['#b_pre##b_start##b_resp#\n#a_pre##a_start##a_ask#'],
        'a_pre': f"{a_nick} ({time}): ",
        'b_pre': f"{b_nick} ({time}): ",
        'punc': ['. ', '! ', '... '],
        'a_start': [
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
        'b_start': [
            'Hey! ',
            'Heya! ',
            'Yo! ',
            'Hello! ',
            'Whats up! ',
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
    if event['protagonist_initiated']:
        return grammar.flatten("#a#\n")
    else:
        return grammar.flatten("#b#\n")
