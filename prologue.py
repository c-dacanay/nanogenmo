import random

person = {
    "name": "Lover",
    "hot": 1,
    "open": .5,
    "con": .5,
    "extra": .5,
    "agree": .5,
    "neuro": .5,
    "commit": .5,
    "libido": .5,
    "exp": .5
}

# properties
name = person.get("name")
hot = person.get("hot")

# strings
not_hot = ["homely", "boring looking", "fine", "unremarkable"]
med_hot = ["charming", "attractive", "sweet-faced", "kind-eyed"]
def_hot = ["smokin'", "lovely", "gorgeous", "cool looking"]

# pull from strings
if hot > .75:
    hot_adj = random.choice(def_hot)
elif hot > .5:
    hot_adj = random.choice(not_hot)
else:
    hot_adj = random.choice(not_hot)

print(name + ' was a ' + hot_adj + ' person.')
