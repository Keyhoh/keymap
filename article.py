from math import floor
from random import randrange

from bs4 import BeautifulSoup


def random_articles():
    target = randrange(0, 13579)
    dir_num = floor(target / 100)
    dir = chr(65 + floor(dir_num / 26)) + chr(65 + dir_num % 26)
    file = 'wiki_' + str(target % 100).rjust(2, '0')
    return './extracted/' + dir + '/' + file


def read(articles):
    xml = BeautifulSoup(articles, 'html.parser')
    return list(map(lambda doc: doc.text, xml.find_all('doc')))
