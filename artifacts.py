import random
import util
from util import get_ab
import math
from relationship import EventType, PROP_NAMES, Relationship, Phase
import relationship_narrator
import tracery
from tracery.modifiers import base_english

# def narrate_artifact(evt: Event):
HEART_EMOJIS = [
    '💖', '<3', '😍', '🥰', '😘', '👅', '👄', '💋', '👀', '🔥', '💦', '🌶', '🍑', '🍆'	    '💖', '<3', '😍', '🥰', '😘', '👅', '👄', '💋', '👀', '🔥', '💦', '🌶', '🍑', '🍆'
]


def get_nickname(name):
    rules = {
        'origin': '#nick#',
        'nick': ['#l#-#dog#', '#name##suffix#'],
        'l': name[0],
        'dog': ['dog', 'dawg', 'cat', 'catz', 'star', 'Z', 'qt', 'babe', 'bob', 'mack', '💖'],
        'name': [name, '#l'],
        'num': ['420', '69'] + [str(n + 80) for n in range(20)],
        'suffix': ['#num#', '_#num#', '#dog##num#']
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")


def get_message_intro(a, b):
    rules = {
        'origin': ['<p>#time.capitalize#, #phrase#.</p>', ''],
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
    return grammar.flatten('#origin#\n')


def get_first_date(event):
    a, b = get_ab(event)
    a_nick = a['nickname']
    b_nick = b['nickname']
    a_interest = a['interest']
    b_interest = b['interest']
    time = event['date']

    preface = get_message_intro(a, b)
    response = 'resp'
    if event['rejected']:
        response = 'rej'

    rules = {
        'a': [
            f'{preface} #a_msg#', '#a_msg#'
        ],
        'b': [
            f'{preface} #b_msg#', '#b_msg#'
        ],
        'a_msg': [
            f'<p>#a_pre#<span class="message">#a_start##punc##a_ask#</span></p><p>#b_pre#<span class="message">#b_{response}#</span></p>'
        ],
        'b_msg': [
            f'<p>#b_pre#<span class="message">#b_start##b_start2##b_ask#</span></p><p>#a_pre#<span class="message">#a_{response}#</span></p>'
        ],
        'a_pre': f"<span class='user'>{a_nick}</span><span class='time'>({time})</span>: ",
        'b_pre': f"<span class='user'>{b_nick}</span><span class='time'>({time})</span>: ",
        'punc': ['. ', '! ', '... ', '#e# ', '#e##e# '],
        'e': HEART_EMOJIS,
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
            'again sometime?',
            'again?'
        ],
        'b_start': [
            'Hey!',
            'Heya!',
            'Yo!',
            'Hello!',
            'Whats up!',
            '',
        ],
        'b_ask': [
            'See me again soon?',
            'Want to do it again?',
            'When are you free next?',
            "Let's do it again sometime.",
        ],
        'b_start2': [
            f'I had a wonderful time.',
            f'I had an awesome time.',
            f'I had a fantastic time.',
            "You're cute.",
            "You're a cutie.",
        ],
        'a_rej': [
            'uhhh let me take a look at my calendar',
            'let me get back to you',
            'im kinda busy rn but ill text u',
        ],
        'b_rej': [
            'Maybe in a bit, I\'m busy this week',
            'Yeah...',
        ],
        'a_resp': [
            ":) #suggest#",
            "yeah id love to! #suggest#",
            "yes!! #suggest#?",
        ],
        'b_resp': [
            'Looking forward to it #suggest#',
            '#suggest#',
            'I\'d love to #suggest#',
            'Of course! #suggest#',
            'Absolutely! #suggest#',
            'For sure! #suggest#',
        ],
        'suggest': [
            'what about #day#?',
            'im free on #day#!',
            'i can do #day#.',
            'i could do #day#.',
            '#day#?'
        ],
        'day': [
            'tomorrow',
            'day after tomorrow',
            'monday',
            'some time next week',
            'tuesday',
            'after work on thursday',
            'wednesday',
            'this weekend',
            'friday',
        ]
    }
    grammar = tracery.Grammar(rules)
    if event['protagonist_initiated']:
        return grammar.flatten("#a#\n")
    else:
        return grammar.flatten("#b#\n")


def get_fight_trigger(event):
    a, b = get_ab(event)
    a_nick = a['nickname']
    b_nick = b['nickname']
    time = event['date']
    rules = {
        'origin': ['#preface#\n#a#\n'],
        'preface': f'{get_message_intro(a, b)}',
        'a_lines': [
            'Hey, there\'s something I want to talk to you about',
            'Hey can we talk?',
            'Hey, I think we should check in later',
            'Hey do you have a minute to chat?'
        ],
        'a_pre': f"<span class='user'>{a_nick}</span><span class='time'>({time})</span>: ",
        'b_pre': f"<span class='user'>{b_nick}</span><span class='time'>({time})</span>: ",
        'a': '<p>#a_pre#<span class="message">#a_lines#</span></p>',
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")
