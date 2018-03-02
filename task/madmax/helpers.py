import math


def total_cost(cos, d, ttw=0):
    return sum([cos, d, ttw])


def distance(coord1, coord2):
    a, b = map(int, coord1)
    x, y = map(int, coord2)
    return math.fabs(a - x) + math.fabs(b - y)


def score(distance, total_cost):
    return distance / total_cost