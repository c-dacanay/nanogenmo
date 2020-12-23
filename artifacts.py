import random
import util
from util import get_ab
import math
from relationship import EventType, PROP_NAMES, Relationship, Phase
import relationship_narrator
import humanize
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


def get_message_html(messages):
    # messages is an array containing objects with keys:
    #   nickname, time, message, a
    # given the array of messages, return them encoded in an HTML string
    time = None
    messages_html = ''
    for m in messages:
        # add timestamp if different day
        if m['time'] != time:
            time = m['time']
            messages_html += f"\n<p class='top-time'>{humanize.naturalday(time)}</p>\n"

        messages_html += f"""
            <div class="message_{m['a']}">
                <p class='msg_header'>
                    <span class='user'>{m['nickname']}</span>
                </p>
                <p class="message from_{m['a']}">
                    {m['text']}
                </p>
            </div>
        """
    return f'''
        <div class='artifact'>
            {messages_html}
        </div>'''


def get_first_date(event):
    a, b = get_ab(event)
    a_nick = event['protagonist']['nickname']
    b_nick = event['person']['nickname']
    a_interest = event['protagonist']['interest']
    b_interest = event['protagonist']['interest']

    # Create the messages array
    if event['protagonist_initiated']:
        messages = [{
            'text':  '#a_start##punc# #a_ask#',
            'time': event['date'],
            'nickname': a_nick,
            'a': 'a'
        }, {
            'text':  '#b_rej#' if event['rejected'] else '#b_resp#',
            'time': event['date'],
            'nickname': b_nick,
            'a': 'b'
        }]
    else:
        messages = [{
            'text':  '#b_start# #b_start2# #b_ask#',
            'time': event['date'],
            'nickname': b_nick,
            'a': 'b'
        }, {
            'text':  '#a_rej#' if event['rejected'] else '#a_resp#',
            'time': event['date'],
            'nickname': a_nick,
            'a': 'a'
        }]

    rules = {
        'origin': ['#preface# #msg#', '#msg#'],
        'preface': get_message_intro(a, b),
        'msg': get_message_html(messages),
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
            'Hm, my week is looking pretty busy',
            'Let me get back to you...',
            'I have a upcoming deadline, can I let you know?'
        ],
        'a_resp': [
            "#suggest# :)",
            "yeah id love to! #suggest#",
            "yes!! #suggest#",
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
            'the day after tomorrow',
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
    return grammar.flatten("#origin#\n")


def get_fight_trigger(event):
    a, b = get_ab(event)
    a_nick = a['nickname']
    b_nick = b['nickname']
    messages = [{
        'text': '#text#',
        'nickname': a_nick,
        'a': 'b',
        'time': event['date']
    }]
    rules = {
        'origin': ['#preface#\n#msg#\n'],
        'preface': f'{get_message_intro(a, b)}',
        'msg': get_message_html(messages),
        'text': [
            'Hey, there\'s something I want to talk to you about.',
            'Hey can we talk?',
            'Hey, I think we should check in later.',
            'Hey do you have a minute to chat?'
        ],
    }
    grammar = tracery.Grammar(rules)
    return grammar.flatten("#origin#")
