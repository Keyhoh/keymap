from random import randint, random


def mutation(keymap, probability):
    for i in range(len(keymap)):
        if random() < probability:
            j = randint(1, len(keymap)) - 1
            keymap[i], keymap[j] = keymap[j], keymap[i]

    return keymap
