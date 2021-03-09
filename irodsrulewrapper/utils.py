import re


def check_project_id_format(project):
    if re.search("^P[0-9]{9}$", project) is not None:
        return True
    else:
        return False


def check_project_path_format(project):
    if re.search("^/nlmumc/projects/P[0-9]{9}$", project) is not None:
        return True
    else:
        return False


def check_collection_id_format(collection):
    if re.search("^C[0-9]{9}$", collection) is not None:
        return True
    else:
        return False


def check_project_collection_path_format(path):
    if re.search("^/nlmumc/projects/P[0-9]{9}/C[0-9]{9}$", path) is not None:
        return True
    else:
        return False


# TODO create rule
import random


class RandomToken:
    ADJECTIVES = """adorable
    adventurous
    aggressive
    agreeable
    alert
    alive
    amused
    angry
    annoyed
    annoying
    anxious
    arrogant
    ashamed
    attractive
    average
    awful
    bad
    beautiful
    better
    bewildered"""

    NOUNS = """aardvark
    addax
    albatross
    alligator
    alpaca
    anaconda
    angelfish
    anteater
    antelope
    ant
    ape
    armadillo
    baboon
    badger
    barracuda
    bat
    batfish
    bear
    beaver
    bee"""
    adjectives = ADJECTIVES.splitlines()
    nouns = NOUNS.splitlines()

    @staticmethod
    def generate_token():
        adjective = random.choice(RandomToken.adjectives)
        noun = random.choice(RandomToken.nouns)
        return adjective.strip() + "-" + noun.strip()
