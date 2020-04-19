import multiprocessing
from copy import copy
from datetime import datetime
from multiprocessing import Pool
from random import random, randint

from article import random_articles, read
from crossover import crossover
from evaluate import evaluate
from finger import Finger
from hand import Hand
from keymap import QWERTY, DVORAK, NORMAN, show_keymap
from mutation import mutation

FINGER_POSITION = (
    {'hand': Hand.LEFT, 'finger': Finger.LITTLE, 'weight': 0},
    {'hand': Hand.LEFT, 'finger': Finger.LITTLE, 'weight': 0},
    {'hand': Hand.LEFT, 'finger': Finger.RING, 'weight': 1},
    {'hand': Hand.LEFT, 'finger': Finger.MIDDLE, 'weight': 2},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 0},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 0},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 0},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 0},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 0},
    {'hand': Hand.RIGHT, 'finger': Finger.MIDDLE, 'weight': 0},
    {'hand': Hand.RIGHT, 'finger': Finger.RING, 'weight': 1},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 1},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 0},

    {'hand': Hand.LEFT, 'finger': Finger.LITTLE, 'weight': 1},
    {'hand': Hand.LEFT, 'finger': Finger.RING, 'weight': 3},
    {'hand': Hand.LEFT, 'finger': Finger.MIDDLE, 'weight': 4},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 3},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 2},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 2},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 3},
    {'hand': Hand.RIGHT, 'finger': Finger.MIDDLE, 'weight': 4},
    {'hand': Hand.RIGHT, 'finger': Finger.RING, 'weight': 3},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 1},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 1},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 0},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 0},

    {'hand': Hand.LEFT, 'finger': Finger.LITTLE, 'weight': 8},
    {'hand': Hand.LEFT, 'finger': Finger.RING, 'weight': 8},
    {'hand': Hand.LEFT, 'finger': Finger.MIDDLE, 'weight': 10},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 10},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 7},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 7},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 10},
    {'hand': Hand.RIGHT, 'finger': Finger.MIDDLE, 'weight': 10},
    {'hand': Hand.RIGHT, 'finger': Finger.RING, 'weight': 8},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 9},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 7},

    {'hand': Hand.LEFT, 'finger': Finger.LITTLE, 'weight': 4},
    {'hand': Hand.LEFT, 'finger': Finger.RING, 'weight': 3},
    {'hand': Hand.LEFT, 'finger': Finger.MIDDLE, 'weight': 5},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 4},
    {'hand': Hand.LEFT, 'finger': Finger.INDEX, 'weight': 6},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 6},
    {'hand': Hand.RIGHT, 'finger': Finger.INDEX, 'weight': 4},
    {'hand': Hand.RIGHT, 'finger': Finger.MIDDLE, 'weight': 5},
    {'hand': Hand.RIGHT, 'finger': Finger.RING, 'weight': 3},
    {'hand': Hand.RIGHT, 'finger': Finger.LITTLE, 'weight': 4},
)

amount = 100
generation = 500
mutate_rate = 0.2
mutate_pb = 0.2
elite_rate = 0.1
keymaps = [copy(DVORAK) for _ in range(amount)]
elites = []


def eval_func(keymap, sentence):
    return evaluate(keymap, FINGER_POSITION, sentence)


def wrap_eval(args):
    return eval_func(*args)


if __name__ == '__main__':
    with open(random_articles(), 'r', encoding='UTF-8') as f:
        s = '\n'.join(read(f))

    for g in range(generation):
        print('Generation: ' + str(g))
        print('now: ' + datetime.now().isoformat())

        # 次世代の生成
        elites = keymaps[:int(len(keymaps) * elite_rate)]
        keymaps = elites
        while len(keymaps) < amount:
            if random() < mutate_rate:
                keymaps.append(mutation(keymaps[randint(1, len(elites)) - 1], mutate_pb))
            else:
                m1 = randint(1, len(elites)) - 1
                m2 = randint(1, len(elites)) - 1
                keymaps.append(crossover(elites[m1], elites[m2]))

        # 評価と順位付け
        with Pool(multiprocessing.cpu_count()) as pool:
            evaluations = pool.map(wrap_eval, list(map(lambda keymap: (keymap, s), keymaps)))

        keymaps = [keymaps[i] for i in sorted(range(amount), key=lambda k: evaluations[k], reverse=True)]
        print('score: ' + str(max(evaluations)))
        show_keymap(keymaps[0])

    for elite in keymaps[:5]:
        print('score: ' + str(evaluate(elite, FINGER_POSITION, s)))
        show_keymap(elite)

    print('score: ' + str(evaluate(QWERTY, FINGER_POSITION, s)))
    show_keymap(DVORAK)
