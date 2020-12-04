from relationship import Relationship
# from main import protagonist
# import relationship_narrator


def get_epilogue(rel, person):
    # Given a relationship object and person return a string
    # representing the epilogue of the relationship

    # notes from cd:
    # ep should not print if there is a rejection
    # comment on last 1-3 conflicts
    # note prop with the most difference
    # if rel > than 4 events, remember a positive development
    # [eventually] reflect the phase of rel and alex's changed props

    r = rel
    # print(l)
    return ""


if __name__ == '__main__':

    test_person = {
        'name': 'Lover',
        'hot': 1,
        'open': .5,
        'con': .5,
        'extra': .5,
        'agree': .5,
        'neuro': .5,
        'commit': .5,
        'libido': .5,
        'exp': .5
    }

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
        'their': 'their'
    }

    r = Relationship(protagonist, test_person)
    r.simulate()
    print(get_epilogue(r, test_person))
