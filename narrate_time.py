import tracery
import datetime


def narrate_month(date):
    months = {
        1: 'winter',
        2: 'winter',
        3: 'spring',
        4: 'spring',
        5: 'spring',
        6: 'summer',
        7: 'summer',
        8: 'summer',
        9: 'fall',
        10: 'fall',
        11: 'fall',
        12: 'winter'
    }
    rules = {
        'origin': f"\n{date.strftime('%B')} #brought# #{months[date.month]}#.\n",
        'brought': ['brought'],
        'winter': [
            '#wadj# #wnoun# and #wadj# #wnoun#',
        ],
        'spring': [
            '#sadj# #snoun# and #sadj# #snoun#',
        ],
        'summer': [
            '#suadj# #sunoun# and #suadj# #sunoun#',
        ],
        'fall': [
            '#fadj# #fnoun# and #fadj# #fnoun#',
        ],
        'wadj': [
            'crisp', 'harsh', 'cloudy', 'cold', 'crisp', 'snowy', 'grey', 'dark', 'wet', 'frosty'
        ],
        'wnoun': [
            'days', 'mornings', 'evenings', 'winds', 'storms', 'breezes', 'blizzards', 'sunsets'
        ],
        'sadj': [
            'dewy', 'breezy', 'crisp', 'sunny', 'lush', 'young', 'delicate', 'balmy', 'vibrant', 'vivid'
        ],
        'snoun': [
            'breezes', 'days', 'mornings', 'evenings', 'flowers', 'sunrises', 'rains'
        ],
        'suadj': [
            'warm', 'hot', 'sunny', 'stifling', 'humid', 'golden', 'muggy'
        ],
        'sunoun': [
            'air', 'days', 'mornings', 'evenings', 'nights', 'sunrises'
        ],
        'fadj': [
            'crisp', 'cool', 'gentle', 'beautiful', 'brisk', 'mild', 'warm', 'sunsets',
        ],
        'fnoun': [
            'air', 'days', 'mornings', 'evenings', 'nights', 'leaves', 'foliage', 'breezes',
        ]
    }
    print(tracery.Grammar(rules).flatten('#origin#'))


def narrate_time(last_event, event):
    if last_event and last_event['date'].month != event['date'].month:
        narrate_month(event['date'])
