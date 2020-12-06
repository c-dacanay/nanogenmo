# assign people 0-3 hobby categories
# give them a specific interest per hobby
# take a person's hobby and generate a hobby event


INTERESTS = {
    'sports': {
        'hobbies': ["basketball", "baseball", "baseball"],
        'location': ["the game", "the sporting goods store"],
        'verb': ["watch #hobby# replays on Youtube", "watch the game at a bar"]
    },
    'outdoors': {
        'hobbies': ["camping", "hiking", "climbing"],
        'location': ["the state park", "a hiking trail"],
        'verb': ["get out of the city", "go on a #hobby# trip"]
    },
    'food-drink': {
        'hobbies': ["beer", "wine", "coffee"],
        'location': ["a winery", "a restaurant that just opened", "a #food_class# class"],
        'verb': ["try a new recipe", "make fancy cocktails"]
    },
    'performing-arts': {
        'hobbies': ["stand-up comedy", "magic tricks", "theatre"],
        'location': ["a play", "#their# next show", "an improv show"],
        'verb': ["go LARPing", "take an acting class"]
    },
     'literature': {
        'hobbies': ["reading", "fiction-writing", "poetry"],
        'location': ["#their# favorite bookstore", "the library", "a release party"],
        'verb': ["read in the park", "write at the cafe"]
    }

}

