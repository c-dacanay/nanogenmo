import random
import util
import math
from relationship import Event, PROP_NAMES, Relationship, Phase


# def narrate_artifact(evt: Event):
def get(event):
    #get artifact
    character_a = event['protagonist'] if event[
        'protagonist_initiated'] else event['person']
    character_b = event['person'] if event['protagonist_initiated'] else event[
        'protagonist']

    artifact = f"{character_a['name']} gave an artifact to {character_b['name']}.\n\n"

    return artifact
