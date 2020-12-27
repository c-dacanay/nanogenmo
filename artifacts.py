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
    '💖', '<3', '😍', '🥰', '😘', '👅', '👄', '💋', '👀', '🔥', '💦', '🌶', '🍑', '🍆', ':)', ';)', ':D',
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


def get_date_artifact(event, events):
    a, b = get_ab(event)
    a_nick = event['protagonist']['nickname']
    b_nick = event['person']['nickname']
    a_interest = event['protagonist']['interest']
    b_interest = event['protagonist']['interest']

    # Look for the most recent event and use it to
    # determine the first message sent
    experiences = [e for e in events if e['type'] != EventType.NOTHING]
    recent_experience = experiences[-1]

    if recent_experience['type'] == EventType.CONFLICT and recent_experience['initiated']:
        # This means there was a conflict recently
        message = [
            "Hey, can I cheer you up?",
            "Sorry about the other day. I wanna make it up to you! ",
        ]
    elif recent_experience.get('rejected'):
        # There was a previous rejection
        if recent_experience['protagonist_initiated'] == event['protagonist_initiated']:
            message = [
                "Hey, uh, ",
                "are you around? ",
                "Mm, ",
                "hello? "
            ]
        else:
            message = [
                "#hello# sorry again I was busy earlier! "
                "Ok I'm free now. ",
                "hey, sorry about that. ",
            ]
    elif recent_experience['type'] == EventType.COMMIT and recent_experience['initiated']:
        if recent_experience['success_ratio'] > 1:
            # we only do these texts in COURTING, this is just a placeholder for now
            message = [';)']
        else:
            message = [
                "Well let's keep hanging out still!",
                "I still enjoy spending time with you",
                "I still really like you",
                "I'm still interested in hanging out more!"
            ]
    else:
        message = util.rank([
            '#hello#, ',
            f'#hello# it was really nice to see you the other day!',
            f'i had fun! ',
            f'i had a lot of fun the other day! ',
            "You're cute. ",
            f"i had a #great# time! ",
            "You're a cutie. ",
            f"you are #great#. ",
            f"can’t stop thinking about you. ",
        ], random.gauss(a['interest'], 0.3))

    # Create the messages array
    if event['protagonist_initiated']:
        messages = [{
            'text':  '#start##punc# #ask#',
            'time': event['date'],
            'nickname': a_nick,
            'a': 'a'
        }, {
            'text':  '#rej#' if event['rejected'] else '#resp#',
            'time': event['date'],
            'nickname': b_nick,
            'a': 'b'
        }]
    else:
        messages = [{
            'text':  '#start##punc# #ask#',
            'time': event['date'],
            'nickname': b_nick,
            'a': 'b'
        }, {
            'text':  '#rej#' if event['rejected'] else '#resp#',
            'time': event['date'],
            'nickname': a_nick,
            'a': 'a'
        }]

    rules = {
        'origin': ['#preface# #msg#', '#msg#', '#msg#'],
        'preface': get_message_intro(a, b),
        'msg': get_message_html(messages),
        'punc': ['', '#e#', '#e##e#', '#e##e##e#'],
        'e': HEART_EMOJIS,
        'start': message,
        'ask': [
            'can i see you again?',
            'when can i see you again?',
            'when can i see u next?',
            'when r u free?',
            'when are u free next?',
            'See me again soon?',
            'Want to hang out #day#?',
            'Want to hang out again?',
            'When are you free next?',
            'When are you free?',
            "I'd love to see you again!",
        ],
        'hello': [
            'hey',
            'heyy',
            'heya',
            'hi',
            'hello!',
            'yo',
            'sup',
            'Hey!',
            'Heya!',
            'Yo!',
            'Hello!',
            'Whats up!',
            '',
        ],
        'great': [
            'great',
            'wonderful',
            'fantastic',
            'awesome',
            'unforgettable'
        ],
        'rej': [
            'uhhh let me take a look at my calendar',
            'let me get back to you',
            'im kinda busy rn but ill text u',
            'Hm, my week is looking pretty busy',
            'Let me get back to you...',
            'I have a upcoming deadline, can I let you know?'
        ],
        'resp': util.rank([
            '#suggest#',
            "#suggest# :)",
            "#suggest# #e#",
            'yea, #suggest#',
            "yes, #suggest#",
            "yes! #suggest#",
            "yeah id love to! #suggest#",
            'Looking forward to it #suggest#',
            'I\'d love to, #suggest#',
            'Of course! #suggest#',
            'Absolutely! #suggest#',
            'For sure! #suggest#',
        ], random.gauss(b['interest'], 0.3)),
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
