import random

# assign people 0-3 hobby categories
# give them a specific interest per hobby
# take a person's hobby and generate a hobby event


def getInterestRules(a, b, interest, pov = 3):

    rules = {
        'a': a['name'],
        '#a_posses': 'my' if pov == 1 else f'{a["name"]}\'s',
        'b': 'you' if pov == 1 else b['name'],
        'their': 'my' if pov == 1 else a['their'],
        'they': 'I' if pov == 1 else a['they'],
        # 'their_hobby': f"{a['hobbies']
        'hobby': [f"{random.choice(INTERESTS[interest]['hobbies'])}"],
        # types of classes
        'food_class': [
            'grilling', 'cheesemaking', 'cooking', 'bartending',
            'cocktail-making', 'beer-brewing', 'breadmaking'
        ],
        'game_type': [
            'an arcade', 'a board', 'a card', 'a strategy', 'an online', 'a video'
        ],
        'fine_arts_topic': f"{random.choice(INTERESTS['fine arts']['hobbies'])}",
        'instrument': [
            "piano", "guitar", "bass", "violin", "viola", "cello", "saxophone", "drums", "flute"
        ],
        'broadway': [
            "Les Miserables", "Wicked", "Book of Mormon", "Oklahoma", "A Chorus Line", "Guys and Dolls", "Hair", "Mamma Mia", "Cabaret", "Chicago", "Cats"
        ]
    }
    return rules


