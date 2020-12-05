import random
import util
import math
from relationship import EventType, PROP_NAMES, Relationship, Phase
import relationship_narrator
import tracery
from tracery.modifiers import base_english

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


def get_message_intro(a, b):
    rules = {
        'origin': ['#time.capitalize#, #phrase#.', ''],
        'phrase': ['#a# #action#', '#b# #passive#'],
        'action': ['sent #b# a text message'],
        'passive': ['noticed a message from #a#'],
        'time': ['the next day', 'the next morning', 'the next evening', 'the next afternoon', 'the next night', 'at dawn the next day', 'at dusk the next day', 'at twilight the next day', 'at #num# the next morning', 'at #num# the next afternoon'],
        'num': ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'],
        'a': f'{a["name"]}',
        'b': f'{b["name"]}',
    }
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    return grammar.flatten('#origin#')


def get_first_date(event):
    a, b = relationship_narrator.get_ab(event)
    a_nick = a['nickname']
    b_nick = b['nickname']
    a_interest = a['interest']
    b_interest = b['interest']
    time = event['date']
    preface = get_message_intro(a, b)

    rules = {
        'a': [
            f'{preface} #a_msg#', '#a_msg#'
        ],
        'b': [
            f'{preface} #b_msg#', '#b_msg#'
        ],
        'a_msg': [
            '#a_pre##a_start##punc#\n#b_pre##b_start##b_ask#'],
        'b_msg': ['#b_pre##b_start##b_resp#\n#a_pre##a_start##punc##a_ask#'],
        'a_pre': f"{a_nick} ({time}): ",
        'b_pre': f"{b_nick} ({time}): ",
        'punc': ['. ', '! ', '... '],
        'a_start': [
            'it was really nice to spend time with you',
            'i had fun tonight',
            f"can’t stop thinking about you",
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


def get_fight_trigger(event):
    a, b = relationship_narrator.get_ab(event)
    a_nick = a['nickname']
    b_nick = b['nickname']
    time = event['date']
    rules = {
        'origin': ['#preface#\n#a#\n'],
        'preface': f'{get_message_intro(b, a)}',
        'a_lines': [
            'Hey, there\'s something I want to talk to you about',
            'Hey can we talk?',
            'Hey do you have a minute to chat?',
        ],
        'a_pre': f"{a_nick} ({time}): ",
        'b_pre': f"{b_nick} ({time}): ",
        'a': '#a_pre##a_lines#',
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")
