import random


def get_prologue(person):
    # properties
    name = person.get("name")
    hot = person.get("hot")
    openness = person.get("open")
    con = person.get("con")
    extra = person.get("extra")
    agree = person.get("agree")
    # neuro = person.get("neuro")
    commit = person.get("commit")
    exp = person.get("exp")

    # strings
    lo_hot = ["homely", "plain looking", "typical", "unremarkable"]
    med_hot = ["charming", "attractive", "sweet-faced", "kind-eyed"]
    hi_hot = ["beautiful", "lovely", "gorgeous", "stunning"]

    lo_open = ["They always invented new games and inside jokes",
               "They constantly sought new hobbies and experiences",
               "They were impulsive in ways, always sensation-seeking"]
    med_open = ["They never made suggestions for dates", "They always stuck to what felt comfortable",
                "They enjoyed trying new things but were still quite skeptical"]
    hi_open = ["They were a picky eater and would lo be convinced to try new food", "They were a creature of habit—inflexible, but reliable",
               "They were cautious and hated surprises"]
    lo_extra = ["a boisterous laugh",
                "a gregarious personality", "an enthusiastic charm"]
    med_extra = ["an easy smile",
                 "a laid-back demeanor", "a relaxed personality"]
    hi_extra = ["a quiet demeanor",
                "a reserved manner", "a cat-like personality"]

    lo_exp = ["insecure about", "nervous about", "timid in"]
    med_exp = ["unsure of", "open to", "relaxed about"]
    hi_exp = ["secure in", "well versed in", "experienced in"]

    lo_commit = ["wanted something casual"]
    med_commit = ["up for anything"]
    hi_commit = ["were ready for something serious"]

    lo_con = ["chaotic", "messy", "disorganized"]
    med_con = ["careless", "meandering", "detail-oriented"]
    hi_con = ["diligent", "exacting", "dutiful"]

    lo_agree = ["argumentative", "callous", "combative"]
    med_agree = ["stubborn", "independent", "affectionate"]
    hi_agree = ["altruistic", "cooperative", "empathetic"]

    # pull from strings
    if hot > .75:
        hot_adj = random.choice(hi_hot)
    elif hot > .5:
        hot_adj = random.choice(med_hot)
    else:
        hot_adj = random.choice(lo_hot)

    if openness > .66:
        open_str = random.choice(hi_open)
    elif openness > .33:
        open_str = random.choice(med_open)
    else:
        open_str = random.choice(lo_open)

    if extra > .66:
        extra_str = random.choice(hi_extra)
    elif extra > .33:
        extra_str = random.choice(med_extra)
    else:
        extra_str = random.choice(lo_extra)

    if exp > .66:
        exp_adj = random.choice(hi_exp)
    elif exp > .3:
        exp_adj = random.choice(med_exp)
    else:
        exp_adj = random.choice(lo_exp)

    if commit > .66:
        commit_str = random.choice(hi_commit)
    elif commit > .3:
        commit_str = random.choice(med_commit)
    else:
        commit_str = random.choice(lo_commit)

    if con > .66:
        con_str = random.choice(hi_con)
    elif con > .3:
        con_str = random.choice(med_con)
    else:
        con_str = random.choice(lo_con)

    if agree > .66:
        agree_str = random.choice(hi_agree)
    elif agree > .33:
        agree_str = random.choice(med_agree)
    else:
        agree_str = random.choice(lo_agree)

    str1 = name + ' was a ' + hot_adj + ' person with ' + extra_str + ". "
    str2 = name + ' initially seemed ' + exp_adj + \
        ' romantic relationships and ' + commit_str + ". "
    str3 = name + ' was ' + con_str + ' and ' + agree_str + ". " + open_str + ". "

    strings = random.sample([str1, str2, str3], k=2)
    result = listToString(strings)
    return result


def listToString(s):
    str0 = " "
    return (str0.join(s))


if __name__ == '__main__':
    test_person = {
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
    print(get_prologue(test_person))