INTERESTS = {
    # solo: spent a lot of time/devoted a lot of time to watching the game, returned to making a cocktail
    'sports': {
        'hobbies': ["basketball", "baseball", "baseball", "cricket", "frisbee", "quidditch", "billiards", "football", "golf", "gymnastics", "hunting", "orienteering", "badminton", "racquet ball", "table tennis", "tennis", "track and field", "sailing", "hockey", "lacrosse", "swimming", "diving", "bowling"],
        'location': ["the game", "the sporting goods store"],
        'verb': ["watch #hobby# replays on Youtube", "watch the game at a bar"],
        'solo': ["watching the game", "thinking about how he could improve his #hobby# game", "getting ready for #hobby# practice"]
    },
    'the outdoors': {
        'hobbies': ["camping", "hiking", "rock climbing", "backpacking", "canoeing", "rappelling", "caving", "hiking", "mountainbiking", "kayaking", "rafting"],
        'location': ["the state park", "a hiking trail", "the outdoor gear shop"],
        'verb': ["get out of the city", "go on a #hobby# trip"],
        'solo': ["planning for #their# next #hobby# trip", "#hobby#"]
    },
    'plants and animals': {
        'hobbies': ["bonsai", "fostering animals", "birdwatching", "beekeeping", "composting", "vegetable gardening", "houseplants"],
        'location': ["the botanic garden", "the farmer's market", "the park", "the animal shelter", "the cat cafe", "the dog park", "a nearby garden center"],
        'verb': ["volunteer at the animal shelter", "go WWOOFing"],
        'solo': ["working a shift at the animal shelter", "birdwatching", "tending to #their# plants", "gardening", "repotting a plant"]
    },
    'food': {
        'hobbies': ["bartending", "competitive eating", "beer", "wine", "coffee", "cocktails", "grilling", "cheese", "cooking", "baking", "tea", "bread", "kombucha"],
        'location': ["a winery", "a restaurant that just opened", "a #food_class# class"],
        'verb': ["cook dinner", "try a new recipe", "make fancy cocktails"],
        'solo': ["watching cooking videos on YouTube", "browsing new recipes on the internet", "meal-prepping", "making a pour-over", "making a cup a tea", "grocery shopping", "mixing a drink"]
    },
    'music': {
        # plays instrument, listening to #music-genre#]
        'hobbies': ["composition", "DJing", "singing", "beat boxing", "audio-tech"],
        'location': ["a concert", "a music store", "a music festival", "the record shop", "#a_posses# next show", "a songwriting class"],
        'verb': ["listen to an album #they# recently discovered"],
        'solo': ["practicing the #instrument#", "listening to music", "making beats", "recording a song", "browsing new music", "writing a song"]
    },
    'gaming': {
        'hobbies': ["arcade games", "card games", "board games", "video games", "roleplaying games"],
        'location': ["boardgame cafe", "a boardgame meet up", "a LAN party", "a game night at #a_posses# friend's house", "a barcade"],
        'verb': ["play #game_type# game", "watch a Twitch stream", "learn #a_posses# favorite game"],
        'solo': ["gaming online", "playing a videogame", "watching a Twitch stream"]
    },
    'performing arts': {
        'hobbies': ["dance", "acting", "puppetry", "historical reeanactment", "stand-up comedy", "magic tricks", "theatre"],
        'location': ["a play", "#their# next show", "an improv show", "a cabaret", "a performance", "a stand-up show", "a puppet show", "a one-man play", "a one-woman play", "a musical", "the opera", "the ballet", "a magic show", "a D&D one-shot"],
        'verb': ["go LARPing", "go dancing", "take an acting class"],
        'solo': ["listening to soundtrack of #broadway#", "practicing #their# singing", "working on #their# latest stand-up set"]
    },
    'fine arts': {
        'hobbies': ["bookmaking", "lifedrawing", "drawing", "painting", "sketching", "printmaking", "sculpture", "ceramics"],
        'location': ["a #fine_arts_topic# class", "a nearby #fine_arts_topic# exhibition", "a print fair", "an art museum"],
        'verb': ["draw in the park", "sketch in the park", "paint in the park"],
        'solo': ["drawing", "sketching", "painting"]
    },
    'health and beauty': {
        'hobbies': ["makeup", "yoga", "meditation", "skincare", "fashion", "fitness", "power-lifting", "weight-training", "bodybuilding", "jogging", "running", "barre", "HIIT workouts"],
        'location': ["the gym", "Sephora", "the beauty store", "a yoga class"],
        'verb': ["do facial masks", "give each other makeovers", "meditate", "go on a run", "work out", "go shopping"],
        'solo': ["meditating", "applying #their# makeup", "working out", "stretching", "shopping"]
    },
    'politics': {
        'hobbies': ["local politics", "state politics", "national politics", "global politics"],
        'location': ["the local board meeting", "town hall", "DC"],
        'verb': ["watch the news", "vote in the local election", "campaign", "attend a protest", "write a letter to their local representative", "listen to #their# favorite political podcast"],
        'solo': ["watching the news", "campaigning", "listening to a political podcast"]
    },
    'digital arts': {
        'hobbies': ["animation", "photography", "videography", "filmmaking", "graphic design"],
        'location': ["the movies", "a screening", "a premiere", "a showcase", "a film festival"],
        'verb': ["binge-watch Netflix", "introduce #b# to #their# favorite show", "watch a movie in bed", "do a photoshoot", "watch video essays on YouTube"],
        'solo': ["animating", "video editing", "watching a film", "watching TV"]
    },
    'literature': {
        'hobbies': ["reading", "fiction-writing", "poetry"],
        'location': ["#their# favorite bookstore", "the library", "a release party", "an author's talk", "a book signing"],
        'verb': ["read in the park", "write at the cafe", "do the crossword", "play Scrabble"],
        'solo': ["reading in the park", "working on #their# writing piece", "reading", "going to book club", "writing a poem"],
    },
    'academics': {
        'hobbies': ["astronomy", "biology", "chemistry", "foreign languages", "geography", "history", "math", "physics", "psychology"],
        'location': ["university library", "the natural history museum", "the science museum"],
        'verb': ["watch #hobby# videos on YouTube"],
        'solo': ["reading about #hobby#", "studying", "reading papers about #hobby#", "learning more about #hobby#"],
    }

}
