import prologue
import artifacts
import random
import datetime
from relationship import Relationship
import relationship_narrator
import epilogue
import names
import argparse

protagonist = {
    "name": "Alex",
    "hot": 0.8,
    "open": .5,
    "con": .5,
    "extra": .5,
    "agree": .5,
    "neuro": .5,
    "commit": .5,
    "libido": .5,
    "exp": .5,
    'confidence': 0.7,
    'their': 'their',
    'they': 'they',
    'nickname': 'xXx_Alex_xXx'
}


def generate_person():
    if random.random() > .5:
        gender = "male"
    else:
        gender = "female"

    if gender == "male":
        they = "he"
        their = "his"
        them = "him"
    else:
        they = "she"
        their = "her"
        them = "her"

    name = names.get_first_name(gender=gender)
    return {
        "name": name,
        "hot": random.random(),
        "open": random.random(),
        "con": random.random(),
        "extra": random.random(),
        "agree": random.random(),
        "neuro": random.random(),
        "commit": random.random(),
        "libido": random.random(),
        "exp": random.random(),
        "confidence": random.random(),
        'they': they,
        'their': their,
        'them': them,
        'nickname': artifacts.get_nickname(name)
    }


def generate_book(num):
    date = datetime.date.fromisoformat('2010-12-01')
    for i in range(num):
        print('# Chapter ' + str(i + 1))
        new_person = generate_person()
        r = Relationship(protagonist, new_person, date)
        r.simulate()
        date = r.events[len(r.events) - 1]['date']
        relationship_narrator.narrate(r)
        print(epilogue.get_epilogue(r, new_person))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="nanogenmo")
    parser.add_argument('-n', dest='num_chaps', type=int,
                        help='the number of chapters to generate',
                        default=10)
    args = parser.parse_args()
    generate_book(args.num_chaps)
