from random import choice
from pathlib import Path

me = Path(__file__).parent
adjectives = (me / "adjectives.txt").read_text().split()
nouns = (me / "nouns.txt").read_text().split()


def random_id():
    return choice(adjectives) + "-" + choice(nouns)
