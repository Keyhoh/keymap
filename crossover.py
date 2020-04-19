from random import random, shuffle

from key import Key


def crossover(keymap1, keymap2):
    child = [keymap1[i] if random() < 0.5 else keymap2[i] for i in range(len(keymap1))]
    short = list((set([key for key in Key]) - set(child)))
    shuffle(short)
    for key in Key:
        if child.count(key) <= 1:
            continue

        child[child.index(key)] = short.pop()

    return child
