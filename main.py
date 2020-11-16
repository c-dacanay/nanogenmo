import prologue
import random
import relationship
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
        print(relationship.get_relationship(protagonist, new_person))
        print(epilogue.get_epilogue(relationship, new_person))


if __name__ == "__main__":
    generate_book()
