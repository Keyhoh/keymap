from finger import Finger
from hand import Hand
from key import Key


def sentence2fingering(key_map, finger_position, sentence):
    return map(lambda k: finger_position[key_map.index(k)] if k in key_map else None, map(Key.of, sentence))


def evaluate(key_map, finger_position, input_sentence):
    pre_hand = Hand.NONE
    same_hand = -1
    pre_finger = Finger.NONE
    same_finger = -1
    equality = 0
    total = 0

    for fingering in sentence2fingering(key_map, finger_position, input_sentence):
        if fingering is None:
            total += same_hand + same_finger
            pre_hand = Hand.NONE
            same_hand = -1
            pre_finger = Finger.NONE
            same_finger = -1
            continue

        hand, finger, weight = fingering.values()

        equality += (hand == Hand.RIGHT) * 2 - 1

        if not hand == Hand.NONE and hand == pre_hand:
            same_hand *= 2
        else:
            same_hand = -1

        if not hand == Hand.NONE and hand == pre_hand and finger == pre_finger:
            same_finger *= 3
        else:
            same_finger = -1

        total += same_hand + same_finger + weight

        pre_hand = hand
        pre_finger = finger

    return total - abs(equality)
