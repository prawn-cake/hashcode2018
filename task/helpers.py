import math


def total_cost(cos, distance, ttw=0):
    return sum([cos, distance, ttw])


def distance(coord1, coord2):
    a, b = coord1
    x, y = coord2
    return math.fabs(a - x) + math.fabs(b - y)


def score(distance, total_cost):
    return distance / total_cost