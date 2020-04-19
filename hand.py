from enum import Enum, auto


class Hand(Enum):
    RIGHT = auto()
    LEFT = auto()
    NONE = auto()


def is_same_hand(h1, h2):
    return not h1 == Hand.NONE and not h2 == Hand.NONE and h1 == h2


def is_same_finger(h1, h2, f1, f2):
    return is_same_hand(h1, h2)
