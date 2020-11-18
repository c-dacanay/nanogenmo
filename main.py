import prologue
import random
from relationship import Relationship
import relationship_narrator
import epilogue
import names

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
    "exp": .5
}


def generate_person():
    return {
        "name": names.get_first_name(),
        "hot": random.random(),
        "open": random.random(),
        "con": random.random(),
        "extra": random.random(),
        "agree": random.random(),
        "neuro": random.random(),
        "commit": random.random(),
        "libido": random.random(),
        "exp": random.random()
    }


def generate_book():
    for i in range(10):
        print('Chapter ' + str(i + 1))
        new_person = generate_person()
        print(prologue.get_prologue(new_person))
        r = Relationship(protagonist, new_person)
        r.simulate()
        print(relationship_narrator.narrate(r))
        print(epilogue.get_epilogue(r, new_person))


if __name__ == "__main__":
    generate_book()
