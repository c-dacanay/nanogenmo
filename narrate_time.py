import tracery
import datetime
import util
import random


def narrate_month(date, delta=random.random()):
    # Delta is a value 0-1 indicating positiveness of the description
    # 1 = very negative, 0 = very positive
    delta = random.gauss(delta, 0.1)
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
        'origin': f"<p>{date.strftime('%B')} #brought# #{months[date.month]}#.</p>",
        'brought': ['brought'],
        'winter': [
            '#wadj# #wnoun# and #w#',
        ],
        'spring': [
            '#sadj# #snoun# and #s#',
        ],
        'summer': [
            '#suadj# #sunoun# and #su#',
        ],
        'fall': [
            '#fadj# #fnoun# and #f#',
        ],
        'wadj': [
            'crisp', 'snowy', 'cloudy', 'grey', 'chilly', 'wet', 'frosty', 'blustery', 'drafty', 'cold', 'bleak', 'harsh', 'dark',
        ],
        'wnoun': [
            'days', 'mornings', 'evenings', 'winds', 'storms', 'breezes', 'blizzards', 'sunsets'
        ],
        'w': [
            'hot chocolate', 'warm blankets', 'wool flannels', '#wadj# #wnoun#', 'wet socks', 'frozen toes', 'fitful nights'
        ],
        'sadj': [
            'dewy', 'breezy', 'crisp', 'sunny', 'lush', 'young', 'delicate', 'balmy', 'vibrant', 'vivid', 'wet',
        ],
        'snoun': [
            'breezes', 'days', 'mornings', 'evenings', 'sunrises', 'rains', 'showers'
        ],
        's': [
            'blooming flowers', 'melodic bird calls', '#sadj# #snoun#', 'hay fever', 'allergies',
        ],
        'suadj': [
            'golden', 'warm', 'hot', 'sunny', 'stifling', 'humid', 'searing', 'muggy', 'unbearably hot'
        ],
        'sunoun': [
            'air', 'days', 'mornings', 'evenings', 'nights', 'sunrises', 'afternoons'
        ],
        'su': [
            'beach days', 'barbeques', '#suadj# #sunoun#', 'cold air-conditioning', 'sweat',
        ],
        'fadj': [
            'crisp',  'gentle', 'beautiful', 'brisk', 'mild', 'warm', 'cool', 'frosty', 'bitter'
        ],
        'fnoun': [
            'air', 'days', 'mornings', 'evenings', 'nights', 'leaves', 'foliage', 'breezes', 'sunsets',
        ],
        'f': [
            'colorful leaves', 'warm sweaters', '#fadj# #fnoun#', 'tacky decorations', 'chapped lips',
        ],
    }
    print(tracery.Grammar(rules).flatten('#origin#'))


def narrate_time(last_event, event):
    if last_event and last_event['date'].month != event['date'].month:
        narrate_month(event['date'], util.scale(
            last_event['delta'] + event['delta'], -1, 1, 1, 0))
